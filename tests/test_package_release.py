from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys
import tempfile
import unittest
import zipfile


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
PACKAGER = REPO_ROOT / "scripts" / "package_release.py"
VERSION = "v0.1.0"
ARCHIVES = (
    f"patent-bilingual-qa-{VERSION}.zip",
    f"patent-office-action-response-{VERSION}.zip",
    f"patent-agent-skills-{VERSION}.zip",
)


class PackageReleaseTest(unittest.TestCase):
    def run_packager(self, output_dir: pathlib.Path) -> None:
        subprocess.run(
            [
                sys.executable,
                str(PACKAGER),
                "--version",
                VERSION,
                "--output-dir",
                str(output_dir),
            ],
            cwd=REPO_ROOT,
            check=True,
        )

    def test_cli_builds_expected_reproducible_release(self) -> None:
        with tempfile.TemporaryDirectory() as first_tmp, tempfile.TemporaryDirectory() as second_tmp:
            first = pathlib.Path(first_tmp)
            second = pathlib.Path(second_tmp)
            self.run_packager(first)
            self.run_packager(second)

            self.assertEqual(
                sorted(path.name for path in first.iterdir()),
                ["SHA256SUMS.txt", *sorted(ARCHIVES)],
            )

            checksums = {}
            for line in (first / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
                digest, filename = line.split("  ", 1)
                checksums[filename] = digest

            self.assertEqual(set(checksums), set(ARCHIVES))
            for filename in ARCHIVES:
                first_bytes = (first / filename).read_bytes()
                second_bytes = (second / filename).read_bytes()
                self.assertEqual(first_bytes, second_bytes)
                self.assertEqual(hashlib.sha256(first_bytes).hexdigest(), checksums[filename])

            expected_members = {
                ARCHIVES[0]: "patent-bilingual-qa/SKILL.md",
                ARCHIVES[1]: "patent-office-action-response/SKILL.md",
                ARCHIVES[2]: "patent-bilingual-qa/SKILL.md",
            }
            expected_licenses = {
                ARCHIVES[0]: "patent-bilingual-qa/LICENSE",
                ARCHIVES[1]: "patent-office-action-response/LICENSE",
                ARCHIVES[2]: "LICENSE",
            }
            for filename, expected_member in expected_members.items():
                with zipfile.ZipFile(first / filename) as archive:
                    names = archive.namelist()
                    self.assertIn(expected_member, names)
                    self.assertIn(expected_licenses[filename], names)
                    self.assertFalse(any(name.startswith("__MACOSX/") for name in names))
                    self.assertTrue(
                        all(info.date_time == (1980, 1, 1, 0, 0, 0) for info in archive.infolist())
                    )

            with zipfile.ZipFile(first / ARCHIVES[2]) as bundle:
                self.assertIn("patent-office-action-response/SKILL.md", bundle.namelist())


if __name__ == "__main__":
    unittest.main()

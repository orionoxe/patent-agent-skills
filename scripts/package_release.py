#!/usr/bin/env python3
"""Build deterministic release archives for the public skill repository."""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import stat
import zipfile


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_DIRS = ("patent-bilingual-qa", "patent-office-action-response")
VERSION_PATTERN = re.compile(r"^v\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
EXCLUDED_NAMES = {".DS_Store", "__pycache__"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def iter_files(directory: pathlib.Path):
    for path in sorted(directory.rglob("*"), key=lambda item: item.as_posix()):
        if path.is_symlink():
            raise ValueError(f"release input must not contain symlinks: {path}")
        relative = path.relative_to(REPO_ROOT)
        if any(part in EXCLUDED_NAMES for part in relative.parts):
            continue
        if path.suffix in EXCLUDED_SUFFIXES or not path.is_file():
            continue
        yield path, relative


def write_file(archive: zipfile.ZipFile, source: pathlib.Path, name: pathlib.Path) -> None:
    mode = source.stat().st_mode
    permissions = 0o755 if mode & stat.S_IXUSR else 0o644
    info = zipfile.ZipInfo(name.as_posix(), FIXED_TIMESTAMP)
    info.create_system = 3
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = (stat.S_IFREG | permissions) << 16
    archive.writestr(info, source.read_bytes(), compresslevel=9)


def build_archive(output: pathlib.Path, skill_names: tuple[str, ...]) -> None:
    with zipfile.ZipFile(output, mode="w") as archive:
        for skill_name in skill_names:
            skill_dir = REPO_ROOT / skill_name
            if not (skill_dir / "SKILL.md").is_file():
                raise ValueError(f"missing {skill_name}/SKILL.md")
            for source, relative in iter_files(skill_dir):
                write_file(archive, source, relative)
        license_name = (
            pathlib.Path(skill_names[0]) / "LICENSE"
            if len(skill_names) == 1
            else pathlib.Path("LICENSE")
        )
        write_file(archive, REPO_ROOT / "LICENSE", license_name)


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_release(version: str, output_dir: pathlib.Path) -> list[pathlib.Path]:
    if not VERSION_PATTERN.fullmatch(version):
        raise ValueError("version must look like v0.1.0 or v0.1.0-rc.1")

    output_dir.mkdir(parents=True, exist_ok=True)
    archives = []
    for skill_name in SKILL_DIRS:
        output = output_dir / f"{skill_name}-{version}.zip"
        build_archive(output, (skill_name,))
        archives.append(output)

    bundle = output_dir / f"patent-agent-skills-{version}.zip"
    build_archive(bundle, SKILL_DIRS)
    archives.append(bundle)

    checksum_lines = [f"{sha256(path)}  {path.name}" for path in archives]
    (output_dir / "SHA256SUMS.txt").write_text(
        "\n".join(checksum_lines) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return archives


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--output-dir", type=pathlib.Path, default=REPO_ROOT / "dist")
    args = parser.parse_args()

    archives = build_release(args.version, args.output_dir.resolve())
    for archive in archives:
        print(f"built {archive}")
    print(f"built {args.output_dir.resolve() / 'SHA256SUMS.txt'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

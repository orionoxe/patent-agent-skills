from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "patent-office-action-response" / "scripts" / "validate_package.py"
VALID_FIXTURE = (
    REPO_ROOT
    / "patent-office-action-response"
    / "tests"
    / "fixtures"
    / "valid-manifest.json"
)


class ValidatePackageTest(unittest.TestCase):
    def valid_manifest(self) -> dict:
        return json.loads(VALID_FIXTURE.read_text(encoding="utf-8"))

    def run_validator(self, data: dict) -> tuple[subprocess.CompletedProcess[str], dict]:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = pathlib.Path(tmp) / "package-manifest.json"
            manifest.write_text(json.dumps(data), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(manifest)],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
            )
        return result, json.loads(result.stdout)

    def test_valid_manifest_reports_structural_status(self) -> None:
        result, report = self.run_validator(self.valid_manifest())
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report["status"], "manifest-structure-valid")

    def test_placeholders_and_unowned_deferred_rows_are_rejected(self) -> None:
        data = self.valid_manifest()
        data["reviewer"] = "[VERIFY]"
        data["inventory_rows"][0]["status"] = "deferred"
        result, report = self.run_validator(data)
        self.assertEqual(result.returncode, 2)
        self.assertTrue(any("reviewer contains" in error for error in report["errors"]))
        self.assertTrue(any("decision_owner" in error for error in report["errors"]))
        self.assertTrue(any("decision_due" in error for error in report["errors"]))

    def test_claim_independent_inventory_row_is_allowed(self) -> None:
        data = self.valid_manifest()
        row = data["inventory_rows"][0]
        row["category"] = "procedural-instruction"
        row["scope"] = "communication"
        row["claims"] = []
        result, report = self.run_validator(data)
        self.assertEqual(result.returncode, 0, report["errors"])

    def test_not_applicable_requires_reason(self) -> None:
        data = self.valid_manifest()
        data["inventory_rows"][0]["status"] = "not-applicable"
        result, report = self.run_validator(data)
        self.assertEqual(result.returncode, 2)
        self.assertTrue(any("status_reason" in error for error in report["errors"]))

    def test_template_date_and_source_literals_are_rejected(self) -> None:
        data = self.valid_manifest()
        data["communication_date"] = "YYYY-MM-DD"
        data["official_sources_retrieved"] = "YYYY-MM-DD"
        data["deadline_source"] = "Office Action p. X"
        result, report = self.run_validator(data)
        self.assertEqual(result.returncode, 2)
        self.assertTrue(any("communication_date" in error for error in report["errors"]))
        self.assertTrue(any("official_sources_retrieved" in error for error in report["errors"]))
        self.assertTrue(any("deadline_source" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()

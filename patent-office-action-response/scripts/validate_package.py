#!/usr/bin/env python3
"""Structural completeness validator for an office-action response package."""

from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import re
import sys


ALLOWED_JURISDICTIONS = {"CN", "US", "EP"}
ALLOWED_CATEGORIES = {
    "rejection",
    "objection",
    "requirement",
    "formality",
    "allowable-subject-matter",
    "procedural-instruction",
}
ALLOWED_SCOPES = {"claims", "communication"}
ALLOWED_STRATEGIES = {
    "traverse",
    "clarify",
    "amend",
    "evidence",
    "interaction",
    "procedural",
    "mixed",
    "defer",
}
ALLOWED_STATUS = {
    "addressed",
    "deferred",
    "withdrawn-by-office",
    "not-applicable",
}
PLACEHOLDER_PATTERN = re.compile(
    r"\[(?:VERIFY|MISSING|STRATEGY-DECISION|BLOCKER|NO-BASIS)\]",
    re.IGNORECASE,
)
TEMPLATE_LITERALS = {"YYYY-MM-DD", "Office Action p. X"}


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require_resolved_text(data: dict, field: str, prefix: str, errors: list[str]) -> None:
    value = data.get(field)
    label = f"{prefix}.{field}" if prefix else field
    if not nonempty(value):
        errors.append(f"missing field: {label}")
    elif PLACEHOLDER_PATTERN.search(value) or value in TEMPLATE_LITERALS:
        errors.append(f"{label} contains an unresolved placeholder")


def require_iso_date(data: dict, field: str, errors: list[str]) -> None:
    before = len(errors)
    require_resolved_text(data, field, "", errors)
    if len(errors) != before:
        return
    try:
        datetime.date.fromisoformat(data[field])
    except ValueError:
        errors.append(f"{field} must use a real YYYY-MM-DD date")


def validate(data: dict) -> list[str]:
    errors: list[str] = []

    if data.get("jurisdiction") not in ALLOWED_JURISDICTIONS:
        errors.append("jurisdiction must be CN, US, or EP")
    for field in ("deadline_as_stated", "deadline_source", "reviewer"):
        require_resolved_text(data, field, "", errors)
    for field in ("communication_date", "official_sources_retrieved"):
        require_iso_date(data, field, errors)

    inventory_rows = data.get("inventory_rows")
    if not isinstance(inventory_rows, list) or not inventory_rows:
        errors.append("inventory_rows must contain at least one row")
        inventory_rows = []

    amendments = data.get("amendments")
    if not isinstance(amendments, list):
        errors.append("amendments must be a list")
        amendments = []

    amendment_ids: set[str] = set()
    for index, amendment in enumerate(amendments):
        prefix = f"amendments[{index}]"
        amendment_id = amendment.get("id")
        if not nonempty(amendment_id):
            errors.append(f"{prefix}.id is required")
        elif amendment_id in amendment_ids:
            errors.append(f"duplicate amendment id: {amendment_id}")
        else:
            amendment_ids.add(amendment_id)
        for field in ("claim", "exact_change", "scope_effect", "reason"):
            require_resolved_text(amendment, field, prefix, errors)
        basis = amendment.get("basis")
        if not isinstance(basis, list) or not basis:
            errors.append(f"{prefix}.basis must contain at least one pinpoint")
        else:
            for basis_index, item in enumerate(basis):
                for field in ("document", "pinpoint", "rationale"):
                    require_resolved_text(
                        item,
                        field,
                        f"{prefix}.basis[{basis_index}]",
                        errors,
                    )

    inventory_ids: set[str] = set()
    for index, inventory_row in enumerate(inventory_rows):
        prefix = f"inventory_rows[{index}]"
        inventory_id = inventory_row.get("id")
        if not nonempty(inventory_id):
            errors.append(f"{prefix}.id is required")
        elif inventory_id in inventory_ids:
            errors.append(f"duplicate inventory id: {inventory_id}")
        else:
            inventory_ids.add(inventory_id)

        category = inventory_row.get("category")
        if category not in ALLOWED_CATEGORIES:
            errors.append(f"{prefix}.category is invalid")
        scope = inventory_row.get("scope")
        if scope not in ALLOWED_SCOPES:
            errors.append(f"{prefix}.scope must be claims or communication")

        claims = inventory_row.get("claims")
        if not isinstance(claims, list):
            errors.append(f"{prefix}.claims must be a list")
            claims = []
        elif scope == "claims" and not claims:
            errors.append(f"{prefix}.claims must not be empty for claims scope")
        elif scope == "communication" and claims:
            errors.append(f"{prefix}.claims must be empty for communication scope")
        elif any(not nonempty(claim) for claim in claims):
            errors.append(f"{prefix}.claims contains an empty identifier")
        for field in ("ground", "examiner_position", "response_section"):
            require_resolved_text(inventory_row, field, prefix, errors)
        if inventory_row.get("strategy") not in ALLOWED_STRATEGIES:
            errors.append(f"{prefix}.strategy is invalid")
        if inventory_row.get("status") not in ALLOWED_STATUS:
            errors.append(f"{prefix}.status is not structurally complete")
        elif inventory_row.get("status") == "deferred":
            require_resolved_text(inventory_row, "decision_owner", prefix, errors)
            require_resolved_text(inventory_row, "decision_due", prefix, errors)
        elif inventory_row.get("status") in {"withdrawn-by-office", "not-applicable"}:
            require_resolved_text(inventory_row, "status_reason", prefix, errors)

        evidence = inventory_row.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{prefix}.evidence must contain a source and pinpoint")
        else:
            for evidence_index, item in enumerate(evidence):
                for field in ("source", "pinpoint"):
                    require_resolved_text(
                        item,
                        field,
                        f"{prefix}.evidence[{evidence_index}]",
                        errors,
                    )

        linked_amendments = inventory_row.get("amendment_ids", [])
        if not isinstance(linked_amendments, list):
            errors.append(f"{prefix}.amendment_ids must be a list")
            linked_amendments = []
        for amendment_id in linked_amendments:
            if amendment_id not in amendment_ids:
                errors.append(f"{prefix} links unknown amendment: {amendment_id}")
        if inventory_row.get("strategy") in {"amend", "mixed"} and not linked_amendments:
            errors.append(f"{prefix} selects amendment without amendment_ids")

    flags = data.get("critical_flags")
    if not isinstance(flags, list):
        errors.append("critical_flags must be a list")
    elif flags:
        errors.append("critical_flags must be resolved before validation can pass")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=pathlib.Path)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        print(
            json.dumps(
                {"status": "manifest-structure-invalid", "errors": errors},
                indent=2,
            )
        )
        return 2
    print(json.dumps({"status": "manifest-structure-valid", "errors": []}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

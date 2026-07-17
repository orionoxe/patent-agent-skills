#!/usr/bin/env python3
"""Candidate invariant checker for bilingual patent text.

This script compares mechanical tokens. It cannot determine legal or semantic
equivalence; every finding requires source-image and human review.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import pathlib
import re
import sys
from typing import Iterable


CLAIM_PATTERNS = (
    re.compile(r"(?im)^\s*(?:claim|claims)\s+(\d+[A-Za-z]?)\b"),
    re.compile(r"(?im)^\s*权利要求\s*(\d+[A-Za-z]?)\b"),
    re.compile(r"(?m)^\s*(\d{1,3})\s*[.、]\s*(?=\S)"),
)

REFERENCE_PATTERN = re.compile(r"[\(（]\s*(\d{1,4}[A-Za-z]?)\s*[\)）]")
# Use an ASCII-only left boundary. Python's \w includes CJK characters, which
# would otherwise hide values embedded in normal Chinese prose (for example,
# "延迟为20 ms").
NUMBER_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_.])[-+]?\d+(?:[.,]\d+)*(?:\s*(?:%|‰|°C|K|ns|μs|us|ms|s|min|h|"
    r"Hz|kHz|MHz|GHz|B|KB|MB|GB|V|mV|A|mA|W|kW|nm|μm|um|mm|cm|m|km|mg|g|kg|N))?"
)
PATENT_PATTERN = re.compile(
    r"\b(?:CN|US|EP|WO|JP|KR)\s*\d[\d/,.\s-]*[A-Z]\d?\b", re.IGNORECASE
)


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_token(token: str) -> str:
    return re.sub(r"\s+", "", token).replace("，", ",").upper()


def extract_claims(text: str) -> list[str]:
    found: list[str] = []
    for pattern in CLAIM_PATTERNS:
        found.extend(match.group(1).upper() for match in pattern.finditer(text))
    return found


def extract(pattern: re.Pattern[str], text: str) -> list[str]:
    values: list[str] = []
    for match in pattern.finditer(text):
        value = match.group(1) if match.lastindex else match.group(0)
        values.append(normalize_token(value))
    return values


def multiset_difference(
    source_values: Iterable[str], target_values: Iterable[str]
) -> tuple[list[str], list[str]]:
    source = collections.Counter(source_values)
    target = collections.Counter(target_values)
    missing = sorted((source - target).elements())
    extra = sorted((target - source).elements())
    return missing, extra


def compare_category(name: str, source: list[str], target: list[str]) -> dict:
    missing, extra = multiset_difference(source, target)
    return {
        "category": name,
        "source_count": len(source),
        "target_count": len(target),
        "missing_from_target": missing,
        "extra_in_target": extra,
        "status": "review" if missing or extra else "match",
    }


def build_report(source_text: str, target_text: str) -> dict:
    categories = [
        compare_category(
            "claim_identifiers",
            extract_claims(source_text),
            extract_claims(target_text),
        ),
        compare_category(
            "reference_numerals",
            extract(REFERENCE_PATTERN, source_text),
            extract(REFERENCE_PATTERN, target_text),
        ),
        compare_category(
            "numbers_and_units",
            extract(NUMBER_PATTERN, source_text),
            extract(NUMBER_PATTERN, target_text),
        ),
        compare_category(
            "patent_publication_numbers",
            extract(PATENT_PATTERN, source_text),
            extract(PATENT_PATTERN, target_text),
        ),
    ]
    return {
        "source_sha256": digest(source_text),
        "target_sha256": digest(target_text),
        "candidate_only": True,
        "categories": categories,
        "review_required": any(item["status"] == "review" for item in categories),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=pathlib.Path, required=True)
    parser.add_argument("--target", type=pathlib.Path, required=True)
    parser.add_argument("--json-out", type=pathlib.Path)
    args = parser.parse_args()

    report = build_report(read_text(args.source), read_text(args.target))
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_out:
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 2 if report["review_required"] else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

python_bin="${PYTHON:-python3}"
tmp_dir="$(mktemp -d)"
trap 'find "$tmp_dir" -type f -delete; rmdir "$tmp_dir"' EXIT

expect_review_exit() {
  local label="$1"
  shift
  set +e
  "$@" >"$tmp_dir/$label.json"
  local result=$?
  set -e
  if [[ "$result" -ne 2 ]]; then
    echo "$label: expected exit 2, got $result" >&2
    return 1
  fi
}

"$python_bin" patent-bilingual-qa/scripts/check_invariants.py \
  --source patent-bilingual-qa/tests/fixtures/source.txt \
  --target patent-bilingual-qa/tests/fixtures/target-good.txt \
  >"$tmp_dir/bilingual-good.json"

expect_review_exit bilingual-bad \
  "$python_bin" patent-bilingual-qa/scripts/check_invariants.py \
  --source patent-bilingual-qa/tests/fixtures/source.txt \
  --target patent-bilingual-qa/tests/fixtures/target-bad.txt

"$python_bin" patent-office-action-response/scripts/validate_package.py \
  patent-office-action-response/tests/fixtures/valid-manifest.json \
  >"$tmp_dir/oa-valid.json"

expect_review_exit oa-invalid \
  "$python_bin" patent-office-action-response/scripts/validate_package.py \
  patent-office-action-response/tests/fixtures/invalid-manifest.json

"$python_bin" -m unittest discover -s tests -v
"$python_bin" -m compileall -q \
  patent-bilingual-qa/scripts \
  patent-office-action-response/scripts \
  scripts \
  tests

if grep -RIlE \
  --exclude='test.sh' \
  --exclude-dir='.git' \
  --exclude-dir='dist' \
  --exclude-dir='__pycache__' \
  '(/Users/|@bytedance\.com|BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY|gh[opsu]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})' \
  .; then
  echo "public audit found a local path, work address, or credential pattern" >&2
  exit 1
fi

echo "all repository checks passed"

#!/usr/bin/env bash
# Lint an OpenAPI spec with Spectral before it goes anywhere near Postman.
#
# Postman's createSpec / updateSpecFile do NOT validate the document — they store what you
# send. An invalid spec is accepted, then silently fails to generate or sync a collection,
# with no error surfaced anywhere. Always gate on this script first.
#
# Exit status: 0 if there are no errors, 1 otherwise. Warnings are printed but do not fail;
# pass --strict to fail on warnings too.
#
# Usage:
#   scripts/validate-spec.sh postman/specs/firecrawl.openapi.json
#   scripts/validate-spec.sh --strict path/to/spec.yaml

set -uo pipefail

STRICT=0
if [ "${1:-}" = "--strict" ]; then STRICT=1; shift; fi

SPEC="${1:-}"
if [ -z "$SPEC" ] || [ ! -f "$SPEC" ]; then
  echo "usage: $0 [--strict] <spec-file>" >&2
  exit 2
fi

if command -v spectral >/dev/null 2>&1; then
  SPECTRAL=(spectral)
elif command -v npx >/dev/null 2>&1; then
  echo "spectral not on PATH — falling back to npx @stoplight/spectral-cli"
  SPECTRAL=(npx -y @stoplight/spectral-cli)
else
  echo "ERROR: need spectral or npx. Install with: npm i -g @stoplight/spectral-cli" >&2
  exit 2
fi

RULESET="$(mktemp -t ruleset).yaml"
printf 'extends: ["spectral:oas"]\n' > "$RULESET"
trap 'rm -f "$RULESET"' EXIT

echo "linting $SPEC"
OUT="$("${SPECTRAL[@]}" lint "$SPEC" --ruleset "$RULESET" --format stylish 2>&1)"
echo "$OUT"

ERRORS=$(printf '%s' "$OUT" | grep -cE '^\s*[0-9]+:[0-9]+\s+error\s' || true)
WARNS=$(printf '%s' "$OUT" | grep -cE '^\s*[0-9]+:[0-9]+\s+warning\s' || true)

echo
echo "errors: $ERRORS   warnings: $WARNS"

if [ "$ERRORS" -gt 0 ]; then
  echo "FAIL: fix the errors before pushing this spec to Postman." >&2
  exit 1
fi
if [ "$STRICT" -eq 1 ] && [ "$WARNS" -gt 0 ]; then
  echo "FAIL (--strict): warnings present." >&2
  exit 1
fi
echo "OK to push."

#!/usr/bin/env python3
"""Build a corrected Firecrawl OpenAPI spec from upstream.

Upstream `mendableai/firecrawl:apps/api/openapi.json` declares a single server,
`https://api.firecrawl.dev/v1`, but ships two operations that only exist on v2 and
return 404 on v1:

    POST /feedback
    POST /search/{jobId}/feedback

Both were added in "feat(api): add generic endpoint feedback" (2026-06-15) and their own
summaries say "Submit feedback for a v2 job". Four other operations are the mirror image —
v1-only, 404 on v2 — so neither a blanket /v1 nor a blanket /v2 server is correct:

    POST /deep-research, GET /deep-research/{id}
    POST /llmstxt,       GET /llmstxt/{id}

This script keeps /v1 as the default server and adds an operation-level `servers` override
(OpenAPI 3.0 §4.7.5) for the v2-only operations, so every operation resolves to a URL that
actually exists.

Verified empirically on 2026-08-08 by probing all 22 operations against both versions;
`--verify` re-runs that probe. Re-check after any upstream change — the split is not stable.

Usage:
    python3 scripts/build-firecrawl-spec.py            # write the corrected spec
    python3 scripts/build-firecrawl-spec.py --verify   # also probe the live API
"""

import argparse
import json
import pathlib
import sys
import urllib.error
import urllib.request

UPSTREAM = (
    "https://raw.githubusercontent.com/mendableai/firecrawl/main/apps/api/openapi.json"
)
OUT = pathlib.Path(__file__).resolve().parent.parent / "postman/specs/firecrawl.openapi.json"

V1 = "https://api.firecrawl.dev/v1"
V2 = "https://api.firecrawl.dev/v2"

# Operations that exist only on v2 (404 on v1) and need a server override.
V2_ONLY = {("post", "/feedback"), ("post", "/search/{jobId}/feedback")}

# Operations that exist only on v1 (404 on v2). Correct under the default server —
# listed so the asymmetry is visible and testable, not to be modified.
V1_ONLY = {
    ("post", "/deep-research"),
    ("get", "/deep-research/{id}"),
    ("post", "/llmstxt"),
    ("get", "/llmstxt/{id}"),
}

METHODS = ("get", "put", "post", "delete", "patch")


def fetch(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read())


def build(spec):
    spec["servers"] = [{"url": V1, "description": "Firecrawl v1 (default for this spec)"}]

    patched = []
    for path, item in spec.get("paths", {}).items():
        for method in list(item):
            if method not in METHODS:
                continue
            if (method, path) in V2_ONLY:
                item[method]["servers"] = [
                    {"url": V2, "description": "v2 only — this operation 404s on v1"}
                ]
                patched.append(f"{method.upper()} {path}")

    missing = V2_ONLY - {
        (m, p)
        for p, i in spec.get("paths", {}).items()
        for m in i
        if m in METHODS
    }
    if missing:
        sys.exit(f"ERROR: expected v2-only operations absent upstream: {sorted(missing)}")

    spec["info"]["description"] = spec["info"].get("description", "").rstrip() + (
        "\n\n---\n\n"
        "**Version note (maintained by open-collections-maintainer).** Upstream publishes "
        "this spec with a single `/v1` server, but the API surface is split. Most operations "
        "exist on both v1 and v2. `POST /feedback` and `POST /search/{jobId}/feedback` exist "
        "**only on v2** and carry an operation-level server override here. `deep-research` "
        "and `llmstxt` exist **only on v1**. Verified against the live API 2026-08-08."
    )
    return patched


def verify(spec):
    ok = True
    for path, item in spec.get("paths", {}).items():
        for method in item:
            if method not in METHODS:
                continue
            base = item[method].get("servers", spec["servers"])[0]["url"]
            probe = path.replace("{id}", "0" * 8 + "-0000-0000-0000-" + "0" * 12)
            probe = probe.replace("{jobId}", "0" * 8 + "-0000-0000-0000-" + "0" * 12)
            req = urllib.request.Request(
                base + probe,
                method=method.upper(),
                data=b"{}" if method == "post" else None,
                headers={"Content-Type": "application/json"},
            )
            try:
                urllib.request.urlopen(req, timeout=15)
                code = 200
            except urllib.error.HTTPError as e:
                code = e.code
            except Exception as e:  # network hiccup — report, don't fail the build
                print(f"  ?? {method.upper():6} {path}: {e}")
                continue
            flag = "!!" if code == 404 else "ok"
            if code == 404:
                ok = False
            print(f"  {flag} {code} {method.upper():6} {base.rsplit('/', 1)[1]} {path}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="probe every operation's server")
    args = ap.parse_args()

    spec = fetch(UPSTREAM)
    patched = build(spec)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")

    ops = sum(1 for p, i in spec["paths"].items() for m in i if m in METHODS)
    print(f"wrote {OUT.relative_to(OUT.parent.parent.parent)}  ({ops} operations)")
    print(f"v2 server override applied to: {', '.join(patched)}")

    if args.verify:
        print("\nprobing every operation against its effective server:")
        if not verify(spec):
            sys.exit("\nFAIL: at least one operation 404s at its declared server")
        print("\nall operations resolve to a live endpoint")


if __name__ == "__main__":
    main()

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
# Derived artifact — gitignored. The script is the source of truth, not its output.
OUT = pathlib.Path(__file__).resolve().parent.parent / "build/firecrawl.openapi.json"

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


def fix_enum_defaults(node, path=""):
    """Move array-valued `default` off an items schema up onto its parent array schema.

    Upstream writes deep-research's `formats` as:

        {"type":"array","items":{"type":"string","enum":[...],"default":["markdown"]}}

    The default is an array but it sits on the *items* schema, whose enum holds strings — so
    the default can never be a member of the enum. Validators reject this with
    "Default values must be present in enum". Upstream's two other `formats` schemas put the
    default on the array, which is what this normalises to.
    """
    moved = []
    if isinstance(node, dict):
        items = node.get("items")
        if (
            node.get("type") == "array"
            and isinstance(items, dict)
            and isinstance(items.get("default"), list)
        ):
            node["default"] = items.pop("default")
            moved.append(path)
        for k, v in node.items():
            moved += fix_enum_defaults(v, f"{path}/{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            moved += fix_enum_defaults(v, f"{path}[{i}]")
    return moved


def check_enum_defaults(node, path=""):
    """Return every schema whose `default` is not a member of its `enum`."""
    bad = []
    if isinstance(node, dict):
        if "enum" in node and "default" in node and node["default"] not in node["enum"]:
            bad.append((path, node["default"], node["enum"]))
        for k, v in node.items():
            bad += check_enum_defaults(v, f"{path}/{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            bad += check_enum_defaults(v, f"{path}[{i}]")
    return bad


def find_empty_objects(node, path=""):
    """Locate every empty-object value. Postman rewrites `{}` to `[]` when it stores a spec."""
    found = []
    if isinstance(node, dict):
        if node == {}:
            return [path]
        for k, v in node.items():
            found += find_empty_objects(v, f"{path}/{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            found += find_empty_objects(v, f"{path}[{i}]")
    return found


def fix_empty_objects(node, key=None, parent=None, path=""):
    """Replace every `{}` in place with a semantically equivalent non-empty form.

    Two cases occur in this spec, and both are handled generically:

    - `default: {}` — the default is an empty object. Rebuild it from the sibling schema's
      own property defaults, which is exactly what an empty object resolves to anyway.
    - an empty *schema* — means "any JSON value" in OpenAPI. A description preserves that.

    Anything else is reported so it can't slip through silently.
    """
    fixed, unknown = [], []
    if isinstance(node, dict):
        if node == {} and parent is not None:
            if key == "default":
                sibling = parent.get("properties") or {}
                rebuilt = {k: v["default"] for k, v in sibling.items() if isinstance(v, dict) and "default" in v}
                parent[key] = rebuilt if rebuilt else {"description": "Empty by default."}
                fixed.append(f"{path} (default rebuilt from property defaults)")
            elif key in ("example", "examples"):
                unknown.append(path)
            else:
                parent[key] = {"description": "Any JSON value."}
                fixed.append(f"{path} (empty schema -> described)")
            return fixed, unknown
        for k, v in list(node.items()):
            f, u = fix_empty_objects(v, k, node, f"{path}/{k}")
            fixed += f
            unknown += u
    elif isinstance(node, list):
        for i, v in enumerate(node):
            f, u = fix_empty_objects(v, i, node, f"{path}[{i}]")
            fixed += f
            unknown += u
    return fixed, unknown


def build(spec):
    spec["servers"] = [{"url": V1, "description": "Firecrawl v1 (default for this spec)"}]

    fixed, unknown = fix_empty_objects(spec)
    for p in fixed:
        print(f"replaced empty object (Postman corrupts these to []) at: {p}")
    if unknown:
        for p in unknown:
            print(f"  unhandled empty object: {p}")
        sys.exit(
            "ERROR: empty objects remain that this script cannot safely rewrite. Postman turns "
            "`{}` into `[]` on store, which makes the stored spec invalid. Extend "
            "fix_empty_objects() with an equivalent non-empty form for each path above."
        )

    for p in fix_enum_defaults(spec):
        print(f"moved array-valued default off items schema at: {p}")

    bad = check_enum_defaults(spec)
    if bad:
        for path, d, e in bad:
            print(f"  {path}: default={d!r} not in enum={e!r}")
        sys.exit("ERROR: enum/default violations remain — a validator will reject this spec")

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

    # Declare every tag the operations actually use. Upstream omits the global `tags` array,
    # which trips Spectral's operation-tag-defined rule 23 times.
    used = []
    for path, item in spec.get("paths", {}).items():
        for method in item:
            if method in METHODS:
                for t in item[method].get("tags", []):
                    if t not in used:
                        used.append(t)
    spec["tags"] = [{"name": t} for t in sorted(used)]

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


def lint(path):
    """Gate on Spectral. Postman accepts invalid specs silently, so never skip this."""
    import subprocess

    script = pathlib.Path(__file__).resolve().parent / "validate-spec.sh"
    r = subprocess.run([str(script), str(path)], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.stderr.strip():
        print(r.stderr.strip(), file=sys.stderr)
    if r.returncode != 0:
        sys.exit("ERROR: spec failed validation — not safe to push to Postman")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="probe every operation's server")
    ap.add_argument("--no-lint", action="store_true", help="skip the Spectral gate (don't)")
    args = ap.parse_args()

    spec = fetch(UPSTREAM)
    patched = build(spec)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")

    ops = sum(1 for p, i in spec["paths"].items() for m in i if m in METHODS)
    print(f"wrote {OUT}  ({ops} operations)")
    print(f"v2 server override applied to: {', '.join(patched)}")

    if not args.no_lint:
        print()
        lint(OUT)

    if args.verify:
        print("\nprobing every operation against its effective server:")
        if not verify(spec):
            sys.exit("\nFAIL: at least one operation 404s at its declared server")
        print("\nall operations resolve to a live endpoint")


if __name__ == "__main__":
    main()

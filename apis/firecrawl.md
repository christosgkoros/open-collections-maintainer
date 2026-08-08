# Firecrawl API

- **Workspace:** `6208dfd5-00ce-43de-a652-e8e205b1f194`
- **Collection:** `6045849-d5490486-fd6e-46ed-9ac4-fd3b4fb33dc7` — 22 requests
- **Spec:** `d17a6e5b-48b6-423b-99a1-9d8566870fc9`, root file `index.json`
- **Environment:** `6045849-26245515-55b7-447c-89db-30ec1382d68e`
- **Auth:** collection-level apikey — `Authorization: Bearer {{vault:FIRECRAWL_API_KEY}}`
- **Collection variable:** `baseUrl` = `https://api.firecrawl.dev/v1`
- **Last synced:** 2026-08-08

## Root source

[`mendableai/firecrawl`](https://github.com/mendableai/firecrawl) → `main:apps/api/openapi.json`

The repo also carries `v1-openapi.json` (20 ops, stale) and `openapi-v0.json` (legacy v0).
**Use `openapi.json`** — it is the one that receives new work, including v2 features.

**Do not push upstream as-is.** It has real defects, described below. Build the corrected
version and let the validator gate it:

```bash
python3 scripts/build-firecrawl-spec.py --verify   # writes build/firecrawl.openapi.json
```

The generated file is **not committed** — it is a derived artifact and `build/` is gitignored.
Regenerate whenever you need it; the script is the source of truth, not the output.

## The API is split across two versions

Verified by probing every operation against both versions on 2026-08-08. Re-verify after any
upstream change — this split is not stable.

| Operations | v1 | v2 |
| --- | :---: | :---: |
| 18 of 22 — scrape, batch/scrape ×4, crawl ×5, map, extract ×2, search, team ×2 | ✅ | ✅ |
| `POST /deep-research`, `GET /deep-research/{id}`, `POST /llmstxt`, `GET /llmstxt/{id}` | ✅ | **404** |
| `POST /feedback`, `POST /search/{jobId}/feedback` | **404** | ✅ |

So **neither a blanket `/v1` nor a blanket `/v2` server is correct**. Upstream declares a single
`/v1` server while shipping the two v2-only operations — pushing it unmodified would put two
permanently broken requests into a public collection.

In the collection, the two v2-only requests **hardcode `https://api.firecrawl.dev/v2`** rather
than `{{baseUrl}}`. That is deliberate and is explained in each request's own description. If
`baseUrl` is ever moved to v2, these become correct but the four v1-only operations break.

## What the build script fixes

1. **Operation-level `servers` override** (OpenAPI 3.0 §4.7.5) on the two v2-only operations,
   so every operation resolves to a URL that exists. `--verify` proves it by probing each one.
2. **Enum/default violation.** `deep-research.formats` puts an array-valued `default` on the
   *items* schema, whose enum holds strings — the default can never be a member. Spectral:
   *"default property type must be string"*. Moved onto the array, matching how upstream writes
   its other two `formats` schemas.
3. **Missing global `tags`.** Upstream declares none, tripping `operation-tag-defined` 23 times.
   Derived from the tags actually used.
4. **Empty objects.** See below — this one is a Postman bug, not upstream's.

Spectral: upstream 46 problems / 1 error → generated 22 problems / **0 errors**. The remaining
22 are operations upstream gives a `summary` but no `description`; fixing those would mean
inventing prose.

## Postman rewrites `{}` to `[]`

**`updateSpecFile` corrupts empty objects.** Send a spec containing `{}` and Postman stores `[]`,
which turns a valid document into an invalid one. Demonstrated 2026-08-08: the generated artifact
linted with 0 errors, and the copy Postman served back had 2 — at exactly the two nodes where
`{}` was sent.

```
javascriptReturns.items.properties.value   sent {}  stored []   error: property type must be object
/search scrapeOptions.default              sent {}  stored []   error: default type must be object
```

The build script emits both in equivalent non-empty form (an empty schema becomes
`{"description": "Any JSON value."}`; `default: {}` is rebuilt from the sibling schema's property
defaults). It **hard-fails** if upstream introduces an empty object it cannot map — do not
bypass that.

## Collection sync does not work

`syncCollectionWithSpec` has been called **four times** across 2026-08-07/08. Every call returned
`202` with a task ID; the collection never changed and `getSpecCollections` still reports
`out-of-sync`. No error surfaces anywhere, and there is no MCP tool to poll a collection-sync task.

The 22 requests were therefore added by hand with `createCollectionRequest`, which works reliably.

Two candidate explanations, neither confirmed:

- **The stored spec was invalid** because of the `{}` → `[]` corruption above. This is the better
  theory and is now testable: push a corruption-immune spec and retry the sync.
- **The collection was never generated from the spec.** It was created 2025-02-03; the spec
  2025-04-23 — nearly three months later — so it was associated, not generated. The tool's
  contract says *"You can only sync collections generated from the given spec ID."* Kubernetes
  v1.36, the one spec-backed collection that demonstrably syncs, had its spec created 14 minutes
  **before** its collection.

Radarr, ACP and Spotify share the collection-predates-spec pattern, so expect the same behaviour
there. Resolve Firecrawl before spending effort on them.

## Outstanding

- **Push the corruption-immune spec.** The live copy still carries Postman's 2 injected errors.
  Then retry the sync — that is the experiment that settles the root cause.
- **Five requests sit at the collection root** — `deep-research` ×2, `llmstxt` ×2, `POST /feedback`
  — because no matching folder exists and the MCP server cannot create one. Add `research`,
  `llmstxt` and `feedback` folders in the UI and move them.

## Re-checking drift

```bash
curl -s https://raw.githubusercontent.com/mendableai/firecrawl/main/apps/api/openapi.json \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(sum(1 for p,i in d['paths'].items() for m in i if m in ('get','put','post','delete','patch')),'operations')"
```

Then rebuild with `--verify`, which re-probes every operation and fails if any 404s at its
declared server.

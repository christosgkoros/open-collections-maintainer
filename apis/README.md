# Open Collections — Inventory

Complete registry of everything published under the **Open Collections** Postman team and
surfaced on <https://opencollections.tech/>. This is the source of truth for what exists, where
each collection comes from, and what state it is in.

- **Team:** `opencollections` · team ID `3476680` · owner user ID `6045849`
- **Portal:** <https://opencollections.tech/> — the `WORKSPACES` array in its HTML defines scope
- **Public profile:** <https://www.postman.com/opencollections>
- **Totals:** 16 workspaces · 30 collections · 7 categories
- **Last full sync:** 2026-08-07

Collection UIDs are `6045849-<uuid>`. Workspace and spec IDs are bare UUIDs.

**Status legend** — `in sync`: verified against root source on the date above · `drift`: root
source has moved ahead · `manual`: no machine-readable root source · `blocked`: sync attempted
and did not apply.

---

## Infrastructure

### Dapr API

- **Workspace:** `c2e6df24-da0a-4c94-bdcb-94adb011a212`
- **Root source:** [`dapr/docs`](https://github.com/dapr/docs) branch `v1.18`, path
  `daprdocs/content/en/reference/api/` (17 markdown files)
- **Sync method:** docs diff → hand-patch requests. No spec involved.
- **Details:** [`dapr.md`](dapr.md)

| Collection | UID | Requests | Status |
| --- | --- | --- | --- |
| Dapr API | `6045849-ce93de13-a186-4a2a-b419-1231d4c20e0d` | 66 across 15 folders + 1 at root | **in sync (v1.18)** |

Open items: `info.description` still reads `_Version: 1.15_`; the new "Shutdown sidecar" request
sits at the collection root and needs a `Shutdown API` folder.

### Kubernetes API

- **Workspace:** `883d5848-bfa7-4628-8bc2-5af5aa2cb0ed`
- **Root source:** [`kubernetes/kubernetes`](https://github.com/kubernetes/kubernetes)
  `release-x.x` branches, path `api/openapi-spec/swagger.json` (OpenAPI 2.0, ~4 MB)
- **Sync method:** one collection per GA version — `createSpec` then `generateCollection`
- **Environment:** `Local`, with a `token` variable for auth
- **Details:** [`kubernetes.md`](kubernetes.md)

| Version | Collection UID | Spec ID | Status |
| --- | --- | --- | --- |
| v1.29 | `6045849-58a070f1-2c72-4f9e-9a51-6fc644b1c95d` | — | frozen |
| v1.30 | `6045849-1f1d88ed-29bd-4eee-8880-feb9c9f84a50` | — | frozen |
| v1.31 | `6045849-389bb600-d473-449d-85e1-a11f4b87de79` | — | frozen |
| v1.32 | `6045849-73802104-74e4-4566-b1ac-c59dc0f4f355` | — | frozen |
| v1.33 | `6045849-f247f85f-45b1-4252-a91d-ee6a0922a655` | — | frozen |
| v1.34 | `6045849-a51a17aa-2431-4584-a282-de1d3dab513e` | — | frozen |
| v1.35 | `6045849-72134652-d0a4-4706-b310-96a36a72a9eb` | — | frozen |
| v1.36 | `6045849-c4b570c3-3fc5-42c3-8959-37f270bcb4e7` | `246f8a3e-b11d-46e4-825e-927af6441480` | **in sync** (1123 ops, 771 defs) |

Open items: duplicate orphan `6045849-e38ebf9d-9b6e-436b-be18-194ef2a2444f` needs deleting;
v1.36 is missing from the portal's `WORKSPACES` array; v1.37 exists as a branch but is **not GA**
(newest tag `v1.36.3`) so no collection yet.

---

## Social

### Social Media Flow

- **Workspace:** `1173303e-d847-4219-9d0d-c6c3362ddabf`
- **Nature:** all six are **forks of upstream community collections**, not spec-generated. There
  is nothing to diff mechanically — review against vendor docs by hand.

| Collection | UID | Forked from | Vendor docs |
| --- | --- | --- | --- |
| Bluesky API | `6045849-e303490f-1190-4da8-9b34-080b81f485b6` | `6045849-788308df-700e-46b9-bf1d-5866e41620e2` | <https://docs.bsky.app/> |
| LinkedIn Content APIs | `6045849-661a02fd-19ec-4459-b2a8-38928941bb44` | `17563548-d647a145-ed20-464a-b414-fa596f6ed06e` | [Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api) |
| Mastodon — Post Status | `6045849-8b762d32-5a4d-41c9-80c5-1bb1a4015bf3` | `35240-33c44776-6125-46e9-9d9f-7857f76ac231` | <https://docs.joinmastodon.org/methods/statuses/> |
| OpenAI | `6045849-52eba9cd-d930-4b78-b969-9e443a004a64` | `13183464-90abb798-cb85-43cb-ba3a-ae7941e968da` | [`openai/openai-openapi`](https://github.com/openai/openai-openapi) `openapi.yaml` |
| Threads API | `6045849-fa9543e1-caa3-4747-9514-cd1a00938903` | `6045849-892f65cb-352c-4217-8ba8-26ffae0723af` | <https://developers.facebook.com/docs/threads> |
| Twitter API v2 | `6045849-841c43d0-5967-42a3-b693-1b91bd600ee4` | `9956214-784efcda-ed4c-4491-a4c0-a26470a67400` | <https://docs.x.com/x-api/introduction> |

Status: **manual** for all six — forks, nothing to diff mechanically.

**Relevance reviewed 2026-08-08** — see [`social-media-flow.md`](social-media-flow.md). Every
endpoint is alive; the problems are configuration and one obsolete API. Headlines: Bluesky's
`baseUrl` is literally `/` and must be fixed; OpenAI is built on the legacy Completions endpoint
and should be retired or repointed; LinkedIn's `LinkedIn-Version` header may have sunset and
needs a token to verify; Twitter/X works but its upstream fork has been abandoned since 2023.

---

## Entertainment

### Spotify API

- **Workspace:** `abb28c01-be84-4ff1-a79f-4968a23e77b6`
- **Collection:** `6045849-7d49cd37-a739-4295-a98f-494a53fb0078`
- **Spec:** `2f284b74-d974-4e23-8b7a-9d5878fb47a6` (OpenAPI 3.0, created 2025-04-23) — `in-sync`
- **Root source:** Spotify publishes no official OpenAPI. Docs:
  <https://developer.spotify.com/documentation/web-api>. Community spec:
  [`sonallux/spotify-web-api`](https://github.com/sonallux/spotify-web-api)
  → `official-spotify-open-api.yml` (upstream last pushed 2026-07-24)
- **Status:** needs review — spec-linked collection reports `in-sync`, but the community source
  has moved since the spec was created. Not yet diffed.

### Radarr

- **Workspace:** `ce5e4601-f944-4759-b03f-74598c308157`
- **Collection:** `6045849-e8686ec6-e032-42c0-b0ef-59834ace8aa4`
- **Spec:** `7481b1ee-c2f5-459c-a23b-419653988a59` (OpenAPI 3.0, root file `index.yaml`) — `in-sync`
- **Root source:** <https://radarr.video/docs/api/> — a Swagger UI page whose spec URL resolves to
  [`Radarr/Radarr`](https://github.com/Radarr/Radarr) `develop:src/Radarr.Api.V3/openapi.json`
  (~302 KB raw / 145 KB minified). Track the docs page; the raw URL is what it currently loads and
  could change. Note it serves **`develop`**, not a release branch.
- **Status:** **drift** — 236 ops in spec vs 237 upstream. Missing `GET /api/v3/qualitydefinition/limits`.

### Sonarr

- **Workspace:** `96bfa815-9da6-49c2-9d86-3ba980ac05ca`
- **Collection:** `6045849-d4e91ced-502c-4fed-99d0-66688c31e52a`
- **Spec:** none — collection was not generated from a Postman spec
- **Root source:** <https://sonarr.tv/docs/api/>, which publishes **two** specs:
  - `develop:src/Sonarr.Api.V3/openapi.json` — Sonarr v3.0.0, 234 ops (what the collection covers)
  - `v5-develop:src/Sonarr.Api.V5/openapi.json` — **Sonarr v5.0.0, 233 ops (not covered at all)**
- **Status:** V3 **in sync** — 234 ops, unchanged upstream since the collection was built
  (2024-12-19). **V5 is a gap**: an entire API version with no collection. Decide whether to add a
  `Sonarr V5` collection alongside, mirroring the Kubernetes one-collection-per-version pattern.

---

## Security & Auth

### OAuth 2.0 Authorization Framework

- **Workspace:** `b740d77d-f22d-496f-b16b-d66f131a0a5f`
- **Nature:** hand-authored from RFC / draft text. No spec.

| Collection | UID | Root source | Status |
| --- | --- | --- | --- |
| OAuth 2.0 (RFC 6749) | `6045849-641c8217-b20c-44be-97c4-1a87bc3f5486` | [RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749) | **in sync** — RFC is final |
| OAuth 2.0 Dynamic Client Registration | `6045849-7d3000e1-d2cb-4f49-aed2-6dafa277a1a0` | [RFC 7591](https://datatracker.ietf.org/doc/html/rfc7591), [RFC 7592](https://datatracker.ietf.org/doc/html/rfc7592) | **in sync** — RFCs are final |
| OAuth 2.1 (IETF Draft) | `6045849-50e114fb-f5aa-4a8d-bbbf-933724e4ce9f` | [`draft-ietf-oauth-v2-1`](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/) | **drift** — built 2025-12-08; current is **rev 15** (2026-03-02) |

Check the current draft revision with:
```bash
curl -s "https://datatracker.ietf.org/api/v1/doc/document/?name__startswith=draft-ietf-oauth-v2-1&format=json" \
  | python3 -c "import json,sys;[print(o['name'],o['rev'],o['time']) for o in json.load(sys.stdin)['objects']]"
```

### MCP Authorization (OAuth)

- **Workspace:** `303fa3f0-51ab-4a82-8c53-122fbc5462a3`
- **Collection:** `6045849-618428d5-f047-4052-8306-bf111991d2b4` — MCP Authorization Flow
- **Root source:** <https://modelcontextprotocol.io/specification/draft/basic/authorization>.
  Released revisions live in
  [`modelcontextprotocol/modelcontextprotocol`](https://github.com/modelcontextprotocol/modelcontextprotocol)
  under `docs/specification/` — currently `2024-11-05`, `2025-03-26`, `2025-06-18`, `2025-11-25`,
  **`2026-07-28`**, plus `draft`.
- **Status:** **drift** — built 2025-12-08 against the then-current draft; there is now a released
  `2026-07-28` revision. Decide whether to track `draft` or pin to the newest release.

---

## Agentic & AI

### Agent Connect Protocol

- **Workspace:** `47abcad3-39fe-435c-9331-b30118e53f65`
- **Collection:** `6045849-fbe5fa08-bec8-420d-9baf-e552ef7be81c`
- **Spec:** `cab538ae-8f3d-4575-ada2-a94a55222156` (OpenAPI 3.0, created 2025-04-23) — `in-sync`
- **Root source:** [`agntcy/acp-spec`](https://github.com/agntcy/acp-spec) `main:openapi.json`
  (~103 KB raw / 61 KB minified)
- **Status:** **drift** — spec is v0.2.1, upstream is **v0.2.3**. Same 30 operations; changes are
  schema-level only.

### Agentic Commerce Protocol

- **Workspace:** `692af8cc-3d2c-4496-a6ad-3a5b68ee9e87`
- **Root source:** [`agentic-commerce-protocol/agentic-commerce-protocol`](https://github.com/agentic-commerce-protocol/agentic-commerce-protocol),
  path `spec/<version>/openapi/`. Released versions: `2025-09-29`, `2025-12-12`, `2026-01-16`,
  `2026-01-30`, **`2026-04-17`**, plus `unreleased`.
- **Status:** **drift** — all three specs are pinned at `2025-09-29`, four versions behind.

| Collection | UID | Spec ID | Upstream file (`2026-04-17`) |
| --- | --- | --- | --- |
| Agentic Checkout API | `6045849-f1df2982-bd93-40c3-98ec-790edbbe33e8` | `22f6c43c-2d49-48c7-9f56-25f557d567fc` | `openapi.agentic_checkout.yaml` — 18 KB → **114 KB** |
| Agentic Checkout Webhooks API | `6045849-22f3306b-4a16-4ad2-a6d8-d3ddb7531bc3` | `8710d7b7-afe0-4835-9c09-3c5244cd245d` | `openapi.agentic_checkout_webhook.yaml` — 4.6 KB → 11 KB |
| Agentic Commerce — Delegate Payment API | `6045849-680ba24b-44ea-46f7-8693-1504a73af9ae` | `2848b7ec-d1a8-4c9b-bac0-bccf5ccda2ee` | `openapi.delegate_payment.yaml` — 12.6 KB → 21 KB |

`2026-04-17` also adds three **entirely new surfaces** with no collection yet:
`openapi.cart.yaml` (10.8 KB), `openapi.delegate_authentication.yaml` (31 KB),
`openapi.feed.yaml` (23.5 KB). Syncing this workspace properly means three updates plus three
new collections.

Note: the webhooks spec is misspelled in Postman as **"Agentic Chekout Webhooks API"** — worth
renaming via `updateSpecProperties`.

### Firecrawl API

- **Workspace:** `6208dfd5-00ce-43de-a652-e8e205b1f194`
- **Collection:** `6045849-d5490486-fd6e-46ed-9ac4-fd3b4fb33dc7` — **22 requests**, 7 folders + 5 at root
- **Spec:** `d17a6e5b-48b6-423b-99a1-9d8566870fc9` (OpenAPI 3.0, root file **`index.json`** —
  renamed from `index.yaml` on 2026-08-08; upstream ships JSON, keep the extension matching)
- **Environment:** `6045849-26245515-55b7-447c-89db-30ec1382d68e`
- **Auth:** collection-level apikey, `Authorization: Bearer {{vault:FIRECRAWL_API_KEY}}`
- **Base URL variable:** `baseUrl` = `https://api.firecrawl.dev/v1`
- **Root source:** [`mendableai/firecrawl`](https://github.com/mendableai/firecrawl)
  `main:apps/api/openapi.json`. **Never push it as published** — it declares a single `/v1`
  server while shipping two operations that only exist on v2, and it carries an enum/default
  error. Build the corrected spec with `scripts/build-firecrawl-spec.py --verify`.
- **Status (2026-08-08):** collection carries all 22 operations; spec in Postman is valid and
  byte-identical to the generated artifact (Spectral: 0 errors). **`syncCollectionWithSpec` does
  not work here** — five no-ops. The collection predates its spec, so it was never generated from
  it. Maintain it by hand, or regenerate and accept a new UID.
- **Details:** [`firecrawl.md`](firecrawl.md) — the version split, the three spec defects, the
  Postman corruption, and what is still outstanding.

---

## Productivity

### Google Keep

- **Workspace:** `b9595039-456f-4779-b7fb-13b7e76b3f77`
- **Collection:** `6045849-a2bf7a62-86ee-4a23-84d5-c05c7c8c2cd2` — 7 requests
- **Root source:** Google Discovery document —
  `https://keep.googleapis.com/$discovery/rest?version=v1` (revision `20260803`)
- **Base URL:** `https://keep.googleapis.com/v1`
- **Auth:** OAuth 2.0, scopes `https://www.googleapis.com/auth/keep` and `.../keep.readonly`.
  Collection variables: `clientID`, `clientSecret`, `scopes`.
- **Status:** **in sync** — all 7 discovery methods present: `notes.list`, `notes.create`,
  `notes.get`, `notes.delete`, `notes.permissions.batchCreate`, `notes.permissions.batchDelete`,
  `media.download`.

Re-check drift with:
```bash
curl -s 'https://keep.googleapis.com/$discovery/rest?version=v1' \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print('rev',d['revision'])"
```

### Geekbot API

- **Workspace:** `07a25e48-f227-414f-99bd-bfa2407bf444`
- **Collection:** `6045849-f2751dfc-d5a4-400a-86e8-68b48d48d7eb` — 14 requests, all v1
- **Auth:** apikey header, `{{vault:GEEKBOT_API_KEY}}` · **`baseUrl`** = `https://api.geekbot.com/v1`
- **Root source:** <https://developers.geekbot.com/> — a Scalar reference page that **does publish
  OpenAPI**, at `https://developers.geekbot.com/openapi.json` (and `.yaml`).
- **Status:** **drift, and previously misclassified.** This was recorded as "manual, no OpenAPI",
  which was wrong. The spec has **37 operations across v1 and v2**; the collection covers 14, all
  v1. Missing: the `/v1/me` family (`me`, `me/standups`, `me/teams`) and **the entire v2 surface**
  (19 ops), including out-of-office (`/v2/ooo`), participation endpoints, and the v2 forms of
  standups, polls and reports.
- **Next:** make it spec-backed — `createSpec` from `openapi.json`, then `generateCollection`.
  Because the existing collection predates any spec it can never be synced (see
  [`firecrawl.md`](firecrawl.md)), so generating a fresh one is the cleaner route here.

---

## Utility

### QR Code Generator API

- **Workspace:** `9b429332-61e1-4903-a908-b2a9c6989caa`
- **Collection:** `6045849-732bb262-7b3a-4be6-9f8e-f6b6bc163a2f`
- **Root source:** <https://www.qr-code-generator.com/qr-code-api/> (HTML docs, no OpenAPI)
- **Status:** **manual** — review by hand

### Will It Rain

- **Workspace:** `7c0c5cc2-ec3a-451d-ba2e-846d110d8149`
- **Collection:** `6045849-861561a6-dc30-48bc-b39f-1492c5ae44e3`
- **Root source:** none — first-party project, this repo's owner is the API author
- **Status:** **n/a** — nothing upstream to track

### Classter API

- **Workspace:** `f91134d4-f6ff-4cd1-8fcb-23c3a68bcebf`
- **Collection:** `6045849-7b7dadb4-8305-47f7-8a1b-1c60f2f6e6f3` — Classter Consumer API
- **Base URL variable:** `baseUrl` = `https://consumerapi.classter.com`
- **Auth:** bearer, `{{bearerToken}}`
- **Root source:** the Classter Consumer API does publish a Swagger endpoint, but
  `https://consumerapi.classter.com/swagger/v1/swagger.json` and `/swagger/index.html` both
  return **401** without credentials. There is no anonymously reachable spec.
- **Status:** **manual, blocked on credentials** — cannot be diffed automatically. Either obtain a
  Classter API token for the sync job, or accept that this collection is reviewed by hand.

---

## Not published

Public Postman workspaces owned by the team that are **not** in the portal's `WORKSPACES` array,
and therefore out of scope:

- `ea717bba-8544-4362-a828-da033327c570` — OpenAPI to GRPC Quarkus Workspace (blog companion)
- `7c4684b7-4c78-4695-99f1-6851c95c1463` — Athens Kubernetes Meetup (talk companion)

---

## Sync procedure

1. Re-read the `WORKSPACES` array from <https://opencollections.tech/> — it defines scope.
2. For each entry, compare against the root source recorded above.
   - **Spec-backed** (Kubernetes, Radarr, Firecrawl, ACP, Agentic Commerce, Spotify): check
     `getSpecCollections` for `in-sync` / `out-of-sync`, then `updateSpecFile` +
     `syncCollectionWithSpec`. **Verify afterwards** — a `202` does not mean it applied.
   - **Docs-backed** (Dapr): diff the upstream docs between versions, then patch requests.
   - **Discovery-backed** (Google Keep): compare the discovery `revision` and method list.
   - **Manual / forks** (Social ×6, Geekbot, QR, Classter): review by hand, nothing to diff.
3. Update this file and the per-project docs, then commit and push.

## Known limitations

### Spec file format must match its extension — `updateSpecFile` will not tell you

**This is the single most important gotcha in this repo.** It cost a full debugging cycle and
produced a confidently wrong diagnosis.

On 2026-08-07 the Firecrawl spec's root file was `index.yaml`. It was updated with the contents
of upstream `apps/api/openapi.json` — i.e. **JSON content written into a `.yaml` file**, on the
reasoning that JSON is a subset of YAML and would parse.

`updateSpecFile` accepted it and returned success. It does **not** validate that the content
format matches the file extension; it stores raw text. But Postman's downstream tooling keys off
the extension, so the spec was thereafter unreadable to the sync pipeline.

The failure was silent and misleading:

- `updateSpecFile` → `200`, with a fresh `updatedAt`.
- `syncCollectionWithSpec` → `202` with a task ID, **twice**. Both no-ops.
- The collection never changed; `getSpecCollections` kept reporting `out-of-sync`.
- No error surfaced at any point, and there is no tool to poll a collection-sync task.

**Resolved 2026-08-08** by renaming the root file to `index.json` in the Postman UI, after which
the collection could be updated. The root file is now `index.json` — keep it that way, since
upstream ships JSON.

**Rules to follow:**

1. Before calling `updateSpecFile`, check the current root file's extension with `getSpecFiles`.
2. Either convert the upstream content to match that extension, or rename the file first.
   `updateSpecFile` takes a `name` parameter, but it rejects multiple body properties in one
   call — so renaming and setting content are two separate calls.
3. Never assume "JSON is valid YAML" makes a `.yaml` file safe to fill with JSON. It does not.

**Do not attribute a failed sync to collection divergence without evidence.** That was the
original (wrong) conclusion here. The collection does carry manual edits — hand-written
description, apikey auth via `{{vault:FIRECRAWL_API_KEY}}`, a `baseUrl` variable, script stubs —
which made divergence a plausible-sounding story. It was not the cause.

The eight endpoints this sync adds are `GET /crawl/active`, `POST /deep-research`,
`GET /deep-research/{id}`, `POST /llmstxt`, `GET /llmstxt/{id}`, `GET /team/token-usage`,
`POST /feedback`, `POST /search/{jobId}/feedback`.

### No delete, folder-create, or collection-PATCH tools

The Postman MCP server exposes no tool to delete a collection, create a folder inside an existing
collection, or PATCH collection-level metadata. Consequences:

- Orphaned collections (e.g. the duplicate Kubernetes v1.36) must be deleted in the UI.
- New requests with no matching folder land at the collection root and need moving by hand.
- `info.description` can only be changed via `putCollection` (full replace) or the UI.

### Large spec files

`updateSpecFile` takes the spec as a string parameter, so an agent must reproduce the whole file
in the tool call. Sizes minified: Firecrawl 56 KB (done by hand, feasible), ACP 61 KB, Radarr
145 KB, Agentic Commerce ~210 KB across six files. Prefer a script that reads the file directly
for anything above roughly 60 KB.

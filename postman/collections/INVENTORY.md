# Open Collections — Inventory

Master tracking list for everything published under the **Open Collections** Postman team
(`opencollections`, team ID `3476680`) and surfaced on <https://opencollections.tech/>.

- **Portal:** <https://opencollections.tech/> — the `WORKSPACES` array in its HTML is the
  authoritative list of what is published. Workspaces that exist in Postman but are not in
  that array are not part of Open Collections (see [Not published](#not-published)).
- **Public profile:** <https://www.postman.com/opencollections>
- **Totals:** 16 workspaces · 30 collections · 7 categories
- **Last full sync:** 2026-08-07

## Collections

Legend for **Status**: `in sync` = verified against the root source on the date above ·
`drift` = root source has moved ahead · `manual` = no machine-readable root source, curated by hand.

### Infrastructure (1 workspace)

| Collection | UID | Root source | Status |
| --- | --- | --- | --- |
| Dapr API | `6045849-ce93de13-a186-4a2a-b419-1231d4c20e0d` | [`dapr/docs`](https://github.com/dapr/docs) `v1.18` → `daprdocs/content/en/reference/api/` | in sync (v1.18) |
| Kubernetes API v1.29 | `6045849-58a070f1-2c72-4f9e-9a51-6fc644b1c95d` | `kubernetes/kubernetes` `release-1.29` → `api/openapi-spec/swagger.json` | in sync (frozen) |
| Kubernetes API v1.30 | `6045849-1f1d88ed-29bd-4eee-8880-feb9c9f84a50` | `release-1.30` | in sync (frozen) |
| Kubernetes API v1.31 | `6045849-389bb600-d473-449d-85e1-a11f4b87de79` | `release-1.31` | in sync (frozen) |
| Kubernetes API v1.32 | `6045849-73802104-74e4-4566-b1ac-c59dc0f4f355` | `release-1.32` | in sync (frozen) |
| Kubernetes API v1.33 | `6045849-f247f85f-45b1-4252-a91d-ee6a0922a655` | `release-1.33` | in sync (frozen) |
| Kubernetes API v1.34 | `6045849-a51a17aa-2431-4584-a282-de1d3dab513e` | `release-1.34` | in sync (frozen) |
| Kubernetes API v1.35 | `6045849-72134652-d0a4-4706-b310-96a36a72a9eb` | `release-1.35` | in sync (frozen) |
| Kubernetes API v1.36 | `6045849-c4b570c3-3fc5-42c3-8959-37f270bcb4e7` | `release-1.36` (spec `246f8a3e-b11d-46e4-825e-927af6441480`) | in sync — **not yet on the portal** |

Details: [`dapr.md`](dapr.md) · [`kubernetes.md`](kubernetes.md)

### Social (1 workspace, 6 collections)

Workspace `1173303e-d847-4219-9d0d-c6c3362ddabf` — Social Media Flow.
All six are **forks of upstream community collections**, not generated from a spec.

| Collection | UID | Root source | Status |
| --- | --- | --- | --- |
| Bluesky API | `6045849-e303490f-1190-4da8-9b34-080b81f485b6` | fork of `6045849-788308df-…`; vendor docs <https://docs.bsky.app/> | manual |
| LinkedIn Content APIs | `6045849-661a02fd-19ec-4459-b2a8-38928941bb44` | fork of `17563548-d647a145-…` | manual |
| Mastodon — Post Status | `6045849-8b762d32-5a4d-41c9-80c5-1bb1a4015bf3` | fork of `35240-33c44776-…` | manual |
| OpenAI | `6045849-52eba9cd-d930-4b78-b969-9e443a004a64` | fork of `13183464-90abb798-…` | manual |
| Threads API | `6045849-fa9543e1-caa3-4747-9514-cd1a00938903` | fork of `6045849-892f65cb-…` | manual |
| Twitter API v2 | `6045849-841c43d0-5967-42a3-b693-1b91bd600ee4` | fork of `9956214-784efcda-…` | manual |

### Entertainment (3 workspaces)

| Collection | UID | Root source | Status |
| --- | --- | --- | --- |
| Spotify API | `6045849-7d49cd37-a739-4295-a98f-494a53fb0078` | spec `2f284b74-d974-4e23-8b7a-9d5878fb47a6`; upstream <https://developer.spotify.com/documentation/web-api> (community OpenAPI: `sonallux/spotify-web-api`) | needs review |
| Radarr | `6045849-e8686ec6-e032-42c0-b0ef-59834ace8aa4` | spec `7481b1ee-c2f5-459c-a23b-419653988a59` ← [`Radarr/Radarr`](https://github.com/Radarr/Radarr) `develop:src/Radarr.Api.V3/openapi.json` | **drift** (+1 op) |
| Sonarr | `6045849-d4e91ced-502c-4fed-99d0-66688c31e52a` | [`Sonarr/Sonarr`](https://github.com/Sonarr/Sonarr) `develop:src/Sonarr.Api.V3/openapi.json` (no Postman spec) | in sync (234 ops, unchanged) |

### Security & Auth (2 workspaces, 4 collections)

| Collection | UID | Root source | Status |
| --- | --- | --- | --- |
| OAuth 2.0 (RFC 6749) | `6045849-641c8217-b20c-44be-97c4-1a87bc3f5486` | [RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749) | in sync (RFC is final) |
| OAuth 2.0 Dynamic Client Registration | `6045849-7d3000e1-d2cb-4f49-aed2-6dafa277a1a0` | [RFC 7591](https://datatracker.ietf.org/doc/html/rfc7591) / [RFC 7592](https://datatracker.ietf.org/doc/html/rfc7592) | in sync (RFCs are final) |
| OAuth 2.1 (IETF Draft) | `6045849-50e114fb-f5aa-4a8d-bbbf-933724e4ce9f` | `draft-ietf-oauth-v2-1` | **drift** — built 2025-12-08, current rev **15** (2026-03-02) |
| MCP Authorization Flow | `6045849-618428d5-f047-4052-8306-bf111991d2b4` | <https://modelcontextprotocol.io/specification/draft/basic/authorization> | **drift** — built against the 2025-12 draft; released revisions now include **2026-07-28** |

### Agentic & AI (3 workspaces, 5 collections)

| Collection | UID | Root source | Status |
| --- | --- | --- | --- |
| Agent Connect Protocol | `6045849-fbe5fa08-bec8-420d-9baf-e552ef7be81c` | spec `cab538ae-8f3d-4575-ada2-a94a55222156` ← [`agntcy/acp-spec`](https://github.com/agntcy/acp-spec) `main:openapi.json` | **drift** — v0.2.1 → v0.2.3 (same 30 ops, schema-level changes) |
| Agentic Checkout API | `6045849-f1df2982-bd93-40c3-98ec-790edbbe33e8` | spec `22f6c43c-2d49-48c7-9f56-25f557d567fc` ← [`agentic-commerce-protocol`](https://github.com/agentic-commerce-protocol/agentic-commerce-protocol) `spec/2025-09-29/openapi/openapi.agentic_checkout.yaml` | **drift** — latest spec version is `2026-04-17` |
| Agentic Checkout Webhooks API | `6045849-22f3306b-4a16-4ad2-a6d8-d3ddb7531bc3` | spec `8710d7b7-afe0-4835-9c09-3c5244cd245d` ← `…/openapi.agentic_checkout_webhook.yaml` | **drift** — same |
| Agentic Commerce — Delegate Payment API | `6045849-680ba24b-44ea-46f7-8693-1504a73af9ae` | spec `2848b7ec-d1a8-4c9b-bac0-bccf5ccda2ee` ← `…/openapi.delegate_payment.yaml` | **drift** — same |
| Firecrawl API | `6045849-d5490486-fd6e-46ed-9ac4-fd3b4fb33dc7` | spec `d17a6e5b-48b6-423b-99a1-9d8566870fc9` (root file `index.yaml`) ← [`mendableai/firecrawl`](https://github.com/mendableai/firecrawl) `main:apps/api/openapi.json` | **drift** — 14 requests vs 22 upstream ops; Postman reports `out-of-sync` |

### Productivity (2 workspaces)

| Collection | UID | Root source | Status |
| --- | --- | --- | --- |
| Google Keep API | `6045849-a2bf7a62-86ee-4a23-84d5-c05c7c8c2cd2` | Discovery doc `https://keep.googleapis.com/$discovery/rest?version=v1` (rev `20260803`) | in sync (7/7 methods) |
| Geekbot API | `6045849-f2751dfc-d5a4-400a-86e8-68b48d48d7eb` | <https://geekbot.com/developers/> | manual |

### Utility (3 workspaces)

| Collection | UID | Root source | Status |
| --- | --- | --- | --- |
| QR Code Generator API | `6045849-732bb262-7b3a-4be6-9f8e-f6b6bc163a2f` | <https://www.qr-code-generator.com/qr-code-api/> | manual |
| Will it rain API | `6045849-861561a6-dc30-48bc-b39f-1492c5ae44e3` | first-party project — no external root source | n/a |
| Classter Consumer API | `6045849-7b7dadb4-8305-47f7-8a1b-1c60f2f6e6f3` | Classter platform API docs | manual |

## Not published

Public Postman workspaces owned by the team that are deliberately **not** in the portal's
`WORKSPACES` array, and therefore out of scope for syncing:

- `ea717bba-8544-4362-a828-da033327c570` — OpenAPI to GRPC Quarkus Workspace (blog companion)
- `7c4684b7-4c78-4695-99f1-6851c95c1463` — Athens Kubernetes Meetup (talk companion)

## Sync procedure

1. Re-read the `WORKSPACES` array from <https://opencollections.tech/> — it is the source of
   truth for what is in scope.
2. For each entry, resolve the root source in the table above and compare.
   - **Spec-backed** (Radarr, Firecrawl, ACP, Agentic Commerce, Spotify, Kubernetes):
     `updateSpecFile` with fresh upstream content, then `syncCollectionWithSpec`.
     Check `getSpecCollections` first — it reports `in-sync` / `out-of-sync` per collection.
   - **Docs-backed** (Dapr): diff the upstream docs between the old and new version
     (`gh api repos/<repo>/compare/<old>...<new>`), then patch requests with
     `updateCollectionRequest` / `createCollectionRequest`.
   - **Manual / forks**: review by hand; there is nothing to diff automatically.
3. Update this file and the per-project docs, then commit.

## Known limitations

The Postman MCP server exposes no tool to **delete** a collection or to **create a folder**
inside an existing collection. Two consequences, both flagged in the per-project docs:

- Orphaned collections must be deleted from the Postman UI.
- New endpoints added to a collection that has no matching folder land at the collection root
  and need to be dragged into place manually.

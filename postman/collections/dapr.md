# Dapr API Collection

- **Collection ID:** `6045849-ce93de13-a186-4a2a-b419-1231d4c20e0d`
- **Source:** https://github.com/dapr/docs (default branch: `v1.18`)
- **Docs path:** `daprdocs/content/en/reference/api/`
- **Current version:** 1.18
- **Last updated:** 2026-08-07

## API Folders

| Folder | Endpoints | Notes |
|--------|-----------|-------|
| Actors API | 14 | GET/POST/PUT/DELETE method variants |
| Bindings API | 2 | Output binding + discovery |
| Configuration API | 3 | Get, subscribe, unsubscribe |
| Cryptography API | 2 | Encrypt/decrypt (alpha1) |
| Distributed Lock API | 2 | Lock/unlock (alpha1) |
| Health API | 2 | Liveness (`/healthz`) + readiness (`/healthz/outbound`) |
| Metadata API | 2 | Get sidecar info + set custom attribute |
| Pub/sub API | 2 | Single + bulk publish |
| Secrets API | 2 | Get + bulk get |
| Service Invocation API | 15 | Dapr, HTTPEndpoint, FQDN variants x 5 methods |
| State Management API | 9 | CRUD + bulk + query (alpha1) + transactions |
| Workflow API | 7 | Start/terminate/raise/pause/resume/purge/get (deprecated) |
| Jobs API | 3 | Schedule/get/delete — **stable at `v1.0` since 1.18** |
| Placement API | 1 | Get placement table |
| Conversation API (alpha) | 1 | LLM converse (alpha2) |
| _(collection root)_ | 1 | Shutdown sidecar — see note below |

## Version History

### v1.17 → v1.18 (2026-08-07)

Upstream diff: `gh api repos/dapr/docs/compare/v1.17...v1.18` — five files changed.

- **Shutdown API (new):** added `POST /v1.0/shutdown`. Graceful by default; the optional
  `Dapr-Force-Shutdown` header skips draining and exits via `os.Exit(1)`. Returns `204`.
  Added with a `204 - No Content` saved response.
- **Jobs API:** graduated from alpha. All three endpoints moved from `/v1.0-alpha1/jobs/…`
  to `/v1.0/jobs/…`. The "currently in alpha" banner was dropped upstream.
- **Conversation API:** `metadata` semantics changed materially. It is no longer a
  component-config override channel — it is now up to 16 free-form key/value tags
  (max 64-char keys, 512-char values), mirroring OpenAI's `metadata`. Credentials such as
  `api_key` must move into the component YAML; typed per-request overrides now go in
  `parameters` (wrapped in `google.protobuf.Any`). `toolChoice` gained `none`.
  The request body example was updated to match upstream.
- **Workflow API:** start-workflow now returns `409` when an instance ID is not yet reusable
  — the workflow *and every child workflow it created* must be in a terminal state
  (`COMPLETED`, `FAILED`, `TERMINATED`). Added a `409 - Conflict` saved response.
- **Actors API:** upstream added ~130 lines documenting `SubscribeActorEventsAlpha1`.
  This is a **bidirectional gRPC streaming RPC**, not an HTTP endpoint, so it is out of
  scope for this HTTP collection. No change made.

### v1.15 → v1.17 (2026-03-25)

- **Health API:** Added `/v1.0/healthz/outbound` readiness endpoint
- **Pub/sub API:** Bulk publish promoted from `v1.0-alpha1` to `v1.0`
- **Conversation API:** Path updated from `v1.0-alpha1` to `v1.0-alpha2`; request body revamped with structured message format (`ofUser`, `ofAssistant`, `ofTool`, etc.), tool calling support (`tools`, `toolChoice`), `responseFormat`, `promptCacheRetention`; response now includes `choices` with `finishReason` and `usage` stats
- **Jobs API:** Added `overwrite` and `failure_policy` fields to schedule job request body
- **Workflow API:** Marked as deprecated

## Outstanding manual steps

Two things could not be done through the Postman MCP server:

1. **Move "Shutdown sidecar" into a folder.** The MCP server has no folder-creation tool, so
   the new request was created at the collection root. Create a `Shutdown API` folder in the
   Postman UI and drag it in, to match the other API groups.
2. **Update the collection description.** `info.description` still opens with `_Version: 1.15_`,
   which has been stale since the 1.17 pass. There is no PATCH-collection tool — only
   `putCollection`, which replaces the entire collection. Edit it in the UI, or do a full
   `putCollection` round-trip.

## How to Update

1. Check the default branch of `dapr/docs`: `gh api repos/dapr/docs --jq '.default_branch'`
   (branches named `v1.19`+ may exist before release — the default branch is the released one)
2. Diff the API reference directory between versions:
   ```bash
   gh api "repos/dapr/docs/compare/v<old>...v<new>" \
     -q '.files[] | select(.filename|test("reference/api/")) | "\(.status)\t+\(.additions)/-\(.deletions)\t\(.filename)"'
   ```
3. Pull the patch for each changed file with `-q '.files[] | select(...) | .patch'`
4. Apply changes via `updateCollectionRequest` / `createCollectionRequest` / `createCollectionResponse`
5. Update this file and [`INVENTORY.md`](INVENTORY.md)

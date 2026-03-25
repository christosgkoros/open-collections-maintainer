# Dapr API Collection

- **Collection ID:** `6045849-ce93de13-a186-4a2a-b419-1231d4c20e0d`
- **Source:** https://github.com/dapr/docs (default branch: `v1.17`)
- **Docs path:** `daprdocs/content/en/reference/api/`
- **Current version:** 1.17
- **Last updated:** 2026-03-25

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
| Jobs API (alpha) | 3 | Schedule/get/delete (alpha1) |
| Placement API | 1 | Get placement table |
| Conversation API (alpha) | 1 | LLM converse (alpha2) |

## Version History

### v1.15 → v1.17 (2026-03-25)

- **Health API:** Added `/v1.0/healthz/outbound` readiness endpoint
- **Pub/sub API:** Bulk publish promoted from `v1.0-alpha1` to `v1.0`
- **Conversation API:** Path updated from `v1.0-alpha1` to `v1.0-alpha2`; request body revamped with structured message format (`ofUser`, `ofAssistant`, `ofTool`, etc.), tool calling support (`tools`, `toolChoice`), `responseFormat`, `promptCacheRetention`; response now includes `choices` with `finishReason` and `usage` stats
- **Jobs API:** Added `overwrite` and `failure_policy` fields to schedule job request body
- **Workflow API:** Marked as deprecated

## How to Update

1. Check the default branch of `dapr/docs` repo: `gh api repos/dapr/docs --jq '.default_branch'`
2. List API doc files: `gh api repos/dapr/docs/contents/daprdocs/content/en/reference/api -q '.[].name'`
3. Fetch individual docs: `gh api repos/dapr/docs/contents/daprdocs/content/en/reference/api/<filename> -q .content | base64 -d`
4. Compare with current collection and update via Postman MCP tools
5. Update this file with changes

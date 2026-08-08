# open-collections-maintainer

You are the maintainer of the Open Collections project. Your purpose is to keep up-to-date
Postman collections for projects that don't publish their own. You weekly observe these
projects' documentation and update workspaces and collections.

This file is the harness-agnostic contract for any agent working in this repo. Anything
specific to a single agent runtime belongs in that runtime's own file (e.g. `CLAUDE.md`).

## Preflight: check the authenticated Postman user

**Before any sync run, call `getAuthenticatedUser` and confirm it returns:**

| Field | Expected |
| --- | --- |
| `id` | `6045849` |
| `username` | `gkorosc` |
| `teamId` | `3476680` |
| `teamName` | `Open Collections` |

If it returns anything else, stop and re-authenticate. Do not proceed.

Every Open Collections resource is owned by user `6045849`. On 2026-08-08 the authenticated
identity silently swapped mid-session to a different account (`cgkoros` / `23548826`, team
`Postman` / `6029`) — most likely an OAuth token refresh landing on the wrong account.

This failure is **silent and easy to misread**:

- Reads keep working. Every Open Collections workspace is public, so `getCollection`,
  `getWorkspace`, and friends all return `200` under the wrong identity. Nothing signals that
  you are no longer the owner.
- Writes are the real hazard. The wrong account is not a member of team `3476680`, so writes
  will fail or behave unpredictably.
- Re-check after any long-running session or after a re-authentication prompt, not just at the
  start.

Confirm ownership on write responses too — collection and spec mutations echo `owner` /
`createdBy`, which should read `6045849`.

## Repo layout

- `apis/` — one markdown context file per API we maintain, plus `README.md`, the registry
  covering all 16 workspaces / 30 collections. An API gets its own file once it needs more than
  a registry row: root source, IDs, quirks, procedure, outstanding work. Currently `dapr.md`,
  `kubernetes.md`, `firecrawl.md`.
  **These are notes, not collection exports** — no Postman collection or spec JSON lives here.
- `scripts/` — the tooling those notes refer to. `validate-spec.sh` lints any spec with Spectral;
  `build-<api>-spec.py` reconstructs a corrected spec from upstream.
- `build/` — gitignored. Generated specs land here. **Never commit a spec artifact**; the script
  that produces it is the source of truth, so it stays correct as upstream moves.
- `astro/` — a self-contained Astropods agent scaffold, unrelated to collection maintenance.
  Out of scope for sync work.

## Scope

The published surface is the **Open Collections** Postman team (`opencollections`,
team ID `3476680`), fronted by <https://opencollections.tech/>.

**The `WORKSPACES` array in that page's HTML is the authoritative list of what is in scope** —
16 workspaces, 30 collections. Re-read it at the start of any sync; do not infer scope from
the Postman workspace list, because the team also owns public workspaces that are talk or blog
companions and are deliberately not published.

## Maintained projects

Full inventory — every collection with its root source, sync status, and known issues — is in
[`apis/README.md`](apis/README.md). **Start there.**

Two projects have multi-version workflows and are documented separately:

### Dapr

- **Collection:** `6045849-ce93de13-a186-4a2a-b419-1231d4c20e0d`
- **Source repo:** `dapr/docs` (default branch tracks the released version)
- **Docs path:** `daprdocs/content/en/reference/api/`
- **Current version:** 1.18
- **Update strategy:** compare endpoints and update the existing collection in place
- **Details:** [`apis/dapr.md`](apis/dapr.md)

### Kubernetes API

- **Workspace:** `883d5848-bfa7-4628-8bc2-5af5aa2cb0ed`
- **Source repo:** `kubernetes/kubernetes` (`release-x.x` branches)
- **Spec path:** `api/openapi-spec/swagger.json`
- **Spec type:** OpenAPI 2.0
- **Latest version:** 1.36 — only cut a collection once the version is GA (check `releases/latest`)
- **Update strategy:** one collection per version — create a spec from swagger.json, then generate
- **Details:** [`apis/kubernetes.md`](apis/kubernetes.md)

## Tools

- **Postman:** always use the Postman MCP server (`mcp.postman.com`). Never use the Postman CLI
  or direct calls to `api.postman.com`.
- **GitHub:** always use the `gh` CLI.

## Workflows

### Dapr — single collection, updated in place

1. Check the default branch of `dapr/docs`. Branches for unreleased versions may exist; the
   default branch is the released one.
2. Diff the API reference directory between the recorded version and the new one:
   `gh api "repos/dapr/docs/compare/v<old>...v<new>"`, filtered to `reference/api/`.
3. Pull the patch for each changed file and work out the HTTP-level impact. Not every docs
   change is a collection change — v1.18 added 130 lines documenting a gRPC streaming RPC that
   has no HTTP surface.
4. Apply changes: update existing requests, create new ones, add saved responses for new status
   codes.
5. Record the change in `apis/dapr.md` and the registry (`apis/README.md`).
6. Commit and push.

### Kubernetes — one collection per version

1. List `release-x.x` branches, and check `releases/latest` to confirm the version is GA.
   A release branch is cut before GA and its swagger.json churns daily until release.
2. Fetch `api/openapi-spec/swagger.json` from the branch (~4MB, under the 10MB Postman limit).
3. Create a spec (`createSpec`, type `OPENAPI:2.0`).
4. Generate a collection (`generateCollection`, folder strategy `Tags`, request names `Fallback`,
   parameters `Example`).
5. Update `apis/kubernetes.md` and the registry (`apis/README.md`).
6. Commit and push.

### Spec-backed collections — Radarr, Firecrawl, ACP, Agentic Commerce, Spotify

**First check whether the collection can sync at all.** `syncCollectionWithSpec` only works on a
collection that was *generated from* the spec. Compare `createdAt` on both: if the collection
predates the spec, the two were merely associated, and every sync call will return `202` and
silently do nothing — proven over five attempts on Firecrawl with a valid, byte-perfect spec in
place. Of the spec-backed collections, only Kubernetes v1.36 has the spec created first.

For a syncable collection:

1. `getSpecCollections` reports `in-sync` / `out-of-sync` — check it first. On a non-generated
   collection this reflects "no diff since linking", not "syncable".
2. Build and **lint** the spec — `scripts/validate-spec.sh` must pass with 0 errors. Postman
   accepts invalid specs without complaint.
3. `updateSpecFile`, then read the spec back and lint *that* — Postman rewrites `{}` to `[]` on
   store and can turn a clean document into an invalid one.
4. `syncCollectionWithSpec`, then **verify by re-reading the collection**.

For a non-generated collection, either hand-maintain it with `createCollectionRequest`, or
regenerate with `generateCollection` — which fixes syncing permanently but changes the collection
UID, so the portal's `WORKSPACES` array and any shared links need updating.

### Detecting drift cheaply

To check whether a large spec has moved without pulling megabytes into context, diff upstream
against the date the Postman spec was created:

```bash
OLD=$(gh api "repos/<owner>/<repo>/commits?sha=<branch>&until=<spec createdAt>&per_page=1" -q '.[0].sha')
gh api "repos/<owner>/<repo>/contents/<path>?ref=$OLD"    -H "Accept: application/vnd.github.v3.raw" > old.json
gh api "repos/<owner>/<repo>/contents/<path>?ref=<branch>" -H "Accept: application/vnd.github.v3.raw" > new.json
# compare the paths / definitions key sets
```

## Postman MCP surface — known limitations

These are properties of the Postman MCP server, not of any particular agent runtime. All of them
were hit in practice; see the registry (`apis/README.md`) for the specific incidents.

- **A spec file's content must match its extension.** `updateSpecFile` stores raw text and does
  **not** validate the two against each other, but Postman's downstream tooling keys off the
  extension. Writing JSON into an `index.yaml` root file returns success and then silently breaks
  every sync from that spec. Check the current extension with `getSpecFiles` first, and either
  convert the content or rename the file. Renaming uses the `name` parameter, and the endpoint
  rejects multiple body properties per call — so rename and set content in two separate calls.
- **A `202` from `syncCollectionWithSpec` does not mean the sync happened.** There is no tool to
  poll a collection-sync task, and a broken spec produces no error anywhere in the chain. Always
  re-read the collection afterwards and confirm the expected endpoints exist. When a sync no-ops,
  suspect the spec file before blaming collection divergence — divergence is a plausible-sounding
  story that has already been wrong once.
- **No delete tool.** Orphaned or duplicate collections must be removed from the Postman UI.
- **No folder-create tool.** `createCollectionRequest` takes a `folderId` but folders can only be
  created via `putCollection`, which replaces the whole collection. New requests that don't have
  an existing folder land at the collection root and need to be moved by hand.
- **No collection-level PATCH.** `info.description` can only be changed via `putCollection` or
  the UI.
- **`updateSpecFile` takes the spec as a string.** An agent must reproduce the entire file in the
  call, so large specs are impractical and risky to push by hand. Prefer a script that reads the
  file directly. Reference sizes (minified): Firecrawl 56 KB, ACP 61 KB, Radarr 145 KB, the six
  Agentic Commerce files ~210 KB total.

## Conventions

- Every collection change is recorded in the registry (`apis/README.md`) and, where one exists, the per-project
  doc under `apis/`.
- Commit and push after a sync. Include what changed upstream and what was applied, and state
  explicitly anything that was left undone.
- Report honestly: if a sync did not land, say so. A silently failed write to a public collection
  is worse than a known gap.

# open-collections-maintainer

You are the maintainer of the Open Collections project. Your purpose is to keep up-to-date
Postman collections for projects that don't publish their own. You weekly observe these
projects' documentation and update workspaces and collections.

This file is the harness-agnostic contract for any agent working in this repo. Anything
specific to a single agent runtime belongs in that runtime's own file (e.g. `CLAUDE.md`).

## Repo layout

- `postman/collections/` — docs for the **maintained public collections** only.
  `INVENTORY.md` is the registry; `dapr.md` and `kubernetes.md` cover the two multi-version
  projects. Nothing else belongs in here.
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
[`postman/collections/INVENTORY.md`](postman/collections/INVENTORY.md). **Start there.**

Two projects have multi-version workflows and are documented separately:

### Dapr

- **Collection:** `6045849-ce93de13-a186-4a2a-b419-1231d4c20e0d`
- **Source repo:** `dapr/docs` (default branch tracks the released version)
- **Docs path:** `daprdocs/content/en/reference/api/`
- **Current version:** 1.18
- **Update strategy:** compare endpoints and update the existing collection in place
- **Details:** [`postman/collections/dapr.md`](postman/collections/dapr.md)

### Kubernetes API

- **Workspace:** `883d5848-bfa7-4628-8bc2-5af5aa2cb0ed`
- **Source repo:** `kubernetes/kubernetes` (`release-x.x` branches)
- **Spec path:** `api/openapi-spec/swagger.json`
- **Spec type:** OpenAPI 2.0
- **Latest version:** 1.36 — only cut a collection once the version is GA (check `releases/latest`)
- **Update strategy:** one collection per version — create a spec from swagger.json, then generate
- **Details:** [`postman/collections/kubernetes.md`](postman/collections/kubernetes.md)

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
5. Record the change in `postman/collections/dapr.md` and `INVENTORY.md`.
6. Commit and push.

### Kubernetes — one collection per version

1. List `release-x.x` branches, and check `releases/latest` to confirm the version is GA.
   A release branch is cut before GA and its swagger.json churns daily until release.
2. Fetch `api/openapi-spec/swagger.json` from the branch (~4MB, under the 10MB Postman limit).
3. Create a spec (`createSpec`, type `OPENAPI:2.0`).
4. Generate a collection (`generateCollection`, folder strategy `Tags`, request names `Fallback`,
   parameters `Example`).
5. Update `postman/collections/kubernetes.md` and `INVENTORY.md`.
6. Commit and push.

### Spec-backed collections — Radarr, Firecrawl, ACP, Agentic Commerce, Spotify

1. `getSpecCollections` reports `in-sync` / `out-of-sync` per collection — check it first.
2. Update the spec's root file with fresh upstream content (`updateSpecFile`).
3. `syncCollectionWithSpec`, then **verify** (see below).

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
were hit in practice; see `INVENTORY.md` for the specific incidents.

- **A `202` from `syncCollectionWithSpec` does not mean the sync happened.** There is no tool to
  poll a collection-sync task. Always re-read the collection afterwards and confirm the expected
  endpoints exist. A collection that has diverged from its generated form (manual description,
  auth, variables, scripts) appears to need interactive conflict resolution in the UI — the API
  call is accepted and then silently does nothing.
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

- Every collection change is recorded in `INVENTORY.md` and, where one exists, the per-project
  doc under `postman/collections/`.
- Commit and push after a sync. Include what changed upstream and what was applied, and state
  explicitly anything that was left undone.
- Report honestly: if a sync did not land, say so. A silently failed write to a public collection
  is worse than a known gap.

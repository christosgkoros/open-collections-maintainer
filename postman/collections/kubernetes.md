# Kubernetes API Collections

- **Workspace ID:** `883d5848-bfa7-4628-8bc2-5af5aa2cb0ed`
- **Workspace name:** Kubernetes API
- **Source repo:** `kubernetes/kubernetes`
- **Spec path:** `api/openapi-spec/swagger.json`
- **Branch pattern:** `release-x.x` (e.g. `release-1.36`)
- **Spec type:** OpenAPI 2.0 (Swagger)
- **Last updated:** 2026-08-07

## Existing Collections

| Version | Collection ID | Branch | Postman spec | Status |
| ------- | ------------- | ------ | ------------ | ------ |
| v1.29 | `58a070f1-2c72-4f9e-9a51-6fc644b1c95d` | `release-1.29` | — | frozen |
| v1.30 | `1f1d88ed-29bd-4eee-8880-feb9c9f84a50` | `release-1.30` | — | frozen |
| v1.31 | `389bb600-d473-449d-85e1-a11f4b87de79` | `release-1.31` | — | frozen |
| v1.32 | `73802104-74e4-4566-b1ac-c59dc0f4f355` | `release-1.32` | — | frozen |
| v1.33 | `f247f85f-45b1-4252-a91d-ee6a0922a655` | `release-1.33` | — | frozen |
| v1.34 | `a51a17aa-2431-4584-a282-de1d3dab513e` | `release-1.34` | — | frozen |
| v1.35 | `72134652-d0a4-4706-b310-96a36a72a9eb` | `release-1.35` | — | frozen |
| v1.36 | `c4b570c3-3fc5-42c3-8959-37f270bcb4e7` | `release-1.36` | `246f8a3e-b11d-46e4-825e-927af6441480` | **in sync** |

Verified 2026-08-07: `release-1.36`'s `swagger.json` is byte-identical to the copy the Postman
spec was created from on 2026-05-14 — 1123 operations, 771 definitions, no change across the
`v1.36.0`–`v1.36.3` patch releases. `getSpecCollections` reports `in-sync`.

## Open items

### Duplicate v1.36 collection

There are **two** collections named `Kubernetes API v1.36` in the workspace:

| Collection ID | Created | Spec-linked | Keep? |
| --- | --- | --- | --- |
| `c4b570c3-3fc5-42c3-8959-37f270bcb4e7` | 2026-05-14 | yes → `246f8a3e-…` | **keep** |
| `e38ebf9d-9b6e-436b-be18-194ef2a2444f` | 2026-04-19 | no (orphan) | **delete** |

The Postman MCP server exposes no collection-delete tool, so `e38ebf9d-…` must be removed
from the Postman UI.

### v1.36 is missing from the portal

The `WORKSPACES` array in <https://opencollections.tech/> still lists v1.29–v1.35 and its
Kubernetes description says "covering all versions from v1.29 through v1.35". Add:

```js
{ name: 'Kubernetes API v1.36', uid: '6045849-c4b570c3-3fc5-42c3-8959-37f270bcb4e7' },
```

### v1.37 — deliberately not created yet

`release-1.37` exists and carries a `swagger.json` (4,475,339 bytes, branch head 2026-08-06),
but **1.37 is not GA** — the newest tag is `v1.36.3`. The branch churns daily until release,
so a collection cut now would be stale within days. Create it once `v1.37.0` is tagged.

## How to Add a New Version

1. **Check for new release branches, and confirm the version is GA:**

   ```bash
   gh api repos/kubernetes/kubernetes/branches --paginate -q '.[].name' | grep '^release-1\.' | sort -t. -k2 -n
   gh api repos/kubernetes/kubernetes/releases/latest -q '.tag_name'   # only cut collections at or below this
   ```

2. **Download the swagger.json** (~4.1MB, under the 10MB Postman limit):

   ```bash
   gh api "repos/kubernetes/kubernetes/contents/api/openapi-spec/swagger.json?ref=release-X.XX" \
     -H "Accept: application/vnd.github.v3.raw" > swagger.json
   ```

3. **Create a spec in Postman** using `mcp__postman__createSpec`:
   - `workspaceId`: `883d5848-bfa7-4628-8bc2-5af5aa2cb0ed`
   - `name`: `Kubernetes API vX.XX`
   - `type`: `OPENAPI:2.0`
   - `files`: single file with path `swagger.json` and the content

4. **Generate a collection** using `mcp__postman__generateCollection`:
   - `specId`: from step 3 response
   - `elementType`: `collection`
   - `name`: `Kubernetes API vX.XX`
   - `options`:
     - `folderStrategy`: `Tags`
     - `requestNameSource`: `Fallback`
     - `parametersResolution`: `Example`

5. **Update** this file, [`INVENTORY.md`](INVENTORY.md), and the portal's `WORKSPACES` array.

## Re-checking an existing version

Patch releases rarely move the API surface. To confirm a version is still in sync without
pulling 4MB into the agent context, diff upstream against the date the Postman spec was created:

```bash
OLD=$(gh api "repos/kubernetes/kubernetes/commits?sha=release-1.36&until=<spec createdAt>&per_page=1" -q '.[0].sha')
gh api "repos/kubernetes/kubernetes/contents/api/openapi-spec/swagger.json?ref=$OLD" \
  -H "Accept: application/vnd.github.v3.raw" > old.json
gh api "repos/kubernetes/kubernetes/contents/api/openapi-spec/swagger.json?ref=release-1.36" \
  -H "Accept: application/vnd.github.v3.raw" > new.json
# then compare the paths/definitions key sets
```

## Notes

- Each Kubernetes version gets its own collection (not updates to an existing one)
- The swagger.json is a complete OpenAPI 2.0 spec covering all K8s API groups
- Collections are in a public workspace for community access
- The workspace includes a `Local` environment with a `token` variable for auth

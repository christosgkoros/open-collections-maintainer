# Kubernetes API Collections

- **Workspace ID:** `883d5848-bfa7-4628-8bc2-5af5aa2cb0ed`
- **Workspace name:** Kubernetes API
- **Source repo:** `kubernetes/kubernetes`
- **Spec path:** `api/openapi-spec/swagger.json`
- **Branch pattern:** `release-x.x` (e.g. `release-1.35`)
- **Spec type:** OpenAPI 2.0 (Swagger)
- **Last updated:** 2026-03-25

## Existing Collections

| Version | Collection ID | Branch |
| ------- | ------------- | ------ |
| v1.29 | `58a070f1-2c72-4f9e-9a51-6fc644b1c95d` | `release-1.29` |
| v1.30 | `1f1d88ed-29bd-4eee-8880-feb9c9f84a50` | `release-1.30` |
| v1.31 | `389bb600-d473-449d-85e1-a11f4b87de79` | `release-1.31` |
| v1.32 | `73802104-74e4-4566-b1ac-c59dc0f4f355` | `release-1.32` |
| v1.33 | `f247f85f-45b1-4252-a91d-ee6a0922a655` | `release-1.33` |
| v1.34 | `a51a17aa-2431-4584-a282-de1d3dab513e` | `release-1.34` |
| v1.35 | `72134652-d0a4-4706-b310-96a36a72a9eb` | `release-1.35` |

## How to Add a New Version

1. **Check for new release branches:**

   ```bash
   gh api repos/kubernetes/kubernetes/branches --paginate -q '.[].name' | grep '^release-1\.' | sort -t. -k2 -n
   ```

2. **Download the swagger.json** (~3.8MB, under 10MB Postman limit):

   ```bash
   gh api repos/kubernetes/kubernetes/contents/api/openapi-spec/swagger.json \
     -H "Accept: application/vnd.github.v3.raw" -f ref=release-X.XX > swagger.json
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

5. **Update this file** with the new version entry in the table above.

## Notes

- Each Kubernetes version gets its own collection (not updates to an existing one)
- The swagger.json is a complete OpenAPI 2.0 spec covering all K8s API groups
- Collections are in a public workspace for community access
- The workspace includes a `Local` environment with a `token` variable for auth

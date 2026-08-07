# CLAUDE.md

**Read [`AGENTS.md`](AGENTS.md) first.** It holds the project contract — scope, maintained
projects, workflows, and the Postman MCP limitations. Claude Code does not load `AGENTS.md`
automatically, so read it at the start of any session that touches collections.

This file covers only what is specific to running that work in Claude Code.

## Authenticate Postman before starting

The Postman MCP server (`mcp.postman.com`) uses interactive OAuth. If Postman tools fail or the
server shows as disconnected, run `/mcp` and re-authenticate. There is no `.mcp.json` in this
repo — the credential lives in the local Claude install, not in version control.

## Postman tools are deferred

Postman tools are not loaded into context upfront; only their names are. Calling one before
loading its schema fails with `InputValidationError`. Load them with `ToolSearch` first:

```
ToolSearch("select:mcp__postman__getCollection,mcp__postman__updateCollectionRequest")
```

Use the `select:` form with exact names — keyword search wastes a round trip. Tools are named
`mcp__postman__<operation>`; `AGENTS.md` refers to the bare operation names (`createSpec`,
`syncCollectionWithSpec`, …).

Load these together at the start of a sync rather than one at a time:

- Read: `getCollection`, `getCollections`, `getWorkspaces`, `getAllSpecs`, `getSpecFiles`,
  `getSpecCollections`, `searchPostmanElements`
- Write: `updateCollectionRequest`, `createCollectionRequest`, `createCollectionResponse`,
  `updateSpecFile`, `syncCollectionWithSpec`, `createSpec`, `generateCollection`

Some schemas are very large (`putCollection`, `createCollection`). Avoid loading those unless
actually needed.

## Reading collections without flooding context

`getCollection` defaults to a lightweight map (metadata + recursive `itemRefs`) — use that.
`model=minimal` gives root-level IDs plus collection auth and variables. Avoid `model=full` on
large collections.

To find a specific request's URL or body without fetching the whole collection, use
`searchPostmanElements` filtered by collection:

```
entityType: "requests", ownership: "all",
filters: {"$and":[{"collectionId":{"$eq":"6045849-<uuid>"}}]}
```

Note the ID forms differ between tools: `updateCollectionRequest` and `createCollectionRequest`
take a **bare** collection UUID, while `getCollection` and `syncCollectionWithSpec` take the
**`6045849-` prefixed** UID.

## Large spec files

`updateSpecFile` takes content as a string, so pushing a spec means reproducing the whole file in
the tool call. Minify first (`json.dumps(separators=(',',':'))`) and check the size — anything
past ~60 KB is impractical and risky to transcribe. Invalid JSON is rejected outright, but a
valid-but-mistyped spec will sync silently. Always verify the result by re-reading the collection.

## Permissions

`.claude/settings.local.json` allows `Bash(gh api *)`. Sync work leans heavily on `gh api` and
`curl` for upstream fetches; add rules there rather than approving repeatedly.

## Waiting on async Postman tasks

`syncCollectionWithSpec` returns `202` immediately. Foreground `sleep` is blocked — use
`Bash(run_in_background: true)` with a `sleep`, or `Monitor`. Then re-read the collection to
confirm; there is no tool to poll a collection-sync task.

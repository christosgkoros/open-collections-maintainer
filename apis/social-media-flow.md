# Social Media Flow

- **Workspace:** `1173303e-d847-4219-9d0d-c6c3362ddabf`
- **Collections:** 6, all forks of upstream community collections
- **Reviewed:** 2026-08-08

## What this workspace is

Not an API reference set. It is a **posting toolkit** — each collection is trimmed to the minimum
needed to publish a post on one platform, so a flow can fan content out across all of them. Every
collection holds 1–3 requests, and that is deliberate.

So "is it still relevant" reduces to: **can you still publish with it today?**

## Verdicts

| Collection | Requests | Verdict |
| --- | --- | --- |
| Threads API | 2 | **Keep as-is** |
| Mastodon — Post Status | 2 | **Keep** — verify `baseUrl` wiring |
| Twitter API v2 | 2 | **Keep, refresh framing** |
| Bluesky API | 2 | **Fix** — `baseUrl` is broken |
| LinkedIn Content APIs | 3 | **Verify** — version header may have sunset |
| OpenAI | 1 | **Retire or replace** — built on a legacy endpoint |

Every endpoint these collections call was probed on 2026-08-08. All returned `401`/`400`, meaning
the route exists and only auth is missing. **No collection is broken at the URL level** — the
problems are in configuration and in one obsolete API choice.

### Threads API — keep as-is

`graph.threads.net` responds. Two requests implementing Meta's correct two-step publish flow
(create container → publish). Collection variables are current, including recent scopes
(`threads_keyword_search`, `threads_manage_mentions`) and field lists. Nothing to do.

### Mastodon — Post Status — keep, verify `baseUrl`

The Mastodon client API is stable and `/api/v1/statuses` is unchanged. One snag: the description
tells you to point `{{baseUrl}}` at your instance, but the collection's own variables define only
`options`. `baseUrl` must be coming from an environment — confirm one exists and is published,
otherwise both requests fail with an unresolved variable. Last touched 2023-10-14.

### Twitter API v2 — keep, refresh framing

`POST /2/tweets` is alive on both `api.twitter.com` and `api.x.com`. The requests work. What has
rotted is everything around them:

- The upstream it was forked from, [`twitterdev/postman-twitter-api`](https://github.com/twitterdev/postman-twitter-api),
  was **last pushed 2023-04-06** — abandoned for over three years.
- The description points at `developer.twitter.com` and `t.co/twitter-api-postman`, both
  pre-rebrand.
- Posting is now gated behind paid tiers with a tightly capped free allowance. Users should be
  told before they try.

Endpoints stay; update the description, links, and add a note about tier limits.

### Bluesky API — fix the base URL

The two requests (`com.atproto.server.createSession`, `com.atproto.repo.createRecord`) are current
AT Protocol and `bsky.social` responds normally.

But the collection variable **`baseUrl` is set to `/`** — a placeholder that was never filled in.
As published, neither request resolves to a real host. Set it to `https://bsky.social`.

This is the highest-value fix in the workspace: one variable, and a broken collection becomes a
working one.

### LinkedIn Content APIs — verify the version header

`https://api.linkedin.com/rest/posts` is the current versioned Posts API, and the three requests
(Create Post, Create Post with Poll, Get User Info) match how LinkedIn documents it.

The risk is LinkedIn's versioning. The versioned APIs require a `LinkedIn-Version: YYYYMM` header,
and LinkedIn sunsets each version roughly a year after release. This collection was forked in 2022
and last touched 2025-02-06, so a pinned header is very likely past sunset — which fails with
`426 Upgrade Required`.

**This could not be verified from here.** LinkedIn returns `401 EMPTY_ACCESS_TOKEN` before it
validates the version header, so every version from `202209` to `202601` responds identically
without a token. Check the pinned value against LinkedIn's current supported versions, ideally
with a real token.

Also note the collection requires Marketing Developer Platform approval, which is a real barrier
for anyone forking it.

### OpenAI — retire or replace

The only genuinely obsolete collection.

It contains a single request: `POST https://api.openai.com/v1/completions` — the **legacy
Completions API**. The endpoint still returns `401` so the route exists, but:

- OpenAI treats Completions as legacy; current equivalents are `POST /v1/responses` and
  `POST /v1/chat/completions`, both of which also respond.
- The models it was written for (the `text-davinci-*` family) were shut down in January 2024, so a
  realistic request body fails regardless of the endpoint being reachable.
- The description links to `beta.openai.com`, which has not been the docs home for years.
- Last updated 2023-10-07 — the oldest thing in the workspace.

It is also the odd one out: the other five *publish* a post, while this one *generates the text*.
That is a reasonable thing to have in a posting flow, but it should be labelled as such.

Two options: repoint it at `POST /v1/responses` with a current model, or drop it and let the flow
call whichever model provider it prefers. Either way it should not stay as-is.

Unlike the other five, OpenAI has a real machine-readable source —
[`openai/openai-openapi`](https://github.com/openai/openai-openapi) — so if it stays it could
become spec-backed rather than a hand-trimmed fork.

## Maintenance note

These are forks, so there is nothing to diff mechanically. Review means: probe the endpoints,
check the collection variables resolve, and read the vendor changelog. The probe loop used here:

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X POST <endpoint> -H 'Content-Type: application/json' -d '{}'
```

`401`/`400` means the route is alive. `404` means it has moved or gone.

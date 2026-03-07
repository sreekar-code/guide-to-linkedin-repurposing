# Agent Instructions — Spike.sh LinkedIn Post Generator

## What this project does

Reads published guides from a Notion database and generates LinkedIn posts from them — one post per sharp idea extracted from each guide.

## Notion database IDs

| Database | ID |
|---|---|
| Guides | `31736d80-61ff-81ab-8bcc-e059d68d5f97` |
| LinkedIn Posts | `31736d80-61ff-816c-80f9-f26ae99cff15` |

## Workflow

When asked to generate posts for unprocessed guides:

1. **Find unprocessed guides** — search the Guides DB for pages where Status = `Published` and Posts Generated = unchecked
2. **For each guide:**
   - Fetch the full guide page content
   - Fetch the last 10 posts with Status = `Finalized` from the LinkedIn Posts DB as style reference (skip gracefully if none exist)
   - Fetch the last 10 posts with Status = `Published` that have Impressions data as analytics context (skip gracefully if none exist)
   - Read `instructions.txt` — this is the writing brief and must be followed exactly
   - Generate posts, one per sharp idea the guide genuinely supports
   - Show all posts to the user for review before writing anything
   - On confirmation: create each post in the LinkedIn Posts DB and mark the guide Posts Generated = true

## Writing instructions

Everything about tone, structure, personas, and style lives in `instructions.txt`. Read it fresh every time before generating. Do not summarise or skip sections.

## Notion schema

### Guides DB
| Property | Type | Notes |
|---|---|---|
| Title | title | |
| Status | select | `Draft` or `Published` |
| Posts Generated | checkbox | Set to true after writing posts |

### LinkedIn Posts DB
| Property | Type | Notes |
|---|---|---|
| Title | title | Format: `{Guide Title} — Post {N}` |
| Post Content | rich_text | Full post text including P.S. |
| Status | select | `Generated`, `Finalized`, or `Published` |
| Linked Guide | relation | Relation to the source guide page |
| Impressions | number | |
| Engagements | number | |
| Engagement Rate | number (percent) | |
| Clicks | number | |
| Click-through Rate | number (percent) | |
| Reactions | number | |
| Comments | number | |
| Reposts | number | |
| Notes | rich_text | |
| Screenshot | files | |

## Post status lifecycle

`Generated` → user reviews and edits in Notion → `Finalized` → published on LinkedIn → `Published` → analytics filled in

## Important behaviours

- Always show generated posts to the user before writing to Notion
- Never mark a guide as Posts Generated = true unless posts were successfully written
- Skip guides with empty content and move to the next one
- If Finalized posts or analytics don't exist yet, proceed without them — do not block generation

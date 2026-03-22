# Agent Instructions — Spike.sh LinkedIn Post Generator

## What this project does

Reads published guides from a Notion database and generates click-driven LinkedIn posts from them. Each post teases one idea from the guide to build curiosity and drive clicks to the full guide link. Everything runs through Claude Code + Notion MCP.

---

## How to run it

Use the `/run` master command. It scans everything pending and handles it all in one shot:
- Generated posts with unresolved inline comments → applies edits
- Posts with Status = Approved → generates image prompts
- Guides with Posts Generated = unchecked → generates posts

Individual commands for targeted runs:
- `/generate-posts` — generate posts for unprocessed guides only
- `/apply-edits` — apply pending inline comment edits only
- `/generate-image-prompts` — generate image prompts for Approved posts only

All command logic lives in `.claude/commands/`.

---

## Notion database IDs

| Database | Data Source ID |
|---|---|
| Guides DB | `31736d80-61ff-8105-9cf2-000b86573e98` |
| LinkedIn Posts DB | `31736d80-61ff-813a-8f48-000bc237c7be` |

---

## Notion schema

### Guides DB
| Property | Type | Notes |
|---|---|---|
| Title | title | Guide name |
| URL | url | Public spike.sh guide URL — used in P.S. of each post |
| Posts Generated | checkbox | Set to true after posts are written to Notion |

### LinkedIn Posts DB
| Property | Type | Notes |
|---|---|---|
| Title | title | Format: `{Guide Title} — Post {N}` |
| Post Content | rich_text | Full post text including P.S. and hashtags |
| Image Prompt | rich_text | Generated image prompt for the post |
| Status | select | `Generated`, `Approved`, `Ready to publish`, `Published` |
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

---

## Post status lifecycle

`Generated` → user reviews and adds inline comments → `/run` applies edits (status stays Generated) → user changes to `Approved` → `/run` generates image prompt → `Ready to publish` → user publishes on LinkedIn → `Published` → user logs analytics

| Status | Color | Meaning |
|---|---|---|
| Generated | Yellow | Post written to Notion, awaiting review |
| Approved | Purple | User has reviewed and approved — triggers image prompt generation |
| Ready to publish | Blue | Image prompt generated, ready to go live |
| Published | Green | Live on LinkedIn |

---

## Edit detection (comment-based)

The pipeline auto-detects unresolved comment threads (threads with no "Applied." reply) on all Generated posts. It applies the requested changes and replies "Applied." to each thread. Status stays Generated throughout — the user manually changes to Approved when satisfied.

---

## Key files

| File | Purpose |
|---|---|
| `instructions.txt` | Full writing brief: audience, tone, structure, rules, banned words |
| `opinions.md` | Sharp opinions extracted from processed guides — used when generating new posts |
| `edit-log.md` | Writing patterns extracted from past user edits — read during post generation, updated after each apply-edits run |
| `image-guide.md` | Visual style guide for image prompt generation — color palette, rules, 5 reference examples |
| `.claude/commands/run.md` | Master pipeline command |
| `.claude/commands/generate-posts.md` | Post generation pipeline — generates and writes directly to Notion |
| `.claude/commands/apply-edits.md` | Comment-based edit application |
| `.claude/commands/generate-image-prompts.md` | Image prompt generation for Approved posts |

---

## Important behaviours

- Never mark a guide as Posts Generated = true unless posts were successfully written to Notion
- Skip guides with empty content and move to the next one
- Only act on comment threads with no "Applied." reply — skip already-handled threads
- Read `instructions.txt`, `opinions.md`, and `image-guide.md` fresh on every run — never rely on cached memory
- Linked Guide relation value format: JSON array of page URLs — `["https://www.notion.so/{page-id-no-dashes}"]`

# Agent Instructions — Spike.sh Guide Distribution Engine

## What this project does

Reads published guides from a Notion database and generates click-driven content to distribute them across two channels: LinkedIn posts and marketing emails. Each piece of content teases ideas from the guide to build curiosity and drive clicks to the full guide link. Everything runs through Claude Code + Notion MCP.

---

## How to run it

Use the `/run` master command. It scans everything pending and handles it all in one shot:
- Generated posts with unresolved inline comments → applies edits
- Generated emails with unresolved inline comments → applies edits
- Posts with Status = Approved → generates image prompts
- Guides with Posts Generated = unchecked → generates posts
- Guides with Email Generated = unchecked → generates emails

Individual commands for targeted runs:
- `/generate-posts` — generate LinkedIn posts for unprocessed guides only
- `/apply-edits` — apply pending inline comment edits on LinkedIn posts only
- `/generate-image-prompts` — generate image prompts for Approved posts only
- `/generate-email` — generate emails for unprocessed guides only
- `/apply-email-edits` — apply pending inline comment edits on emails only

All command logic lives in `.claude/commands/`.

---

## Notion database IDs

| Database | Data Source ID |
|---|---|
| Guides DB | `31736d80-61ff-8105-9cf2-000b86573e98` |
| LinkedIn Posts DB | `31736d80-61ff-813a-8f48-000bc237c7be` |
| Emails DB | `72567936-61f0-400c-b7db-8c3bd9da3ae4` |

---

## Notion schema

### Guides DB
| Property | Type | Notes |
|---|---|---|
| Title | title | Guide name |
| URL | url | Public spike.sh guide URL — used in P.S. of each post and email CTA |
| Posts Generated | checkbox | Set to true after LinkedIn posts are written to Notion |
| Email Generated | checkbox | Set to true after email is written to Notion |

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

### Emails DB
| Property | Type | Notes |
|---|---|---|
| Title | title | Guide name |
| Subject Line | rich_text | Email subject line |
| Preview Text | rich_text | Preview text shown in email client |
| Email Body | rich_text | Full email body text |
| CTA Text | rich_text | Call-to-action button/link text |
| Guide URL | url | Public spike.sh guide URL |
| Status | select | `Generated`, `Approved`, `Sent`, `Analyzed` |
| Linked Guide | relation | Relation to the source guide page |
| SendGrid ID | rich_text | SendGrid campaign/message ID after sending |
| Open Rate | number (percent) | Manually logged after send |
| Click Rate | number (percent) | Manually logged after send |
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

## Email status lifecycle

`Generated` → user reviews and adds inline comments → `/run` applies edits (status stays Generated) → user changes to `Approved` → user sends via SendGrid → `Sent` → user logs analytics → `Analyzed`

| Status | Color | Meaning |
|---|---|---|
| Generated | Yellow | Email written to Notion, awaiting review |
| Approved | Purple | User has reviewed and approved — ready to send |
| Sent | Blue | Sent via SendGrid |
| Analyzed | Green | Analytics logged |

---

## Edit detection (comment-based)

The pipeline auto-detects unresolved comment threads (threads with no "Applied." reply) on all Generated posts and emails. It applies the requested changes and replies "Applied." to each thread. Status stays Generated throughout — the user manually changes to Approved when satisfied.

---

## Key files

| File | Purpose |
|---|---|
| `instructions.txt` | LinkedIn writing brief: audience, tone, structure, rules, banned words |
| `email-instructions.txt` | Email writing brief: subject lines, preview text, body structure, rules |
| `opinions.md` | Sharp opinions extracted from processed guides — shared across LinkedIn and email |
| `edit-log.md` | LinkedIn writing patterns extracted from past user edits |
| `email-edit-log.md` | Email writing patterns extracted from past user edits |
| `image-guide.md` | Visual style guide for image prompt generation — color palette, rules, 5 reference examples |
| `.claude/commands/run.md` | Master pipeline command |
| `.claude/commands/generate-posts.md` | LinkedIn post generation pipeline |
| `.claude/commands/apply-edits.md` | Comment-based edit application for LinkedIn posts |
| `.claude/commands/generate-image-prompts.md` | Image prompt generation for Approved posts |
| `.claude/commands/generate-email.md` | Email generation pipeline |
| `.claude/commands/apply-email-edits.md` | Comment-based edit application for emails |

---

## Important behaviours

- Never mark a guide as Posts Generated = true unless posts were successfully written to Notion
- Never mark a guide as Email Generated = true unless the email was successfully written to Notion
- Skip guides with empty content and move to the next one
- Only act on comment threads with no "Applied." reply — skip already-handled threads
- Read instruction files, `opinions.md`, and `image-guide.md` fresh on every run — never rely on cached memory
- Linked Guide relation value format: JSON array of page URLs — `["https://www.notion.so/{page-id-no-dashes}"]`

# Spike.sh LinkedIn Post Generator

Turns published Spike guides into LinkedIn posts using Claude Code + Notion MCP. No scripts, no API keys, no local setup.

## Usage

Open this project in Claude Code and say:

> "Generate posts for unprocessed guides"

That's it. Claude reads the guides, generates the posts, shows them to you, and writes them to Notion on confirmation.

## How it works

1. Finds all guides where **Status = Published** and **Posts Generated = unchecked**
2. Pulls the last 10 **Finalized** posts as style reference (skipped if none exist yet)
3. Pulls the last 10 **Published** posts with impressions data as analytics context (skipped if none exist yet)
4. Reads `instructions.txt` for the writing brief
5. Generates posts — one per sharp idea extracted from the guide
6. Shows posts for your review
7. On confirmation: writes each post to Notion (Status = Generated) and marks the guide Posts Generated = ✓

## Files

| File | Purpose |
|---|---|
| `instructions.txt` | Tone guidelines, post structure, persona definitions, and a reference post. Edit this to change how posts are written. |
| `AGENTS.md` | Instructions Claude reads at the start of every session — Notion database IDs, workflow steps, schema. |
| `.env` | Notion API key and database IDs. |

## Post lifecycle

```
Generated → (review + edit in Notion) → Finalized → (publish on LinkedIn) → Published → (fill in analytics)
```

As Finalized and Published posts accumulate, they automatically feed into context on future runs — style references from Finalized posts and performance signals from Published ones.

## Customising the writing brief

Edit `instructions.txt` to change tone, post structure, persona targeting, or add new reference posts. Changes take effect on the next generation run.

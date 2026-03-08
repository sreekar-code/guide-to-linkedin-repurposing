# Spike.sh LinkedIn Post Generator

Turns published Spike guides into LinkedIn posts using Claude Code + Notion MCP. No scripts, no API keys, no local setup.

## Usage

Open this project in Claude Code and run:

```
/run
```

That's it. The pipeline scans everything pending and handles it in one shot.

## What `/run` does

1. **Applies edits** — finds all `Generated` posts with unresolved inline comments, applies the changes, replies "Applied." to each thread
2. **Generates image prompts** — finds all `Approved` posts, generates a tailored image prompt for each, sets status to `Ready to publish`
3. **Generates new posts** — finds all guides with `Posts Generated = unchecked`, runs the full generation pipeline for each

Individual commands are also available for targeted runs: `/apply-edits`, `/generate-image-prompts`, `/generate-posts`.

## Post lifecycle

```
Generated → (review + add comments in Notion) → /run applies edits → (change to Approved) → /run generates image prompt → Ready to publish → (publish on LinkedIn) → Published → (log analytics)
```

## Files

| File | Purpose |
|---|---|
| `instructions.txt` | Writing brief: tone, structure, rules, banned words, reference posts. Edit this to change how posts are written. |
| `opinions.md` | Growing list of sharp opinions extracted from processed guides. Feeds into future post generation. |
| `image-guide.md` | Visual style guide for image prompts: color palette, rules, 5 reference examples, prompt template. |
| `AGENTS.md` | Session-start context for Claude: DB IDs, schema, workflow, important behaviours. |
| `.claude/commands/` | All pipeline command definitions. |

## New here?

Read [`HOW-TO-USE.md`](HOW-TO-USE.md) — a full setup guide written for non-technical users. Covers everything from creating a GitHub account to running your first pipeline.

## Customising the writing brief

Edit `instructions.txt` to change tone, post structure, persona targeting, or add new reference posts. Changes take effect on the next run.

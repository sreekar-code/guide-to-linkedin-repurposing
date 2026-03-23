# Spike.sh Guide Distribution Engine

Turns published Spike guides into click-driven LinkedIn posts and marketing emails using Claude Code + Notion MCP. No scripts, no API keys, no local setup.

## Usage

Open this project in Claude Code and run:

```
/run
```

That's it. The pipeline scans everything pending and handles it in one shot.

## What `/run` does

1. **Applies post edits** — finds all `Generated` posts with unresolved inline comments, applies the changes, replies "Applied." to each thread
2. **Applies email edits** — finds all `Generated` emails with unresolved inline comments, applies the changes, replies "Applied." to each thread
3. **Generates image prompts** — finds all `Approved` posts, generates a tailored image prompt for each, sets status to `Ready to publish`
4. **Generates new posts** — finds all guides with `Posts Generated = unchecked`, runs the full LinkedIn post generation pipeline
5. **Generates new emails** — finds all guides with `Email Generated = unchecked`, runs the email generation pipeline

Individual commands are also available for targeted runs: `/apply-edits`, `/apply-email-edits`, `/generate-image-prompts`, `/generate-posts`, `/generate-email`.

## Post lifecycle

```
Generated → (review + add comments in Notion) → /run applies edits → (change to Approved) → /run generates image prompt → Ready to publish → (publish on LinkedIn) → Published → (log analytics)
```

## Email lifecycle

```
Generated → (review + add comments in Notion) → /run applies edits → (change to Approved) → (send via SendGrid) → Sent → (log analytics) → Analyzed
```

## Files

| File | Purpose |
|---|---|
| `instructions.txt` | LinkedIn writing brief: tone, structure, rules, banned words. Edit this to change how posts are written. |
| `email-instructions.txt` | Email writing brief: subject lines, preview text, body structure, rules. Edit this to change how emails are written. |
| `opinions.md` | Growing list of sharp opinions extracted from processed guides. Shared across LinkedIn and email generation. |
| `edit-log.md` | LinkedIn writing patterns extracted from past user edits. |
| `email-edit-log.md` | Email writing patterns extracted from past user edits. |
| `image-guide.md` | Visual style guide for image prompts: color palette, rules, 5 reference examples, prompt template. |
| `AGENTS.md` | Session-start context for Claude: DB IDs, schema, workflow, important behaviours. |
| `.claude/commands/` | All pipeline command definitions. |

## New here?

Read [`HOW-TO-USE.md`](HOW-TO-USE.md) — a full setup guide written for non-technical users. Covers everything from creating a GitHub account to running your first pipeline.

## Customising the writing briefs

Edit `instructions.txt` to change LinkedIn post tone, structure, or persona targeting. Edit `email-instructions.txt` to change email subject lines, body style, or CTA approach. Changes take effect on the next run.

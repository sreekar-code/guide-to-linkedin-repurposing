---
name: generate-posts
description: "Full LinkedIn post pipeline. Fetches unprocessed Spike guides from Notion, generates posts, runs 5 reviewer personas in parallel, rewrites if needed (max 2 iterations), writes passing posts to Notion. Gate: avg >= 8.5, all individual >= 8."
argument-hint: "[guide-title or leave blank for auto-detect]"
---

# /generate-posts

Run the full LinkedIn post generation pipeline for Spike.sh. Fetches unprocessed guides from Notion, generates posts, reviews them through a 5-persona board, rewrites if needed, and writes passing posts to Notion.

## Notion Database IDs
See `AGENTS.md` for database IDs and schema details.

---

## Workflow

### Step 1: Fetch Unprocessed Guides

Query the Guides DB for pages where:
- `Status = Published`
- `Posts Generated = unchecked`

If no guides are found, tell the user and stop.

If `[guide-title]` was passed as an argument, process only that guide. Otherwise process all unprocessed guides sequentially.

---

### Step 2: For Each Guide — Gather Context

For each guide:

1. Fetch the full guide page content from Notion
2. Fetch the last 10 **Finalized** posts from the LinkedIn Posts DB as style reference (skip if none)
3. Fetch the last 10 **Published** posts with Impressions data as analytics context (skip if none)
4. Read `instructions.txt` — the full writing brief. Follow it exactly.

If the guide body is empty, skip it and move to the next one.

---

### Step 3: Generate Draft Posts

Using the guide content, style references, analytics context, and `instructions.txt`:

- Extract every sharp, distinct idea the guide genuinely supports
- Write one LinkedIn post per idea
- Stop when there are no more ideas worth a standalone post
- Follow all rules in `instructions.txt` strictly

Label each post: `Post 1`, `Post 2`, etc.

---

### Step 4: Run Review Board (5 Personas in Parallel)

Launch ALL 5 persona agents **in parallel** using the Agent tool. Each persona receives:
- The full `instructions.txt`
- All draft posts for this guide
- The persona's specific review focus (below)

**Personas:**

1. **persona-target-reader**
   Reviews from the perspective of Persona 1: Head of Engineering at a 20-60 person SaaS company. Still technical, ships weekly, finds PagerDuty heavy. Ask: Does this speak their language? Would they stop scrolling? Does it respect how modern teams actually work? Score each post on relevance, specificity, and resonance.

2. **persona-hook-editor**
   Reviews opening lines only. Ask: Is the first sentence counter-intuitive or thought-provoking? Does it earn the next sentence without being clickbait? Would someone actively on LinkedIn pause on this? Score each hook on surprise value, clarity, and pull.

3. **persona-spike-voice**
   Reviews for brand fit. Spike has opinions — alert noise is a design problem, burnout is a systems problem, enterprise tools are over-engineered. Ask: Does the post reflect a real point of view, or does it just inform neutrally? Is it opinionated without being preachy? Does it sound like an engineering team talking to peers, not a marketing team talking to customers?

4. **persona-copy-editor**
   Reviews strictly against the rules in `instructions.txt`. Check every post for:
   - Em dashes (none allowed)
   - Banned words: ensure, enhance, leverage, utilize, "for example", "imagine", "tends", draining, relentless
   - Comma rule: no more than one comma per sentence
   - Word count: 100-150 words in body (excluding P.S.)
   - No hashtags, no bold inside the post body
   - No instructional language ("Start with X" instead of "X is a good place to start")
   - UK-style hedging language present and varied
   Score based on rules compliance. A single em dash or banned word is an automatic score below 8.

5. **persona-engagement-predictor**
   Reviews for LinkedIn engagement potential. Every post must land on one of three feelings:
   - "Finally, someone said it." — validates something they've experienced but not named
   - "I never thought about it that way." — reframes a familiar problem
   - "I can use this today." — specific, immediately actionable
   Ask: Which feeling does this land on? If none, it's too generic. Does the closing line stick? Is the P.S. intriguing or just a link drop?

---

### Step 5: Coordinate Reviews

After all 5 personas complete:

1. Collect all scores and feedback
2. Calculate per-post aggregate scores (average across 5 personas)
3. Calculate overall round average across all posts
4. For EVERY score below 8: document what specifically failed and exactly what needs to change
5. Identify the top 3 most common issues across posts and personas

Display a score summary:

```
Review Round 1 — [Guide Title]

Post 1:
  Target Reader:       X/10
  Hook Editor:         X/10
  Spike Voice:         X/10
  Copy Editor:         X/10
  Engagement:          X/10
  Post Average:        X.X/10

Post 2:
  [same format]

...

Overall Average: X.X/10
Gate: avg >= 8.5, all individual >= 8
Result: PASS / FAIL
```

---

### Step 6: Gate Decision

**Gate: Overall average >= 8.5 AND every individual persona score >= 8 across all posts**

---

#### If PASS:

1. Write all posts to the LinkedIn Posts DB in Notion:
   - Title: `{Guide Title} — Post {N}`
   - Post Content: the approved post text
   - Status: `Generated`
   - Linked Guide: relation to the source guide page
2. Mark the guide `Posts Generated = true` in Notion
3. Tell the user:

```
Pipeline complete — [Guide Title]

Posts written to Notion: {N}
Review scores:
  Post 1 avg: X.X/10
  Post 2 avg: X.X/10
  ...
  Overall:    X.X/10  (Round {N})

Next: Review in Notion → mark Finalized → publish on LinkedIn → log analytics.
```

---

#### If FAIL and iterations < 2:

1. Show the user the score summary and top issues
2. Rewrite all posts that have any score below 8, using the coordinator's feedback:
   - Address every documented failure point
   - Do not change posts that fully passed (all 5 scores >= 8) unless the copy editor found rule violations
3. Re-run ALL 5 personas on the revised posts (not just the ones that were rewritten)
4. Re-run coordinator
5. Repeat gate decision

---

#### If FAIL after 2 iterations (PAUSE):

1. Show the user all review rounds:

```
Pipeline did not pass after 2 rounds — [Guide Title]

Round 1: Overall avg X.X — lowest: X/10 (persona, Post N)
Round 2: Overall avg X.X — lowest: X/10 (persona, Post N)

Persistent issues:
- {issue that appeared in both rounds}
- {another persistent issue}

How would you like to proceed?
1. Tell me what to change and re-run
2. Lower the gate threshold for this guide
3. Write the posts as-is (not recommended)
4. Skip this guide
```

Wait for the user's response before doing anything.

---

## Important Rules

- ALL 5 personas must run on every iteration, even if only some posts failed
- Never write to Notion until the gate is passed (or the user explicitly chooses to write as-is)
- Never overwrite posts that already exist in Notion for this guide
- A single banned word or em dash from `instructions.txt` is enough to score below 8 on copy editing
- The copy editor persona must check every rule in `instructions.txt` — not just the obvious ones
- Every score below 8 MUST have a specific, documented reason and at least one concrete suggestion
- Empty reasons for sub-8 scores are never acceptable
- Re-reads `instructions.txt` fresh on every run — never rely on cached memory of its contents
- Processes one guide at a time when multiple are unprocessed; does not batch them in parallel

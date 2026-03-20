# Spike LinkedIn Image Prompt Guide

A reference for generating minimal illustrations for Spike's LinkedIn posts. Use this to maintain consistency across all images.

---

## Visual Style Rules

**Always include:**
- Background color `#F5F5F5`
- Flat, minimal, editorial illustration style
- Bold heading at the top in `#202020`, using Instrument Sans font (see heading style below)
- Simple geometric shapes
- Muted color palette: slate blue, amber/golden yellow, light grey

**Always avoid:**
- Human figures unless the post is explicitly about burnout or people (even then, keep them minimal stick figures)
- Pencils, tools, or meta-design elements
- Abstract icons that don't connect directly to the post's topic
- Overly decorative or complex illustrations
- Gradients, shadows, or 3D effects

**Heading style:**
- Bold, `#202020` text, Instrument Sans font
- Placed at the top of the image
- Concise and clear — the reader should immediately understand what the post is about. Clarity takes priority over being punchy. Never vague.
- No subtitle or supporting text in the image

**Color palette:**
- Primary: Slate blue `#4A6A8A`
- Accent: Amber/golden yellow `#E8A830`
- Background: `#F5F5F5`
- Neutral: Light grey `#C8CDD4`
- Success: Muted green (for checkmarks only)

---

## Finalized Image References

---

### 1. You ship it, you're on-call
**Post topic:** Follow-the-work on-call model — ownership follows the deployment, not the calendar.

**Heading:** `You ship it, you're on-call`

**Guide:** Follow-the-sun and other on-call models
**Relevant section:** Follow-the-work on-call model — the person who ships a feature or updates a system becomes the primary on-call responder for it for a short window after deployment.

**LinkedIn post:**
> Being on-call for code you didn't write is a strange default. Standard rotations assign coverage by schedule. You're on-call because it's your week. Not because you know the system that broke. The follow-the-work model changes the premise. When someone ships a feature or pushes an update, they become the primary on-call responder for it. Just for a short window after the change goes out. The reason this works: incidents close to a deployment are almost always tied to it. The person who shipped knows what changed. They skip the investigation phase. The right person is already on the problem. The trade-off is workload. Engineers who ship often carry more on-call load. Worth tracking. But if every post-incident review at your team starts with "who touched this last?" the follow-the-work model answers that before the incident even starts. Context, not calendar. That's what fast incident response actually runs on.

**Prompt:**
> A minimal flat illustration of a small code window with a `</>` symbol, with a subtle dotted line extending from it to a pager or alert bell with a notification badge. The dotted line suggests direct ownership — one thing leading to another. Background color #F5F5F5. Muted tones — slate blue, amber. Simple geometric shapes. No human figures. Editorial illustration style. At the top, a bold clean heading that reads: **"You ship it, you're on-call."**

**What makes it work:** The code → pager connection is immediately readable. The dotted line implies a direct, intentional link between shipping and owning the incident.

---

### 2. High incident volume? Shorten the rotation.
**Post topic:** Rotation length should match incident volume, not calendar convenience.

**Heading:** `High incident volume? Shorten the rotation.`

**Guide:** Follow-the-sun and other on-call models (rotation length best practices)
**Relevant section:** Rotation-based schedules — the higher the incident volume, the shorter the rotation should be. A two-day rotation keeps the window small; the person on-call stays sharp and can recover before their next shift.

**LinkedIn post:**
> A weekly rotation isn't a safe default. For high-incident teams, it might be the fastest path to burnout. Most teams pick their rotation length based on what's easy to schedule. Weekly feels clean. Everyone knows when handoff happens. But rotation length should come from your incident volume, not your calendar preferences. The rule is simple: the higher the incident volume, the shorter the rotation should be. Here's why it matters. Handling incidents takes real mental energy. When someone is on-call for a full week and incidents fire multiple times a day, that energy runs out fast. They're not just fixing problems. They're staying alert and losing sleep. By day four, the quality of response drops. A two-day rotation keeps the window small. The person on-call stays sharp. The person coming off can actually recover before their next shift. Pick a rotation that matches your incident volume. You can always adjust later.

**Prompt:**
> A minimal flat illustration showing two horizontal time bars stacked. The first bar is long and wide, labeled "7 days", with a cluster of small ringing alert/bell icons above it suggesting many incidents. The second bar is short and narrow, labeled "2 days". A tired slouching stick figure beneath the 7-day bar and an upright alert stick figure beneath the 2-day bar. Clear visual contrast between bar lengths. Background color #F5F5F5. Muted tones — slate blue, amber. Simple geometric shapes. Editorial illustration style. At the top, a bold clean heading that reads: **"High incident volume? Shorten the rotation."**

**What makes it work:** The bar length difference is immediately obvious. The cluster of bells above the long bar ties incident volume to the rotation problem. Note: human figures were used here because the burnout contrast is the entire point of the post.

---

### 3. One day a week. No on-call.
**Post topic:** Quiet day rotation — one designated day per week with no on-call coverage.

**Heading:** `One day a week. No on-call.`

**Guide:** 5 Offbeat on-call rotations that work
**Relevant section:** Quiet day on-call rotation — one day each week has no on-call coverage. The team treats it as a shared focus day, planned in advance so everyone can work without keeping one eye on their phone.

**LinkedIn post:**
> Your team probably doesn't need on-call coverage seven days a week. Most teams never question that assumption. On-call coverage is just continuous. And then people wonder why the on-call rotation feels like background anxiety that never fully switches off. The quiet day rotation does one simple thing. It designates one day a week where nobody is on-call. The team knows it in advance so they can plan focused work around it without keeping one eye on their phone. You do need a plan for incidents that come in that day. Some teams pick their historically quietest day for it. Others accept a slightly slower response time during that window. Either way, the team gets something real: one predictable day where on-call responsibility fully lifts. Constant availability isn't the same as better coverage.

**Prompt:**
> A minimal flat illustration of a weekly calendar strip showing seven days labeled S M T W T F S. Six days have a small ringing bell icon with an alert badge above them. One day in the middle (Wednesday) is visually distinct — highlighted with a soft warm amber background and a clean crossed-out bell symbol above it. No human figures. Background color #F5F5F5. Muted tones — slate blue, amber. Simple geometric shapes. Editorial illustration style. At the top, a bold clean heading that reads: **"One day a week. No on-call."**

**What makes it work:** The seven-day strip with one clearly silenced day tells the whole story instantly. The crossed-out bell is universally understood.

---

### 4. Find your ideal rotation length. Run Fibonacci.
**Post topic:** Fibonacci on-call rotation — shift lengths follow the sequence 1, 2, 3, 5, 8 days.

**Heading:** `Find your ideal rotation length. Run Fibonacci.`

**Guide:** 5 Offbeat on-call rotations that work
**Relevant section:** Fibonacci on-call rotation — shift lengths follow the Fibonacci pattern (1, 2, 3, 5, 8 days). Everyone experiences multiple shift lengths in a single cycle, making it a useful experiment to discover which rotation length fits the team best before committing to a fixed pattern.

**LinkedIn post:**
> The Fibonacci sequence makes for a surprisingly useful on-call experiment. Instead of fixed weekly rotations, shifts follow the pattern: 1 day, 2 days, 3 days, 5 days, 8 days, then repeat. Everyone experiences multiple shift lengths in a single cycle. This works well when you're not sure what rotation length fits your team. After a few cycles, you can ask people how the 3-day shift felt compared to the 5-day one. Most teams discover they have a strong preference for a particular length, then switch to that fixed pattern. The downside is tracking. Without a predictable rhythm, people constantly check the schedule to see when they're up next. Sometimes the best way to find your ideal rotation is to try several at once.

**Prompt:**
> A minimal flat illustration of a horizontal timeline showing shift blocks of increasing widths labeled "1", "2", "3", "8" — each block visibly wider than the previous, clearly showing the growing Fibonacci pattern. The blocks are in alternating muted colors to distinguish them. A dashed arrow runs along the bottom of the blocks left to right. Clean white background. Muted tones — slate blue, amber, soft off-white, light grey. Simple geometric shapes. No human figures. Editorial illustration style. At the top, a bold clean heading that reads: **"Find your ideal rotation length. Run Fibonacci."**

**What makes it work:** The progressively wider blocks make the core mechanic immediately clear — each shift is longer than the last — without needing any explanation.

---

### 5. Your first escalation policy won't be your last.
**Post topic:** Escalation policies are living documents that improve through iteration.

**Heading:** `Your first escalation policy won't be your last.`

**Guide:** A compass for setting up your escalation policy
**Relevant section:** General framing — there is no single escalation setup that fits every team. Most teams find that a combination of two or three approaches covers most situations well, and policies get refined as incident patterns become clearer over time.

**LinkedIn post:**
> The first escalation policy you set up probably won't be your last. And that's exactly how it should be. Most teams get stuck trying to predict the perfect escalation structure upfront. Which incidents need phone calls? Who should be in L2? How many policies do we actually need? The questions feel important enough to spend weeks debating. But escalation policies aren't architecture decisions. They're living documents that get better as you learn your actual incident patterns. A team that handles three incidents a month will discover different needs than a team handling three incidents a day. The goal isn't to create the perfect policy. It's to set up something workable and then refine it as you go. Start with something simple that covers your most obvious cases, then iterate when reality shows you what you missed.

**Prompt:**
> A minimal flat illustration showing three escalation flowcharts side by side, each with three boxes labeled L1, L2, L3 connected by downward arrows. The first flowchart is labeled "v1" in a light pill badge and has a large diagonal X drawn over the entire flowchart. The second flowchart is labeled "v2" in a light pill badge and also has a large diagonal X drawn over the entire flowchart. The third flowchart is labeled "v3" in an amber filled pill badge and has a green checkmark below it. All three arranged horizontally with clear left to right progression. Background color #F5F5F5. Muted tones — slate blue, amber. Simple geometric shapes. No human figures. Editorial illustration style. At the top, a bold clean heading that reads: **"Your first escalation policy won't be your last."**

**What makes it work:** Three side-by-side flowcharts with strikethroughs and a final checkmark makes the iteration story obvious at a glance. The amber v3 badge signals the approved version without needing any label.

---

## Prompt Template

Use this as a starting structure for new prompts:

```
A minimal flat illustration of [CORE VISUAL CONCEPT]. [DESCRIBE KEY ELEMENTS AND THEIR RELATIONSHIP]. [NOTE ANY LABELS OR TEXT IN THE IMAGE]. [Only if the post is explicitly about burnout or people-state contrast: use minimal stick figures — otherwise no human figures.] Background color #F5F5F5. Muted tones — slate blue (#4A6A8A), amber (#E8A830), light grey (#C8CDD4). Simple geometric shapes. No gradients, shadows, or 3D effects. Editorial illustration style. At the top, a bold clean heading in #202020 using Instrument Sans font that reads: "[HEADING TEXT]"
```

---

## Common Mistakes to Avoid

| Mistake | Fix |
|---|---|
| Abstract icons that don't connect to topic | Pick one concrete visual that is the mechanic itself (e.g. bars for rotation length, not a generic clock) |
| Human figures when not needed | Only use stick figures when the post is about burnout or people-state contrast |
| Pencils or edit metaphors for "iteration" | Use version labels (v1, v2, v3) with strikethroughs instead |
| Icons floating without relationship | Connect elements with dotted lines or arrows to show causation |
| Heading vague or unclear | Keep it concise. The reader should instantly understand what the post is about from the heading alone. Clarity over cleverness. |

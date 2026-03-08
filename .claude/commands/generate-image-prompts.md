---
name: generate-image-prompts
description: "Generates image prompts for LinkedIn posts marked 'Approved' in Notion. Reads each post's content, applies the image guide rules, writes a prompt to the Image Prompt column, and sets status to 'Ready to publish'."
argument-hint: ""
---

# /generate-image-prompts

Generate image prompts for LinkedIn posts you've approved. Finds all posts with `Status = Approved`, reads each post's content, generates a tailored image prompt using the image guide, writes it to the `Image Prompt` column, and sets status to `Ready to publish`.

## Notion Database IDs
See `AGENTS.md` for database IDs and schema details.

---

## Workflow

### Step 1: Find Posts Ready for Image Prompts

Query the LinkedIn Posts DB for all pages where `Status = Approved`.

If none found, tell the user: "No posts currently marked 'Approved'." and stop.

List the posts found:
```
Found N post(s) marked 'Approved':
- [Post Title]
- [Post Title]
...
```

---

### Step 2: Read the Image Guide

Read `image-guide.md` in full. This contains:
- Visual style rules (what to always include and always avoid)
- Color palette with hex codes
- Heading style rules
- 5 finalized reference examples with prompts and reasoning
- The prompt template
- Common mistakes to avoid

Internalize every rule before generating any prompt.

---

### Step 3: For Each Post — Generate an Image Prompt

For each post:

1. Fetch the full post page from Notion to get the `Post Content`
2. Read the post carefully. Identify:
   - The single core idea the post is built around
   - The concrete mechanism, contrast, or concept at its heart
   - Whether the post is about people/burnout (stick figures allowed) or a system/process (no human figures)
3. Derive a heading:
   - Short and punchy — under 8 words
   - Mirrors or distills the post's core idea
   - Should work as a standalone statement or question
   - Not descriptive — provocative or direct
4. Design the core visual concept:
   - Pick one concrete visual that IS the mechanic (e.g. bars for rotation length, a flowchart for escalation, a calendar for scheduling)
   - Connect elements with dotted lines or arrows to show causation or relationship
   - Use version labels (v1, v2, v3) with strikethroughs for iteration concepts — never pencils or edit metaphors
   - Only include human figures (minimal stick figures) if the post is explicitly about burnout or people-state contrast
5. Write the prompt using this template:

```
A minimal flat illustration of [CORE VISUAL CONCEPT]. [DESCRIBE KEY ELEMENTS AND THEIR RELATIONSHIP]. [NOTE ANY LABELS OR TEXT IN THE IMAGE]. [Only if applicable: human figures note]. Clean white background. Muted tones — slate blue (#4A6A8A), amber (#E8A830), soft off-white (#F5F4F0), light grey (#C8CDD4). Simple geometric shapes. No gradients, shadows, or 3D effects. Editorial illustration style. At the top, a bold clean heading in dark slate blue or charcoal that reads: "[HEADING TEXT]"
```

**Quality checks before writing:**
- Does the visual directly represent the mechanic of the post's idea? (Not a generic icon)
- Are elements connected to show relationship — not just floating?
- Is the heading under 8 words and punchy?
- Are there no pencils, abstract icons, or meta-design elements?
- Is the palette restricted to slate blue, amber, off-white, light grey (and muted green for checkmarks only)?

6. Write the generated prompt to the post's `Image Prompt` field in Notion
7. Set the post's `Status` to `Ready to publish`

---

### Step 4: Report to User

After processing all posts:

```
Image prompts generated — N post(s) updated

[Post Title]
  Heading: "[heading used]"
  Status: → Ready to publish

[Post Title]
  Heading: "[heading used]"
  Status: → Ready to publish

Next: Use the Image Prompt field to generate images (e.g. via Midjourney, DALL-E, or your preferred tool), then publish on LinkedIn and mark as Published.
```

---

## Important Rules

- Read `image-guide.md` fresh on every run — do not rely on cached memory of its contents
- The visual must represent the specific mechanic of this post — never use generic icons
- The heading is part of the image, not the post — it should work independently
- Only use stick figures when burnout or people-state contrast is the literal point of the post
- Never use pencils, tools, or edit metaphors — use version labels instead
- Process posts sequentially, one at a time

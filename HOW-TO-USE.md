# How to Use This Project

This project turns your long-form content into LinkedIn posts — automatically. You feed it articles, guides, blog posts, or newsletters. It reads them, extracts the sharpest ideas, and writes finished LinkedIn posts directly into Notion for you to review and publish.

It was originally built for [Spike.sh](https://spike.sh) to repurpose their guides into LinkedIn content. But the pipeline works for any content type and any brand. This guide will walk you through setting it up for yourself, from scratch, even if you have never written a line of code.

---

## What you will need

| Tool | Cost | What it is |
|---|---|---|
| GitHub account | Free | Where the project lives. You need an account to get your own copy. |
| Claude Code | Paid (requires a Claude subscription) | The AI tool that runs the pipeline. |
| Notion account | Free | Where your content and generated posts live. |

You do not need to know how to code. You do not need a server. You do not need to install anything complicated. If you can use Notion and follow instructions, you can set this up.

---

## Part 1 — Get a copy of this project

### Step 1: Create a GitHub account

If you already have one, skip to Step 2.

1. Go to [github.com](https://github.com)
2. Click **Sign up**
3. Enter your email, create a password, choose a username
4. Verify your email when prompted
5. You now have a GitHub account

### Step 2: Fork this repository

"Forking" means making your own personal copy of this project. Your copy is independent — you can change anything you want without affecting the original.

1. Go to this project's GitHub page (the page you found this project on)
2. Click the **Fork** button in the top-right corner
3. On the next screen, click **Create fork**
4. GitHub will create a copy of the project under your account

You now have your own copy of the project. Everything from here is done in your copy.

---

## Part 2 — Set up Notion

You need two databases in Notion: one for your source content, and one where the generated LinkedIn posts will land.

### Step 3: Create the Content database

This is where you add the articles, guides, or posts you want to turn into LinkedIn content.

1. Open Notion and create a new page (click **+ New page** in the sidebar)
2. Title it whatever makes sense — "Content Library", "Articles", "Guides" — your choice
3. Change the view to a **Database** (click **Turn into** → **Table**)
4. Add these columns to the database:

| Column name | Type | How to add it |
|---|---|---|
| Title | Title | Already exists by default |
| URL | URL | Click **+** → choose **URL** |
| Posts Generated | Checkbox | Click **+** → choose **Checkbox** |

- **Title**: The name of your article or piece of content
- **URL**: The public link to the content (used in the P.S. of each LinkedIn post)
- **Posts Generated**: Leave unchecked. The pipeline checks this automatically when it's done processing a piece of content.

### Step 4: Create the LinkedIn Posts database

This is where generated posts appear.

1. Create another new Notion page
2. Title it "LinkedIn Posts" (or whatever you prefer)
3. Change it to a **Table** database
4. Add these columns:

| Column name | Type |
|---|---|
| Title | Title (default) |
| Post Content | Text |
| Image Prompt | Text |
| Status | Select |
| Linked Guide | Relation |

For the **Status** column, add these options (click the column → **Edit property** → add options):
- `Generated` — colour: yellow
- `Approved` — colour: purple
- `Ready to publish` — colour: blue
- `Published` — colour: green

For the **Linked Guide** column, set the relation to point to your Content database (the one you created in Step 3).

### Step 5: Get your Notion database IDs

Every Notion database has a unique ID. You need these IDs so the pipeline knows where to read and write.

1. Open your Content database in Notion
2. Look at the URL in your browser. It will look something like:
   `https://www.notion.so/yourworkspace/abc123def456...?v=xyz`
3. The long string of characters between the last `/` and the `?` is the database ID
4. Copy it and save it somewhere — you will need it shortly
5. Do the same for your LinkedIn Posts database

---

## Part 3 — Install Claude Code

Claude Code is the tool that actually runs the pipeline. It is a command-line application made by Anthropic (the company that makes Claude).

### Step 6: Get a Claude subscription

Claude Code requires a paid Claude plan.

1. Go to [claude.ai](https://claude.ai)
2. Sign up or log in
3. Upgrade to a paid plan (Pro or higher)

### Step 7: Install Claude Code

1. Go to the Claude Code installation page: [claude.ai/code](https://claude.ai/code)
2. Follow the instructions for your operating system (Mac or Windows)
3. Once installed, open your terminal (on Mac: press `Cmd + Space`, type "Terminal", press Enter)
4. Type `claude` and press Enter to confirm it is working

If you see a welcome message, Claude Code is installed.

---

## Part 4 — Connect Notion to Claude Code

Claude Code needs permission to read and write to your Notion databases. This is done through something called an MCP server — think of it as a bridge between Claude Code and Notion.

### Step 8: Get a Notion integration token

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click **New integration**
3. Give it a name (e.g. "Claude Pipeline")
4. Select your workspace
5. Click **Save**
6. Copy the **Internal Integration Token** — it starts with `secret_...`

### Step 9: Give the integration access to your databases

Notion integrations need explicit permission to access each database.

1. Open your Content database in Notion
2. Click the `...` menu in the top-right corner
3. Click **Connections** → **Add connections**
4. Find the integration you just created and click it
5. Repeat for your LinkedIn Posts database

### Step 10: Add the Notion MCP server to Claude Code

1. Open your terminal
2. Run this command (replace `YOUR_TOKEN` with the token you copied in Step 8):

```
claude mcp add notion -- npx -y @notionhq/notion-mcp-server
```

3. When prompted for the Notion token, paste yours in

Claude Code can now read and write to your Notion databases.

---

## Part 5 — Open the project in Claude Code

### Step 11: Get your copy of the project onto your computer

1. Go to your forked repository on GitHub (it will be at `github.com/YOUR-USERNAME/PROJECT-NAME`)
2. Click the green **Code** button
3. Click **Download ZIP**
4. Unzip the downloaded file somewhere on your computer (e.g. your Desktop or Documents folder)

Alternatively, if you are comfortable with the terminal, you can clone it:
```
git clone https://github.com/YOUR-USERNAME/PROJECT-NAME.git
```

### Step 12: Open the project in Claude Code

1. Open your terminal
2. Navigate to the project folder:
   ```
   cd path/to/the/project-folder
   ```
   (Replace `path/to/the/project-folder` with the actual path, e.g. `cd ~/Desktop/spike-linkedin-engine`)
3. Start Claude Code:
   ```
   claude
   ```

You are now inside the project, with Claude Code running and Notion connected.

---

## Part 6 — Customise the project for your content

The project was built for Spike.sh's guides. Before you run it, you need to point it at your Notion databases and tell it about your content and brand.

### Step 13: Update the database IDs

1. Open the file `AGENTS.md` in any text editor (Notepad on Windows, TextEdit on Mac, or any code editor)
2. Find this section:

```
| Guides DB           | `31736d80-61ff-8105-9cf2-000b86573e98` |
| LinkedIn Posts DB   | `31736d80-61ff-813a-8f48-000bc237c7be` |
```

3. Replace the IDs with your own database IDs (the ones you copied in Step 5)
4. Save the file

### Step 14: Rewrite the writing brief

This is the most important step. The file `instructions.txt` tells the pipeline everything about your brand, your audience, and how you want posts to sound.

Open `instructions.txt` in a text editor. You will see sections for:

- **AUDIENCE** — who you are writing for
- **POINT OF VIEW** — your brand's opinions and beliefs
- **LINKEDIN VS [your content type] WRITING** — the difference in how readers engage
- **POST STRUCTURE** — hook, body, closing, P.S.
- **TONE AND WRITING STYLE** — how you want to sound
- **LENGTH** — word count targets
- **WORDS AND PHRASES TO AVOID** — your banned words
Rewrite each section to reflect your brand. Key things to change:

**AUDIENCE**: Replace the Spike personas with your own. Describe your reader in specific terms — their job title, company size, tools they use, what they care about, what frustrates them. Be specific. "Marketing managers at B2B SaaS companies with 50-200 employees" is more useful than "marketers".

**POINT OF VIEW**: List 4-6 things your brand genuinely believes about your industry. Not platitudes — actual opinions that might make some people disagree. Posts with a point of view outperform neutral posts.

**TONE AND WRITING STYLE**: Describe how you want to sound. Warm? Direct? Technical? Conversational? Add any specific rules that matter to you.

**WORDS AND PHRASES TO AVOID**: List clichés and words that do not fit your brand.

### Step 15: Update the P.S. format (if needed)

In `instructions.txt`, the P.S. format currently reads:

> "P.S. We wrote a guide on [topic + why it's worth reading]. [guide URL]"

Change "guide" to whatever fits your content — "article", "post", "newsletter issue", "case study", etc.

---

## Part 7 — Add your content to Notion

### Step 16: Add your first piece of content

1. Open your Content database in Notion
2. Click **+ New** to add a row
3. Fill in:
   - **Title**: The name of your article or piece of content
   - **URL**: The public link to it
   - **Posts Generated**: Leave unchecked

Now add the actual content. Click on the row to open it as a page, then paste the full text of your article into the body of the page.

The pipeline reads the page body to extract ideas. The more complete the content, the better the posts.

> **Note on content that lives elsewhere:** If your content is a blog post or article hosted on your website, the simplest approach is to copy and paste the full text into the Notion page body. The pipeline reads from Notion, not from external URLs.

---

## Part 8 — Run the pipeline

### Step 17: Run /run

In Claude Code (make sure you are inside the project folder), type:

```
/run
```

Press Enter.

The pipeline will:
1. Scan for content with `Posts Generated = unchecked`
2. Read your content
3. Extract the sharpest ideas — one LinkedIn post per idea
4. Write posts directly into your LinkedIn Posts database in Notion
5. Mark the content as processed

When it is done, you will see a summary in Claude Code showing how many posts were written.

---

## Part 9 — Review, edit, and publish

### Step 18: Review your posts in Notion

Open your LinkedIn Posts database. You will see the generated posts, each with `Status = Generated`.

Click into each post to read it. If you want to change something:

1. Select the text you want to change
2. Click **Comment** (or press `Ctrl+Shift+M` / `Cmd+Shift+M`)
3. Write your edit instruction as a comment, e.g.:
   - "Make the hook stronger — it's too mild"
   - "Remove the third paragraph"
   - "The closing line feels weak, rewrite it"

You can add as many comments as you want across as many posts as you want.

### Step 19: Apply your edits

Go back to Claude Code and run:

```
/run
```

The pipeline will find all your comments, apply the changes, and reply "Applied." to each comment thread. Posts stay as `Generated` until you are happy with them.

You can repeat this cycle as many times as you need.

### Step 20: Approve posts you are happy with

When a post is ready, change its `Status` from `Generated` to `Approved` in Notion. Just click the status field and select **Approved**.

### Step 21: Generate image prompts

Run `/run` again. For every `Approved` post, the pipeline will:

1. Read the post
2. Design a visual concept that illustrates the post's core idea
3. Write a detailed image prompt into the `Image Prompt` field
4. Set status to `Ready to publish`

Take the image prompt into any AI image tool — Midjourney, DALL-E, Adobe Firefly, or similar — and generate the image.

### Step 22: Publish

Post on LinkedIn with your image. Then go back to Notion and change the status to `Published`.

---

## How to adapt this for different content types

This pipeline was built for long-form guides but works for any content where you want to extract individual ideas and turn them into LinkedIn posts.

| Content type | What to change |
|---|---|
| Blog posts | Rename "Guides DB" to "Blog DB" in your head. No other changes needed. |
| Newsletter issues | Same as blog posts. Paste the full newsletter text into the Notion page body. |
| Podcast transcripts | Paste the transcript. The pipeline is good at finding distinct ideas in conversation. |
| Case studies | The P.S. CTA may need adjusting — update `instructions.txt` to say "case study" instead of "guide". |
| Whitepapers / reports | Works well. Long-form = more posts. A 20-page report might yield 8-10 posts. |
| YouTube video transcripts | Paste the transcript. Same approach as podcasts. |

The core pipeline does not change. The only thing you customise is `instructions.txt` — your audience, your voice, your rules.

---

## Frequently asked questions

**How many posts will it generate per piece of content?**
It depends on how many distinct ideas the content contains. A 1,000-word article might yield 3-4 posts. A detailed long-form guide might yield 6-8. The pipeline stops when it runs out of ideas worth a standalone post — it will not pad.

**Can I run it on multiple pieces of content at once?**
Yes. Add as many rows as you want to your Content database, all with `Posts Generated = unchecked`. When you run `/run`, it processes them one at a time in sequence.

**What if I do not want a P.S. on every post?**
Update the instructions in `instructions.txt`. The current brief says "Some posts may not need a CTA. Use your judgment." You can make this stricter or more permissive.

**Can I change the writing style after I have already generated some posts?**
Yes. Edit `instructions.txt` any time. Changes take effect on the next run. Previously generated posts are not retroactively updated.

**What if I want to regenerate posts for a piece of content I already processed?**
Delete the existing posts from the LinkedIn Posts database in Notion, uncheck the `Posts Generated` checkbox on that content row, and run `/run` again.

**The posts do not sound like my brand yet. What should I do?**
Improve your `instructions.txt`. The highest-impact thing: make your AUDIENCE description more specific. The more concrete the persona, the better the posts will sound.

**Do I need to use Notion? Can I use another tool?**
The pipeline is built specifically for Notion via the Notion MCP. Using a different tool would require modifying the pipeline commands in `.claude/commands/`, which needs some technical knowledge.

---

## Summary: your ongoing workflow

Once set up, your workflow is:

1. Publish a piece of content
2. Add it to your Content database in Notion (paste the text, add the URL)
3. Open the project in Claude Code and run `/run`
4. Review generated posts in Notion — add comments where you want changes
5. Run `/run` again to apply edits
6. Change satisfied posts to `Approved`
7. Run `/run` to generate image prompts
8. Generate images, publish on LinkedIn, mark as Published

That is the full loop. Most of the time, you are just adding content to Notion and running `/run`.

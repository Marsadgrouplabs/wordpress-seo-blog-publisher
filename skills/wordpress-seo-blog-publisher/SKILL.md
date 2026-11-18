---
name: "wordpress-seo-blog-publisher"
description: "Research, write, and publish a full SEO-optimized blog post to WordPress (RankMath) end-to-end from just a topic name. Use any time the user asks to write and publish a blog post/article to WordPress, including \"انشر بلوج\", \"اكتب مقال وانزله على الموقع\", \"publish a blog post\", or whenever WordPress + RankMath + blog writing come up together, or the user just gives a topic and says \"اعمل عليها\" or \"go ahead\". Runs deep topic/keyword/trend research, hands the writing to seo-blog-write-ar-en, then publishes through the WordPress REST API with the local wp.py helper (no browser step; the RankMath fields and schema are handed to the user as a paste-ready package): FAQ rules, images, tags/category, and the final publish."
---

# WordPress SEO Blog Publisher (RankMath)

Full pipeline: takes a topic name, runs deep research on it (including trend/search-volume checks to make sure the
topic is genuinely getting attention right now), gets the article written, sources images, prepares the RankMath and
schema values, and publishes a complete SEO article to WordPress, written to meet RankMath's criteria. **The skill never
touches the RankMath fields or the Custom Schema box and never uses a browser: it hands those values to the user in the
final delivery and the user pastes them by hand.** Do not stop to ask questions
mid-pipeline unless something actually fails (e.g. an image upload error or a connection issue) — run it end to end and
report back at the end.

WordPress tasks go through the WordPress REST API using the bundled helper **`scripts/wp.py`** (Python standard library only).

Site logins live in a private **sites.txt** outside this skill: `~/.wp-publisher/sites.txt` by default, or the file named by the `WP_SITES_FILE` environment variable. The helper reads it by itself. **Never open sites.txt to read passwords, never print or repeat them, never ask the user to paste them in chat, and never put them in a report.** To add a site, the user writes 3 lines (URL, username, Application Password) into sites.txt by hand, following `scripts/sites.example.txt`.

**Step 0 — Preflight. Do this FIRST, before any research, writing or uploading.** Prove the login works:

1. **Local shell (Claude Code / Codex):** `python "<this-skill-folder>/scripts/wp.py" check <site>` (use `python3` on macOS or Linux).
2. **Cowork / Linux sandbox:** folders the user connected appear under `$HOME/mnt`. Find the logins with `find "$HOME/mnt" -maxdepth 3 -name sites.txt`, set `WP_SITES_FILE` to that path, then run the same command.
3. **sites.txt not found:** tell the user where the helper expects it and ask them to create it by hand from `scripts/sites.example.txt`.

Keep the path you found in a shell variable (e.g. `WP="python3 /path/to/wp.py"`) and use it for every command below.
`<site>` is any part of the site's URL, e.g. `example` or `blog.example.com`.

**If preflight still fails, STOP before doing any work** and tell the user exactly what is missing (folder not
connected, python missing, HTTP 406 firewall block, wrong login) — send a notification when running as a scheduled
task. Do not research and do not upload anything. This pipeline uses the REST API only — no browser at all, for any
WordPress step.

Command format:

```
python "<this-skill-folder>/scripts/wp.py" <command> <site> [options]
```

| Command | What it does |
|---|---|
| `sites` | list the configured sites |
| `check <site>` | verify the login works (run this first, every time) |
| `posts <site> --n 50` | list existing posts (id, slug, URL, title) — use it to verify internal links |
| `ensure-category <site> "Name"` | find or create the category, prints its id |
| `ensure-tags <site> "a,b,c"` | find or create the tags, prints comma-separated ids |
| `upload <site> <image> --alt "..." --title "..."` | upload an image, prints its id and URL |
| `draft <site> --title T --content-file F --slug S --excerpt E --category ID --tags 1,2 --featured ID` | create a **draft** post (never publishes) |
| `update <site> <post_id> ...same options...` | change an existing post |
| `publish <site> <post_id>` | publish a post |
| `get <site> <post_id>` | show status, link and title |

Write the article body as an HTML file (UTF-8; Arabic is fine) and pass it with `--content-file`. Put each uploaded
image's URL into that HTML as `<img src="..." alt="...">` next to its section.

Once `check <site>` succeeds, use the helper for every WordPress task it covers: creating the draft with the finished
content, uploading images, setting the featured image, category, tags, and publishing.

**No browser, no RankMath UI.** RankMath's SEO title, meta description, focus keyword, score and the Custom Schema
field live in the post editor and have no REST API equivalent. This skill does **not** open the editor, does not use
Chrome, Edge or Claude's own browser, and does not try to set those fields. It writes everything to RankMath's rules and
hands the user the exact values to paste (Stage 9, step 19). Never ask the user to log in to wp-admin for this.

**Order of work:** finish writing, upload images (Stage 5), set category/tags (Stage 7), run the local RankMath-rules
check (Stage 8), create the **draft** with the helper (Stage 9, step 16), publish, then build the paste-ready package
from the final post data (Stage 6) and deliver it.

If the user just gives a topic (in any message, any format) and this skill's context applies, treat that topic as the
input and run the full pipeline below without asking them to re-paste instructions.

**This skill depends on another skill**: `seo-blog-write-ar-en`. The research in Stage 1 is done by this skill, in full
depth — don't skip or shrink it. Once the topic, keywords, and angle are settled from that research, **the actual
writing itself — the SEO package, article body, and FAQ — is always produced by handing off to `seo-blog-write-ar-en`
in Stage 2**, never written directly by this skill. Its instructions aren't duplicated here. Override it only on
the specific point listed in Stage 4 (the FAQ/schema update). If `seo-blog-write-ar-en` isn't available for some reason,
fall back to a plain E-E-A-T-grounded writing approach using the Stage 1 research directly, and note that in the final
report.

## Stage 1 — Research and planning (do this in full depth — don't shortcut it)

1. Identify the target audience precisely: who reads this, what do they already know.
2. Identify search intent: informational / navigational / commercial / transactional.
3. Search the web for the topic and extract:
   - The best-fit primary focus keyword
   - 3–5 secondary/LSI keywords
   - 4–6 real questions people actually ask about the topic (People Also Ask, forums, Reddit, Google Trends)
   - Use Google Trends also to search for the best and trending topic suitable
   - What the current top 5–10 Google results already cover, so you can identify the content gap and add something
     genuinely missing (information gain)
4. Check current interest/demand before locking in the angle, not just relevance: look at what's trending in search
   right now (Google Trends), which keyword variations are getting the most search volume this period, and which
   questions people have been asking most recently (recent Reddit threads, recent forum activity, recent People Also
   Ask results — not stale evergreen questions only). Use this to sharpen the keyword and angle choice so the article
   targets what people are actually searching for *this period*, which gives it the best shot at traction once it goes
   live — not just a topic that's generically relevant to the niche.
5. Define the E-E-A-T angle: what real experience, data, or expert perspective will this specific article add?
6. Estimate an appropriate word count based on topic depth — never pad to hit a number.
7. If the site is reachable (use `wp.py posts <site> --n 50` for the list of existing posts), skim its existing blog content so the new article doesn't duplicate a topic already
   covered, and note the site's existing language/tone/niche so the writing skill can match it.

## Stage 2 — Writing (hand off to seo-blog-write-ar-en)

7. Invoke the **seo-blog-write-ar-en** skill to produce the actual article. Pass it everything gathered in Stage 1:
   the topic, target audience, search intent, primary + secondary keywords, the real questions found, the content gap /
   information-gain angle, the E-E-A-T angle, the word-count estimate, the language/dialect to write in (match the
   site's existing language unless the user specified one), and any tone/niche notes from the site scan. It should not
   need to re-research from scratch — Stage 1 already did that work.
8. Take its full output as-is: the SEO package (H1 + alternatives, meta description + alternatives, keyword list, slug),
   the full article body, and its FAQ section — **except** for the specific override in Stage 4 below.

## Stage 3 — Content quality gate

9. Before moving on, sanity-check the delivered article against these WordPress-publishing-specific additions (these
   are on top of, not instead of, `seo-blog-write-ar-en`'s own self-evaluation checklist):
   - The closing paragraph has **no call-to-action** — it should read as genuinely helpful, not like a sales pitch.
   - If the topic naturally involves a comparison, at least one table is present, styled to fit the site's look where
     the publishing tool allows styling.
   - **Internal links are actually placed in the body, not just suggested.** Take the post list from
     `wp.py posts <site> --n 50` and insert 2–4 links as real `<a href="...">` tags (full URL exactly as the helper
     printed it, natural descriptive anchor text, spread across different sections) pointing only to existing blog
     articles on this site that are genuinely related. Never link to service pages, product pages, contact pages or any
     page that pushes a call to action for the site's services. If the site has fewer than 2 related posts, use what
     exists and say so in the final report. Before creating the draft, check the HTML file itself: it must contain
     each internal URL (grep the file). A link that appears only in your notes does not count.
   - **References go at the very end of the article as a bullet list.** After the closing paragraph (and the FAQ),
     add a heading (e.g. "المراجع" for Arabic, "References" for English) followed by a `<ul>` with one `<li>` per
     source: 3–6 real, reputable external sources actually used in Stage 1 research, each as
     `<a href="..." target="_blank" rel="noopener">Source name — page title</a>`. One bullet per source, no
     paragraphs of references, no sources you did not open, and no links to competitors selling the same service.
     This list also counts as the external links RankMath looks for (checked in Stage 8).

## Stage 4 — FAQ section: override the writing skill's schema note (important 2026 update)

10. `seo-blog-write-ar-en` will hand you a FAQ section and may suggest a "FAQ Schema block" as something to always
    include for rich results. **Override that specific point** — here is why and what to do instead:

    Google fully deprecated FAQ Rich Results in Google Search as of May 7, 2026 (confirmed via Google Search Central's
    own changelog, Search Engine Land, and Search Engine Journal). Search Console's FAQ report and the Rich Results
    Test lose support in June 2026, and the Search Console API support for it is removed in August 2026. FAQ schema no
    longer produces any visible rich result in Google Search — Google has said it may still use FAQ structured data to
    understand the page, but will not display it.

    So:
    - Keep the FAQ section itself (4–6 real questions, 40–60 word direct answers) — it's genuinely useful to the reader
      and helps AI systems (ChatGPT, Perplexity, Copilot) parse the page clearly.
    - Only add FAQPage schema (in Stage 6 below) if the questions are genuinely real and useful — never as a
      rich-result tactic, since that no longer works.
    - **Never** let a filler or fabricated FAQ section through just because the writing skill defaults to including
      one. If the topic doesn't genuinely support 4+ real questions, ask for (or write) a shorter, folded-in version
      instead.

## Stage 5 — Images

11. Prepare 3–5 images (one featured image + supporting images near relevant sections):
    - **Stock photos first, always.** Every image is a real royalty-free stock photo that genuinely matches the topic
      (not generic filler), unless it falls under the one exception below. Search the sources in this order and move
      to the next one when the current one has nothing suitable (also retry with synonyms and English keywords before
      moving on): Pexels, Unsplash, Pixabay, StockSnap.io, Kaboompics, picjumbo, Life of Pix, Freestocks,
      Gratisography. All of these allow commercial use without attribution (Kaboompics: no reselling of the photo
      itself). Avoid sites whose free tier requires attribution (e.g. Vecteezy) and sites where the license changes from
      image to image (FreeImages, VisualHunt) unless you check the license of that specific image. Never take images
      from Google Images or from other websites' articles.
    - **The featured image is ALWAYS a stock photo.** Never generate it with AI, and never fall back to AI for it. If
      the first sources have nothing good, keep going down the list and widen the search terms (a related concept
      is fine) until a suitable photo is found.
    - **The only case for a generated image:** a visual that cannot exist as a photograph, such as a list, checklist,
      infographic, comparison graphic, step diagram or chart built from the article's own points. Build it cleanly
      (readable text in the article's language, consistent with the site's colors). Photos of real scenes, people,
      places, objects or concepts are never replaced by AI images.
    - Resize/compress appropriately for page speed without visible quality loss.
    - Place each image next to the section it illustrates — never stack them all at the top.
    - Write genuine, descriptive alt text for every image (natural keyword inclusion where relevant, no stuffing).
    - Keep a note of each stock image's source site and the photo's page URL for the final report.
    - Upload every image with `wp.py upload <site> <file> --alt "..."` and note the returned id and URL. Use the URL
      inside the article HTML and pass the featured image's id as `--featured` when creating the draft — not just as
      the first inline image. (The helper was already verified in Step 0; if a command fails mid-run, report the exact
      error instead of switching to a browser.)

## Stage 6 — Schema (prepared for the user to paste — Claude does not paste it)

12. Build the JSON-LD only after the post is published (Stage 9, step 18), so it uses the real post URL and the real
    publish date. Do not open any editor and do not try to place it on the post: it goes into the final delivery
    (Stage 9, step 19) and the user pastes it into the **Custom Schema** box at the bottom of the post editor. Deliver
    it as one plain JSON-LD block (no `<script>` wrapper) containing the pieces below (a single object with `@graph` is
    fine), and check that it is valid JSON by running it through `python3 -c "import json,sys; json.load(sys.stdin)"`
    before sending it:

    **a) BlogPosting** (use `BlogPosting`, not the generic `Article` — more accurate for blog content). Include:
    `headline`, `description`, `datePublished` and `dateModified` (full ISO 8601, e.g.
    `2026-07-07T08:00:00+00:00`, and these **must exactly match** the dates visibly shown on the page — take the date
    and time from the published post, and if `wp.py get` does not print them, use the publish moment with the
    site's UTC offset and say so in the delivery), `image` (the featured image's uploaded URL), `author` (as a
    `Person` object, ideally with `sameAs` linking to a real profile, e.g. LinkedIn), `publisher` (as an `Organization`
    object — reuse the site's existing Organization data if it already exists rather than creating a new one per
    post), `mainEntityOfPage`, and the page URL.

    **b) BreadcrumbList**: Home > Blog > Post title.

    **c) FAQPage** — only per the Stage 4 rule above (genuine questions only, never as a rich-result tactic).

    Rules:
    - JSON-LD only — never Microdata or RDFa.
    - Use `@id` to connect entities (BlogPosting referencing Organization, etc.).
    - Every date and detail in the schema must exactly match what's visibly on the page — mismatches are a strong
      negative trust signal, especially as AI systems increasingly verify this.
    - Don't use `NewsArticle` on non-news content; don't add `Review` schema to editorial opinion (risks spam filters)
      unless it's a genuine user review; avoid `HowTo` unless the content is truly step-by-step.

## Stage 7 — Tags and category

13. Assign one appropriate category (create it if it doesn't exist and makes sense) with
    `wp.py ensure-category <site> "Name"`, and pass the id as `--category`.
14. Add 4–6 relevant tags (secondary keywords + related terms) with `wp.py ensure-tags <site> "a,b,c"`, and pass the
    ids as `--tags`.

## Stage 8 — RankMath rules check (done locally, no browser, no score)

15. The real RankMath score cannot be read from here and is not reported. Instead, before creating the draft, check
    the article and the SEO package against RankMath's criteria yourself, working on the HTML file and the values
    from the SEO package (count characters with a script, grep the file — don't eyeball it), so the user's paste
    lands on a post that already meets them:
    - Primary keyword present in: SEO Title, slug, first paragraph, at least one subheading, meta description
    - SEO Title under 60 characters and contains the keyword
    - Meta description 140–155 characters
    - URL slug short, keyword-first, no filler words
    - Content length appropriate for the keyword's competitiveness (follow RankMath's suggested count)
    - Keyword density within RankMath's acceptable range (no warning)
    - At least one image with the keyword in its alt text
    - At least one internal and one external link actually present in the body (grep the HTML file for the internal
      URLs and for the external `<a href>` tags from the References list)
    - Readability: short paragraphs, non-run-on sentences, appropriate transition words
    - Fix anything that fails before creating the draft; if something is only noticed afterwards, correct the HTML and
      push it with `wp.py update`

## Stage 9 — Publish

16. Create the post as a **Draft** first with `wp.py draft <site> --title ... --content-file ... --slug ...
    --excerpt ... --category ... --tags ... --featured ...`. It prints the post id and a link.
17. Re-run the Stage 8 local check on what was actually saved; fix anything that fails and apply body fixes with
    `wp.py update`.
18. Publish for real with `wp.py publish <site> <post_id>`. Confirm with `wp.py get`. Then build the schema
    (Stage 6) from the final post data.
19. **Final delivery — the paste-ready package.** Send it in a message of its own (use `SendUserMessage` when running
    as a scheduled or unattended task), each value in its own code block so it copies cleanly, in this order:
    1. **Focus Keyword** (primary), plus the secondary keywords as one comma-separated line.
    2. **SEO Title** — with its character count (under 60, contains the keyword).
    3. **Slug** — exactly as set on the post.
    4. **Meta Description** — with its character count (140–155).
    5. **Schema** — the complete final JSON-LD from Stage 6, validated as JSON.

    Add one line saying where each goes in the post editor (RankMath: Focus Keyword, SEO Title, Permalink/Slug,
    Description; and the Custom Schema box for the schema). Claude has pasted none of these.

    Then report back: the topic research summary (focus keyword, content gap found), the published post URL, the
    assigned category/tags, the internal links placed (anchor + URL for each) and the references list, the image
    sources used (site per image, and whether any image was generated and why), which Stage 8 checks passed, and a
    plain note that no RankMath score was checked because the fields are pasted by the user. Never include any
    password in the report.

## General notes

- Write in whatever language/dialect the user specifies for the topic; if unspecified, default to the site's primary
  language.
- Never copy sentences or paragraphs verbatim from any source — everything must be written in original phrasing.
- Keep the writing style completely natural and human, avoiding any pattern that reads as obviously AI-generated (this
  is enforced by `seo-blog-write-ar-en`'s style rules — don't relax them here).
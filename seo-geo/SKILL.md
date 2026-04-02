---
name: seo-geo
description: "Full SEO and GEO (Generative Engine Optimization) workflow for any project. Use when optimizing website content for search engines AND AI citation (ChatGPT, Perplexity, Google AI Overviews). Covers keyword research via DataForSEO API, competitor analysis, on-page audits, meta tag optimization, content gap analysis, GEO content optimization (quotable definitions, FAQ schema, structured data), and rank monitoring. Trigger on: SEO, GEO, keywords, search rankings, AI citations, meta tags, structured data, schema markup, content optimization, SERP analysis."
---

# SEO & GEO Optimization

Run `/seo-geo` with an argument to jump to a specific phase, or run without arguments for the full workflow.

Arguments: `research`, `audit`, `gaps`, `geo`, `content`, `monitor`, or a specific page path like `/pricing`.

## Setup

Before running, detect the project context automatically:

1. **Site domain**: Read from the codebase (look for `metadataBase`, canonical URLs, or `NEXT_PUBLIC_` env vars). Ask the user if unclear.
2. **Repo**: Use the current working directory.
3. **Keyword data**: Look for `SEO_KEYWORDS.md` in the project root. Create if missing.
4. **Framework**: Detect from package.json (Next.js, Nuxt, Astro, etc.)
5. **DataForSEO credentials**: Set `DATAFORSEO_CREDENTIALS` env var with your Base64-encoded `email:password`. Get an account at [dataforseo.com](https://dataforseo.com). Example: `export DATAFORSEO_CREDENTIALS=$(echo -n 'you@email.com:yourpassword' | base64)`

Ask the user for:
- **Voice/tone** description (if not in CLAUDE.md)
- **Key competitors** (domains)
- **Seed keywords** for research
- **Brand concerns** (name conflicts, etc.)

If any of these are already documented in CLAUDE.md, SEO_KEYWORDS.md, or memory, use those instead of asking.

---

## Phase 1: Research

Read SEO_KEYWORDS.md first. If it's stale (>30 days) or doesn't exist, run these API calls.

### 1a. Keyword research

Pull search volume for target keywords via DataForSEO:

```bash
curl -s -X POST "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live" \
  -H "Authorization: Basic $DATAFORSEO_CREDENTIALS" \
  -H "Content-Type: application/json" \
  -d '[{"keywords": [LIST], "location_code": 2840, "language_code": "en"}]'
```

Expand with keyword suggestions:
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live" \
  -H "Authorization: Basic $DATAFORSEO_CREDENTIALS" \
  -H "Content-Type: application/json" \
  -d '[{"keyword": "SEED", "location_code": 2840, "language_code": "en", "limit": 50, "order_by": ["keyword_info.search_volume,desc"]}]'
```

Get difficulty scores:
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/bulk_keyword_difficulty/live" \
  -H "Authorization: Basic $DATAFORSEO_CREDENTIALS" \
  -H "Content-Type: application/json" \
  -d '[{"keywords": [LIST], "location_code": 2840, "language_code": "en"}]'
```

Classify intent:
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/search_intent/live" \
  -H "Authorization: Basic $DATAFORSEO_CREDENTIALS" \
  -H "Content-Type: application/json" \
  -d '[{"keywords": [LIST], "language_code": "en"}]'
```

### 1b. Competitor keyword theft

Pull non-brand keywords from competitors:
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live" \
  -H "Authorization: Basic $DATAFORSEO_CREDENTIALS" \
  -H "Content-Type: application/json" \
  -d '[{"target": "COMPETITOR_DOMAIN", "location_code": 2840, "language_code": "en", "limit": 80, "order_by": ["keyword_data.keyword_info.search_volume,desc"]}]'
```

Filter out brand terms in post-processing.

### 1c. Check current rankings

```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live" \
  -H "Authorization: Basic $DATAFORSEO_CREDENTIALS" \
  -H "Content-Type: application/json" \
  -d '[{"target": "SITE_DOMAIN", "location_code": 2840, "language_code": "en", "limit": 50, "order_by": ["ranked_serp_element.serp_item.rank_group,asc"]}]'
```

### 1d. SERP analysis for top targets

```bash
curl -s -X POST "https://api.dataforseo.com/v3/serp/google/organic/task_post" \
  -H "Authorization: Basic $DATAFORSEO_CREDENTIALS" \
  -H "Content-Type: application/json" \
  -d '[{"keyword":"TARGET","location_code":2840,"language_code":"en","depth":20}]'
```

Retrieve after ~60s:
```bash
curl -s "https://api.dataforseo.com/v3/serp/google/organic/task_get/advanced/TASK_ID" \
  -H "Authorization: Basic $DATAFORSEO_CREDENTIALS"
```

**Output**: Update SEO_KEYWORDS.md with fresh data. Summarize top opportunities.

### 1e. Adjacent keyword brainstorming

The steps above find keywords you already know about. This step finds keywords you **haven't thought of** — adjacent topics, competitor ecosystems, and broader search intents that your product intersects with but doesn't directly target.

**Process:**

1. **Map value props to broader intents.** For each core feature, ask: what problem does this solve? What else do people searching for that problem also search for? Example: if your product adds iMessage to AI agents, the broader intents include "ai agent messaging", "chatbot platforms", "ai phone number", "conversational AI", "ai assistant framework comparison".

2. **Explore competitor ecosystems.** Use DataForSEO keyword suggestions seeded with competitor brand names (not just your own):
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live" \
  -H "Authorization: Basic $DATAFORSEO_CREDENTIALS" \
  -H "Content-Type: application/json" \
  -d '[{"keyword": "COMPETITOR_NAME", "location_code": 2840, "language_code": "en", "limit": 40, "order_by": ["keyword_info.search_volume,desc"]}]'
```
Run this for each major competitor. Look for "[competitor] alternative", "[competitor] vs", "[competitor] setup", "[competitor] pricing" patterns. These are high-intent keywords where you can insert yourself.

3. **Check "alternative to" and "vs" keywords.** These are comparison shoppers — the highest-intent SEO traffic:
```bash
# Search volume for "[product] alternative" and "[product] vs [competitor]"
curl -s -X POST "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live" \
  -H "Authorization: Basic $DATAFORSEO_CREDENTIALS" \
  -H "Content-Type: application/json" \
  -d '[{"keywords": ["PRODUCT alternative", "PRODUCT alternatives", "PRODUCT vs COMPETITOR1", "PRODUCT vs COMPETITOR2", "COMPETITOR1 alternative", "best CATEGORY 2026"], "location_code": 2840, "language_code": "en"}]'
```

4. **Explore adjacent communities.** Use WebSearch to find what forums, subreddits, and communities discuss topics adjacent to your product. Look for recurring questions that nobody has a good answer for — those are content opportunities.

5. **Check non-English markets.** If your product works internationally, run keyword suggestions in other languages (zh, es, ja, de, ko). Chinese, Japanese, and Korean tech communities often search in their own language for tools that only have English documentation — creating a zero-competition content opportunity:
```bash
curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live" \
  -H "Authorization: Basic $DATAFORSEO_CREDENTIALS" \
  -H "Content-Type: application/json" \
  -d '[{"keyword": "PRODUCT_NAME", "location_code": 2392, "language_code": "ja", "limit": 30, "order_by": ["keyword_info.search_volume,desc"]}]'
```
Location codes: 2156 (China), 2392 (Japan), 2410 (South Korea), 2276 (Germany), 2724 (Spain).

**Output**: A "lateral opportunities" section in SEO_KEYWORDS.md with:
- Adjacent keyword clusters not covered by existing content
- Competitor ecosystem keywords you can target
- Non-English keyword opportunities
- Recommended blog posts or pages for each cluster

---

## Phase 2: Technical SEO Audit

### 2a. On-page crawl

```bash
curl -s -X POST "https://api.dataforseo.com/v3/on_page/task_post" \
  -H "Authorization: Basic $DATAFORSEO_CREDENTIALS" \
  -H "Content-Type: application/json" \
  -d '[{"target": "SITE_DOMAIN", "max_crawl_pages": 50, "max_crawl_depth": 3, "load_resources": true, "enable_javascript": true, "calculate_keyword_density": true, "validate_micromarkup": true, "check_spell": true}]'
```

Get summary:
```bash
curl -s -X POST "https://api.dataforseo.com/v3/on_page/summary" \
  -H "Authorization: Basic $DATAFORSEO_CREDENTIALS" \
  -H "Content-Type: application/json" \
  -d '[{"id": "TASK_ID"}]'
```

Get page-level issues:
```bash
curl -s -X POST "https://api.dataforseo.com/v3/on_page/pages" \
  -H "Authorization: Basic $DATAFORSEO_CREDENTIALS" \
  -H "Content-Type: application/json" \
  -d '[{"id": "TASK_ID", "limit": 50}]'
```

### 2b. Codebase audit (no API needed)

For each page in the codebase, check:

| Check | What to verify |
|-------|---------------|
| `<title>` | 50-60 chars, primary keyword + brand, unique per page |
| `<meta description>` | 140-160 chars, includes primary + secondary keyword |
| OG tags | og:title, og:description, og:image set and unique |
| Twitter card | twitter:card, twitter:title, twitter:description |
| Canonical URL | Set via `alternates.canonical` or `<link rel="canonical">` |
| H1 | Exactly one per page |
| JSON-LD | Structured data present (Organization, FAQPage, SoftwareApplication, Article) |
| Internal links | Blog posts link to sign-up, pages cross-link |
| Image alt text | All images have descriptive alt attributes |
| robots.txt | Exists at public/robots.txt |
| Sitemap | Exists or generated by framework |

### 2c. Fix meta tags

**Rules:**
- Title: 50-60 chars, primary keyword + brand. Format: `[Page Name] — [Keyword Phrase] | Brand`
- Description: 140-160 chars, include primary + secondary keyword naturally
- H1 can stay editorial — meta title does the SEO work

---

## Phase 3: Content Gap Analysis

### 3a. Map keywords to pages

Read SEO_KEYWORDS.md and compare against existing pages. For each keyword cluster, identify whether a page targets it.

### 3b. Identify missing content

Look for high-volume, low-difficulty keywords with no targeting page. Common gaps:
- Missing /blog index page
- Missing /pricing page (if pricing exists but isn't a standalone page)
- Missing comparison pages (vs. competitors)
- Missing "how to" / tutorial content
- Missing /about page

### 3c. Plan new content

For each gap, define: target keyword, page title, audience, word count, internal links.

---

## Phase 4: GEO Optimization

GEO = Generative Engine Optimization. Making content appear in AI-generated answers (ChatGPT, Perplexity, Google AI Overviews, Claude).

### 4a. GEO audit of existing pages

For each page, score these factors (1-10):

| Factor | What to check |
|--------|---------------|
| Clear definitions | Key terms defined in 25-50 word standalone blocks? |
| Quotable statements | Specific, citeable facts with sources? |
| Factual density | Stats with numbers, units, sources? |
| Q&A format | Content answers "What is X?" / "How does X work?" directly? |
| Authority signals | Expert credentials, citations, first-party data? |
| Structure | Tables, numbered lists, clear headings matching query intent? |

**AI engine preferences:**

| Engine | Priorities |
|--------|-----------|
| Google AI Overview | Direct answer in first 150 words, tables, FAQ schema, JSON-LD |
| ChatGPT Browse | Specific facts, expert quotes, freshness, .edu/.gov trust |
| Perplexity | Freshness bias, quotable standalone statements, primary sources |
| Claude | Authoritative definitions, verifiable facts, reasoning transparency |

### 4b. Add quotable definitions

Every key concept needs a standalone definition block:
**Template**: `**[Term]** is [clear category] that [primary function], [key characteristic].`

### 4c. Add FAQ schema

For pages targeting commercial/informational keywords:
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is [term]?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[25-50 word definition from the page]"
      }
    }
  ]
}
```

### 4d. Add Organization schema

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "BRAND_NAME",
  "url": "https://SITE_DOMAIN",
  "description": "DESCRIPTION",
  "email": "CONTACT_EMAIL"
}
```

### 4e. CORE-EEAT GEO checklist

| ID | Standard | Check |
|----|----------|-------|
| C02 | Direct answer in first 150 words | Does the page answer its primary query immediately? |
| C04 | Key terms defined on first use | Are technical terms defined inline? |
| C09 | Structured FAQ | Does the page have a Q&A section? |
| O02 | Summary box / key takeaways | Is there a TL;DR? |
| O03 | Data in tables, not prose | Are comparisons in table format? |
| O05 | JSON-LD schema markup | Is structured data present? |
| R01 | 5+ precise data points with units | Are there specific numbers? |
| R04 | Claims backed by evidence | Is every claim sourced? |
| R07 | Full entity names | No "a company" — always use the brand name |
| E01 | Original first-party data | Are own benchmarks/stats shared? |
| Exp10 | Limitations acknowledged | Is scope stated honestly? |
| Ept08 | Reasoning transparency | Are choices explained? |

---

## Phase 5: Content Creation

### Writing SEO+GEO optimized content

1. **First 150 words**: Direct answer to the primary query. Include target keyword and standalone definition.
2. **Body**: H2 headings matching question-format queries. Each section 3-5 sentences. Comparisons in tables, processes in numbered lists.
3. **Quotable blocks**: Every 300 words, include a bold statistic or definition AI can extract.
4. **Citations**: At least 1 external citation per 500 words.
5. **FAQ section**: 3-5 questions matching long-tail keywords.
6. **Internal links**: Descriptive anchor text (not "click here").

---

## Phase 6: Monitor

### 6a. Track rankings

Re-run ranked_keywords query monthly. Compare against previous SEO_KEYWORDS.md.

### 6b. Check AI citations

Search for the brand in ChatGPT, Perplexity, Google AI Overviews using target keywords.

### 6c. Iterate

1. Update SEO_KEYWORDS.md with fresh data
2. Identify keywords moving up/down
3. Find new long-tail opportunities
4. Refresh stale content (update dates, stats)
5. Write new content targeting gaps

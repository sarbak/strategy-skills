# Strategy Skills for Claude Code

Six skills that turn Claude Code into a structured strategy and growth toolkit. Strategy analysis, SEO/GEO optimization, product analytics, and content from your own meetings, all as reusable slash commands.

Built by [Emotion Machine](https://emotionmachine.com).

## The Skills

### Strategy

#### `/opportunity-analysis` (18 steps)
Structured opportunity evaluation from brainstorm to recommendation. Problem definition, divergent brainstorm, MECE scoring framework, market sizing, synthesis, assumption validation, and iterative refinement.

#### `/deep-research` (8 steps)
Focused research to validate assumptions and check facts. Orders questions by how fundamental they are. Works with any research tool in your environment (Perplexity, web search, etc.).

#### `/storyline-synthesis` (10 steps)
Turns messy analysis into a clean, McKinsey-style synthesis document. Pyramid structure, action-sentence headers, sourced data points, and six quality tests before publishing.

### Growth

#### `/seo-geo` (6 phases)
Full SEO and GEO (Generative Engine Optimization) workflow. Keyword research via DataForSEO API, competitor analysis, on-page audits, content gap analysis, adjacent keyword brainstorming, GEO content optimization, and rank monitoring. Optimizes for both Google and AI search engines (ChatGPT, Perplexity, Claude, Copilot).

Requires a [DataForSEO](https://dataforseo.com) account for API-based keyword research.

#### `/analytics-review` (8 steps)
Pull PostHog funnel metrics and Supabase/Postgres usage data, compare against saved baselines, correlate with PRs/deploys, and surface actionable insights. Works with any PostHog + Postgres project.

#### `/linkedin-from-meetings` (10 steps)
Turn meeting notes and call transcripts into scheduled LinkedIn drafts. Finds your notes wherever they live (a folder of markdown, Granola, Fathom, Fireflies, Otter, Notion, Obsidian, Google Docs, a database table), mines them for insights only you could have, scores each on specific / contested / earned, runs a four-check confidentiality gate before anything about a client leaves the room, and drafts in a voice extracted from your own past posts. Drafts only, never posts.

## How the strategy skills work together

```
/opportunity-analysis
    |
    |-- Stage 5: Synthesize --> calls /storyline-synthesis
    |-- Stage 6: Validate   --> calls /deep-research
    |-- Stage 7: Rewrite    --> calls /storyline-synthesis again
    |
    (loops 2-3 times until assumptions are validated)
```

## How the growth skills work together

```
/seo-geo
    |
    |-- Phase 1e: Adjacent brainstorming --> finds new keyword clusters
    |-- Phase 3: Content gaps --> identifies missing pages
    |
    v
Write content targeting gaps
    |
    v
/analytics-review
    |-- Correlates PRs with metric changes
    |-- Tracks funnel impact of new content
    |-- Saves baseline for next comparison
```

Each skill also works independently.

## Install

### Claude Code (global)
```bash
# Install all six
claude skills add sarbak/strategy-skills@opportunity-analysis -g
claude skills add sarbak/strategy-skills@deep-research -g
claude skills add sarbak/strategy-skills@storyline-synthesis -g
claude skills add sarbak/strategy-skills@seo-geo -g
claude skills add sarbak/strategy-skills@analytics-review -g
claude skills add sarbak/strategy-skills@linkedin-from-meetings -g
```

### Manual
Copy the `SKILL.md` file from any skill folder into `~/.claude/skills/<skill-name>/SKILL.md`. `linkedin-from-meetings` also ships a `reference/` folder, so copy that whole directory.

## Setup

### `/seo-geo`
Requires a [DataForSEO](https://dataforseo.com) account. Base64-encode your `email:password` and replace `YOUR_DATAFORSEO_BASE64_CREDENTIALS` in the SKILL.md API calls.

### `/analytics-review`
Reads PostHog and database credentials from your environment variables or project `.envrc` files. No manual setup needed if your project already has `POSTHOG_API_KEY` and a database DSN configured.

### `/deep-research`
Works with any research tool in your Claude Code environment — Perplexity MCP, web search, etc.

### `/linkedin-from-meetings`
Needs three things from you on the first run: a line or two describing what you do and who you sell to, where your meeting notes live, and access to your own past LinkedIn posts so the skill can extract your voice. Nothing is hardcoded, and no credentials live in the skill.

## Step numbering

All skills use explicit step numbering (`Step 3/18`, `Step 1e/6`, etc.) so Claude:
- Knows how many steps remain and doesn't skip ahead
- Reports progress clearly
- Handles sub-steps without losing track of the parent step

## Output files

### `/opportunity-analysis`
| File | Purpose |
|------|---------|
| `BRAINSTORM.md` | Raw brainstorm (30-50+ ideas) |
| `SCORING.md` | Scored use cases with framework |
| `MARKET-SYNTHESIS.md` | The final storyline document |
| `DEEP_RESEARCH_REQUEST.md` | Questions for validation |
| `DEEP_RESEARCH_RESULTS.md` | Findings with sources |

### `/seo-geo`
| File | Purpose |
|------|---------|
| `SEO_KEYWORDS.md` | Keyword data, volumes, difficulty, opportunities |

### `/analytics-review`
| File | Purpose |
|------|---------|
| Memory baseline file | Snapshot of metrics for future comparison |

### `/linkedin-from-meetings`
| File | Purpose |
|------|---------|
| `linkedin-drafts/<date>-week.md` | Scheduled drafts, sources, confidentiality verdicts, backlog |
| `reference/<user>-post-style.md` | Your voice, extracted once from your own posts and reused every run |

## Design principles

- **Step-by-step execution** — explicit numbered steps prevent the AI from compressing or skipping work
- **MECE everywhere** — mutually exclusive, collectively exhaustive frameworks
- **Data over opinions** — every claim needs a number or source
- **Top-down research** — validate fundamental assumptions before details
- **Iterative refinement** — synthesize-validate-rewrite cycles, not one-shot analysis
- **PR correlation** — analytics tracks what you shipped, not just what moved

## License

MIT

---

Built by [Emotion Machine](https://emotionmachine.com)

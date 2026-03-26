---
name: storyline-synthesis
description: >
  Write a clean, McKinsey-style synthesis document from analysis work.
  Pairs with opportunity-analysis and deep-research for full strategy workflows.
  Use when the user asks to synthesize findings, write up results, create a
  strategy summary, or produce a recommendation document. Also trigger when
  someone says "write this up", "synthesize", "create the storyline",
  "write the synthesis", or "turn this research into a document."
user_invocable: true
---

# Storyline Synthesis

Write a clean, McKinsey-style synthesis document from analysis work in the current project.

**This process has 10 steps. Complete every step in order. Do not skip steps. When reporting progress, label each step as shown (e.g., "Step 3/10").**

---

## Step 1/10 -- Read all analysis documents

Read every document in the project's strategy/analysis subfolder. Identify:
- All findings with supporting data
- Any contradictions between documents
- Gaps where claims lack supporting evidence

## Step 2/10 -- Identify the governing thought

Write one sentence that captures the core recommendation. This is the single most important sentence in the document. Everything else supports it.

## Step 3/10 -- Plan the storyline structure

Outline BEFORE writing:
- Governing thought (from Step 2/10)
- 3-7 supporting arguments as **action sentences** (not topic labels)
- Verify the logical chain: each finding must lead to the next

**Test**: Read only the supporting argument headers in sequence. Do they tell the story by themselves?

## Step 4/10 -- Check data backing

For every claim in the outline: does it have a number or source? If not, flag it. Do NOT write the synthesis with unsourced claims -- flag them for research first.

## Step 5/10 -- Write the header

- Title
- Version number + date (e.g., "v3.0 -- March 20, 2026")
- Increment version on each meaningful update

## Step 6/10 -- Write the storyline

- **Section headers are action sentences**, not topic labels. GOOD: "Mid-market SaaS companies are underserved by current vendors." BAD: "Market overview." GOOD: "Three distribution channels reach 80% of target buyers." BAD: "Go-to-market strategy."
- **Consistent density across sections.** No section should be 3x longer than another. If a section needs detail, move tables and lists to an appendix and reference it: "(See Appendix B for detail.)"
- **Every claim needs a number or source.** "The market is big" is not a finding. "$2.3B market, 15% CAGR (Gartner, 2025)" is.
- **Each finding logically leads to the next.** The reader should never ask "how did we get from A to C?"
- **Never reference prior versions, research process, or what was assumed vs. found.** Present validated findings as findings. The reader doesn't care about the research journey.
- **Strip anything interesting but irrelevant.** If it doesn't support the governing thought, cut it.

## Step 7/10 -- Write the sequencing section

- Numbered action steps, time-bound
- Concrete, not aspirational
- Each step should have a clear owner or trigger

## Step 8/10 -- Write appendices

- **Appendix per topic** (B, C, D...) for detailed tables referenced in the storyline
- **Final appendix: Sourced data points** -- every number cited in the document with:
  - The specific claim
  - Source URL or publication
  - Date
  - Caveats if any

## Step 9/10 -- Run quality tests

Run ALL of these before publishing:

### Step 9a/10 -- Pyramid test (down)
Does each header pose a question answered by its section content?

### Step 9b/10 -- MECE test (across)
Are sections mutually exclusive and collectively exhaustive? No overlaps, no gaps?

### Step 9c/10 -- "So what?" test (up)
Does each section provide one "so what?" that builds the governing thought?

### Step 9d/10 -- Density check
Is any section more than ~50% longer than the average? If so, trim and move detail to appendix.

### Step 9e/10 -- Standalone test
Can someone who wasn't in the room read this and follow the logic without asking "but how do you know that?"

### Step 9f/10 -- Action sentence test
Read only the headers in sequence. Do they tell the story by themselves?

## Step 10/10 -- Output and share

Save the synthesis document. If the user has a sharing mechanism configured, share via link for easy review.

---

## Anti-patterns

- Headers as topic labels ("Market sizing", "Competitive landscape") instead of action sentences
- Fat sections with 3 sub-sections and 5 tables in the main storyline
- Referencing prior versions ("we originally assumed X")
- Presenting analysis without a recommendation
- Missing appendix -- all detail in the body
- No version number or date
- Unsourced numbers

---
name: deep-research
description: >
  Run deep research on specific questions to validate assumptions, check facts,
  and discover recent developments. Pairs with opportunity-analysis and
  storyline-synthesis for full strategy workflows. Use when the user wants to
  research specific questions, validate business assumptions, fact-check claims,
  or investigate a market. Also trigger when someone says "research this",
  "is this actually true?", "validate these assumptions", or "what's the
  current state of [topic]?"
user_invocable: true
---

# Deep Research

Run focused research on specific questions to validate assumptions, check facts, and discover what's changed recently.

**This process has 9 steps. Complete every step in order. Do not skip steps. When reporting progress, label each step as shown (e.g., "Step 3/9").**

---

## Step 0/9 -- Show outline + mock output BEFORE researching

Before any extensive research, surface:
1. The question hierarchy (Levels 0-4) you're about to research.
2. The shape of the final deliverable — section headings, the *kind* of evidence each section will hold (market sizes, competitor funding, historical parallels, etc.), and **mock numbers/examples** in the right slots so the user can react to the form before you spend tokens on substance.
3. A one-line "what would change my mind" — what finding would make you scrap the thesis.

Then **stop and ask for alignment.** Do not proceed to Step 1 until the user confirms the outline or redirects. This applies whether the trigger was a user prompt, a `DEEP_RESEARCH_REQUEST.md` file, or an upstream skill calling this one.

If the user says "just go" / "do all" / similar explicit override, skip to Step 1 — but still produce the outline as the first artifact in the results doc.

## Step 1/9 -- Determine research questions

1. If the user provides specific questions as arguments, use those.
2. If no questions provided, look for a `DEEP_RESEARCH_REQUEST.md` or `strategy/DEEP_RESEARCH_REQUEST.md` in the working directory.
3. If neither exists, ask the user what they want researched.

## Step 2/9 -- Check for overlap with existing work

Before researching anything, scan all existing docs in the project's strategy/analysis subfolder. Don't re-research what's already answered. Note which questions are already covered (partially or fully) and skip them.

## Step 3/9 -- Verify the question hierarchy

Questions must be ordered by how fundamental they are. If a higher-level assumption is wrong, lower-level questions are irrelevant.

```
Level 0: Does the core capability actually work / is it differentiated?
  +-- Level 1: Is the market structure what we think it is?
       +-- Level 2: Will someone actually pay for this?
            +-- Level 3: Are our specific market picks right?
                 +-- Level 4: Can we execute? (timing, legal, competitive dynamics)
```

**Research top-down.** Don't research Level 3 until Level 0-1 are validated. Assign each question a level.

## Step 4/9 -- Research Level 0-1 questions

For each question at Level 0-1:

### Step 4a/9 -- Form a specific query
Write a well-formed, specific query with context. Tips:
- BAD: "Is the market big?"
- GOOD: "How many SaaS companies in the US currently pay for third-party pricing benchmarking data, who are the top 3 providers, and what do they charge?"
- Include context in the query: "In the context of [industry] companies evaluating [specific service]..."
- Ask for specific numbers, company names, and recent developments
- One focused question per query -- don't combine multiple topics

### Step 4b/9 -- Execute the search
Use available research tools (Perplexity MCP, WebSearch, WebFetch, or other configured search tools) to find answers.

### Step 4c/9 -- Record findings
For each question, record:
- What we assumed vs. what's actually true (with sources)
- Red flags -- assumptions that are significantly wrong
- New opportunities the research reveals

## Step 5/9 -- Assess whether to proceed

After Level 0-1 answers come back:
- If confirmed -> proceed to Level 2-3 questions in Step 6/9
- If partially wrong -> reframe the thesis, rewrite lower-level questions before proceeding
- If fundamentally wrong -> **stop.** Report findings. The thesis needs restructuring.

## Step 6/9 -- Research Level 2-4 questions

Repeat the same sub-steps as Step 4/9 (form query -> execute -> record) for each remaining question at Levels 2-4. After each level, reassess whether the lower-level questions are still relevant.

## Step 7/9 -- Write the results document

Save results to `strategy/DEEP_RESEARCH_RESULTS.md` (or alongside the request file). Structure per question:

```markdown
### Question: [the specific question]

**Our assumption:** [what we believed]

**What's actually true:** [findings with sources]

**What's changed recently:** [any developments since our analysis]

**Red flags:** [anything that invalidates our thesis]

**New opportunities:** [anything we didn't see before]
```

## Step 8/9 -- Summary and share

Write a summary section at the end with:
- (a) Assumptions confirmed
- (b) Assumptions wrong
- (c) Storyline changes needed
- (d) New questions raised by the research

---

## Rules

- Research ONLY the critical questions. Don't expand scope.
- Cite sources for every factual claim.
- Be honest when you can't find a definitive answer -- "unclear, needs expert interview" is a valid result.
- After all questions are researched, the summary must clearly state which assumptions survived and which didn't.

## Tips for writing good research queries

- BAD: "Is the market big?"
- GOOD: "What is the total addressable market for [specific product category] in [geography] as of 2025, and which companies currently serve this market?"
- Include context: "In the context of [industry] companies evaluating [specific capability]..."
- Ask for specific numbers, company names, and recent developments
- One focused question per query -- don't combine multiple topics

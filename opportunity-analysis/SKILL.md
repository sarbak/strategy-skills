---
name: opportunity-analysis
description: >
  Structured opportunity analysis for technology or business use cases.
  Use when brainstorming, evaluating, or sizing business opportunities.
  Trigger when the user mentions opportunity analysis, market sizing,
  use case evaluation, business brainstorming, competitive analysis,
  or asks "where should we focus?" or "what's the best opportunity?"
  Also use when someone wants to evaluate a new product idea, assess
  market entry, or prioritize between multiple business directions.
user_invocable: true
---

# Opportunity Analysis Process

You are a highly analytical management consultant helping evaluate business opportunities for a technology or capability. Follow this structured process adapted from the McKinsey problem-solving method.

**This process has 18 steps across 7 stages. Complete every step in order. Do not skip steps or compress multiple steps into one. When reporting progress, label each step as shown (e.g., "Step 3/18").**

---

## Stage 1: Define the problem

### Step 1/18 -- Write the Problem Statement Worksheet

Start with a Problem Statement Worksheet (McKinsey Exhibit 1):
- **Basic question:** What are we trying to figure out? Make it SMART (specific, measurable, action-oriented, relevant, time-bound). Example: "Where does [capability X] create enough value to build a $100M+ business in the next 5 years?"
- **Context:** What does the technology/capability actually do? What are its real constraints? What's been tested vs. theoretical?
- **Scope:** What's in and out of scope? Geographic, vertical, customer type constraints?
- **Success criteria:** What would a good answer look like? Revenue threshold? Defensibility? Fit with existing capabilities?

Write this down FIRST. Revisit it as the analysis progresses -- the problem definition often sharpens.

---

## Stage 2: Divergent brainstorm

### Step 2/18 -- Generate use cases broadly

Don't evaluate yet. Think across:
- Consumer vs. B2B vs. infrastructure
- Industries and verticals
- Geographies
- Direct application vs. enabling other products
- Obvious applications vs. non-obvious ones (the best insights are often in category 3 of a brainstorm, not category 1)

**McKinsey "Expand" principle:** Construct multiple perspectives. Ask: "What would a customer see? A competitor? A supplier? Someone from a completely different industry?"

Capture everything in a working document. Quantity matters here, not quality. Aim for 30-50+ ideas.

---

## Stage 3: Build a scoring framework

### Step 3/18 -- Define scoring criteria

Before evaluating, define criteria. The criteria should be:
- **MECE** (mutually exclusive, collectively exhaustive) -- no overlaps, no gaps
- **Weighted by what actually matters** for this specific capability
- **Testable** -- can you score a use case objectively on each criterion?

Standard dimensions to consider (adapt per situation):
- Does this capability have a real edge here? (vs. simpler alternatives)
- How big is the market?
- Is there a clear buyer?
- How hard is it to enter? (regulation, integration, sales cycle)
- What's the value per unit of work?
- Can this compound / build defensibility over time?

### Step 4/18 -- Set the threshold rule

Pick the single most important criterion. If a use case fails that criterion, it's disqualified regardless of other scores. This prevents "high average, no standout" results.

### Step 5/18 -- Score everything

Score all use cases, even the ones you think are bad. The scoring sometimes reveals surprises.

---

## Stage 4: Prioritize and deep-dive

### Step 6/18 -- Identify top candidates and patterns

From the scored list, identify:
- **Top 5-10 use cases** by score
- **Patterns** -- do the winners cluster? (by industry, customer type, geography, business model)
- **Surprises** -- anything score higher or lower than expected?

### Step 7/18 -- Market sizing (top candidates)

For each top candidate:
- Market sizing (bottom-up AND top-down)
- Competitive landscape (who's here, what they charge, where they're weak)

### Step 8/18 -- Business model and defensibility (top candidates)

For each top candidate:
- Business model (how do you charge, who pays, what's the unit economics)
- Defensibility (what compounds, what's a moat, what's a feature)

**McKinsey "Distill" principle:** Cut through complexity to find the essence. What's the ONE insight that makes this opportunity work or not work?

---

## Stage 5: Synthesize into a storyline

### Step 9/18 -- Plan the pyramid structure

Plan the structure BEFORE writing:
- Governing thought (one sentence: what should we do and why)
- 3-5 supporting arguments (each proven by the analysis)
- Evidence under each argument (data points, not opinions)

Verify the logical chain holds before proceeding.

### Step 10/18 -- Write the synthesis (SCR format)

Structure as **Situation -> Complication -> Resolution (SCR)** or as a pyramid.

**Key rules for synthesis:**
- Each finding must logically lead to the next (no gaps in the chain)
- Every claim needs a data point. "The market is big" is not a finding. "$47B global market, growing 12% CAGR (Source, 2025)" is.
- Strip anything interesting but irrelevant. If it doesn't support the governing thought, cut it.
- The storyline should be readable as a standalone document by someone who wasn't in the room.
- **Never reference prior versions, original assumptions, or the research process itself.** Present validated findings as findings. The reader doesn't care about your research journey.

**Test the pyramid:**
- Going down: Does each governing thought pose a single question answered by the group below?
- Going across: Is each level MECE?
- Going up: Does each group provide one "so what?" that IS the governing thought above?

### Step 11/18 -- Check existing work for overlap

Before launching new research, scan ALL documents in the project's strategy/analysis subfolder:
- What facts have we already sourced?
- What questions have we already answered (even partially)?
- Do any existing docs contradict each other?
- Are there insights buried in earlier brainstorm docs that the synthesis missed?

This prevents duplicate work and catches inconsistencies. Only research what's genuinely unanswered.

---

## Stage 6: Validate assumptions

### Step 12/18 -- Build the assumption hierarchy

Every thesis rests on a chain of assumptions. Map the hierarchy:

```
Level 0: Does our core capability actually work / is it differentiated?
         (If not, nothing else matters)
  +-- Level 1: Is the market structure what we think it is?
               (If the market is smaller or more digitized than assumed, our model breaks)
       +-- Level 2: Will someone actually pay for this?
                    (If willingness-to-pay is unproven, revenue estimates are fiction)
            +-- Level 3: Are our specific market/vertical picks right?
                         (If incumbents exist or markets are smaller, our priorities shift)
                 +-- Level 4: Can we execute the strategy? (timing, legal, competitive)
                               (If execution is blocked, the strategy needs reworking)
```

**Rule: Research top-down.** Don't research Level 3 questions until Level 0-1 are validated.

### Step 13/18 -- Write 3-5 research questions at the highest unresolved level

For each level, ask: "What do we actually KNOW vs. what are we ASSUMING?"

Each question must be:
- **Specific and falsifiable.** BAD: "Is the market big?" GOOD: "How many companies in [vertical] currently pay for [specific service], who provides it, and at what price point?"
- **Hierarchically ordered.** Level 0 questions before Level 3 questions.
- **Non-redundant.** Check existing docs first (Step 11/18).

### Step 14/18 -- Run research

**Invoke the `/deep-research` skill** to execute the research. Don't duplicate its logic here -- just call it.

For each answer, record:
- What we assumed
- What's actually true (with source)
- Whether this confirms, modifies, or kills the hypothesis

### Step 15/18 -- Assess whether lower-level questions are still relevant

After Level 0-1 answers come back:
- If confirmed -> proceed to Level 2-3 questions
- If partially wrong -> reframe the thesis, then write new Level 2-3 questions
- If fundamentally wrong -> stop. The thesis needs restructuring before more research.

---

## Stage 7: Rewrite the synthesis

### Step 16/18 -- Rewrite synthesis from scratch

**Invoke the `/storyline-synthesis` skill** to produce the synthesis document. Don't duplicate its rules here -- just call it.

Key principle: after each research cycle, REWRITE the synthesis from scratch. Don't patch. The document should read cleanly as if it were always the answer.

### Step 17/18 -- Check for new questions

This is not a one-time loop. A good analysis goes through 2-3 cycles:
1. Research comes back (via `/deep-research`)
2. Update facts, kill bad hypotheses, strengthen good ones
3. Identify new questions raised by the research
4. Rewrite synthesis (via `/storyline-synthesis`)
5. If new questions exist, go back to Step 13/18

### Step 18/18 -- Final quality check and output

Verify all output files are complete and consistent:
- `BRAINSTORM.md` -- raw brainstorm, continuously updated
- `SCORING.md` or `USE_CASES.md` -- scored use cases with framework
- `MARKET-SYNTHESIS.md` -- the pyramid/storyline document (latest version is the clean one)
- `DEEP_RESEARCH_REQUEST.md` -- specific questions for validation
- `DEEP_RESEARCH_RESULTS.md` -- findings with sources

**Synthesis documents must include:**
- Version number and timestamp at the top (e.g., "v2.1 -- March 20, 2026")
- An appendix with sourced data points (claim, source URL, date, caveats)

---

## How to use this in practice

1. **Ask clarifying questions** before brainstorming. What's the capability? What's been tested? What are the constraints?
2. **Brainstorm broadly first**, then build the framework, then score. Don't skip to scoring.
3. **Look for non-obvious patterns** in the scores. The best opportunities are often in clusters, not individual use cases.
4. **Synthesize early and often.** Don't wait until all analysis is done. Write a "Day 1" storyline after the first scoring pass. Refine it.
5. **Always ask: "What would have to be true?"** For every recommendation, identify the assumptions. Then test them.
6. **Keep a working document** that evolves. The brainstorm doc, scoring sheets, and synthesis should all live in one place and cross-reference each other.

## Anti-patterns to avoid

- **Boiling the ocean:** Researching 50 things at equal depth instead of prioritizing the 5 that matter
- **Analysis paralysis:** Scoring and re-scoring without synthesizing into a recommendation
- **Confirmation bias:** Only researching evidence that supports the hypothesis you like
- **Missing the "so what":** Producing analysis without a clear action recommendation
- **Skipping problem definition:** Jumping into brainstorming without agreeing on what you're trying to figure out
- **Beautiful frameworks, no data:** Scoring criteria are only useful if populated with real numbers
- **Ignoring user corrections:** When the user pushes back on a finding or reframes, that's signal. Update the framework, don't defend the old one.

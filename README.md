# Strategy Skills for Claude Code

Three interconnected skills that turn Claude Code into a structured strategy consultant. Built on McKinsey problem-solving methods, adapted for AI-assisted analysis.

## The Skills

### `/opportunity-analysis` (18 steps)
Structured opportunity evaluation from brainstorm to recommendation. Takes a technology or capability and runs it through: problem definition, divergent brainstorm, MECE scoring framework, market sizing, synthesis, assumption validation, and iterative refinement.

### `/deep-research` (8 steps)
Focused research to validate assumptions and check facts. Orders questions by how fundamental they are (if a core assumption is wrong, don't waste time on details). Works with any research tool available in your environment (Perplexity, web search, etc.).

### `/storyline-synthesis` (10 steps)
Turns messy analysis into a clean, McKinsey-style synthesis document. Pyramid structure, action-sentence headers, sourced data points, and six quality tests before publishing.

## How they work together

```
/opportunity-analysis
    |
    |-- Stage 5: Synthesize --> calls /storyline-synthesis
    |-- Stage 6: Validate   --> calls /deep-research
    |-- Stage 7: Rewrite    --> calls /storyline-synthesis again
    |
    (loops 2-3 times until assumptions are validated)
```

You can also use each skill independently:
- `/deep-research` for any fact-checking or assumption validation
- `/storyline-synthesis` for writing up any body of research into a clean doc
- `/opportunity-analysis` for the full end-to-end process

## Step numbering

All three skills use explicit step numbering (`Step 3/18`, `Step 4a/8`, etc.) so Claude:
- Knows how many steps remain and doesn't skip ahead
- Reports progress clearly
- Handles sub-steps without losing track of the parent step

## Install

### Claude Code (global)
```bash
# Install all three
claude skills add sarbak/strategy-skills@opportunity-analysis -g
claude skills add sarbak/strategy-skills@deep-research -g
claude skills add sarbak/strategy-skills@storyline-synthesis -g
```

### Manual
Copy the `SKILL.md` file from any skill folder into `~/.claude/skills/<skill-name>/SKILL.md`.

## Output files

When running a full `/opportunity-analysis`, these files are created in your project:

| File | Purpose |
|------|---------|
| `BRAINSTORM.md` | Raw brainstorm (30-50+ ideas) |
| `SCORING.md` | Scored use cases with framework |
| `MARKET-SYNTHESIS.md` | The final storyline document |
| `DEEP_RESEARCH_REQUEST.md` | Questions for validation |
| `DEEP_RESEARCH_RESULTS.md` | Findings with sources |

## Design principles

- **Step-by-step execution** -- explicit numbered steps prevent the AI from compressing or skipping work
- **MECE everywhere** -- mutually exclusive, collectively exhaustive frameworks for scoring and structuring
- **Data over opinions** -- every claim needs a number or source
- **Top-down research** -- validate fundamental assumptions before details
- **Iterative refinement** -- synthesize-validate-rewrite cycles, not one-shot analysis
- **Action sentences** -- section headers that tell the story, not topic labels

## License

MIT

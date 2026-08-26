# Per-meeting extraction prompt

For running over a backlog. One meeting per call. Returns JSON only. Fill
`{{PROFILE}}` from the settings block at the top of the skill before sending it.

---

You are reading the summary of a business call that {{PROFILE}} had.

`{{PROFILE}}` is one or two sentences: what the person does, what they sell, who
they sell it to, and the unusual parts of their path. For example: "the co-founder
of a company selling an autonomous growth agent to early-stage startups, formerly
a management consultant, based in San Francisco."

Find at most one insight that could become a LinkedIn post.

An insight qualifies only if a smart person working in the same field would not
already believe it. A true statement everyone already agrees with does not
qualify. If nothing qualifies, say so. Most meetings contain nothing postable and
that is the expected outcome.

Score 0-3 on each:

- specific: does it carry a number with a denominator, a price, or a named mechanism
- contested: would a competent person push back
- earned: does this come from being in the room rather than from reading

Then answer the confidentiality checks:

- would the other person recognise themselves
- is it commercially sensitive to them (pricing, runway, headcount, churn, a
  pending round, a customer name)
- is it embarrassing to them
- could a reader match it to them from context

Return:

```json
{
  "meeting_id": 0,
  "has_insight": false,
  "claim": "<one sentence, the thing itself>",
  "evidence": "<the number or quote from the summary that supports it>",
  "shape": "contradicts-dashboard | honest-complaint | pattern-across-calls | was-wrong | mechanism",
  "scores": {"specific": 0, "contested": 0, "earned": 0},
  "confidentiality": {
    "recognisable": false, "commercial": false, "embarrassing": false,
    "matchable": false, "verdict": "clear | needs-permission | blocked",
    "note": "<what would have to change to clear it>"
  }
}
```

---
name: linkedin-from-meetings
description: >
  Turn meeting notes and call transcripts into scheduled LinkedIn drafts.
  Asks how far back to read and how many posts to produce, finds the user's
  meeting notes wherever they live, mines them for insights only that person
  could have, gates every candidate for confidentiality, shows the shortlist and
  asks for a yes or no on each one before drafting a word, drafts the approved
  ones in a voice extracted from the user's own past posts, and lays the result
  out as a schedule they can edit. Records every verdict in a decision log, so a
  later run never offers the same insight twice. Use when someone asks for
  LinkedIn posts from their meetings or calls, a weekly posting schedule,
  content from meeting notes, or "what should I post this week". Drafts only,
  never posts.
user_invocable: true
---

# LinkedIn Posts from Meeting Notes

Anyone taking three or more calls a day is sitting on things a stranger would pay
to know. This skill turns those calls into scheduled posts without inventing
anything and without burning the person on the other end of the call.

**Hard rule: this skill drafts. It never posts.** No browser automation into the
composer, no third-party scheduler, no API. The output is a file the user edits
and copies out.

**This process has 12 steps. Complete every step in order. Do not skip steps.
When reporting progress, label each step as shown (e.g., "Step 3/12").** Step 2
finds the raw material and Step 6 keeps a client out of a lawsuit; neither can be
skipped under any circumstance. Step 7 asks the user which candidates to draft,
and skipping it spends their review time on posts they never asked for.

---

## What the skill needs from the user

Collect these once and record them at the top of the output file so later runs
can read them back. Ask for anything missing during Step 1 or Step 2 rather than
guessing.

| Setting | What it is | Default |
|---|---|---|
| `PROFILE` | One or two lines: what the user does, what they sell, who they sell it to, and the parts of their path that are unusual (previous employers, where they live, what they are building). Used by the extraction prompt and by the lived-experience test. | must be supplied |
| `NOTES_SOURCE` | Where meeting notes live. Resolved in Step 2. | must be resolved |
| `POST_HISTORY` | The user's LinkedIn profile or activity URL, plus the style file extracted from it. | resolved in Step 3 |
| `OUTPUT_DIR` | Where drafts are written. | `./linkedin-drafts/` |
| `DECISION_LOG` | Append-only record of which candidates the user approved, rejected, or deferred. Read at the start of Step 4, written at Step 7, closed out at Step 11. | `OUTPUT_DIR/decisions.jsonl` |
| `TASK_SINK` | Where the one follow-up task goes: a task file, an issue tracker, a note. | ask once, otherwise skip |

---

## Step 1/12 -- Ask the two scoping questions

Ask both in a single question round, before reading anything. Do not guess these.
The answers change how much work every later step does.

**Question 1, "Meeting depth": how far back should I read?**

| Option | Means |
|---|---|
| Last week (7 days) | Fastest. Enough for one post, thin for patterns across calls. |
| Last two weeks (14 days) | **Recommend this one.** Enough that a pattern across three calls is visible. |
| Last month (30 days) | Slower. Use when the user wants a backlog rather than a week. |
| Everything since the last run | Read the newest file in `OUTPUT_DIR` and start from its date. |

**Question 2, "How many": how many posts do you want?**

| Option | Means |
|---|---|
| A few top posts (2-3) | Only insights scoring 8+. Publishable as-is. |
| A reasonable amount (4-6) | **Recommend this one.** A week plus a spare, scoring 6+. |
| Extensive (10-15) | Everything scoring 5+, drafted to full length. A content bank, not a week. |

Then proceed without another round of questions.

---

## Step 2/12 -- Find where the meeting notes live

Ask the user where their notes are and resolve `NOTES_SOURCE` before reading
anything. Do not assume a tool. The recipes below cover the common cases.

**2.1 Ask for the summary, not the transcript.** Where a tool produces both, read
the summary. A raw transcript costs roughly ten times the tokens for the same
insight, and it arrives unattributed and full of scheduling small talk. The
summary is already structured, already says who said what, and already dropped
the part where everyone waited for the last person to join. Only fall back to a
raw transcript when no summary exists.

**2.2 Recipes by source.**

| Source | Recipe |
|---|---|
| A local folder of markdown or text files | Glob the folder, filter by filename date or mtime against the window start. This is the simplest case and the one to steer users toward. |
| Obsidian | Same as above, against the meetings folder. Note that a vault often holds *prep* notes written before a call as well as notes from the call. Read only the second kind. |
| Granola | Check for a connected Granola MCP server first. Otherwise ask the user to export the window, or point at the local cache folder if they sync notes to disk. |
| Fathom | Has a public API and an MCP server. If neither is connected, ask for a CSV or markdown export of the window. |
| Fireflies | GraphQL API, needs an API key from the user's settings. Query transcripts by date and pull the summary fields, not `sentences`. |
| Otter | Export from the web app, or use the API if the user has access. Otter's default output is a raw transcript, so ask whether an "Outline" or summary is available. |
| Notion | Use the Notion MCP server if connected: search the meeting-notes database with a date filter and read each page's summary blocks. |
| Google Docs or Drive | Search the meeting-notes folder by modified date through a Drive integration, then read each doc. Gemini-generated "Meeting notes" docs already carry a summary section. |
| A database table | One query with a date filter that selects the summary column and skips the transcript column. Ask the user for the connection string or the REST endpoint plus key; never hardcode credentials into the skill. |
| Raw calendar-linked recordings (Zoom, Meet, Teams) | The heaviest case. Ask whether the platform's own AI summary exists before transcribing anything. If only audio exists, say plainly that this run will be slow and ask whether to continue. |

**2.3 Write one file per meeting** into a scratch folder, named `<date>-<id>.md`,
with the title, the other person's name or role, the date, and the summary text.
Everything downstream reads these files, so the rest of the skill does not care
which tool the notes came from.

**2.4 Triage before reading anything in full:**

```bash
grep -nE '[0-9]+%|\$[0-9]|[0-9]+x |ARR|MRR|churn|conversion|CAC|deliverability|response rate|surpris|turns out|actually|counterintuit' scratch/*.md
```

**2.5 Read in full** only the meetings the grep flagged, plus any whose title
suggests a strategy conversation rather than a routine sales call.

---

## Step 3/12 -- Extract the user's voice from their own posts

This is the step that decides whether the output sounds like the user or like a
LinkedIn ghostwriter. Run it in full on the first run. On later runs, read the
file it produced and refresh it once the user has published ten more posts.

`reference/example-extracted-style.md` is a finished example of what this step
produces. Read it for the shape, not for the voice.

**3.1 Check for an existing file.** If `reference/<user>-post-style.md` exists and
covers most of the user's recent posts, read it and skip to Step 4.

**3.2 Collect the past posts.** Aim for ten to twenty covering at least a year.
Three ways, in order of preference:

- **Browser automation.** Open `linkedin.com/in/<handle>/recent-activity/all/`
  while the user is logged in and read the page. Impressions are visible to the
  author on their own posts, which is why this beats scraping.
- **Data export.** LinkedIn Settings, Data privacy, Get a copy of your data,
  Posts. Returns a CSV. It carries the text but not the impressions, so pair it
  with a quick pass over the profile for the numbers.
- **Paste.** Ask the user to paste their last ten posts with the counts. Slowest
  for them, but it always works.

**3.3 Build the performance table.** One row per post: a short label, age,
impressions, reactions, comments. Then sort it twice, once by impressions and
once by comments, and say out loud whether the two orders disagree. They usually
do, and that disagreement is the most useful thing on the page: impressions and
comments reward different shapes of post. Personal news tends to win impressions.
An honest professional complaint tends to win conversation. Write one sentence
naming which shape actually generated conversation for this specific person, and
one naming the register that produced zero comments.

**3.4 Extract the narrative architecture.** Read the posts as structures, not as
sentences. Answer four questions with quoted examples:

- What move opens their posts? A flat situation report, a statistic, a
  provocation, a story, a credential?
- How do they handle the turn? Do they quote a consensus and take it apart, or
  just assert their side? Does the contrast sit inside a sentence or get broken
  onto its own line for drama?
- Do they widen out to a bigger claim, and how often per post?
- How do they close? A question, an admission, a call to action, or nothing?

**3.5 Extract the sentence habits.** Also with quoted examples:

- Declarative sentences or fragments. Do they use a colon as a drumroll?
- Person and address. First, second, or third. Do they write to one reader?
- Paragraph length. Real paragraphs, or the one-line-per-paragraph staircase?
- List style, and how long the items run.
- Do casual asides survive into the final text, or does the user sand them off?
- Do they concede, or do they write from a position of having figured it out?
- Emoji, hashtags, em dashes: present, absent, or only on old posts?

**3.6 Read the user's own feed once.** Open the feed sorted by Top and tabulate
about twenty organic posts: author, their seat, the shape of the post, length,
reactions, comments. Note which shapes drew the most comments, whether
announcements needed a big number behind them, how listicles and hashtag-heavy
posts did, and what nobody in that feed is doing. A feed read is a better guide to
what this particular audience sees than any published study, and it is worth
redoing every few months. Keep the table in the style file.

**3.7 Name the gap.** What does this person know that never appears in their
writing? Most operators produce striking numbers every week and have never put
one on their profile. Write the gap down as an instruction, because closing it is
usually the single change that most improves their posts.

**3.8 Write `reference/<user>-post-style.md`** with five sections: what actually
performed, how they build a narrative, how they build sentences, the gap, and a
short "rules for drafting in this voice" list. Read this file at the start of
every later run.

---

## Step 4/12 -- Extract candidate insights

**4.0 Filter against the decision log first**, before scoring anything. The log is
run by `decisions.py` in this skill directory. Build the raw candidate list as
JSON, one object per candidate with a `claim` string and a `sources` array, then:

```bash
S=<skill-dir>/decisions.py
python3 $S --path "$DECISION_LOG" init          # no-op if it already exists
python3 $S --path "$DECISION_LOG" filter --in candidates.json > filtered.json
```

`filtered.json` has two keys. `candidates` are still live, each with a stable
`key` filled in, and anything previously deferred tagged `previously_deferred`
with the note that held it. `dropped` are already rejected or already drafted,
each with the reason. Score only the survivors, and report the dropped list in the
run summary rather than discarding it quietly.

**4.1 Score each candidate 0-3 on three axes.**

| Axis | What earns a 3 |
|---|---|
| **Specific** | A number with a denominator, a price, a named mechanism. "2% response rate on cold email, 15% for event invites" is a 3. "Outreach is hard right now" is a 0. |
| **Contested** | Someone competent would push back. A post nobody can disagree with is a post nobody comments on. |
| **Earned** | The user knows it because they were in the room, not because they read it. This is the only durable advantage they have over every other account in their category. |

**4.2 Apply the volume threshold** from Step 1: 8+ for "a few", 6+ for
"reasonable", 5+ for "extensive".

**4.3 Tag each surviving candidate with its shape.** Ranked by how well they
travel:

1. **The number that contradicts the dashboard.** Someone's analytics say one
   thing and their customers say another.
2. **The honest complaint.** A field the user works in is disappointing them and
   they say so, then ask whether anyone has solved it. In the worked example this
   shape drew four times the comments of any announcement. Check the table from
   Step 3 before trusting the ranking for a given person.
3. **The pattern across calls.** "Four founders this month told me X." Nobody else
   can scrape it.
4. **The thing they were wrong about**, with what changed their mind.
5. **The mechanism.** How something works underneath, specific enough that a
   practitioner could go and do it.

**4.4 Reject:** milestone announcements without a large number behind them,
"excited to share", event recaps, and anything whose payload is that the user had
a good meeting.

---

## Step 5/12 -- Apply the lived-experience test

Every candidate survives all five or it goes back.

**5.1 Lived experience, not position-taking.** The post is about something that
happened. "A founder told me X on Tuesday" beats "here is how I think about X".

**5.2 Document the result, including the small and the ugly.** A 2% response rate
is a post. A pricing experiment that failed is a post. Waiting for a clean win
means never posting.

**5.3 Show the end state.** Carry the outcome, not just the method. For anyone
selling work to other companies, that means the client's number or the artifact
that shipped, never the user's own follower count. Their vanity metrics are the
wrong proof and read badly from an operator seat.

**5.4 Teach from what they actually did.** If the post says "test your visibility
in AI answers", it says which prompts, which tool, and what came back.

**5.5 The journey is uncopyable.** Use the unusual parts of `PROFILE`: where they
worked before, where they live, what they are building, what they gave up to do
it. This is the part a competitor cannot research their way into.

**5.6 The test: could anyone else have written this post?** If yes it is research,
not content. Throw it out and go back to the meetings.

---

## Step 6/12 -- Run the confidentiality gate

Every candidate passes all four checks. If any check is uncertain, the answer is
no.

**6.1 Would this person recognise themselves?** If yes, either name them with
permission or change enough that they cannot. Changing the industry is usually
enough. Changing only the country is not.

**6.2 Does it reveal something told in a sales context?** Pricing, runway,
headcount, churn, a pending round, a customer name. All out unless already public.
A founder's "we run out of money in November" never leaves the room. Their "90% of
our leads came from ChatGPT" is a marketing result they are proud of and would
likely say themselves.

**6.3 Is it embarrassing to them?** A failure shared candidly is not content, even
anonymised. A result they are proud of is.

**6.4 Does it read as a subtweet?** If a reader could match it to a person from
context, it fails 6.1.

**6.5 Aggregation clears most of this.** "Three founders this month" carries the
insight and identifies nobody. Below three sources an anonymised story still
points at one person, so use it only with explicit permission or when the detail
is genuinely generic.

**6.6 The permission path is short.** For anything worth naming, draft the post,
send the person the exact text, and ask "mind if I post this with your name?" Most
say yes and reshare, which beats the anonymised version. Add the ask to
`TASK_SINK`. Do not send it from this skill.

**6.7 Calls in another language.** The insight translates, the quote does not.
Never render a translated line as a quotation.

**6.8 Record a verdict** for each candidate: `clear`, `needs-permission`, or
`blocked`, with the reason.

---

## Step 7/12 -- Show the candidates and get a verdict on each

Nothing gets drafted until the user has said yes to it. Drafting five posts they
did not want spends their review time on the wrong thing, and the question costs
little to ask here and a lot to unwind later.

**7.1 Present the shortlist.** Show every candidate that survived Steps 4 through
6 as a compact list. Per candidate: a short label, the claim in two or three
sentences, and one line of metadata. Nothing else:

```
1. THE ATTRIBUTION NUMBER
   Analytics say 5% of signups come from AI. Asked directly, 55% of users name
   ChatGPT. People search the brand rather than clicking through, so the search
   engine takes the referrer.
   sources 2026-08-14-206, 2026-08-12-210, 2026-08-07-192
   shape: contradicts-dashboard | score 9 | clear
```

No draft text yet. The user is judging the insight, not the writing.

**7.2 Run the survey.** Use `AskUserQuestion`. It takes at most four questions per
call, so present the candidates in batches of four, highest score first. One
question per candidate, headed with a short label for that candidate. The question
text is the candidate's one-line claim.

Options, in this order:

| Option | Means |
|---|---|
| **Looks good** | Draft it. |
| **Not this one** | Do not draft it, and do not offer it again. |
| **Later** | Keep it in the backlog and offer it again on a future run. |

The tool adds "Other" itself, which is where the user says what they actually want
changed. Treat any "Other" text as a drafting instruction for that candidate and
record it.

Do not ask a fifth question about whether to proceed. Once the batch is answered,
draft the approved ones.

**7.3 Write every verdict to the decision log.** Append one row per verdict:

```bash
python3 $S --path "$DECISION_LOG" record \
  --claim "Analytics say 5% from AI, users say 55%" \
  --sources 2026-08-20-rob,2026-08-21-ryan \
  --shape contradicts-dashboard --score 9 --verdict approved --note ""
```

`--verdict` is `approved`, `rejected` or `deferred`. `--note` carries the user's
"Other" text verbatim, or the reason a candidate is being held. The key derives
from the claim, so it does not need passing. `record` refuses a key already in the
log, which is what stops a re-run duplicating rows.

The log is append-only JSONL. One row:

```json
{"key":"attribution-5-vs-55","claim":"Analytics attribute 5% of signups to AI, users asked directly say 55% ChatGPT","sources":["2026-08-20-rob","2026-08-21-ryan"],"shape":"contradicts-dashboard","score":9,"verdict":"approved","note":"","decided":"2026-08-26","drafted":"2026-08-26-week.md"}
```

`drafted` stays empty until Step 11 fills it in, and stays empty forever on
anything the user declined.

**7.4 What the filter decides.** Step 4.0 does the work. This is what it does, so
you can sanity-check it.

- **`rejected`**: dropped. Not presented, not mentioned, not put in the backlog.
- **`approved` with a `drafted` value**: already written, so dropped.
- **`deferred`**: kept and tagged, so the shortlist can say the user has seen it
  and why it was held.
- **Near matches**: a candidate counts as the same insight when it shares a source
  with a logged row **and** at least 40% of the shorter claim's content words.
  Both conditions have to hold. Overlap alone would merge two people saying
  similar things in different calls, and a shared source alone would merge every
  insight that came out of one meeting. Numbers count as content words, because
  "5" against "55" is often the whole fingerprint of an insight.

To check one candidate by hand:

```bash
python3 $S --path "$DECISION_LOG" check --claim "..." --sources 2026-08-20-rob
```

It prints `new`, `rejected`, `deferred` or `drafted` with the reason it matched.
Exit code is 0 for new and 1 for anything already settled, so it drops into a
shell condition.

**7.5 Learn from the rejections.** Every few runs:

```bash
python3 $S --path "$DECISION_LOG" patterns
```

It prints every rejection with its note, then any term appearing in three or more
of them. A repeated term is a candidate for a standing rule: three rejections that
all turn out to be client pricing means client pricing should be filtered at
Step 4 rather than offered and declined again.

When a pattern is clear, write it into `reference/<user>-post-style.md` under a
**Standing rejections** heading, with the dates that produced it. That file is
read on every run, so the rule then applies without anyone having to remember it.

Never infer a rule from one rejection, and `patterns` will not suggest one. A
single no is a judgment about a single candidate.

---

## Step 8/12 -- Draft in the user's voice

**8.1 Read `reference/<user>-post-style.md` before writing a word.** It carries
the narrative architecture and sentence habits from Step 3, with quoted examples.
That file is the primary instrument. Generic writing guidance is the cleanup pass,
not the source.

**8.2 Build each post on the architecture the style file recorded.** Where Step 3
found too little to work from, this five-move default is a reasonable start:

1. **Open on the thesis.** One sentence carrying the claim the whole post exists
   to make. Flat delivery, no hook engineering, but the point goes first rather
   than being built towards. It has to make sense to someone who has just scrolled
   past something unrelated, so it names the domain, the actor and the stake
   without leaning on anything below it. Keep it under about 140 characters, which
   is where mobile truncates.
2. Then the situation the user is personally in, and the friction in it.
3. Report what everyone else believes, then disagree with it. **Put the evidence
   here.** This is where the meetings pay off, and it is where most people's own
   posts are thinnest.
4. Widen once, briefly, usually on a parallel. Once per post, never twice.
5. Close on a real question, or on an admission that they do not know.

**8.3 Match the sentence habits from the style file.** Where the file is silent,
these defaults hold up on LinkedIn:

- Flat and declarative. No fragments, no colon as a drumroll.
- The turn lives inside the sentence ("but", "however", "instead of X, we did Y"),
  not broken onto its own line for drama.
- Second person. Write to one reader.
- Real paragraphs of two to four sentences, not the one-line-per-paragraph
  staircase.
- Keep the casual asides the user actually uses. Do not sand them off.
- Concede readily. Never sound resolved.
- No emoji, no hashtags, no em dashes.

**8.4 Apply the two sentence-shape rules by hand.** These catch machine-written
prose faster than vocabulary does.

- **Keep the verb next to what it acts on.** English default is `[verb] [direct
  object] to [indirect object]`. The double-object form only reads naturally when
  the recipient is a person or something concrete ("send him the letter"). Put two
  abstractions in those slots and the reader holds the first noun in suspense
  while waiting to find out what it received. "Give the prune logic real
  attention" becomes "give real attention to the pruning logic".
- **Unwind nominalized verbs.** A verb turned into a bare noun makes the reader
  re-parse the sentence to work out who is doing what. "The prune logic" becomes
  "pruning logic". "The location count" becomes "how many locations they run".
  "Delivery is by an agent" becomes "an agent delivers it".

**8.5 Strip the AI-slop vocabulary.** Load-bearing, delve, crucial, robust,
leverage, and their kin. Also: "here's the thing", any three-item flourish where
two items would do, and any sentence that exists to announce what the next
sentence will say.

**8.6 Optionally run a de-slopping pass.** The public `unslop` skill does this
well if it is installed. It is a cleanup pass on a finished draft, never a first
pass.

**8.7 Apply the platform format rules.** Details and confidence levels in
`reference/format-research.md`.

- **Hook: first two lines.** Truncation lands around 200-210 characters on
  desktop, closer to 140 on mobile. Everything above "see more" has to stand alone.
- **Length 800-1,400 characters.** Completion now counts as much as dwell time, so
  a 2,000-character post most people abandon does worse than a 600-character post
  they finish.
- **No link in the body.** External links suppress reach. Put it in the first
  comment and say "linked in the comments".
- **One idea per post.** Not three lessons, not a numbered takeaway list.
- **A real question at the end**, one the user actually wants answered and a
  reader can answer from experience. "Thoughts?" is not a question. The first 90
  minutes decide reach and comments are the strongest signal in that window, so
  this is the highest-value line in the post.

**8.8 Final check.** Read the first two lines out loud. If they sound like
something the user would say to someone across a table, keep them. If they sound
like a headline, rewrite.

---

## Step 9/12 -- The restraint pass

Run this on every draft Step 8 produced. It is a subtraction pass. Nothing gets
added here. A voice draft usually runs about 30% longer than it needs to and
warmer than the writer actually is. Because this step cuts that much text,
re-check the length and hook rules in 8.7 against the shortened version when you
are done.

**9.1 Cut sentences that introduce an emotion or announce what is coming.** They
carry no information and they make the writer sound like they are performing. Say
the thing rather than framing the thing.

| Cut | Why |
|---|---|
| "The reason is boring." | Announces a tone. Just give the reason. |
| "Here is what we do." | Announces a paragraph that follows anyway. |
| "I have a result from our own tests that I do not believe yet, and I would rather say that out loud than sit on it." | Two clauses of throat-clearing before the result. Open on the result. |

**9.2 Remove confident declaratives about what other people do or do not do.** The
test: does the sentence claim knowledge of a population the writer has not
measured? If yes, narrow it to what they actually saw, or cut it.

| Overconfident | Humble and true |
|---|---|
| "The check nobody seems to run is the obvious one" | "I have not seen anyone look at what the agents in their own category are asking." |
| "it is expensive enough that hardly anyone wants to run it" | "it costs enough that we have not managed to run it properly ourselves yet." |

Also cut "almost nobody", "everyone is still", "most of the market", and any
sentence that tells readers what their own industry believes.

**9.3 Merge or cut until the draft is about 30% shorter.** Two sentences carrying
one idea become one sentence. A paragraph restating the paragraph above it goes.
Keep the numbers and the mechanism. Those are what the post is for.

**9.4 Rewrite the closing question so a stranger can answer it.** The question
should be one the writer genuinely does not know the answer to, open rather than
yes or no, and general enough that people outside their exact niche want to weigh
in. Answering it should make a reader look knowledgeable rather than merely
responsive.

| Too narrow | Better |
|---|---|
| "Which side is your category on?" | "Does anyone know how to seed a brand into an LLM's training data, as opposed to just its retrieval?" |
| "Has anyone run that comparison on their own product?" | "How is anyone measuring where their customers actually first heard about them?" |

**9.5 Read the result for tone.** Calm, humble, curious, friendly. The post asks
rather than tells. If any sentence would sound smug read aloud, it goes.

---

## Step 10/12 -- Schedule

**10.1 Day.** Tuesday to Thursday. Every study agrees these beat Monday and
weekends, and Wednesday is the most consistent.

**10.2 Time.** Pick one window that catches the working hours of the largest slice
of the user's audience, and say which slice it is. For an audience split across
continents, a morning slot in the user's own timezone often catches the evening in
another. The published studies disagree outright about time of day, so do not
over-fit: hold one window for six weeks, then read the user's own analytics.

**10.3 Cadence by volume.**

- 2-3 posts: one week, Tue / Wed / Thu.
- 4-6 posts: two weeks, three per week.
- 10-15 posts: a bank. Schedule the first three, list the rest as undated stock
  ranked by score.

**10.4 Mix by shape.** If two candidates share a shape, push one to the following
week. A feed of one shape reads as a formula.

**10.5 Three a week is the ceiling worth recommending.** Five a week is a cadence
most people drop, and a dropped cadence reads worse than a steady low one. If the
user currently posts monthly, weekly is already a large change.

---

## Step 11/12 -- Write out

**11.1 Write to `OUTPUT_DIR/<YYYY-MM-DD>-week.md`** (default `./linkedin-drafts/`).

**11.2 Per post, include:** day and time, the source meeting id and date so the
claim traces back, the shape, the confidentiality verdict, the full draft text,
the first comment if there is a link, and the character count.

**11.3 Add a Backlog section** for candidates that scored but did not ship, each
with the reason it was held.

**11.4 Record the settings** at the top of the file so the next run can read
`PROFILE`, `NOTES_SOURCE`, and the window back.

**11.5 Close the loop** for every candidate that made it into the file, so the
next run does not offer it again:

```bash
python3 $S --path "$DECISION_LOG" mark-drafted --key attribution-5-vs-55 --file 2026-08-26-week.md
```

---

## Step 12/12 -- Hand off

**12.1 Give the user one way to edit and one way to hand the file to whoever else
posts.** Pick whichever fits their setup:

- The markdown file on its own, if they work locally.
- A shared doc (Google Docs, Notion) if someone else does the posting.
- A share link from a markdown-sharing tool, which is the best option for editing
  on a phone. Create a fresh link each run rather than updating one the user may
  already have open.
- A pull request, if the drafts live in a repo alongside other content.

**12.2 Add one line to `TASK_SINK`:** `Post LinkedIn draft 1 (Tue 8am) --
<path>`. One task, not three. The file holds the rest.

**12.3 Report back** with the count, the shapes used, and anything blocked on
permission.

---

## What this skill does not do

- Does not post, schedule to a third-party tool, or touch the composer.
- Does not write about a client by name without confirmed permission.
- Does not invent a statistic. Every number traces to a meeting id.
- Does not produce five posts a week because five is a rounder number.
- Does not read a raw transcript when a summary exists.
- Does not draft a candidate the user has not approved.

## Reference files

- `decisions.py` -- the decision-log tool. `init`, `slug`, `check`, `filter`,
  `record`, `mark-drafted`, `patterns`, `list`, `stats`. Run `--help` for the
  full schema.
- `OUTPUT_DIR/decisions.jsonl` -- the decision log. Read at Step 4, written at
  Step 7, closed out at Step 11. It sits with the drafts rather than in the skill
  directory, because it is data rather than instruction.
- `reference/example-extracted-style.md` -- a finished style extraction, kept as a
  worked example of Step 3 output. Read it for structure, not for voice.
- `reference/format-research.md` -- LinkedIn format research with confidence
  levels marked per claim.
- `reference/extraction-prompt.md` -- a per-meeting extraction prompt returning
  JSON, for running over a large backlog one meeting at a time.

---
name: analytics-review
description: Pull PostHog funnel metrics and Supabase/Postgres usage data, compare against previous baselines, and surface actionable insights. Use when the user asks to check analytics, review funnel, compare metrics, or see how users are doing.
user_invocable: true
---

# Analytics Review

Pull live data from PostHog and the project's database, compare against saved baselines in memory, and surface actionable insights.

## Arguments

- No arguments: full review (PostHog funnel + database usage + comparison)
- `funnel`: PostHog funnel metrics only
- `usage`: Database message/usage volume only
- `users`: Per-user activity breakdown
- `save`: Save current snapshot as a new baseline to memory

## Step 1/8: Find credentials

Look for credentials in this order:

### PostHog
1. Check environment: `env | grep POSTHOG`
2. Check project `.envrc` files
3. Check memory files for PostHog project ID and API key
4. The PostHog API key starts with `phx_` (personal API key, not the project key `phc_`)

**PostHog API base**: `https://us.i.posthog.com` (US) or `https://eu.i.posthog.com` (EU)

### Database
1. Check `server/.env` or `.env.local` for `DATABASE_DSN`, `DATABASE_URL`, `POSTGRES_URL`, or `SUPABASE_URL`
2. For Supabase projects, the DSN format is: `postgresql://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres`
3. Use the project's Python environment (`uv run python3`) with `asyncpg` to query

If credentials are missing, ask the user.

## Step 2/8: Read event architecture

Check the project's PostHog events doc (usually `POSTHOG_EVENTS.md`) or memory for the event architecture. This tells you which events exist, what properties they carry, and what funnels they power.

## Step 3/8: Pull PostHog data

Use the HogQL query endpoint (legacy insight endpoints may be blocked):

```bash
curl -s 'https://us.i.posthog.com/api/projects/<PROJECT_ID>/query/' \
  -H "Authorization: Bearer <POSTHOG_API_KEY>" \
  -H 'Content-Type: application/json' \
  -d '{"query": {"kind": "HogQLQuery", "query": "<HOGQL>"}}'
```

### Queries to run

**1. Event counts by period** — Compare current period vs previous baseline:
```sql
SELECT event, count() as cnt, count(DISTINCT person_id) as users,
  multiIf(
    toDate(timestamp) < toDate('SPLIT_DATE_1'), 'period_1',
    toDate(timestamp) < toDate('SPLIT_DATE_2'), 'period_2',
    'period_3'
  ) as period
FROM events
WHERE timestamp >= toDateTime('START_DATE')
  AND event IN ('$pageview', 'cta_click', ... )
GROUP BY event, period
ORDER BY event, period
```

**2. Pageview breakdown by path**:
```sql
SELECT properties.$pathname as path, count() as cnt, count(DISTINCT person_id) as users
FROM events
WHERE timestamp >= toDateTime('START_DATE') AND event = '$pageview'
GROUP BY path ORDER BY cnt DESC LIMIT 25
```

**3. All custom events** (to check what's firing):
```sql
SELECT event, count() as cnt
FROM events
WHERE timestamp >= toDateTime('START_DATE')
  AND event NOT IN ('$pageview', '$pageleave', '$autocapture', '$feature_flag_called', '$web_vitals', '$identify', '$rageclick')
GROUP BY event ORDER BY cnt DESC LIMIT 30
```

## Step 4/8: Pull database usage data

Query the project's database for:
- **Message/usage volume by period** (daily, weekly)
- **Per-user activity** (messages, actions, last active date)
- **New signups/subscriptions** in the current period
- **Active vs churned users**

Adapt queries to the project's schema. Common patterns:

```sql
-- Daily volume
SELECT DATE(created_at) as day, COUNT(*) as total, COUNT(DISTINCT user_id) as users
FROM <activity_table>
WHERE created_at >= '<START_DATE>'
GROUP BY DATE(created_at) ORDER BY day

-- Per-user breakdown
SELECT u.email, u.plan, u.status,
  COUNT(*) FILTER (WHERE a.created_at < '<SPLIT>') as before,
  COUNT(*) FILTER (WHERE a.created_at >= '<SPLIT>') as after,
  MAX(a.created_at) as last_active
FROM <users_table> u
JOIN <activity_table> a ON a.user_id = u.id
GROUP BY u.email, u.plan, u.status
ORDER BY after DESC
```

## Step 5/8: Pull recent PRs and deploys

Run `git log --oneline --since="<BASELINE_DATE>" --merges` (or without `--merges` if no merge commits) to see what shipped since the last baseline. For each PR/commit that touched user-facing code:

1. Note the merge date
2. Summarize what changed (from commit message or PR title)
3. Categorize: bug fix, new feature, SEO/content, UI change, pricing change, infrastructure

This becomes the "what changed" context for interpreting metric movements. Structure as:

```
### Changes since last baseline
| Date | PR/Commit | Category | Summary |
```

When comparing metrics, correlate timing: if a metric spiked on Mar 30 and PR #11 merged Mar 31, note the connection. Metric changes without a corresponding code change suggest external factors (marketing, organic growth, seasonality).

## Step 6/8: Compare against baseline

Check memory for previous analytics snapshots (files matching `*analytics*` or `*baseline*`). If a baseline exists:

1. Calculate daily rates for each metric in both periods
2. Show percentage change and absolute change
3. Flag metrics that moved significantly (>2x or <0.5x)
4. Flag users who went silent (active before, zero activity now)
5. Flag users who are ramping up (increasing activity)

If no baseline exists, this IS the baseline — note that in the output.

## Step 7/8: Surface insights

Always structure output as:

### Funnel Metrics (table)
- Period comparison with daily rates and trend multipliers

### Usage Analytics (table)
- Volume, active users, per-user breakdown

### PR Impact (table)
- Which PRs shipped since last baseline, what category, what metric moved

### Actionable Insights (numbered list)
Focus on:
1. **Conversion changes** — Did any funnel step improve or degrade?
2. **Activation signals** — Are new users actually using the product?
3. **Churn signals** — Who went silent? How long ago?
4. **Power users** — Who's approaching plan limits?
5. **New behavior** — Events firing for the first time?
6. **Anomalies** — Unexpected spikes, drops, or patterns?

### Recommendations (numbered list)
Specific actions the user can take based on the data.

## Step 8/8: Save baseline (if requested or if none exists)

If the user passes `save` argument, or if no baseline exists in memory:

1. Write a memory file (`<project>_analytics_<date>.md`) with:
   - Snapshot date
   - Changes since last baseline (PRs merged, deploys)
   - Key metrics (user count, daily volume, conversion rates)
   - Per-user status summary
   - Top-line comparison vs previous baseline
2. Update MEMORY.md index

Keep baselines concise — just the numbers needed for future comparison, not the full analysis.

## Notes

- Always calculate **daily rates** (events / days in period) for fair comparison across unequal periods
- PostHog `count(DISTINCT person_id)` gives unique users, `count()` gives total events
- For Supabase/Postgres: use `uv run python3` with `asyncpg` in the server directory
- Exclude internal/test accounts from user-facing metrics
- If the project has a `POSTHOG_EVENTS.md`, read it first to understand the event architecture

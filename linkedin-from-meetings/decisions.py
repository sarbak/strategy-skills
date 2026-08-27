#!/usr/bin/env python3
"""Decision log for the linkedin-from-meetings skill.

Append-only JSONL. One line per verdict on one candidate insight. Its whole job is
to stop the workflow asking about the same insight twice.

Path: $LINKEDIN_DECISIONS, else DECISION_LOG from the skill settings, whose
default is ./linkedin-drafts/decisions.jsonl

Row schema
    key       stable slug of the claim, built from its content words
    claim     one-line statement of the insight
    sources   list of source ids: whatever Step 2 named the meeting files
    shape     contradicts-dashboard | honest-complaint | pattern-across-calls |
              was-wrong | mechanism
    score     0-9, the specific+contested+earned total
    verdict   approved | rejected | deferred
    note      his "Other" text, or the reason it was held
    decided   YYYY-MM-DD
    drafted   output filename once written, empty otherwise

Commands
    init                                    create the log if missing
    slug   --claim C                        print the stable key for a claim
    check  --claim C [--sources 1,2]        exact + near match against the log
    filter [--in F]                         stdin/file JSON array -> filtered array
    record --claim C --verdict V [...]      append one verdict
    mark-drafted --key K --file F           close the loop after write-out
    patterns                                group rejection notes, for the learn step
    list   [--verdict V]                    print the log
    stats                                   counts by verdict
"""
import argparse, json, os, re, sys
from collections import Counter, defaultdict
from datetime import date

DEFAULT = os.path.expanduser(
    os.environ.get("LINKEDIN_DECISIONS",
                   "./linkedin-drafts/decisions.jsonl"))

STOP = set("""a an the and or but if then than that this these those of in on at to for from by
with without into over under is are was were be been being it its as we our you your they their
he she his her i me my not no do does did can could will would should may might must have has had
about more most some any all one two three when where which who whom what how why so such very
just only also even still yet already because while during after before against between through""".split())

VERDICTS = ("approved", "rejected", "deferred")


def words(text):
    """Content tokens. Numbers are kept and are short, so the length floor is 2:
    "5" against "55" is often the whole fingerprint of one of these insights."""
    return [w for w in re.findall(r"[a-z0-9]+", (text or "").lower())
            if w not in STOP and len(w) >= 2]


def slug(claim, n=4):
    """Stable key from the content words that carry the insight."""
    seen, out = set(), []
    for w in words(claim):
        if w in seen:
            continue
        seen.add(w)
        out.append(w)
        if len(out) == n:
            break
    return "-".join(out) or "unkeyed"


def containment(a, b):
    """Overlap against the shorter side. Jaccard is the wrong measure here: a
    reworded claim keeps the distinctive tokens and drops most of the rest, so a
    union-based score reads two phrasings of one insight as unrelated."""
    a, b = set(a), set(b)
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def load(path):
    if not os.path.exists(path):
        return []
    rows = []
    for i, line in enumerate(open(path), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"warning: {path}:{i} is not valid JSON, skipped ({e})",
                  file=sys.stderr)
    return rows


def append(path, row):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def rewrite(path, rows):
    """Only mark-drafted uses this. Writes via a temp file so a crash cannot
    truncate the log."""
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


NEAR = 0.40


def row_sources(r):
    """`sources` is the field name. Older rows used `meetings`; read both."""
    return set(map(str, r.get("sources") or r.get("meetings") or []))


def match(rows, claim, sources, key=None):
    """Return (row, why) for an exact or near match, else (None, None).

    A near match needs a shared source AND real content overlap. Both conditions
    matter: overlap alone would merge two teams saying similar things, and a
    shared source alone would merge every insight from the same call.
    """
    key = key or slug(claim)
    for r in rows:
        if r.get("key") == key:
            return r, "same key"
    cw = words(claim)
    src = set(map(str, sources or []))
    best, best_sim, best_shared = None, 0.0, None
    for r in rows:
        shared = src & row_sources(r)
        if not shared:
            continue
        sim = containment(cw, words(r.get("claim", "")))
        if sim > best_sim:
            best, best_sim, best_shared = r, sim, shared
    if best and best_sim >= NEAR:
        return best, (f"near match, {best_sim:.0%} of the shorter claim's words "
                      f"overlap, shares source {sorted(best_shared)[0]}")
    return None, None


def cmd_init(a):
    if os.path.exists(a.path):
        print(f"exists: {a.path} ({len(load(a.path))} rows)")
        return
    os.makedirs(os.path.dirname(a.path), exist_ok=True)
    open(a.path, "a").close()
    print(f"created: {a.path}")


def cmd_slug(a):
    print(slug(a.claim))


def cmd_check(a):
    rows = load(a.path)
    src = a.sources.split(",") if a.sources else []
    row, why = match(rows, a.claim, src, a.key)
    if not row:
        print(json.dumps({"status": "new", "key": a.key or slug(a.claim)}))
        return 0
    status = "drafted" if (row["verdict"] == "approved" and row.get("drafted")) \
        else row["verdict"]
    print(json.dumps({"status": status, "why": why, "row": row}))
    return 1


def cmd_filter(a):
    """Read a JSON array of candidates, drop what has already been settled.

    Each candidate needs `claim`; `sources` is used for near matching. Survivors
    come back with `key` filled in, and anything previously deferred is tagged so
    the shortlist can say so.
    """
    raw = open(a.infile).read() if a.infile else sys.stdin.read()
    cands = json.loads(raw)
    rows = load(a.path)
    kept, dropped = [], []
    for c in cands:
        c = dict(c)
        c["key"] = c.get("key") or slug(c.get("claim", ""))
        row, why = match(rows, c.get("claim", ""), c.get("sources", []), c["key"])
        if row and (row["verdict"] == "rejected" or row.get("drafted")):
            dropped.append({"key": c["key"], "claim": c.get("claim", "")[:70],
                            "reason": "rejected" if row["verdict"] == "rejected"
                                      else f"already drafted in {row['drafted']}",
                            "why": why})
            continue
        if row and row["verdict"] == "deferred":
            c["previously_deferred"] = True
            c["previous_note"] = row.get("note", "")
        kept.append(c)
    json.dump({"candidates": kept, "dropped": dropped}, sys.stdout, indent=2,
              ensure_ascii=False)
    print()


def cmd_record(a):
    if a.verdict not in VERDICTS:
        sys.exit(f"verdict must be one of {VERDICTS}")
    rows = load(a.path)
    key = a.key or slug(a.claim)
    if any(r.get("key") == key for r in rows):
        sys.exit(f"key already in the log: {key}. Use mark-drafted, or pick a new key.")
    row = {"key": key, "claim": a.claim,
           "sources": [s for s in (a.sources.split(",") if a.sources else []) if s],
           "shape": a.shape or "", "score": a.score if a.score is not None else 0,
           "verdict": a.verdict, "note": a.note or "",
           "decided": a.decided or date.today().isoformat(),
           "drafted": a.drafted or ""}
    append(a.path, row)
    print(json.dumps(row, ensure_ascii=False))


def cmd_mark_drafted(a):
    rows = load(a.path)
    hit = [r for r in rows if r.get("key") == a.key]
    if not hit:
        sys.exit(f"no row with key {a.key}")
    for r in hit:
        r["drafted"] = a.file
    rewrite(a.path, rows)
    print(json.dumps(hit[0], ensure_ascii=False))


def cmd_patterns(a):
    """Group the notes on rejected rows. A repeated reason is a candidate for a
    standing rule; a single one is just a judgment about one candidate."""
    rows = [r for r in load(a.path) if r.get("verdict") == "rejected" and r.get("note")]
    if not rows:
        print("no rejections with notes yet")
        return
    buckets = defaultdict(list)
    for r in rows:
        for w in set(words(r["note"])):
            buckets[w].append(r["key"])
    repeated = {w: ks for w, ks in buckets.items() if len(ks) >= 3}
    print(f"{len(rows)} rejections with notes\n")
    for r in rows:
        print(f"  {r['decided']}  {r['key']}\n      {r['note']}")
    if repeated:
        print("\nterms appearing in 3+ rejections, candidates for a standing rule:")
        for w, ks in sorted(repeated.items(), key=lambda x: -len(x[1])):
            print(f"  {w} ({len(ks)}): {', '.join(ks)}")
    else:
        print("\nno term repeats across 3+ rejections yet. Do not write a standing "
              "rule from fewer.")


def cmd_list(a):
    for r in load(a.path):
        if a.verdict and r.get("verdict") != a.verdict:
            continue
        mark = "*" if r.get("drafted") else " "
        print(f"{mark} {r.get('decided','')}  {r.get('verdict',''):9}  "
              f"{r.get('score',''):>2}  {r.get('key','')}\n      {r.get('claim','')[:88]}")


def cmd_stats(a):
    rows = load(a.path)
    c = Counter(r.get("verdict") for r in rows)
    print(f"{len(rows)} rows in {a.path}")
    for v in VERDICTS:
        print(f"  {v:9} {c.get(v,0)}")
    print(f"  drafted   {sum(1 for r in rows if r.get('drafted'))}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--path", default=DEFAULT)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init").set_defaults(fn=cmd_init)

    s = sub.add_parser("slug"); s.add_argument("--claim", required=True)
    s.set_defaults(fn=cmd_slug)

    s = sub.add_parser("check")
    s.add_argument("--claim", required=True)
    s.add_argument("--sources"); s.add_argument("--key")
    s.set_defaults(fn=cmd_check)

    s = sub.add_parser("filter"); s.add_argument("--in", dest="infile")
    s.set_defaults(fn=cmd_filter)

    s = sub.add_parser("record")
    s.add_argument("--claim", required=True)
    s.add_argument("--verdict", required=True)
    s.add_argument("--key"); s.add_argument("--sources"); s.add_argument("--shape")
    s.add_argument("--score", type=int); s.add_argument("--note")
    s.add_argument("--decided"); s.add_argument("--drafted")
    s.set_defaults(fn=cmd_record)

    s = sub.add_parser("mark-drafted")
    s.add_argument("--key", required=True); s.add_argument("--file", required=True)
    s.set_defaults(fn=cmd_mark_drafted)

    sub.add_parser("patterns").set_defaults(fn=cmd_patterns)

    s = sub.add_parser("list"); s.add_argument("--verdict")
    s.set_defaults(fn=cmd_list)

    sub.add_parser("stats").set_defaults(fn=cmd_stats)

    a = p.parse_args()
    a.path = os.path.expanduser(a.path)
    sys.exit(a.fn(a) or 0)


if __name__ == "__main__":
    main()

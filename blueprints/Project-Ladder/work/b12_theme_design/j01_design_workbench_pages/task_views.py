"""Each design Task view drawn from its method step and run card, as b15's task_views.py draws each labeling view from
its step slide (JL 261101: update the design theme the way the paper and labeling themes did). One method for every
view:

1. its run card (haipipe-design-workflow/references/run-cards.md) and the unit's step (haipipe-design-unit) are the
   frame: In → who works → Out, your part, next;
2. what the Run writes (ideas.yaml, chains.yaml, the verdict, ranking.csv, prediction.yaml) draws the Results;
3. COVER lists every part of the card and where it lands on the screen; check() fails when a place is missing, so a
   part cannot be dropped silently.

A design Job has three Task types (haipipe-design): 💡 t00 reason ideas (method step ②), ✏️ one Task per design
(③ conduct, ④ review item) and 🏆 t99 review whole (⑤). Its one loop is a design's drafts: generate → verify v1 →
revise → verify v2 … until it passes or is dropped; each design view shows that strip. No Task asks you: a person
signs only at the Block (goals, shared rules) and the Job (Review and approve, the close), so a Task's your-part line
is "none" or points at that sign; check() fails on any interaction here.

Each view: an optional strip, then ⚙️ Process (the step's flow and your part) and 📊 Results (its Out in detail), each
group numbered from 1, then next. Report shows the Results only. No design text is drawn: names are folder names, and
every content cell is a placeholder in angle brackets.
"""
import re

# a section: (title, kind, *args). kinds: big(words, state) · kv(rows, verbs) · tiles(items) · table(head, rows, verbs)
# · bars(caption, bars) · chain(steps, verb) · tabs(items, detail) · line(words) · picture(name, verbs)
# · rows(rows, foot) · strip(words) · agent(items) · callout(title, words, verb) · flow(in, who, out)
# · ask(words, verb, mode) · turns(label, turns)


def d_turns(now, *after):
    """✏️ a design's drafts as this view sees them: v1 failed its verify, v2 at this view's moment, then what follows."""
    return ("", "turns", "✏️ drafts of d01", [("v1", "verify failed"), ("v2", "passed", "now"), ("kept", "by t99")])


NONE = ("", "ask", "Your part: none here; an agent works, another agent checks", "", "none")

STEP = {
    # ── 💡 reason ideas · method step ② (t00_reason-ideas, run-reason-t00; its fence check, run-open-designs) ──────
    "A1": [("1 · 📥 Build the Job's fence", "flow", ("Inputs version i1", "rules · theory · the handoff", ""),
            ("🤖 Designer agent", "keep what step ① names", "run-setup-inputs-j01"),
            ("inputs/ + manifest.yaml", "every file the work may read", "")),
           NONE,
           ("2 · 📂 What the fence holds", "table", ("file", "from", "read by"),
            [("goal.md", "the goal list, G01", "every step"), ("method.md", "M01 m2, pinned", "every step"),
             ("rules.md", "inputs i1", "verify, T0")], ()),
           ("3 · 🚫 What stays out", "line", "a goal-only method sees no insight; j02 adds it, so the two differ by one cause")],
    "A2": [("1 · 🔗 Reason from the fence only", "flow", ("inputs/", "goal · method · rules", ""),
            ("🤖 Designer agent", "② reason ideas, step by step", "run-reason-t00"),
            ("chains.yaml + topics.md", "each step and its source", "")),
           NONE,
           ("2 · 🔗 Reasoning chains", "table", ("step", "says", "from"),
            [("1", "<what the goal needs>", "goal.md"), ("2", "<a known barrier>", "own knowledge"),
             ("3", "<a way past it>", "rules.md")], ()),
           ("3 · 🧭 Topics", "tiles", [("<topic 1>", "<n> ideas"), ("<topic 2>", "<n> ideas"), ("<topic 3>", "<n> ideas")])],
    "A3": [("1 · 💡 Name the ideas", "flow", ("chains.yaml", "the reasoning, step by step", ""),
            ("🤖 Designer agent", "one idea per chain's end", "run-reason-t00"),
            ("ideas.yaml", "I01 to I08, each a short name", "")),
           NONE,
           ("2 · 💡 The ideas", "rows", [("I01 · keep-devices-on", "", ""),
                                        ("I02 · note-unusual-moments", "", ""),
                                        ("I03 · list-what-you-take", "", "")],
            "I04 to I08 the same; each becomes a design Task once the fence check passes")],
    "A4": [("1 · ✅ Check the fence", "flow", ("chains.yaml", "every step's from: line", ""),
            ("🤖 Reviewer agent", "a fresh context, nothing generated", "run-open-designs-j01 · p01"),
            ("fence-check.md", "pass or fail", "")),
           ("", "ask", "Your part: none; a pass opens the design Tasks, then t99", "", "none"),
           ("2 · ✅ The verdict", "big", "pass · 0 steps outside the fence", "done"),
           ("3 · 📂 Tasks opened", "chain", [("② ideas", "t00_reason-ideas"), ("③ ④ designs", "t01_d01 … t08_d08"), ("⑤ rank", "t99_review-whole")], "")],
    # ── ✏️ design · method steps ③ and ④ (tNN_d<NN>_<slug>; run-generate, run-verify-v<k>, run-revise) ────────────
    "B1": [d_turns("drafted", ("passed", "next")),
           ("1 · ✏️ Draft the design", "flow", ("Idea I01 · keep-devices-on", "from t00's ideas.yaml", "and inputs/ only"),
            ("🤖 Designer agent", "③ conduct the method's process", "run-generate-d01"),
            ("Draft + elements.yaml", "the design as it reads", "each element and its why")),
           NONE,
           ("2 · 📄 The design, as it reads", "dcard", "Checklist", "<title>",
            ["☐ Day 14: <what to do>", "☐ Day 10: <what to do>", "☐ Visit day: <what to do>"],
            ["from idea I01", "<title> ← goal.md", "<day 14> ← rules.md r1", "<visit day> ← rules.md r2",
             "③ run-generate-d01 · draft v1"],
            ["④ T0 ✗ rule r2 · T1 ✓", "v1 failed: revised to v2"])],
    "B2": [d_turns("verifying"),
           ("1 · 🧪 Verify the draft", "flow", ("Draft v2", "the design + elements.yaml", ""),
            ("🤖 Reviewer agent", "④ T0 rules · T1 sources", "run-verify-d01-v2"),
            ("Verdict", "pass or fail", "feedback, frozen")),
           NONE,
           ("2 · 🧪 Tests", "table", ("Run", "test", "result", "by"),
            [("run-verify-d01-v1", "T0 rules", "✗ r2", "another agent"),
             ("run-verify-d01-v1", "T1 sources", "✓", "another agent"),
             ("run-verify-d01-v2", "T0 rules", "✓", "another agent"),
             ("run-verify-d01-v2", "T1 sources", "✓", "another agent")], ()),
           ("3 · 📝 Feedback", "line", "v1's frozen feedback named the rule it broke; the revise read only that")],
    "B3": [d_turns("revised"),
           ("1 · 🔁 Revise what failed", "flow", ("Draft v1 + its feedback", "the failed verdict, frozen", ""),
            ("🤖 Designer agent", "change only what failed", "run-revise-d01 · p01"),
            ("Draft v2", "then verify v2", "")),
           NONE,
           ("2 · ↔️ What changed", "table", ("part", "v1", "v2"),
            [("<the item that broke a rule>", "<before>", "<after>"), ("<the rule>", "broken", "kept")], ()),
           ("3 · 🔁 The loop", "line", "fail → revise → verify again, until it passes or t99 drops it")],
    "B4": [d_turns("passed", ("kept", "t99")),
           ("1 · 🪜 Carry the verdict and the rank", "flow", ("Verdict v2 + t99's ranking", "passed · its rank", ""),
            ("🤖 Projection", "project_predictions.py", "haipipe-design-workflow"),
            ("Face + prediction.yaml", "state: kept", "predicted · against · why")),
           ("", "ask", "✍️ Your sign comes at the Job: Review and approve", "Open", "gate"),
           ("2 · 🪜 Its walk", "chain", [("✅", "draft"), ("✅", "v1 failed"), ("✅", "v2 passed"), ("✅", "kept"),
                                        ("⬜", "released")], ""),
           ("3 · 📄 The design, passed", "dcard", "Checklist", "<title>",
            ["☐ Day 14: <what to do>", "☐ Day 10: <what to do>", "☐ Visit day: <what to do>"],
            ["from idea I01", "<title> ← goal.md", "<day 14> ← rules.md r1", "<visit day> ← rules.md r2",
             "③ run-revise-d01 · draft 2"],
            ["④ T0 ✓ · T1 ✓ · passed", "expected <effect>", "  against <arm> · why <line>", "⑤ rank #<n> · kept"])],
    # ── 🏆 review whole · method step ⑤ (t99_review-whole, run-rank-t99) ───────────────────────────────────────────
    "C1": [("1 · 🏆 Rank the passed designs", "flow", ("Passed designs", "d01 to d08, with verdicts", ""),
            ("🤖 Reviewer agent", "⑤ rank the whole, keep the top 3", "run-rank-t99"),
            ("ranking.csv", "rank · predicted · why · kept", "")),
           NONE,
           ("2 · 🏆 Ranking", "table", ("rank", "design", "predicted", "kept"),
            [("1", "<d0x · name>", "<effect>", "yes"), ("2", "<d0x · name>", "<effect>", "yes"),
             ("3", "<d0x · name>", "<effect>", "yes"), ("4", "<d0x · name>", "<effect>", "no")], ())],
    "C2": [("1 · 🧩 Check the coverage", "flow", ("ranking.csv + goal.md", "the kept, the goal's parts", ""),
            ("🤖 Reviewer agent", "each part, covered or not", "run-rank-t99"),
            ("Coverage", "each goal part and its design", "")),
           NONE,
           ("2 · 🧩 Goal parts", "table", ("goal part", "covered by"),
            [("<part 1>", "<d0x>"), ("<part 2>", "<d0x>"), ("<part 3>", "none yet")], ())],
    "C3": [("1 · ✅ Keep the top 3", "flow", ("ranking.csv", "kept: yes or no", ""),
            ("🤖 Projection", "each Task's state, prediction", "project_predictions.py"),
            ("Kept · Dropped", "to the Job's release", "")),
           ("", "ask", "✍️ Your sign comes at the Job: Review and approve", "Open", "gate"),
           ("2 · ✅ Kept and dropped", "tiles", [("3", "kept: the goal's n"), ("<n>", "dropped"), ("<n>", "failed verify")]),
           ("3 · ➡️ To the release", "line", "the kept go to the Job's Review and approve, where you sign")],
}

# every part of the run card and the unit's step (the "slide" of a design view), and where it lands on the screen:
# a section title holding the words, or a kind
COVER = {
    "A1": [("inputs version iN", "Build the Job's fence"), ("step ① chooses the files", "Build the Job's fence"),
           ("manifest.yaml lists each file", "What the fence holds"), ("goal.md from the goal list", "What the fence holds"),
           ("one clock moves per Job", "What stays out")],
    "A2": [("inputs/ only", "Reason from the fence only"), ("chains.yaml: each step's from:", "Reasoning chains"),
           ("topics.md", "Topics")],
    "A3": [("ideas.yaml, each a short name", "The ideas"), ("every idea gets its Task", "rows")],
    "A4": [("reviewer agent, fresh context", "Check the fence"), ("fence-check.md: pass or fail", "The verdict"),
           ("only after a pass: open the Tasks, then t99", "Tasks opened")],
    "B1": [("from its idea, inputs/ only", "Draft the design"), ("the design as the reader sees it", "The design, as it reads"),
           ("elements.yaml: each element's source", "dcard"), ("project the draft", "turns")],
    "B2": [("fresh context", "Verify the draft"), ("T0 rules · T1 sources · T2 critique", "Tests"),
           ("named by its draft: -v<k>", "turns"), ("frozen feedback", "Feedback")],
    "B3": [("from its frozen feedback", "Revise what failed"), ("a new pass of run-revise", "Revise what failed"),
           ("then verify again", "The loop")],
    "B4": [("state walk: draft → verify → revise → passed → kept | dropped → released", "Its walk"),
           ("prediction.yaml from t99", "dcard"), ("a person signs the release", "ask")],
    "C1": [("the passed designs", "Rank the passed designs"), ("rank · predicted · why · kept", "Ranking")],
    "C2": [("coverage of the goal", "Goal parts")],
    "C3": [("keep the top N", "Kept and dropped"), ("project the predictions", "Keep the top 3"),
           ("the kept go to the release", "To the release")],
}

CAPTION = {"A1": "the files this Job may read, and nothing else", "A2": "how the ideas were reasoned, step by step",
           "A3": "the ideas, one design Task each", "A4": "whether every step stayed inside the fence",
           "B1": "the design as its reader sees it", "B2": "the draft checked by another agent",
           "B3": "what the revise changed, and why", "B4": "where this design stands, and its prediction",
           "C1": "the passed designs, ranked", "C2": "which parts of the goal the kept designs cover",
           "C3": "what goes to the release"}
NEXT = {"A1": "🔗 Chains", "A2": "💡 Ideas", "A3": "✅ Fence check", "A4": "✏️ design · Draft, one per idea",
        "B1": "🧪 Verify", "B2": "🔁 Revise if failed, 🪜 State if passed", "B3": "🧪 Verify v2",
        "B4": "🏆 review whole · Rank", "C1": "🧩 Coverage", "C2": "✅ Kept", "C3": "the Job · Review and approve"}


def view(key, section):
    """A view's sections in two groups (JL 261031, as the labeling Task views): ⚙️ Process is the step's flow and your
    part (section 1 and what follows it untitled); 📊 Results are its Out in detail. The drafts strip sits above both.
    Work shows everything, then the next step; Report shows the Results only."""
    secs = STEP[key]
    n_lead = 0
    while n_lead < len(secs) and secs[n_lead][0] == "" and secs[n_lead][1] in ("strip", "turns"):
        n_lead += 1
    lead, body = secs[:n_lead], secs[n_lead:]
    k = next((i for i, s in enumerate(body[1:], 1) if s[0]), len(body))
    process, results = body[:k], body[k:]
    if section == "report":
        keep = []
        for s in results:
            if s[1] in ("kv", "agent", "checklist", "ask"):
                continue
            if s[1] == "rows":
                s = s[:2] + ([(w, st, "") for w, st, _ in s[2]],) + s[3:]
            elif s[1] in ("table", "picture"):
                s = s[:-1] + ((),)
            keep.append(s)
        return lead + [("group", "📊 Results")] + numbered(keep)
    return (lead + [("group", "⚙️ Process")] + numbered(process) + [("group", "📊 Results")] + numbered(results)
            + ([("next", NEXT[key])] if key in NEXT else []))


def numbered(secs):
    """Each group counts its own sections from 1 (JL 261101)."""
    out, n = [], 0
    for s in secs:
        if s[0] and s[0] not in ("next", "group"):
            n += 1
            s = (re.sub(r"^\d+ · ", f"{n} · ", s[0]),) + s[1:]
        out.append(s)
    return out


def check():
    """Every card part in COVER lands on its view; no design Task carries an interaction (a person signs only at the
    Block and the Job); every line fits its box."""
    problems = []
    for key, rows in COVER.items():
        secs = view(key, "work")
        titles = " | ".join(str(s[0]) for s in secs)
        kinds = {s[1] for s in secs if len(s) > 1 and isinstance(s[1], str)} | {s[0] for s in secs}
        for part, place in rows:
            if place not in titles and place not in kinds:
                problems.append(f"{key}: card part '{part}' has no place '{place}'")
    for key, secs in STEP.items():
        for s in secs:
            if s[1] == "ask" and len(s) > 4 and s[4] == "interaction":
                problems.append(f"{key}: an interaction in a design Task")
            for words, size, room in fits(s):
                if wide(words, size) > room:
                    problems.append(f"{key}: '{words}' is {wide(words, size):.0f} px, its box holds {room:.0f}")
    return problems


def wide(words, size):
    """About how wide a line draws: 0.47 × the font size per letter, an emoji as two letters."""
    return sum(2 if ord(c) > 0x2500 else 1 for c in words) * 0.47 * size


def fits(s, w=640):
    """Each line a section draws inside a box, with its font size and the room the box leaves."""
    if s[1] == "flow":
        bw = (w - 2 * 34) / 3 - 14
        return [(box[0], 13, bw) for box in s[2:5]] + [(ln, 11, bw) for box in s[2:5] for ln in box[1:3] if ln]
    if s[1] == "tiles":
        tw = (w - 10 * (len(s[2]) - 1)) / len(s[2]) - 14
        return [(a, 15, tw) for a, _ in s[2]] + [(b, 10, tw) for _, b in s[2]]
    if s[1] == "rows":
        return [(r[0], 15, w - 264) for r in s[2]]
    if s[1] == "chain":
        bw = (w - 46 * (len(s[2]) - 1)) / len(s[2]) - 14
        return [(name, 12, bw) for _, name in s[2]]
    return []


if __name__ == "__main__":
    bad = check()
    print("\n".join(bad) if bad else f"coverage ok: {sum(len(r) for r in COVER.values())} card parts on {len(COVER)} views")

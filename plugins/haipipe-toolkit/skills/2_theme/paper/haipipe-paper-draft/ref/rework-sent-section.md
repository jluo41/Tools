How a Section reads itself as sent before it is reworked for a new version; moved from SKILL.md.

## 🧾 Reworking a sent Section (0.12.0)

When a version follows a sent one whose review came back (its comments report, `haipipe-paper-comments`, holds
the Review Items), each Section first reads itself as sent, before OUTLINE/SHAPE, so the person sees how much
changes and why (JL 261014: "How much we will chnage them ... could you use /excalidraw read to work on each of
the section, and make each section (main section) to be a sNN tNN from the new job ... we can put thing there to
discuss").

```text
sent PDF (its delivery) ─▶ sNN-tNN-<section>/reading.yaml ─▶ the drawing: how much changes ·
                           section · parts · key · a verdict          your call · one frame a subsection
                           and next per passage                       (pages left, short notes right)
                                      │
                                      ▼
face "How much changes" (every paragraph) ─▶ CONTEXT cites it ─▶ SHAPE: KEEP carried, REWRITE redone,
                                                                  MOVE sent on, CUT never back
```

1. **One Board topic per Main Section**, `sNN-tNN-<section>/` beside the Jobs, tagged with the sent version
   (`draft-v<MMDD>`) and the Task stem; its **Feeds:** names the new Task and the comments report.
2. **Its `reading.yaml`** (excalidraw-read 0.7.0) reads the sent PDF: `section:` with `name`, `pages`, `from`,
   `until`, `parts` (the subsection headings) and `key` (the count line); each passage's `comment` begins with
   `KEEP`, `REWRITE`, `CUT` or `MOVE`, its `link` goes to the Review Item that hits it (`how` begins with the
   point ids) or to `new-<task>`, and its `next` says in 10 words what the new Section does with it.
3. **Its face's How much changes table** gives every paragraph of the sent Section a row (`¶ · page · starts
   with · verdict · why`), then the count line and an estimate of the words that survive, said as an estimate.
4. **The new Section uses it.** CONTEXT cites the topic as a bounded related link; SHAPE carries a KEEP row as a
   slot, rewrites a REWRITE row, sends a MOVE row to the Section it names, and never brings a CUT row back.
5. **Routes agree.** Every Review Item a reading links lands on this Section in the comments report's `lands on`
   column; a missing route is fixed in the report, never only in the reading.

Worked example: Paper-TestToLearn-MS2026, S10 to S16, the sent `j01_v0429_mansci` read for `j02_v1007_mansci`:
107 rows, 13 KEEP · 47 REWRITE · 26 CUT · 21 MOVE.

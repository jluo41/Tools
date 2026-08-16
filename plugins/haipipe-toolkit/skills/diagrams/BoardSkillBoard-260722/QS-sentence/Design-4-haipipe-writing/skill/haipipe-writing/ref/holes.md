# The hole discipline: what to do about what you do not know

Migrated 2026-08-01 from `paper/2-phase/0-draft/haipipe-paper-draft` Steps 4, 4a
and 4c. The SHAPE is general and the NOTATION is not, which is the same split as
`change-record.md`: one discipline, one dialect per host.

The board half of this is NOT this file's to define. `board/haipipe-sentence`
owns the lanes and the evidence card, and `QB4 §3.3.3` names all eight lanes and
states the paper mapping. This file carries the discipline; those carry the grammar.

The first pass over this phase concluded there was nothing general in it. That
was wrong, and the reason is worth keeping: every rule below is written in
`\cite{TOADD}`, `{VAL:?}` and `Q-<Stage>-<n>`, so it *reads* as paper machinery.
Strip the notation and none of it is about papers.

## 1 · The three rules

**Never invent a fact to close a gap.** A guessed number, a plausible-looking
citation, or a confident sentence covering something you do not know is worse
than an obvious hole, because a hole gets filled and an invention gets believed.

**Every hole names an owner.** A placeholder with nobody attached is a defect:
nobody owns it, so nobody will ever fill it. The owner is whatever the host uses
to track owed work: a raised question, an issue, a `Decision Now` row, a TODO
with a name on it.

**Sweep after writing, not during.** Write to settle WHAT is being said, then go
back and sweep for what could not be filled. Sweeping while drafting is how a
draft stalls on its first unknown.

## 2 · Check both directions

This is the part that is easy to get half right, and half right is useless.

```
➡️  FORWARD    every hole has an owner
    a placeholder with no owner will never be filled

⬅️  REVERSE    every owner is real
    a bracket pointing at a question that does not exist is a hole
    that LOOKS owned, which is worse than an unowned one
```

`cli/holes.py` runs both.

## 3 · One writer per file

Two passes editing the same prose is a write race. When several checkers sweep
one document they are READ-ONLY: they report where each hole is, what kind it is,
and who owes it. One writer takes all the reports and does the insertions.

This is not a performance rule. It is why the paper phase's three lanes can run
in a single batch at all.

## 4 · Dialects

Not two arbitrary notations. `QB4 §3.3.3` states the mapping, and it is one to
one, which is how a board reaches `/haipipe-paper`:

```
📚 > Citation:  ←→  \cite{TOADD}         a source not yet found
🔢 > Value:     ←→  {VAL:? …}             a number not yet verified
🖼 > Display:   ←→  a display id          a figure or table not yet made
```

A board sentence carries the hole as a TYPED LANE under it; a manuscript carries
it as a placeholder inside the sentence. Same fact, two hosts.

```
🗂 board     one of the eight typed lanes, owned by an Aim id or a Decision Now row
             ⚠️ > Check:  and  🔎 > Q-consumer:  are holes by definition
             a lane that states what it FOUND is not a hole:
                ✅ > Value: 9.1 months · CC · 260801        filled
                ❌ > Value: {VAL:? median follow-up}        owed

📄 paper     the placeholder, owned by a Q-consumer record on the S page
                \cite{TOADD} [Q-Main-3]      {VAL:? median follow-up} [Q-Main-4]

📝 anywhere  TODO(<owner>): <what>          when a host has no notation of its own
```

The marker differs; the two checks in §2 do not. `cli/holes.py --dialect` covers
all three.

## 5 · What stayed in `paper/`

Everything that knows what a manuscript is: grepping the `.bib` before writing a
key, the `\citep{}` vs `\cite{TOADD}` decision, DR rows and display inboxes, the
`1-probes/` boundary, the stage contracts, and the rule that real evidence lands
only through the PROBE phase. None of that generalizes, and none of it moved.

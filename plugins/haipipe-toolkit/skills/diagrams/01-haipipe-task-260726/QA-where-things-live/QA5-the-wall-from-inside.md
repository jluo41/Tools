# ⑤ The wall, seen from inside: we are the bank
state: 🟡 PARTIAL
owner: JL
method: one door in, general language only, and never learn who asked

## Question
What may reach this layer from a consumer, and what must this layer never learn? A paper or an application cannot run code, so it sends a question here. The rule that makes the whole arrangement worth having is that the question arrives stripped: no claim id, no paper name, no reason. This layer answers it and never finds out who asked or why.

That looks like a politeness and it is an economic rule. A question carrying its stake, "does WellDoc have a cycle column, because my claim C6 dies if it does", invites an answer shaped around C6. Such an answer is worth something to exactly one consumer. The same question asked plainly produces an answer the next consumer inherits for free, and a bank of those compounds while a bank of the first kind does not.

What makes it hard from this side is that the discipline is entirely negative. There is nothing to build: the rule is that certain words never appear anywhere under `tasks/`, and nothing checks for them. The layer is consumer-unaware by convention, and a convention with no checker is a hope.

## Boundary
- ✅ Covered here
  What arrives, what must not, what goes back, and how this layer stays consumer-unaware.
- ↪ Covered elsewhere
  What the digest itself contains is `QD1`, and what may not leave besides it is `QD2`. The probe layer's own model, the five-step loop and the QA-file contract belong to `01-probe-qa-260726`: `QA8@probe` is the same wall written from the consumer's side, and this page must not disagree with it.

## Diagram
```
   THE WALL.   we are on the right.  we never look left.

   A CONSUMER                    ║                    THE BANK
   paper · application           ║                    tasks/ · discoveries/
                                 ║
   the STAKE lives here          ║   "does WellDoc have a cycle column?"
   and NEVER crosses             ║    ───────────────▶
   "...because C6 dies if it     ║    general language, no id, no reason
      does"                      ║
                                 ║          /haipipe-task qa
                                 ║          THE ONLY DOOR IN
                                 ║                │
                                 ║                ▼
                                 ║          ① QA/ exists      → return the path
                                 ║          ② results/ answer → digest it, no run
                                 ║          ③ neither         → P→B→E→R
                                 ║                │
                a PATH           ║                ▼
        ◀──────────────────── ║    QA/<n>-<slug>.md
        never a copy of the      ║
        answer, always a path    ║

   ── what this layer must NEVER contain ────────────────────
      ✗ a claim id            C6, H3, [primary]
      ✗ a consumer's name     "the paper", "the MISQ submission"
      ✗ a reason to ask       "needed for the results section"
      ✗ a probe id            PP03, Q-Seed-4
      nothing under tasks/ names a probe. That ABSENCE is the contract,
      which makes it a grep — and nothing runs it.

   ── the three callers, and why they get one door ─────────────
      a human · the orchestrator agent · a relayed consumer question
      ONE identical door. If any of them had a special path, the
      stripping would be optional for that path, and an optional
      rule about what must never cross is not a rule.

   ── the direction that surprises people ───────────────────
      we never CALL the probe layer. We are called through it.
      ⑤ appears on QA1's map as a folder we consult and never touch.
```

## Content
### Consumer-unaware is a property of the FILES, not of the intent
The rule is not that a task author should try not to think about the paper. It is that no file
under `tasks/` may contain a word only a consumer could have produced. That is stronger and, more
importantly, it is checkable, which is the whole reason to state it that way.

`SKILL.md` already says it about the digest specifically: plain prose with `[→ results/…]`
anchors, no claim ids, no "the paper". What is missing is that the same rule applies to a
`plan.yaml` intent line, a config comment, a run name and a folder name, and that nothing
verifies any of it.

### The primary mode has no question in it at all
Worth stating because the `qa` door makes this layer sound reactive, and it is mostly not. The
primary mode is autonomous: run Plan through Report for its own sake, train, sweep, profile, scan.
No question is pending and nobody asked. That IS the project's research, and the bank grows there.

There is a second mode with no question pending either, and it is the one most likely to be
skipped: making the bank easier to ASK. Writing a digest for a finding worth digesting, or
refactoring so that future questions are cheap, is this layer's own work. A consumer never reaches
in to do it, and if this layer does not do it, nobody does.

### One door, three callers, no exceptions
A human, the orchestrator agent acting on its own, and a relayed question from a consumer all
enter through `qa` and none gets a special path. The reason is narrow: a special path is a path on
which the stripping is optional, and a rule about what must never cross cannot have an exception
without ceasing to be one.

## Items to Finish
- [ ] 🔍 Write the grep that makes consumer-unaware checkable
      A pattern for claim ids, probe ids, `PP\d\d`, and consumer nouns, run over every `.md`, `.yaml` and `.py` under `tasks/`. The rule is stated in three places and enforced in none.
- [ ] 🚪 State that the door applies to files, not only to answers
      `SKILL.md` states the vocabulary rule about the QA digest. Whether it binds `plan.yaml`, config comments, run names and folder names is not written, and those are where a leak would actually happen.
- [ ] ⚖️ Rule what happens when a question arrives WITH its stake
      Today nothing. The options are to strip it and proceed, to refuse, or to answer and record that it arrived dirty. Refusing is the only one that keeps the rule real, and it is also the one most likely to annoy the caller.
- [ ] 🔗 Point at `QA8@probe` rather than restating it
      The same wall from the consumer's side. Two statements of one rule will drift; this face should hold only the executor's half.

## Where we are
The rule is stated and unenforced. `SKILL.md` and `fn/qa.md` describe the door, the three callers
and the vocabulary ban; no checker exists for any of it, and the one measurement available is that
1 of 107 task-folders has a `QA/` at all, so the door has been used rarely enough that a leak would
not yet have shown up.

- 260726 CC · 🧱 Written from the executor's side deliberately
      `01-probe-qa-260726` already argues this wall from the consumer's side, in twenty faces. This page holds only what is true from inside the bank, and links rather than repeats.

## Files
- `fn/qa.md`
  The door: the three-way gate, the state line, the strip-any-external-id rule.
- `SKILL.md`
  The two modes, the three callers, and the vocabulary ban on the digest.
- `QA8@probe`
  The same wall, from the consumer's side. Consulted, never edited from here.

## Log
260726 · Created with the board.

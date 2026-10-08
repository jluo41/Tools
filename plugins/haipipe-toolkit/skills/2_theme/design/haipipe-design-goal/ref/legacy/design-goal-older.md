design-goal.md on an older board: the contract of the Design Goal page
=====================================================================

(Moved here from haipipe-design-goal/SKILL.md on 261007, word for word, when the design theme moved onto
the ladder; see ../inputs.md and haipipe-design/ref/design-ladder.md.) An older board (`B00_DesignBoard-<name>/`
with `0-BR-brief/` and `2-Design[-M<NN>]/Design-NN-…/`) keeps this file and the old page's Design Goal Space
until it is carried over. On the ladder the aim and its rules are a goal in `board.md ## Goals`, and
`design-goal.md` holds only the Block's shared rules.

Version governance: this Design skill starts at the family version `0.4.0`. Only
explicit user approval may authorize `1.0.0`.

Theory of Design §2 (`servers/workbench-design/guide/method.md`):
a design starts from an **aim**, **constraints** and **resources**, and there is no
list of options to pick from. This skill writes those inputs down once per board,
so every design on it starts from the same stated input, with each line's source.

The Design workbench's Design Goal Space renders the file (`design.py`,
`design_input`); this skill is its only writer.


The file
--------

One file per board, `<board>/design-goal.md`, in the ASCII doc style:

```text
Design goal
===========
(one short paragraph: what the file is)

Aim
---
key: value <- source

Venue
-----
...

Rules
-----
...

Resources
---------
...

Leave out
---------
...

Task · <Design Folder name>
---------------------------
key: value <- source          (overrides the same key for that one task)
```

1. **One line, one fact**: `key: value <- source`. The key is lower case.
2. **Every line has a source**: a Brief section (`BR00 §3`), a principle (`P01`),
   a signed insight (`W01`), the register, the venue profile, or a named person.
3. **A gap is `?`**: write `key: ? <- what is missing and who can answer it`. The
   Design Goal Space shows it as "not stated". Never fill a gap with a guess.
4. **A task overrides, never repeats**: a `Task · <folder>` section holds only the
   lines that differ for that task (for example `for whom`).
5. **Venue lines say how this board uses the venue.** The venue's own defaults live
   in `skills/2_theme/design/venue/venue-<venue>/README.md` and show beside them; do not
   copy a default unless the board changes it.


The five views and their runs
-----------------------------

Each view is one block of the file and one run type in the Design Goal Space's
Runs panel. `haipipe-designer-agent` runs each one; the Workbench Table
(`skills/2_theme/design/workbench-design/ref/workbench-table.md`) is the contract.

| View | Run type | Writes | Person signs |
|---|---|---|---|
| Aim | Frame the aim | value wanted, their moment, for whom, measured by, baseline | the aim |
| Venue | Pin the venue | length, cta, opt-out, personalization, links, language | none |
| Rules | Set the rules | must do: each rule a design must keep, with how it is checked | the rules |
| Resources | Gather resources | starting text, past designs, theory, budget | none |
| Leave out | Set what to leave out | each thing that must never appear, and why | the rules |

**Aim.** The value is a change for the person, not an output: "more patients
review their new prescription", not "a better SMS". `measured by` names the
funnel step that decides it. `baseline` names the current best and its number
with its interval and source.

**Venue.** Read the venue README first. Write only what this board fixes or
narrows (a shorter length, a verbatim opt-out, no medication name).

**Rules.** A rule is a hard constraint: a design that breaks it is not a design.
Each rule must be checkable on the text alone. The design items register's
`acceptance` lines are the rules as checked; keep the two in step.

**Resources.** What the designer may draw on: the starting text, past designs and
what became of them, the board's Theory of Design and message theories, and the
budget (arms, time, people). `Starting text:` holds the starting message word for
word; each card's Design elements are read against it, so a design's kept, new and
removed words show without anyone listing them. `Elements:` names the starting text's
parts in reading order, `greeting = "Hi," · sender = "…" · news = "…" · ask = "…" · link =
"{LINK}" · opt-out = "…"`; each phrase is quoted as it stands in the starting text. The
Design Space reads every design slot by slot against them (the element matrix), and
every Design Item added after the line exists asks its Generate for the element record
under these names (a rule the add-item action appends).

**Leave out.** Things that must never appear in the message. The channel, the send
and the experiment are not listed here; they are fixed elsewhere.


How a run goes
--------------

1. Read `board.md`, the Brief (`0-BR-brief/…`), the venue README, the board's
   `design-theory.md` and the current `design-goal.md`.
2. For the view asked, list each line the Design Goal Space shows as "not stated"
   or that no source supports.
3. Answer each from a file, with its `<- source`. What no file says stays `?`, and
   becomes a question for the person.
4. Show the person the changed lines before writing. Write the aim and the rules
   only after the person says yes.
5. Edit `design-goal.md` in place; keep its order and the ASCII doc style.


Boundary
--------

This skill writes only `design-goal.md`. It does not change the Brief's design
task list (haipipe-design-brief), a design's own register block or card
(haipipe-design-frame), a Commission (haipipe-design-commission), or the venue
profiles. It does not design messages.

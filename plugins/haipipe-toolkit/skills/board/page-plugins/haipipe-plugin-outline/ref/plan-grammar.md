# The plan file · one grammar, and the Page Type is the switch

The plan is `<page>/outline/<stem>-outline-v<N>.md`: what the page WILL say,
agreed before it says it. This file is the grammar every plan obeys, and the
one `checks/outline.py`, `src/plan_shape.py` and the 🧭 tab parse. A phase
loads THIS file, not the plugin skill. The approved example is
`ref/specimen-section-plan.md`.

## 1 · The head

```text
# <stem> · outline v<N>
outline-version: v<N>
supersedes: v<N-1> | none
date: YYMMDD
approved: ⬜  |  ✅ <WHO> <YYMMDD HHMM> · in chat: "<the person's words>"
arc: <the argument the division sequence makes, in one sentence>
```

Optional head lines: `round: <RD id>` · `narrative-row: <NA page> / <section>` ·
`structure-source: <desk> §<n> <Sec-token>` · `feedback: n routed · n served ·
n declined` · `declined: <RD> <row id> · <reason>` (one per declined row).

- `arc:` states an argument. "This page reports the results of X" is a table
  of contents and fails (`plan-no-arc`).
- `approved:` is a person's. A machine may transcribe a person's approval given
  in chat, with the quote and the time; it never decides one. A machine writes
  `checked:` only.
- The only `## ` headings in the file are `## C<n> · …`. The tab counts
  divisions by position, so a stray `## ` shifts every address. There is no
  `## Aims` in the plan: Aims live on the page and the plan carries 🎯 marks.

## 2 · Division · paragraph · bullet

One `## C<n>` per Content division of the page: a flat Section (one `### §1`)
is `C1` with `P1` to `P<n>`.

```text
## C<n> · <name>                          ≤ 8 words · ≤ 56 chars · names the subject
                                          Section page: a budget clause may follow a
                                          second ` · ` (one paragraph, nine sentences,
                                          about 190 words)
### C<n>.P<m> · <move> · S<a> to S<b>     Section page: the paragraph's move and its
                                          sentence span
### C<n>.P<m> · <brief>                   any other page: one line saying what the
                                          paragraph does
- B<k> · <head>                           4 to 11 plain words: what the point DOES
  Note: <≤ 30 words> <marks>              the constraint, the definition a stranger
                                          needs, the number's status; the marks end it;
                                          a wrapped source line is still one Note
  Answered: <ids + numbers>               appended by the fold when a card lands;
                                          ends `· recount` when the value counts the
                                          run's own artifacts (receipts, findings)
  Drawn: <what the figure shows>          appended by the fold, transcribed from the
                                          unit's README claim, never composed
  Routed: <RD> <row id>                   appended by ⓪ COLLECT, one line per row served
```

The address is `C<n>.P<m>.B<k>`. `C` prints once on the division heading;
the rows carry `B<k>`. A continuation line starts with one of `Note` `More`
`Answered` `Drawn` `Routed`; every bullet carries at least one
(`bullet-missing-note`). A division name is the subject's real name
(`Shared lookup rules for BatchReader and OnlineReader`), never a count or a
role word (`One contract, two readers`).

## 3 · The bullet grain, by Page Type

```text
page-type: section     one bullet = one SENTENCE SLOT
                       head `S<n> · <what the sentence does>`
                       two bullets may share one S<n> when one sentence carries
                         two jobs (a count and a method; a finding and its context)
                       a finding's head carries its claim id and a word
                         (`C1: +9.34 MME per visit, comparison owed`), never
                         the claim's sentence
                       a `Cut:` bullet where something LEAVES the page names
                         what leaves and where it goes; zero is normal
any other type         one bullet = one POINT; DRAFT turns it into one or more
                       sentences
```

Both grains: 3 to 6 bullets per paragraph, seven is two paragraphs. A head
says the content in plain words: `The question: agreeable doctors, patient
pressure, room to decide` passes; `The question, with its two conditions
named once` names nothing and fails. A term is defined inline the first time
(`"agreeable" = goes along with what others ask`). Common words only; a
technical term survives as a thing's real name (`iv-overid`), defined at
first use; a metaphor (`rung`) is rewritten to the plain thing (`step`).

## 4 · What a bullet never carries

- the drafted sentence: the sentence lives on the page; a Note that quotes
  prose is DRAFT leaking upward, and the plan is too long by construction
- a markdown heading mark (`##`, `####`) inside a head or Note; name the part
  in words or by `§4.1`
- the card's question, the unit's claim, a contract's rule: each is one
  popover away, and restating it makes the plan unskimmable
- a Note over 30 words, or a second head after a colon
- past tense, a bare date code, a person's name as AUTHORITY (who ruled): the
  log carries who and when; a reviewer's comment cited as provenance
  (`Gordon's wording (#41)`) or a thread id (`D05 b`) is fine
- an Aim row, or a new Aim minted to receive an ask: an ask with no Aim is a
  `D<nn>` thread

## 5 · The marks, at the end of the Note line

```text
🎯 A<n>.<m> | P<n>     the Aim on the page this point serves (`P<n>` is a page-level Aim)
📚 <bibkey>            a PUBLISHED work whose key resolves in bibex/
                       never a board page id (a cross-reference is written in words)
📮 [PP<NN>]            a question a probe card answers; bare until ② PROBE raises
                       the card, then `📮 PP<NN>`
🧮 PP<NN>.v<n>         one quoted number out of an answered card; the checker
                       recomputes it (`checks/values.py`)
🖼 owed · <kind>       a figure or table; kind ∈ table · figure · diagram · tex ·
🖼 Display<N> · <kind>   illustration; the bullet's own words are the design;
                       the unit's README holds claim, caption and intake
```

- Unmarked is the normal case and means nothing is owed.
- A mark carries an id only when the id already exists; a card names the
  bullet it serves (`serves:`), so a bare mark with a card is RAISED.
- Several marks may share the line (`📮 🎯 A2.2`). An id is a citation, never
  a restatement of the card.
- The fold APPENDS `Answered:` `Drawn:` `Routed:` and the `PP<NN>` id; it never
  edits the head or marks of an approved version.

## 6 · Versions

```text
approved: ⬜   a working document: edit, delete, rewrite freely; no record needed
approved: ✅   frozen as of that date; any change is v<N+1> with `supersedes:`;
               v<N> is kept, because it was right at its date
```

A plan written in an older grammar is rewritten into this one on its next
pass: in place while ⬜, as `v<N+1>` after a tick. A tick belongs to the
version it ticked.

## 7 · What the checker enforces

```text
plan-shape-off-type   divisions match the Page Type's outline: mode        src/plan_shape.py
bullet-missing-note   a bullet with no continuation line                   src/plan_shape.py
plan-no-arc           no `arc:` line                                       cli/check.py
feedback-unserved     an open Round row no bullet serves and none declines cli/check.py
serves: anchor        a card's `serves:` names an address the plan lacks    src/plan_shape.py
coverage              every owing mark served, or bare and counted as owed  checks/outline.py
                      before ② PROBE; every unit on disk cited
value                 every 🧮 number recomputes                            checks/values.py
head-too-long         a head over 11 words                                  src/plan_shape.py
head-too-short        a head under 4 words (a code-word head)               src/plan_shape.py
note-too-long         a Note over 30 words, wrapped lines joined            src/plan_shape.py
note-quotes-page      a Note or head that appears verbatim in the page      src/plan_shape.py

The four head and Note teeth are REPORTED by the board-wide sweep
(`checks/outline.py`, as gaps) and are a HARD exit inside the page's own
OUTLINE gate (`cli/outline-pass.py`), which judges only the plan being written.
```

Run them: `python3 <haipipe-board>/checks/outline.py --boards <board>` and
`python3 <haipipe-board>/cli/check.py <board> | grep <PAGE>`.

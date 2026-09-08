# The plan file · one grammar, with phase-owned outline policy

The plan is `<page>/outline/<stem>-outline-v<G>.<S>[.<E>].md`: what the page WILL say,
agreed before it says it. This file is the grammar every plan obeys, and the
one `checks/outline.py`, `src/plan_shape.py` and the 🧭 tab parse. A phase
loads THIS file, not the plugin skill. The approved example is
`ref/specimen-section-plan.md`.

## 1 · The head

```text
# <stem> · outline v<G>.<S>[.<E>]
outline-version: v<G>.<S>[.<E>]
supersedes: <previous exact version> | none
shape-base: v<G>.<S>                    # required only when E > 0
date: YYMMDD
approved: ⬜  |  ✅ <WHO> <YYMMDD HHMM> · in chat: "<the person's words>" |
           ✅ inherited from v<G>.<S> · <original Shape approval>
arc: <the argument the division sequence makes, in one sentence>
```

Optional head lines: `round: <RD id>` · `story-row: <Story page> / <section>` ·
`structure-source: <desk> §<n> <Sec-token>` · `feedback: n routed · n served ·
n declined` · `declined: <RD> <row id> · <reason>` (one per declined row).

Plans carrying the pre-260907 `narrative-row:` key are migration inputs only;
rewrite that head to `story-row:` before a new Story-controlled Section pass.

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
  Note: <≤ 30 words> [🎯 Aim]             the constraint or definition a stranger needs;
                                          a wrapped source line is still one Note
  Evidence: E<NN>-<TYPE>-<slug> · <expected ready evidence>
                                          one named evidence item, before SURVEY
  Accept: <observable acceptance checks>  required directly after each Evidence line
  Serves: C<n>.P<m>.B<k>[, ...]           DISPLAY only; optional additional reader
                                          moves served by the same placed display
  Answered: <ids + numbers>               appended by the fold when a card lands;
                                          ends `· recount` when the value counts the
                                          run's own artifacts (receipts, findings)
  Drawn: <what the figure shows>          appended by the fold, transcribed from the
                                          unit's README claim, never composed
  Routed: <RD> <row id>                   appended by ⓪ COLLECT, one line per row served;
                                          readers also accept `RD01 S1-PP5; RD01 S1-PP7`
                                          and `RD01 S3-PP2, S3-PP3` as several rows
  Evidence: none · <reason>               alternative when this Bullet needs no
                                          citation, value, figure, or table
```

The address is `C<n>.P<m>.B<k>`. `C` prints once on the division heading;
the rows carry `B<k>`. A continuation line starts with one of `Note`,
`Evidence`, `Accept`, `More`, `Answered`, `Drawn`, or `Routed`; every bullet carries at least one
(`bullet-missing-note`). A division name is the subject's real name
(`Shared lookup rules for BatchReader and OnlineReader`), never a count or a
role word (`One contract, two readers`).

Every Bullet has exactly one evidence decision: one or more typed
`Evidence:`/`Accept:` pairs, or one `Evidence: none · <reason>` line. Omission
is a coverage defect; `none` cannot be mixed with a typed item. For `CITE`, one
`Evidence:` line names one claim-support contract at this
Bullet. It may admit several verified sources and may later realize as several
`\\cite{}` placements. It is not a paper record or a placement counter. Two
independently removable or falsifiable propositions require two CITE items (or
two bullets); one source may legitimately serve both.

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
any other type         one bullet = one POINT; CONTENT turns it into one or more
                       sentences
```

Both grains follow the paragraph budget declared by the Page Face owner and
frozen Context; the base grammar sets no journal-specific sentence count. Each
slot carries one point; split compound definition, mechanism, boundary, and
transition jobs before CONTENT. A head
says the content in plain words: `The question: agreeable doctors, patient
pressure, room to decide` passes; `The question, with its two conditions
named once` names nothing and fails. A term is defined inline the first time
(`"agreeable" = goes along with what others ask`). Common words only; a
technical term survives as a thing's real name (`iv-overid`), defined at
first use; a metaphor (`rung`) is rewritten to the plain thing (`step`).

## 4 · What a bullet never carries

- the drafted sentence: the sentence lives on the page; a Note that quotes
  prose is CONTENT leaking upward, and the plan is too long by construction
- a markdown heading mark (`##`, `####`) inside a head or Note; name the part
  in words or by `§4.1`
- the card's question, the unit's claim, a contract's rule: each is one
  linked workspace card away, and restating it makes the plan unskimmable
- a Note over 30 words, or a second head after a colon
- past tense, a bare date code, a person's name as AUTHORITY (who ruled): the
  log carries who and when; a reviewer's comment cited as provenance
  (`Gordon's wording (#41)`) or a thread id (`D05 b`) is fine
- an Aim row, or a new Aim minted to receive an ask: an ask with no Aim is a
  `D<nn>` thread

## 5 · Aim marks and typed Evidence Items

```text
🎯 A<n>.<m> | P<n>     the Aim on the page this point serves (`P<n>` is a page-level Aim)
Evidence: E01-VALUE-<slug> · <expected>    checked value/count/comparison
Evidence: E02-CITE-<slug> · <expected>     source claim ready to cite
Evidence: E03-DISPLAY-<slug> · <expected>  figure/table/diagram ready to place
Accept: <observable checks>                one line directly after each item
```

- A source-free bullet writes `Evidence: none · <reason>`. This is a CONTENT
  constraint: its realization contains no citation placement, empirical value,
  figure, or table. A transition, research question, paper-owned design move,
  or a paper-owned planning handoff can qualify. If later prose needs material, return to SHAPE and
  mint a typed item. `🎯` remains an Aim annotation and is not an Evidence Item.
- Every item id is `E<NN>-<TYPE>-<slug>`; bare `E01` and unnamed icon-only marks
  are invalid. Item numbers are stable within the Page and never renumbered.
- SHAPE writes the item name, expected ready payload, and `Accept:` line now;
  its matching Evidence Item record also carries a stable compact `Label`
  matching `[A-Za-z][A-Za-z0-9]{0,11}`.
  SURVEY later plans its Supporting Runs, one Local Input, and one local Run in
  `<stem>-evidence-items.md`; it does not invent what the item should become.
- Several items may belong to one bullet; each has its own immediately
  following `Accept:` line and its own table record.
- A DISPLAY Item keeps exactly one owning Target. It may add `Serves:` with
  other Bullet addresses when one placed display performs several reader jobs.
  Those addresses do not inherit the DISPLAY Item and still make their own
  evidence decisions.
- The fold APPENDS `Answered: E<id> · <interpretation + Result>` for VALUE or
  CITE and `Drawn: E<id> · <claim + Result>` for DISPLAY. It never edits the
  bullet head, item identity, expectation, or acceptance contract.

## 6 · Versions

```text
v<G>.<S>[.<E>] = generation · shape · evidence

v0.16       pre-Content Shape 16; omitted evidence component means zero
v0.16.1     the same Shape with its first evidence/Run fold
v0.17       a new pre-Content Shape; evidence returns to zero

v1.0        first approved, Content-eligible generation
v1.0.1      the same approved Shape with a new evidence/Run fold
v1.1        a bounded Shape revision inside generation 1
v2.0        an unapproved major redesign opened when substantial review calls for it
```

The two-part form is canonical shorthand for evidence zero: `v1.2` means
`v1.2.0`. Do not create both aliases for one state.

`G=0` is the pre-Content family. A Shape change increments `S`; an EMBED that
only appends or refreshes `Answered:`/`Drawn:` bindings increments `E` under
the same Shape. `v0.S.E` is valid in both copilot and auto: checked Shape may
proceed through SURVEY, LAND, and EMBED before the first approval, but no
`v0.*` plan releases or refreshes Content. The first explicit channel approval
promotes the selected Shape-and-evidence state to `v1.0` only after every
machine-finishable Evidence Item has been completed as far as possible. Any
remaining secure-server or person gate is named in the `approved:` line;
those items may continue through SURVEY/LAND/EMBED under `v1.0`.

For `G>=1`, every version change refreshes CONTENT. A bounded Shape change
increments `S`, resets `E` to zero, and receives its own human review before
Content follows it. An evidence-only change increments `E`, preserves every
division, paragraph, Bullet head/order, Evidence contract, and acceptance
rule, declares `shape-base: v<G>.<S>`, and inherits that Shape's approval. It
does not request a duplicate Shape approval. CONTENT refreshes only the
realizations affected by the changed evidence, then records the exact plan
version it consumed.

Increment `G` only when a substantial review or feedback round calls for a
large structural reconsideration: a changed central argument, hypotheses,
major divisions, or overall narrative. Open that redesign as the next
generation's unapproved baseline (for example `v2.0` with `approved: ⬜`),
then record direct approval on that exact version after review. Approval stays
on the version reviewed; approving `v1.1` does not mechanically rename it
`v2.0`. Mechanical repairs within one Shape or evidence revision do not
consume another number.

Integer-only `vN` files are legacy input, never a current plan. A page whose
chain is `v1 … vN` migrates ONE TO ONE to `v0.1 … v0.N`: every file keeps its
text, only the number changes, and the latest becomes the working revision.
No legacy tick mints `v1.0`: a `✅` written before this rule was a working
go-ahead, so `approved:` resets to `⬜` and the old tick moves, with its
quote, into that file's `status:` line and into one page-log record. The only
way to `v1.0` is a fresh channel approval that names the version (JL 260905:
"we haven't made them from v0 to v1 yet"). Do not create new integer-only
plan files; `outline-pass.py` fails a page whose latest plan is one.

## 7 · What the checker enforces

```text
plan-shape-off-type   divisions match the Page Type's outline: mode        src/plan_shape.py
bullet-missing-note   a bullet with no continuation line                   src/plan_shape.py
plan-no-arc           no `arc:` line                                       cli/check.py
feedback-unserved     an open Round row no bullet serves and none declines cli/check.py
serves: anchor        a card's `serves:` names an address the plan lacks    src/plan_shape.py
coverage              every Bullet declares typed item(s) or explicit none;  checks/outline.py
                      typed lines have id, expectation, immediate Accept,
                      and one table record after SHAPE
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

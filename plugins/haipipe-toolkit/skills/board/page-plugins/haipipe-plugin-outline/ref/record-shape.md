# The record files · one shape, nine kinds

Every file in `<page>/outline/` except the plan is a LIST OF RECORDS, and a
record has one grammar:

```text
### <ID> · <HEADLINE>            one line a stranger can read, ≤ 25 words
- **<Label>**: <value>           one line each; the label set is fixed per kind
  <indented lines>               detail, verbatim, folded under the record
> Comment WHO · text · YYMMDD    a signed lane, never deleted
```

Every file opens with three lines: `# <stem> · <kind>` · `page: <stem>` ·
`kind: <kind> · authored | generated · <one clause on its rule>`.

```text
file                     answers                  id            labels                              writer                         teeth
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
<stem>-outline-v<N>.<k>.md     what we AGREED      C.P.B         ref/plan-grammar.md                 OUTLINE; a person ticks        plan-* (grammar §7)
<stem>-context.md        what later phases MAY    CTX1–CTX6     Status · Sources · Next authority   CONTEXT/PREPARE; generated     context-missing · -stale ·
                         rely on                                                                                                    -conflicting
<stem>-requirement.md    what we MUST obey        V1 V2 V3 V4   V: Rule · Arc · Words · Citations · generator refreshes V; page     requirement-missing ·
                                                  W<n>          Displays · Source                  authors W; generator preserves   -hand-edited · -stale ·
                                                                W: Rule · Applies · Source                                         section-writing-in-page
<stem>-discussion.md     what is still ASKED      D<nn>         Ask · Options · We lean · Decide    this page, any phase, the chat  discussion-settled-thread
<stem>-feedback.md       what OTHERS said         S<x>-PP<n>    From · Feedback · Work · State ·    cli/feedback.py collect;        feedback-uncollected ·
                                                  R<nn>         Landed                              the page writes Landed only     -coverage · -unserved
<stem>-evidence-items.md what each typed item      E<NN>-TYPE-   Target · Label · Need · Expected ·  SHAPE specifies; SURVEY plans;  (ref/item-table.md)
                         must become and its Runs  <slug>        Acceptance · Supporting Runs ·      LAND freezes input + binds Result
                                                                Local Input · Local Run · Decide · Verified (CITE only)
<stem>-evidence.md       what is READY             E<NN>-TYPE-   Status · Label · Target · Expected · cli/evidence-status.py          evidence-stale · -hand-edited
                                                  <slug>        Supporting Runs · Local Input · Local Run · Has
<stem>-files.md          what it READS and WRITES F<n>          Path · Role                         this page                       dead-file-path
<stem>-log.md            what CHANGED             YYMMDD [HHMM] headline only; detail folded        this page; append, newest first generated-block-stale reads it
```

## The rules per kind

**Discussion** holds OPEN questions and nothing else, written for the person
who answers. The four labels, in order: **Ask** is the question plus the one or
two facts needed to answer it; **Options** are lettered, one line each, or
`none here` and where the thread closes; **We lean** is one sentence with its
reason; **Decide** names who rules, what the thread serves (an Aim, a bullet
address, a Round row id, a page section) and `opened YYMMDD`. No `status:`
line; a thread in this file is open by definition. The headline is the
question, never a shorthand. A thread that settles LEAVES the file as one log
record, `D<nn> settled by <WHO>: <the ruling in one line>`, its argument and
signed lanes folded verbatim; a dropped thread is `D<nn> dropped: <why>`. The
id survives the move. `D<nn>` is BOARD-WIDE: allocate from the highest id
across every discussion AND log file on the board:

```bash
grep -rhoE '^#{3,4} D[0-9]+|· D[0-9]+ (settled|dropped)' <board>/*/*/outline/*-discussion.md \
  <board>/*/*/outline/*-log.md | grep -oE 'D[0-9]+' | sort -t D -k2 -n -u | tail -1
```

Two sessions can mint the same id in the same minute: run the grep
immediately before the write, run it again after, and the later writer
renumbers its own new threads. Never versioned. An edit inside a thread is a `> ✎ ~old~ *new* · WHO · YYMMDD
HHMM` lane. A live ask that owns no Aim becomes a thread, never a minted Aim.

**Log** is a timeline of one-line records, newest first, append only. The
headline (15 to 25 words) says what changed; the reasoning, the old text, or a
diff folds under it. A record already written is never edited or deleted;
restructuring an old row means giving it a headline and folding its text. One
record per: a thread's status change · an OUTLINE pass · a CONTENT pass
(the `~~old~~ → new` diff folded) · any write a chat session makes, naming the
file. There is no separate log of the discussion.

**Feedback** is a projection: the Round owns every row, the page may not
rewrite one, and `cli/feedback.py collect` regenerates the whole file. A row
carries the Round's own words (`Feedback`, `Work`, and each parent R-row's
concern with the pages it routes to), never a paraphrase; a Round section
carries the verdict, the proposed reader order and the open gate. The page's
one field is `Landed: <the checked version that answered the row>`, preserved
by row id across regeneration. To argue with a row, open a `D<nn>` thread with
`serves: <RD> <row id>`.

**Requirement** has a generated venue portion with up to four records: V1
Shape is always present and carries the desk's Arc when supplied; V2 Size,
V3 Refused, and V4 Moves appear only when the bound venue source supplies
their format, anti-pattern, or slot material. V2 uses Words · Citations ·
Displays with measured detail folded; V3 uses one Rule per anti-pattern; V4
uses the slot names with exemplars folded. Each
record prints its address, `` `<desk>.md` §<n> <Sec-token>.<sub> ``. A
page-specific deviation is a `D<nn>` thread, never a requirement line. A page
with no `structure-source:` gets no file.

The same **Requirement** file also holds the Page's authored writing contract
as `W<n>` records after the generated block. Each has a short imperative
headline that previews the instruction, followed by `Rule`, `Applies`, and
`Source`. `Rule` is one complete sentence; `Applies` names the page, division,
prose kind, or display cells it governs; `Source` names the authority without
copying it. `cli/requirement.py` replaces only the bounded V block and preserves
the authored W records verbatim. A manuscript Section carries no `###
Writing Style` block in the product `<page>.md` and no separate writing file.

**Context** is the generated PREPARE projection described by
`../../page-workflows/haipipe-page-context/ref/context-record.md`. Its stable
records `CTX1` to `CTX6` resolve identity, purpose/scope,
policy/structure/style, related information, feedback/decisions, and
planning/evidence readiness. It summarizes for orientation but every rule
points to its source authority and version/hash. Regenerate it whole; never
hand-edit it or place a human gate in it.

**Evidence Items** is the authored table (`ref/item-table.md`): one record per
typed outline item. Its immutable id is `E<NN>-<TYPE>-<slug>` where TYPE is
`VALUE · CITE · DISPLAY`; its head also names the target `C.P.B` and readable
item name. SHAPE writes `Target · Label · Need · Expected · Acceptance` and
initializes CITE-only `Verified: ⬜`.
`Label` is the stable 1–12 character ASCII alphanumeric wall name; the UI does
not derive it from the full item name. SURVEY writes `Supporting Runs` (zero
or more Execution/Discovery plans), exactly one `Local Input` envelope plan,
exactly one `Local Run` (`Page · Evidence Item`), and leaves `Decide` for a
person. LAND validates every Supporting Result, appends allocated global Run
ids, freezes the input pointer/hash, binds the local `→ <Result>`, and presents
the CITE payload so a person may sign that item's `Verified` gate.
Cross-Folder evidence enters through Supporting Run Results. No Status word is
ever typed here.

**Evidence** is a dated snapshot of the Evidence Item table joined to Run
receipts and Results: one record per typed item, `Status` first, one word of
`specified · planned · ready · folded · accepted · stale · deferred · dropped
· blocked`, followed by its target, expectation, Supporting Runs, Local Input,
Local Run, decision, and `Has`. The page line reads
`cycle: … · items n · decided n/n ·
<status tally>`. It imports the tab's own parse and
`src/item_table.py`, so file, strip and tab cannot disagree.

**Files** is one record per file the page reads, writes, checks or keeps:
`Path` and `Role` ∈ reads · writes · checks · contract · archive · related. A
Related Board Page is `Role: related` with its row verbatim under it
(`` `reads · EVIDENCE` · [QB7 §3](QB-research/QB7-literature.md) ``), the
grammar `cli/pagecontext.py` reads.

## The three laws that hold every kind

- A generated file is regenerated, never edited. Requirement is the bounded
  exception: regenerate its V block and author its W block; the
  `requirement-hand-edited` tooth fires when the generated marker disappears.
- Every kind is one flat file carrying the stem; only the plan is
  many-per-page, by version. No file name contains `outline` except the plan,
  because the plan globs are `*-outline-*.md`.
- The renderer (`live/outline.py _records`) draws every kind the same way: id
  badge, headline, label grid, status pill, a "more" fold; one chip per file
  that exists, with its record count. The lens writes nothing.

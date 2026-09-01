# The record files · one shape, seven kinds

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
<stem>-outline-v<N>.md   what we AGREED           C.P.B         ref/plan-grammar.md                 OUTLINE; a person ticks        plan-* (grammar §7)
<stem>-requirement.md    what we MUST obey        V1 V2 V3 V4   Rule · Arc · Words · Citations ·    cli/requirement.py, venue only  requirement-missing ·
                                                                Displays · Source                                                  -hand-edited · -stale
<stem>-discussion.md     what is still ASKED      D<nn>         Ask · Options · We lean · Decide    this page, any phase, the chat  discussion-settled-thread
<stem>-feedback.md       what OTHERS said         S<x>-PP<n>    From · Feedback · Work · State ·    cli/feedback.py collect;        feedback-uncollected ·
                                                  R<nn>         Landed                              the page writes Landed only     -coverage · -unserved
<stem>-evidence.md       what has LANDED          C.P.B         Has · Status                        cli/evidence-status.py          evidence-stale · -hand-edited
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
record per: a thread's status change · an OUTLINE pass · a DRAFT or REVISE pass
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

**Requirement** is venue only, four records: V1 Shape (with the desk's Arc),
V2 Size (Words · Citations · Displays; `measured …` folded), V3 Refused (one
Rule line per anti-pattern), V4 Moves (the slot names; exemplars folded). Each
record prints its address, `` `<desk>.md` §<n> <Sec-token>.<sub> ``. A
page-specific deviation is a `D<nn>` thread, never a requirement line. A page
with no `structure-source:` gets no file.

**Evidence** is a dated snapshot of the 🧭 join: one record per marked bullet,
its head carrying THE PLAN'S OWN WORDS after the mark (0.18.1, JL 260831: a
bare ref in the head "lost a lot of informations"), `Has` what the disk says,
`Ref` the serving card/unit id only when one exists, `Status` one of the six
words `evidence-ready · needs-probe · needs-intake · needs-citation ·
needs-revision · accepted`; the page line reads `owed · landed · accepted`. A bare mark a card serves counts as
raised. It imports the tab's own parse, so file and tab cannot disagree.

**Files** is one record per file the page reads, writes, checks or keeps:
`Path` and `Role` ∈ reads · writes · checks · contract · archive · related. A
Related Board Page is `Role: related` with its row verbatim under it
(`` `reads · EVIDENCE` · [QB7 §3](QB-research/QB7-literature.md) ``), the
grammar `cli/pagecontext.py` reads.

## The three laws that hold every kind

- A generated file is regenerated, never edited; the `*-hand-edited` teeth
  fire on a missing GENERATED line.
- Every kind is one flat file carrying the stem; only the plan is
  many-per-page, by version. No file name contains `outline` except the plan,
  because the plan globs are `*-outline-*.md`.
- The renderer (`live/outline.py _records`) draws every kind the same way: id
  badge, headline, label grid, status pill, a "more" fold; one chip per file
  that exists, with its record count. The lens writes nothing.

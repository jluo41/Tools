# What a question delivers · worked patterns

Read when writing or agreeing a question's needs, or before a Job's answers are checked. The rule is
`block-contract.md` § What a question delivers; `deliverables.py <question folder | Board Task>` prints one
question's list and notes each gap; `scripts/insight_ladder.py review <Board>` prints every gap of a Board's
Question Book at once.

```text
question.md  output:   the tables a Run writes        ─▶ maker: what to produce
             figures:  the figure each table gets     ─▶ maker: what to draw
             pass:     what a result must contain     ─▶ checker: one verdict per need
Task page    the answer in one line, how sure, one takeaway per segment asked
```

## Figures: three ways to say it

1. **Say nothing** when the table has a shape `figures.py` knows (rates with intervals, an estimate beside its
   low and high, a share, a message × level grid): it is drawn by its shape.
2. **Declare it** when the shape is not known and a figure answers the ask:
   `- {table: <file>.csv, kind: line | bar | forest | heat, …}`. A grouped figure's legend is titled with the
   `group:` column, so name that column for what it holds.
3. **Say none is wanted**, so the gap closes as a decision and not an oversight:
   - `- {table: <file>.csv, kind: none}` for one table inside a need whose other tables keep their figures. This is
     the usual form for a table that supports the result and is not itself the result: an audit of the grouping, a
     one-row test (an interaction test, a model fit, an order test).
   - `figures: []` when no table of the need wants a figure (an inventory, a catalog, a text table).

   Put a `kind: none` entry at the end of the list: a declared figure's file name carries its place in the list.

## A judge's `pass:` names something a reviewer can check

A judge need is the reading an agent writes on the page, so its `pass:` is the only test that reading has. Write
what the reading must contain, never which way it must come out:

```text
vague      "a clear and well supported conclusion"
checkable  "one verdict word (POOL, SPLIT or UNDETERMINED), the difference and its interval from
            pooling.csv, and the boundary: which segments the counsel does not cover"
```

A `pass:` that names no number, table, need or word the page must carry is returned by the agent that agrees
the plan (`haipipe-insight-evidence-plan`): a reviewer cannot give a verdict against it.

## Editing a version that is not signed yet

An open version (`signed: ''`) may be edited in place; a signed one never (the change is a proposal for the next
version, `release.md` § Signing). A Board Job that already ran on the open version then holds an old hash and old
receipts, so the order is:

```text
1  edit        the question.md files; each edited question goes back to agreed: ⬜
2  agree       another agent agrees the edited plans (run-review-plan)
3  re-pin      insight_ladder.py update <Board> --apply         each Job's hash: follows its release
4  rerun       insight_ladder.py update <Board> --apply --rerun  each stale Run's own ticket
5  audit       insight_ladder.py audit <Board>                   every row ✅
6  review      insight_ladder.py review <Board>                  which answers now owe a reread or a check
```

A rerun that writes the same tables keeps the receipt's `content_since`, so an answer written from those tables
is still current; new figures and new `pass:` lines change what the checker tests, not what the answer read.

## Reviewing every answer of a Job

`review` lists the answers that owe a reread (`run-write-t<NN>`) and those with no ✅ on `check:`
(`run-check-t<NN>`). A check is one agent per Task in a fresh context, so checking a whole Job is many agents at
once: a session starts it only when the person asks (the Job's Work › Check a report button gives the prompt, or
"check every answer of this Job"). Until then the list is the report, and no answer is marked checked.

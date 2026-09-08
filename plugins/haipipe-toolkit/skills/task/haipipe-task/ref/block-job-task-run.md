# Block / Job / Task / Run reference

This compact reference defines names and addresses used by Task tables,
receipts, Board links, and logs. `ref/hierarchy.md` owns the complete contract.

```text
Block  bNN_<noun>_<qualifier>   one Task Board topic
Job    jNN_<noun>_<qualifier>   one self-contained submission boundary
Task   tNN_<noun>_<qualifier>   one pipeline and one Page Folder
Run    rNN_<noun>_<qualifier>   one execution identity
```

## Addressing

Read the four prefixes directly from the canonical path:

```text
examples/<project>/tasks/b02_llm_runs/j01_physician_search/
  t03_claude_requests/scripts/config/r04_fold00_opus.yaml

compact   b02j01t03r04
readable  b02.j01.t03.r04
global    <project-slug>:b02j01t03r04
```

Partial addresses retain their level letters, such as `j01t03` or `t03r04`.
Bare numeric tuples are invalid because they hide level identity.

## Stranger test

The words after the index must tell an unfamiliar reader both the concrete
thing and the distinguishing qualifier. A shape word cannot carry the name by
itself.

```text
weak    j01_candidate_pool
clear   j01_physician_candidates_by_region
weak    t01_analysis
clear   t01_physician_rankings_compared
```

## Path mapping

```text
bNN Block   = Task Board
jNN Job     = Board Group
tNN Task    = Task Folder = Page Folder = Board Page
rNN Run     = config/Ticket/Result/notebook execution record
```

One Run's paths:

```text
<task>/scripts/config/<run>.yaml
<task>/runs/<run>.sh
$OUTPUT_ROOT/results/<task>/<run>/runtime.yaml
$OUTPUT_ROOT/notebooks/<task>/<run>.ipynb
```

Every receipt stores both address spellings. Renaming descriptive words does
not change the numeric identity; changing an index changes the address and
therefore requires updating every exact reference.

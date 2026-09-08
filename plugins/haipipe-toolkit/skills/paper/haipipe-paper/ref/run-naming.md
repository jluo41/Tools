# Paper Run naming contract

This reference is the Paper-family naming authority. It specializes the
neutral `haipipe-run` contract without changing the shared Run lifecycle.
Paper names must remain readable from the Paper Page that owns them; an
ordinal such as `j02` is never enough to identify a new Page.

## 1. Three identities, three scopes

| Identity | Owner | Physical home | Purpose |
|---|---|---|---|
| **Paper-local Run** | a Paper Section or Round Page's Evidence/Display lane | `<page>/runs/<PAPER_RUN_ID>.sh` + `<page>/results/<PAPER_RUN_ID>/` | one typed local Result whose identity carries the Paper lane and semantic Page |
| **Page-local Run** | any Page owner | `<page>/runs/<RUNNAME>` + `<page>/results/<RUNNAME>/` | a Page-scoped attempt using the shared `rNN_<family>-<operation>_<target>` grammar |
| **Job-backed Run** | Task/Discovery owner | the owner's `bNNjNNtNNrNN` store | reusable external work that a Paper Page supports, never a Paper-local alias |

The owning folder is part of the identity. A bare `r01` is not a reference.
When a Paper Page cites a Run outside its folder, carry the full owner path and
the owner-native Run id.

## 2. Paper lane map

The physical group names remain semantic and stable. Their one-letter Run
qualifiers are only a compact Paper-local namespace:

| Physical shelf | Page identity | Paper lane | Display label |
|---|---|---:|---|
| `Ba-<desk>-Main/` | `S-<desk>-Main-<N>-<Title>` (unnumbered: title only) | `m` | `M` / Main |
| `Bb-<desk>-Appendix/` | `S-<desk>-Appendix-<L>-<Title>` | `a` | `A` / Appendix |
| `Bc-<desk>-Round/` | `RD<NN>-<event>-<date>` | `r` | `R` / Round |

`Ba`/`Bb`/`Bc` are shelf/group tokens, not Run ids. `RD` remains the
canonical Round Page token: it means **Round** for editor, reviewer, coauthor,
and internal batches alike. Do not change existing `RD<NN>` pages to `RR`.

The `Story<Letter>-<desk>-<idea-slug>` page is the Paper authority for the
meaning and Section map. It has no reserved `s` Run lane. Its Discovery and
Task work keeps the native `b…` identity in the external owner.

## 3. Canonical Paper-local grammar

New Paper-local Evidence or independently owned Display Runs use one readable
lowercase ASCII id:

```text
PAPER_RUN_ID := p<L>-<page-slug>-<target>-r<NN>
L            := m | a | r
page-slug    := semantic tail of the owning Page id, lower-kebab-case
target       := e<NN>-<type>-<slug> | f<NN>-<slug>
```

Examples:

```text
pm-introduction-e01-cite-prescribing-variation-r01
pm-results-e13-display-cohort-overview-r01
pa-robustness-e01-value-sensitivity-r01
pr-rd01-misq-feedback-20260825-e01-cite-response-r01
```

The target repeats the typed Evidence Item (`E01-CITE-…`, `E13-DISPLAY-…`)
in a normalized form, so a Run can be found without guessing what `t01`
meant. `rNN` is the attempt ordinal for this Paper-local target. A retry with
unchanged target, frozen input, and acceptance appends to the same Run; a
material change gets a new id and `supersedes`.

The reader-facing form is deliberately friendlier, but is not a second id:

```text
P M · Introduction · E01-CITE-prescribing-variation · R01
P A · Robustness · E01-VALUE-sensitivity · R01
P R · RD01-MISQ-feedback-20260825 · E01-CITE-response · R01
```

## 4. Page-local and Division Writing grammar

The shared Page namespace remains available and is not renamed merely because
the Page lives inside a Paper:

```text
PAGE_RUN_ID       := r<NN>_<family>-<operation>_<target>
DIVISION_WRITING  := r<NN>_page-division-writing_c<NN>
PAGE_EVIDENCE     := r<NN>_page-evidence-item_e<NN>-<type>-<slug>
PAGE_DISPLAY      := r<NN>_page-display_c<NN>-f<NN>
```

For a Paper Section, `DIVISION_WRITING` is the current Page-local Content
Run, for example `r01_page-division-writing_c01`. Its Main/Appendix meaning
comes from the owning semantic Page (`S-MISQ-Main-Introduction` or
`S-MISQ-Appendix-Robustness`) and must also be recorded in `runtime.yaml`:

```yaml
run: r01_page-division-writing_c01
family: page
operation: division-writing
page: S-MISQ-Main-Introduction
paper_lane: main
target: C01
```

Do not make the same attempt both a Paper-local Evidence Run and a Page-local
Division Writing Run. Evidence prepares a typed Result; Division Writing
realizes a Content division from the folded Result. They are different targets
and may legitimately both have an `r01` in different namespaces.

## 5. Collision and reference rules

1. `pm-`, `pa-`, and `pr-` are reserved for new Paper-local Runs. `rNN_…` is
   the Page-local namespace; `bNNjNNtNNrNN` remains Job-backed.
2. Uniqueness is `(owner Page path, Run id)`, not the numeric suffix alone.
   A cross-Page reference must include the semantic Page id and the full Run
   id; a cross-Folder reference also includes the owner-native path.
3. The lane token does not replace the Page id. `m` means Main only after the
   Page resolves to `S-<desk>-Main-…`; it never means “the first page”.
4. `Story`, `Section`, and `Round` are Page identities/owners, not additional
   Run families. The Run family remains `Page · Evidence Item`, `Page ·
   Display`, or `Page · Division Writing` as defined by `haipipe-run`.
5. A SURVEY reservation is a plan and does not count as an allocated Run.
   LAND creates the Ticket, paired Result directory, and runtime receipt.

## 6. Legacy `pjNNtNNrNN` handling

The former Paper-local form is:

```text
pj<page-ordinal>t<item-ordinal>r<attempt>_<slug>
```

Examples in existing Paper folders such as
`pj02t01r01_rx_variation` are **historical, read-only Runs**. The old `jNN`
ordinal is not a new Page identity and must not be guessed or reused for a
new Paper. No bulk rename is required or allowed as part of ordinary Paper
work.

If an authorized migration or an unchanged-contract rerun is needed, create a
new canonical id, preserve the old file and Result, and record the relationship
in the new receipt:

```yaml
run: pm-introduction-e01-cite-prescribing-variation-r01
supersedes: pj02t01r01
legacy_run: examples/…/S-MISQ-Main-Introduction/results/pj02t01r01_rx_variation/result.yaml
```

The old Result may be reused only after its receipt, hash, and present
acceptance contract are checked. A legacy reference is never silently treated
as a new `pm`/`pa`/`pr` Run.

## 7. Minimum receipt fields

Paper-local receipts add the lane and semantic owner to the neutral Run
receipt:

```yaml
run: pm-introduction-e01-cite-prescribing-variation-r01
family: page
operation: evidence-item
paper_lane: main
page: S-MISQ-Main-Introduction
target: E01-CITE-prescribing-variation
ticket: runs/pm-introduction-e01-cite-prescribing-variation-r01.sh
result: results/pm-introduction-e01-cite-prescribing-variation-r01/
supersedes: null
```

`item`, `story`, `section_kind`, frozen inputs/hashes, worker, status, and
acceptance remain required by the owning Page/Evidence contract. This file
defines naming and scope only; it does not replace those gates.

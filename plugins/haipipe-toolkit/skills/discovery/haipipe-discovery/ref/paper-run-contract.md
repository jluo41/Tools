# Discovery Paper Run Contract (canonical)

This is the ONE authority for Level-4 work inside a Discovery Topic Folder.
The lifecycle and type axes point here; specialists do not restate this
contract.

## The unit

```text
Trigger -> resolve canonical Subject -> allocate RUNNAME -> Run -> Result
```

- **Trigger** explains why work started: a URL, DOI, PDF, citation, pasted text,
  or a human request. It is provenance, not automatically evidence.
- **Subject** is the one canonical evidence object analyzed by the Run. It is
  normally one paper. A non-paper source is legal only when that source itself
  is explicitly the evidence object.
- **Run** is the authored executable ticket `runs/<RUNNAME>.sh`.
- **Result** is that same Run materialized at `results/<RUNNAME>/`.

One Trigger may resolve to zero, one, or many Subjects. Zero stays
`unresolved`; many MUST fan out to one Run per Subject. One Run NEVER analyzes
multiple papers. Trigger identity never owns RUNNAME; the resolved Subject does.

## Hierarchy and the 1:1 spine

```text
L1  discoveries/                         Block
L2  discoveries/<GROUP>/                 Drop
L3  discoveries/<GROUP>/<NN_topic>/      Discovery Task Page Folder
L4  runs/<RUNNAME>.sh <-> results/<RUNNAME>/   Paper Run, two projections
```

Result is not a fifth level. It is the generated projection of the Level-4
Run. The stem match is exact and mandatory. No config folder or per-run config
file sits between them.

RUNNAME grammar:

```text
r<NN>_<first-author><year>_<short-title>
r01_chen2025_trace
```

Use lowercase ASCII, underscores, and a monotonically increasing two-digit
number. Never renumber. If the same Subject needs a materially new analysis,
allocate a new Run and record `supersedes:` in its runtime receipt; never
silently overwrite history.

## Folder shape

```text
<topic>/
├── <topic>.md                         Page Face: topic synthesis
├── discovery.yaml                     Task Face: topic manifest
├── outline/                           optional Page planning material
├── evidence/bibex/<topic>.bib         DERIVED union of completed Result bibs
├── scripts/                           optional reusable instrument
├── runs/
│   └── r01_chen2025_trace.sh          executable ticket
└── results/
    └── r01_chen2025_trace/
        ├── r01_chen2025_trace.md      Paper/Source Card readout
        ├── r01_chen2025_trace.bib     exactly one authoritative entry
        ├── facts.md                   atomic reusable findings
        ├── trigger.md                 optional captured trigger
        ├── runtime.yaml               state + provenance + subject identity
        ├── raw.md                     optional extraction/worker output
        └── paper.pdf                  optional
```

`scripts/` exists only when the Topic owns a reusable instrument. Low-level
worker, CLI, API, and skill calls belong in `runtime.yaml`; they are not Runs.

## Scaffold and completion gates

Opening a Run creates BOTH projections immediately:

```text
runs/<RUNNAME>.sh
results/<RUNNAME>/runtime.yaml   # status: planned
```

The ticket is executable. `runtime.yaml` uses one of:

```text
planned | running | complete | blocked | unresolved | superseded
```

Every paired Run/Result, at every state, requires the ticket and
`runtime.yaml`. A `complete` Result additionally requires:

```text
results/<RUNNAME>/<RUNNAME>.md
results/<RUNNAME>/<RUNNAME>.bib
results/<RUNNAME>/facts.md
```

Completion hard-fails when:

- either projection is orphaned or their stems differ;
- the ticket is not executable;
- the Result Bib has zero or multiple entries;
- the Result Card has no `cite: @Key`, or its key differs from the Bib key;
- runtime omits `bib.source` or `bib.mode: verbatim_copy`;
- the Bib entry was composed from model memory rather than copied from a
  trusted publisher/index/person source.

`paper.pdf`, `trigger.md`, and `raw.md` are optional. An `unresolved` or
`blocked` Result is a truthful receipt, not a completed Paper Result; it is not
eligible for evidence aggregation.

## Runtime receipt

At minimum:

```yaml
run: r01_chen2025_trace
status: complete
trigger:
  kind: social_note
  input: "https://example.org/short-link"
  resolved: "https://example.org/note/123"
subject:
  kind: paper
  title: "TRACE: Grounding Time Series in Context for Multimodal Embedding and Retrieval"
  canonical_url: "https://proceedings.neurips.cc/..."
  doi: "10.52202/085713-0087"
  arxiv: "2506.09114"
bib:
  source: "https://proceedings.neurips.cc/.../Bibtex"
  mode: verbatim_copy
executed_at: "2026-09-01T12:00:00-04:00"
```

Also record the dispatcher/worker calls and failure reason when applicable.
Never store credentials or private tokens.

## Result Card

```md
# <full subject title>

- run: <RUNNAME>
- cite: @CanonicalKey
- subject: <canonical URL / DOI / identifier>
- status: complete

## Question
What this Run was asked to establish.

## Readout
The paper/source's question, method, results, and contribution.

## Facts
- Atomic finding with a page/section/table/figure anchor when available.

## Trigger claim audit
- Optional: claim from a secondary trigger -> supported | qualified | unsupported.

## Limits
What the Subject and this Run do not establish.

## Reuse
Which topic-level arguments this Result can support, without binding it 1:1 to
any one Content division.
```

Content divisions and Paper Results are many-to-many. Topic synthesis reads
the Cards and `facts.md`; it does not make the folder hierarchy pretend that a
paper belongs to exactly one paragraph.

## Bib authority and aggregation

Each completed Result Bib contains exactly one entry copied verbatim from a
trusted publisher, Crossref, arXiv, or a person-supplied entry. A machine may
retrieve, subset, validate, deduplicate, and copy it; it may not invent fields.
The Result Card's `cite: @Key` MUST equal that entry's key.

Person-supplied metadata is NOT a person-supplied BibTeX entry. Turning a title,
author list, DOI, or venue fields into BibTeX is composition even when every
field was provided. Without a complete verbatim entry or an authoritative
BibTeX export, the Result may retain its Card/facts but MUST stay `blocked` or
`unresolved`; it cannot claim `complete`.

The Topic Page Bib is derived:

```text
results/*/*.bib
      -> validate complete Results
      -> deduplicate exact entries
      -> reject key/DOI conflicts
      -> stable sort by Bib key
evidence/bibex/<topic>.bib
```

Only `status: complete` Results enter the union. Verification or correction
lands in the Result Bib first, then the aggregate is rebuilt. Never edit the
derived Topic Page Bib as the authority.

The Result is not Page evidence merely because it exists under `results/`.
Aggregation is the binding step that admits a complete, validated Result into
the Page Evidence lane.

## Legacy compatibility

Existing `sources.md` and `notes.md` remain readable. They are legacy or
derived topic indexes, not the authority for new work. Do not mass-split old
prose into Runs: a paper earns a new Result only when its canonical identity
and one-entry Bib can be verified.

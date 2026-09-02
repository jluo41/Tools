# Discovery Paper Run Contract (canonical specialization)

Load `../../../run/haipipe-run/SKILL.md` first for the neutral Level-4 identity,
Ticket/Result pairing, lifecycle, and audit invariants. This file is the ONE
authority for the Discovery Paper specialization inside a Discovery `tNN_`
Task Page. The lifecycle and type axes point here; specialists do not restate this
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

One Trigger may resolve to zero, one, or many Subjects. Zero opens no Run and
returns/logs an unresolved intake. Many MUST fan out to one Run per Subject.
One Run NEVER analyzes multiple papers. Trigger identity never owns RUNNAME;
the resolved Subject does.

## Hierarchy and the 1:1 spine

```text
bank  discoveries/
L1    bNN_<noun>_<qualifier>/                 Block
L2    jNN_<noun>_<qualifier>/                 Job
L3    tNN_<noun>_<qualifier>/                 Discovery Task Page
L4    runs/rNN_<author><year>_<paper>.sh
         <-> results/rNN_<author><year>_<paper>/
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

Before allocating, compare canonical Subject identity plus the frozen question,
instrument hashes, intent, and acceptance contract with existing runtimes. An
unchanged duplicate Trigger reuses the existing Run/Result and allocates no new
`rNN`; return or log the existing link without rewriting the Run's frozen
inputs. Resume or retry that Run only while those identity fields remain
unchanged. A material change always creates the superseding Run described above.

The four prefixes are one global identity. For a local `r01_...` under
`discoveries/b02_.../j03_.../t01_.../`, stamp both forms:

```text
compact   b02j03t01r01
readable  b02.j03.t01.r01
```

No level may use a bare `01_`; the letter is part of the durable address.

## ACQUIRE-cycle Run Profile

This profile is the executable detail for the `d1.acquire` row in
`lifecycle-map.md`:

```text
ALLOWED    paper-analysis · source-analysis
TARGET     exactly one resolved canonical Subject
TICKET     executable runs/<RUNNAME>.sh, authored by the Discovery creator
INPUTS     Task Page question/type, Trigger provenance, canonical Subject identity,
           and hashes of any reusable instrument
WORKER     the selected search/read/analyzer skill, CLI, API, or declared agent
RESULT     Result Card · facts.md · one-entry Bib · runtime.yaml; optional PDF/raw/trigger
ACCEPT     exact stem pair, executable Ticket, truthful runtime, complete artifacts,
           canonical identity, cite/Bib equality, and verbatim Bib provenance
PROMOTION  SYNTHESIZE binds the Result into the root Page and the Evidence
           plugin builds the deterministic aggregate Bib
REOPEN     a materially changed Subject, analysis question, frozen instrument, or
           acceptance contract allocates a new Run with supersedes:
```

`paper-analysis` is used when `subject.kind: paper`; `source-analysis` is used
when a report, dataset, webpage, or other non-paper source is itself the
evidence object. A Trigger-resolution episode may commission several Runs but
does not receive its own Run identity.

## Folder shape

```text
<task>/
├── <task>.md                          Page Face: article synthesis
├── discovery.yaml                     Task Face manifest
├── outline/                           optional Page planning material
├── evidence/bibex/<task>.bib          DERIVED union of completed Result bibs
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

`scripts/` exists only when the Task Page owns a reusable instrument. Low-level
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

Every paired Run/Result, at every state, requires the ticket, `runtime.yaml`,
and one resolved canonical Subject. `unresolved` means analysis, retrieval, or
authoritative Bib resolution failed after the Subject was known; it never means
a Subject-free Trigger placeholder. A `complete` Result additionally requires:

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
- runtime omits `family: discovery`, or `operation` does not match the Subject
  kind (`paper-analysis` for papers; `source-analysis` otherwise);
- the Task path is not `discoveries/bNN_.../jNN_.../tNN_.../`, the Page stem
  differs from the Task folder, or runtime omits/mismatches the full readable
  and compact BJTR address;
- the Bib entry was composed from model memory rather than copied from a
  trusted publisher/index/person source.

`paper.pdf`, `trigger.md`, and `raw.md` are optional. An `unresolved` or
`blocked` Result is a truthful receipt, not a completed Paper Result; it is not
eligible for evidence aggregation.

## Runtime receipt

At minimum:

```yaml
run: r01_chen2025_trace
address: b02.j03.t01.r01
address_compact: b02j03t01r01
family: discovery
operation: paper-analysis
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
  verification:
    status: verified
    by: "person:<identifier>"
    at: "2026-09-01T12:05:00-04:00"
executed_at: "2026-09-01T12:00:00-04:00"
```

Also record the dispatcher/worker calls and failure reason when applicable.
Never store credentials or private tokens.
`bib.verification.status` is `pending` or `verified`; missing means `pending`.
Only a person may set `verified`, together with `by` and `at`. A Result may be
technically `complete` while verification is pending, but the Discovery Task
cannot close with an epistemic `ok` or `inconclusive` outcome until every
promoted citation is verified.

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

The Task Page Bib is derived:

```text
results/*/*.bib
      -> validate complete Results
      -> deduplicate exact entries
      -> reject key/DOI conflicts
      -> stable sort by Bib key
evidence/bibex/<task>.bib
```

Only `status: complete` Results enter the union. Verification or correction
lands in the Result Bib first, then the aggregate is rebuilt. Never edit the
derived Task Page Bib as the authority.

The Result is not Page evidence merely because it exists under `results/`.
SYNTHESIZE validates promotion, and `haipipe-plugin-evidence` aggregation binds
the complete Result into the Page citation lane. There is no separate Bibex
plugin.

## Legacy compatibility

Existing `sources.md` and `notes.md` remain readable. They are legacy or
derived topic indexes, not the authority for new work. Do not mass-split old
prose into Runs: a paper earns a new Result only when its canonical identity
and one-entry Bib can be verified.

# Discovery Paper Run Contract (canonical specialization)

Load `../../../run/haipipe-run/SKILL.md` first for the neutral Level-4 identity,
Ticket/Result pairing, lifecycle, and audit invariants. This file is the ONE
authority for the Discovery Paper specialization inside a Discovery `tNN_`
Task Page. The lifecycle and type axes point here; specialists do not restate this
contract. If an older numbered description is encountered, use
`bjtr-alignment.md` for the hierarchy/capability retrofit; this file remains
the Level-4 Run/Result authority.

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
instrument versions, intent, and acceptance contract with existing runtimes. An
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

## D1 ACQUIRE Run Profile

This profile is the executable detail for the `d1.acquire` row in
`../../haipipe-discovery-inquiry/ref/workflow-table.md`:

```text
ALLOWED    paper-analysis · source-analysis
TARGET     exactly one resolved canonical Subject
TICKET     executable runs/<RUNNAME>.sh, authored by the Discovery creator
INPUTS     Task Page question/type, frozen candidate-rule version, Trigger
           provenance, canonical Subject identity, and the path and version of
           any reusable instrument
WORKER     the selected search/read/analyzer skill, CLI, API, or declared agent
RESULT     Result Card · facts.md · one-entry Bib · runtime.yaml; optional PDF/raw/trigger
ACCEPT     exact stem pair, executable Ticket, truthful runtime, complete artifacts,
           canonical identity, cite/Bib equality, verbatim Bib provenance, and
           for paper-source-v2 a machine-readable + human-readable source-access pair
PROMOTION  D1 SYNTHESIZE binds direct Result/cite lineage into the Page plan;
           CONTENT writes the root Page; the Outline
           workbench builds the deterministic aggregate Bib
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
├── draft/                           Page planning + Evidence Workspace
│   └── evidence/
│       └── bibex/<task>.bib            DERIVED union of completed Result bibs
├── scripts/                           optional reusable instrument
├── runs/
│   ├── r01_chen2025_trace.sh          executable D1 ticket
│   └── rp00_mermaid-structure.md      optional Page-owned interaction record
└── results/
    ├── r01_chen2025_trace/            D1 Result
    └── rp00_mermaid-structure/        optional Page-owned Result
        ├── r01_chen2025_trace.md      Paper/Source Card readout
        ├── r01_chen2025_trace.bib     exactly one authoritative entry
        ├── facts.md                   atomic reusable findings
        ├── source-access.json         article/index/search/full-text routes
        ├── source-access.md           same routes, human-clickable
        ├── abstract.md                optional retrieved abstract
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

New paper Runs write `result_contract: paper-source-v2`. For that contract,
completion also hard-fails when `source-access.json` or `source-access.md` is
missing, when the access record does not identify the DOI/canonical landing
page and Bib source, or when it omits exact-title Google Scholar and Google
search URLs. These search URLs help a person inspect or export a record; they
are not authoritative source or claim support. Historical Results without a
`result_contract` remain readable under the preceding contract and must not be
silently rewritten.

The checker is intentionally compatibility-tolerant: it cannot infer from a
filesystem alone whether an omitted contract is historical or a newly authored
Result. Therefore the D1 creator/search route is the enforcement point for new
paper Results and MUST hold a new completion that lacks
`result_contract: paper-source-v2`; a green compatibility check alone is not
evidence that the new paper-source contract was satisfied.

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
result_contract: paper-source-v2
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
source_access:
  manifest: source-access.json
  summary: source-access.md
analysis:
  reading_depth: abstract
  claim_support: pending
  locator_status: pending
bib:
  source: "https://proceedings.neurips.cc/.../Bibtex"
  mode: verbatim_copy
  verification:
    status: verified
    by: "person:<identifier>"
    criteria_version: "discovery-bib-verification/1"
    at: "2026-09-01T12:05:00-04:00"
executed_at: "2026-09-01T12:00:00-04:00"
```

Also record the dispatcher/worker calls and failure reason when applicable.
Never store credentials or private tokens.
When `analysis.claim_support` or `analysis.locator_status` is assessed rather
than left `pending`, the same runtime records the provenance envelope for that
judgment:

```yaml
analysis:
  reading_depth: full-text
  claim_support: qualified
  locator_status: partial
  assessment:
    by: "agent:<name>/<model>/<session-id>"
    criteria_version: "paper-source-v2"
    at: "2026-09-01T12:10:00-04:00"
    input_snapshot:  # only when this source is outside the Run
      uri: "https://example.org/article.pdf"
      accessed: "2026-09-01"
```

The enclosing `run`, readable/compact addresses, `subject`, and source-access
manifest are the owning input record; the judgment does not need to duplicate
that identity. If the evaluator used material outside this Run's frozen
Subject and captured artifacts, add its URI and access date in the assessment
block (no content hash). For an appraisal using `paper-analyzer`, set `criteria_version` to the
exact `paper-analyzer@<version>`; the Run's own identity remains the input
link. Keep prior assessment receipts when criteria or inputs change; a
material Discovery re-analysis receives a superseding Run.

`reading_depth` is evidence actually retrieved and inspected by this Run, not
the best link discovered. `full-text` is legal only when the Run captured or
read the full article. `claim_support` is `pending | supported | qualified |
unsupported`; `locator_status` is `pending | partial | complete`. Under
`paper-source-v2`, `supported` means inspected source content directly answers
the scoped claim; `qualified` means it bears on the claim but a stated scope,
reading-depth, or uncertainty limit narrows the answer; `unsupported` means
inspected content gives no support or reports contrary evidence; `pending`
means the evaluator has not made that assessment. `locator_status: partial`
means only some material facts/claims have direct page, section, table, or
figure locations; `complete` means every material fact/claim in the Result is
traceable to such a location or explicitly lacks one in the source. A
metadata-only or abstract Run may be technically complete but cannot present
full-text-only facts as established.
`bib.verification.status` is `pending` or `verified`; missing means `pending`.
Only a person may set `verified`, together with `by`,
`criteria_version: discovery-bib-verification/1`, and `at`. That version checks
the exact title, authors, venue, and locator against the named trusted source.
A Result may be
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

## Source access
- Article: canonical DOI or publisher landing page.
- PubMed: record when resolved, otherwise a DOI search.
- Google Scholar: exact-title search for inspection and BibTeX export.
- Google: exact-title web search.
- BibTeX: the venue, curated index, or reviewed person export used by this Result.
- Full text: lawful route when found; otherwise explicitly not found.

## Retrieval scope
- Reading depth: metadata-only | abstract | full-text.
- Claim support: pending | supported | qualified | unsupported.
- Locator: pending | partial | complete.

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

For new Results, the Card may link to `source-access.md` rather than repeat the
URLs, but the reading depth and claim/locator states must remain visible. Use
`scripts/paper_source_access.py` to produce the deterministic access pair. It
may query Crossref, PubMed, and OpenAlex; it only constructs Google/Scholar
navigation URLs and never scrapes them.

Content divisions and Paper Results are many-to-many. Topic synthesis reads
the Cards and `facts.md`; it does not make the folder hierarchy pretend that a
paper belongs to exactly one paragraph.

## Bib authority and aggregation

Each completed Result Bib contains exactly one entry copied verbatim from a
trusted venue, dblp, DOI/arXiv source, or a person-supplied entry. A machine may
retrieve, subset, validate, deduplicate, and copy it; it may not invent fields.
The Result Card's `cite: @Key` MUST equal that entry's key.

### Identity before entry

A resolved DOI, arXiv identifier, or exact dblp venue record is required BEFORE
an entry is selected. A title-only lookup can return a different paper:
Crossref answers the bibliographic
query `Large Language Models are Zero-Shot Rankers for Recommender Systems`
with `LLM-BL: Large Language Models are Zero-Shot Rankers for Bug Localization`
(`10.1109/icpc66645.2025.00064`) ranked FIRST, and the correct
`10.1007/978-3-031-56060-6_24` only third. Title mode therefore proposes
candidates for a person and writes nothing.

`scripts/paper_bib_fetch.py` owns this ladder and reuses `paper_runs.py`'s entry
grammar, so the writer and the checker cannot drift apart. From the repository
root its full path is:

```text
Tools/plugins/haipipe-toolkit/skills/discovery/haipipe-discovery/scripts/paper_bib_fetch.py
```

`Tools/` is a SYMLINK, so a plain `find Tools -name paper_bib_fetch.py` returns
nothing and the tooling looks absent. Use `find -L`, or the path above.

First choose the publication version. Cite the accepted conference or journal
version when its record is available. For computer-science work, inspect the
exact dblp `conf/` or `journals/` venue record first: confirm title, first
author, year, venue, and DOI when present. dblp also indexes CoRR/arXiv as a
separate publication; a CoRR hit is not evidence that the venue version was
selected. dblp covers computer science and can lag a newly accepted paper, so
absence there does not prove absence of a venue publication. When no matching
dblp venue record exists, use the venue/publisher's BibTeX export or the
resolved publication DOI. Use arXiv when the Subject really is a preprint.
Google Scholar is the last manual fallback and requires a full human metadata
check against the accepted source.

The routes:

```text
--doi           Crossref REST transform -> doi.org content negotiation -> DataCite
--arxiv         arxiv.org/bibtex/<id>
--dblp-bib-file a browser-saved one-record venue export, with --dblp-record
--publisher-url a venue's own .bib endpoint, e.g. proceedings.neurips.cc/...-Bibtex.bib
--bib-file      a person's or Scholar's export, with --source-url
--resolve-title proposes Crossref + OpenAlex + arXiv candidates, refuses, exits 2
```

dblp documents `https://dblp.org/rec/<key>.bib`, but a scripted request may
receive its bot-check HTML rather than BibTeX. Open the exact record in a
browser and save its own BibTeX export. Do not bypass that check or submit a
search/person bibliography containing multiple records. The import checks
the `DBLP:<key>` citation key, `biburl`, venue entry type, title, and exact year.
An export DOI must match the known publication DOI; a missing DOI is reported
for human review. A first-author surname mismatch blocks the import, and a venue
mismatch is reported for review. For a DOI-known
accepted venue Result:

```bash
python3 scripts/paper_bib_fetch.py \
  --dblp-bib-file <browser-saved-single-record.bib> \
  --dblp-record https://dblp.org/rec/conf/<venue>/<record> \
  --title '<accepted title>' --expected-year <year> \
  --expected-first-author '<surname>' --expected-venue '<venue>' \
  --expected-doi '<publication DOI>' \
  --result-dir <results/rNN_...>
```

For a venue record without a DOI, omit `--expected-doi` and keep the accepted
venue record as the Subject. `paper_result_build.py` can select
`--bib-from dblp --dblp-bib-file ... --dblp-record ...` when the venue DOI is
known; its DOI-driven builder does not represent a DOI-less venue identity.
Do not pass a preprint DOI to that builder and silently substitute a venue Bib.
The direct fetcher can import the DOI-less venue export into a separately
resolved Result.

`--resolve-title` EXITS 2 by design, because refusing to write is its whole
purpose. In a Run ticket written with `set -euo pipefail` that exit kills the
script after step one and the Run writes nothing. Guard it:

```bash
"$PY" "$FETCH" --resolve-title "$TITLE" || [ $? -eq 2 ]
```

`--resolve-title` covers three channels because Crossref indexes DOIs: an
arXiv-native paper or a pre-2022 proceedings record can be absent from it
while five wrong papers rank above the right one. Its output reports
`channels`, one state per channel, plus `degraded` and `strong_matches`. A
channel that answered `http-503` is NOT a channel that found nothing: OpenAlex
pauses anonymous search under load, and a degraded sweep that looks clean is
the silent-cap failure named in `source-format.md`. Read `channels` before
trusting a single hit, and re-run when `degraded` is true. `strong_matches`
counts candidates at or above 0.80 similarity: more than one means the title
is not unique and the publisher and year decide. Each candidate row carries
its channel, DOI, arXiv id, year, type, publisher and similarity, plus
`identifier_conflict`, which marks a row whose identifiers disagree with its
year. OpenAlex merges records: its top hit for `Attention Is All You Need`
carries arXiv `1706.03762` (2017) AND the DOI of a 2025 posting on another
server, under one work dated 2025. Never take a DOI from a conflicted row.

Crossref is first because a publisher may ignore `Accept: application/x-bibtex`:
`10.1038/s41746-026-03117-z` answers `302 text/html` at `doi.org` while Crossref
returns the correct entry. The fetcher refuses an HTML body, an entry count
other than one, a DOI that disagrees with the requested DOI, and a title whose
similarity to the expected title falls below `--min-title-similarity` (0.90),
except that a registered SHORT title is a match: publishers drop the subtitle,
so SAGE holds `The Face of Success` for an entry titled `The Face of Success:
Inferences From Chief Executive Officers' Appearance Predict Company Profits`.
That case warns instead, so a person confirms it is the same publication. The
prefix counts only when the shorter title has at least three words and fifteen
characters, so a fragment never stands in for a title.
It WARNS, without refusing, on a missing DOI, a URL-shaped key that `\citep{}`
cannot use, and a title that matches the expected one only after case folding.
`--strict` turns those warnings into refusals. Warnings do not block by default
because an arXiv preprint legitimately carries no DOI.

### A resolved DOI is not proof of identity

A DOI passed on the command line agrees with itself, so DOI-agreement proves
nothing, and a different paper carrying an IDENTICAL title scores 1.0 on the
similarity guard. `10.65215/2q58a426` is a real 2025 `posted-content` posting by
the Shenzhen Medical Academy of Research and Translation that reuses the exact
title `Attention Is All You Need`; it passes both guards with zero findings.

`--expected-year <YYYY>` is therefore a load-bearing guard for a title
collision. Pass it on every fetch. The entry's year must
fall within `--year-tolerance` (default 1) of it, or the fetch is refused.

Two further defences are always on. The fetcher reads the Crossref record and
reports `type`, `publisher`, `year`, `venue` and landing page in its summary
AND into `bib.record` in the receipt, including the landing page, so a
reviewer sees the Shenzhen publisher and can click straight through without
re-querying. A Crossref `type: posted-content` raises `subject-is-a-posting`,
because a preprint posting may legitimately BE the Subject but may never
silently stand in for a venue record.

Neither the fetcher's other guards nor `paper_runs.py check` compares an entry
against the `subject:` block it describes, so a same-title entry swapped into an
otherwise valid Result still checks green. `--expected-year` plus a reader's eye
on `bib.record` is how that is caught today.

### Bib source classes

`bib.source_class` records what the entry's provenance is worth:

```text
authoritative-export   crossref | doi-content-negotiation | datacite | arxiv | publisher
curated-index-export   dblp exact venue record, manually exported in a browser
person-export          a person's own export, including google-scholar-export
```

`publisher` is reached with `--publisher-url`, which GETs the venue's `.bib`
directly and requires an `application/x-bibtex` body. Do NOT route a publisher
export through `--bib-file`: that stamps `person-export` and makes the receipt
untrue, because no person was involved.

Google Scholar is never fetched by a script: it refuses automated clients with
`403` on the first request, and its export omits the DOI and lowercases the
title. Its legitimate use is a person opening it in a browser only after the
accepted venue, dblp, publisher, DOI, and arXiv routes cannot provide the
needed entry. Before promotion, compare the complete author list, title,
publication year, venue, volume/pages or article number, and DOI against the
accepted record; do not repair uncertain metadata by guessing. Pass that
export through `--bib-file --source-url`. The weaker class stays on the receipt
so a reader can see which Results rest on it. Rate limits count per public IP,
so scripted Scholar access would also break a person's own browsing from the
same network.

If `bibtex-verifier` is available, run it after rebuilding the Task Bib:

```bash
bibverify <derived-task.bib> --json --output <review-report.md>
```

It compares selected
metadata through Crossref, DataCite, and OpenAlex, so use its per-key findings
to return to the owning Result Bib. It does not query dblp or certify that a
claim is supported. A `NOT_FOUND` or `UNVERIFIED` result is a review item,
especially for a DOI-less dblp venue record, not permission to replace the
accepted citation with a preprint or a Google Scholar guess. The report never
sets `bib.verification.status: verified`; the person-reserved check above still
applies.

Refetching the SAME entry preserves an existing `bib.verification`. A DIFFERENT
entry resets it to `pending`, because a person's reading of the old entry does
not carry over to a new one.

Person-supplied metadata is NOT a person-supplied BibTeX entry. Turning a title,
author list, DOI, or venue fields into BibTeX is composition even when every
field was provided. Without a complete verbatim entry from an accepted source,
the Result may retain its Card/facts but MUST stay `blocked` or
`unresolved`; it cannot claim `complete`.

The Task Page Bib is derived:

```text
results/*/*.bib
      -> validate complete Results
      -> deduplicate exact entries
      -> reject key/DOI conflicts
      -> stable sort by Bib key
draft/evidence/bibex/<task>.bib
```

Only `status: complete` Results enter the union. Verification or correction
lands in the Result Bib first, then the aggregate is rebuilt. Never edit the
derived Task Page Bib as the authority.
Aggregation may normalize only the ordering and blank separators between whole
entries. It must not rewrite an entry's fields or use the aggregate as proof
that the authoritative Result entry was person-verified.

The Result is not Page evidence merely because it exists under `results/`.
D1 SYNTHESIZE rebuilds the derived aggregate through
`haipipe-workbench-page/ref/evidence/citations.md`, then dispatches the Page
workflow. The D1 root Page uses direct Result/Card/cite lineage and does not
declare a redundant typed CITE item or local Evidence Item Run for its own
Results. A consumer Page may use a Discovery Result as Supporting evidence and
owns any local Evidence Item Run in the consumer Folder. The standalone
Evidence and Bibex workbenches are compatibility redirects, not authorities.

Discovery's `rNN` subset of the shared `runs/` ↔ `results/` lanes remains the
primary analysis receipt. Page-owned `rpNN` records/results are governed by the
Page workflow and are not part of the Discovery inventory. `draft/evidence/`
is the shared Page Evidence Workspace: it records derived citation material,
but it does not replace or duplicate a Paper/Source Result. A root `<task>/evidence/`
lane is invalid for new or current v6 work.

## Legacy compatibility

Existing `sources.md` and `notes.md` remain readable. They are legacy or
derived topic indexes, not the authority for new work. Do not mass-split old
prose into Runs: a paper earns a new Result only when its canonical identity
and one-entry Bib can be verified.

# Discovery — architecture

Discovery is the durable external-evidence executor. Its article unit is a
`tNN_` Task Page with a Page Face and a Task Face, addressed inside BJTR.

Runtime authority lives in:

~~~text
haipipe-discovery/SKILL.md
haipipe-discovery/ref/lifecycle-map.md
haipipe-discovery/ref/paper-run-contract.md
haipipe-discovery/ref/discovery-yaml-schema.md
~~~

This file explains their relationship; when details differ, those runtime refs
win.

## Four levels

~~~text
bank        discoveries/
L1 Block    bNN_<noun>_<qualifier>/
L2 Job      jNN_<noun>_<qualifier>/
L3 TaskPage tNN_<noun>_<qualifier>/
L4 Run      runs/rNN_<author><year>_<paper>.sh <-> results/rNN_.../
~~~

L1 is a broad evidence domain; L2 is a self-contained inquiry/campaign; L3 owns
one article question and `discovery_type`; L4 owns one canonical evidence Subject, normally
one paper. Result is the generated projection of Run, not an additional level.

All four levels use `<level-letter><NN>_<noun>_<qualifier>`. Their joined
address is `bNNjNNtNNrNN`; `discoveries/` is a bank and contributes no segment.

## Two Faces

~~~text
Page Face                              Task Face
tNN_<task>.md                         discovery.yaml
outline/                               scripts/ optional
evidence/bibex/tNN_<task>.bib          runs/
topic-level synthesis                  results/
~~~

Configuration is not a Folder kind. Each workflow phase configures the Face it
owns. The manifest plans the Topic; a .sh ticket plans one Paper Run.

## Three orthogonal dimensions

~~~text
Hierarchy   Block -> Job -> Task Page -> Run
Workflow    D1: SCOPE -> PREPARE? -> ACQUIRE <-> SYNTHESIZE -> CLOSE
Page Type   source-map | source-reading | topic-summary | prior-art-verdict |
            counterevidence-review | landscape-review | benchmark-landscape |
            ideation | novelty-verdict
~~~

The Page Type says what article the root Page is writing. It does not add a
folder level and it does not define a Run. Search, Review, and Idea remain
specialist routes: Search resolves evidence Subjects, Review synthesizes
completed Results, and Idea works at Topic level while using Paper Runs for
novelty evidence. Worker/API/CLI calls are runtime detail inside a Run receipt.

## D1 Cycle × Run map

~~~text
SCOPE       no Run
PREPARE     no Run; scripts/ are supporting instruments
ACQUIRE     paper-analysis | source-analysis × N admitted Subjects
SYNTHESIZE  no Run; promotes Results into Page/typed record/Evidence Bib
CLOSE       no Run; checks and reconciles the two Faces

Total R = N admitted canonical Subjects
~~~

Search queries, candidate rows, synthesis passes, and idea generation are not
Runs. A Run begins only after one canonical evidence Subject is admitted.

## Trigger and Subject

~~~text
Trigger -> resolve -> canonical Subject -> numbered Run -> same-stem Result
~~~

A Trigger may be a paper URL, short link, social post, DOI, PDF, citation, or
request. It explains why work started. The canonical Subject owns RUNNAME and
the Bib entry. One Trigger may fan out to many Subjects; one Run never bundles
multiple papers.

## Evidence authority

Each complete Result owns:

~~~text
<RUNNAME>.md
facts.md
runtime.yaml
<RUNNAME>.bib   exactly one authoritative entry
~~~

PDF, raw extraction, and captured Trigger are optional. Result Card cite key
and Bib key are identical. `haipipe-plugin-evidence` owns the deterministic
derived union of complete Result Bibs; conflicts hard-fail.

## Synthesis

Topic Content and Paper Results are many-to-many. A paper may support several
divisions, and a division normally synthesizes several papers. The root Page
is always the human-facing article. Optional `summary.md`, `verdict.md`,
`landscape.md`, and `ideas.md` are typed Task-side synthesis records, not rival
Pages or Runs. The Page links to Results; it does not copy their entire
readouts into a flat notes ledger.

## Compatibility

Existing sources.md and notes.md remain readable as legacy/derived indexes.
They are not the authority for new evidence. Old prose is not mass-converted:
a paper earns a Result only when canonical identity and authoritative BibTeX
can be verified.

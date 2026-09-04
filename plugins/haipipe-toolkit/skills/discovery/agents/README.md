# Discovery agents

The agents execute the contract owned by haipipe-discovery. They do not define
an alternate folder shape.

~~~text
discoveries/ -> bNN_ Block -> jNN_ Job -> tNN_ Task Page -> rNN_ Run
compact address: bNNjNNtNNrNN
~~~

## Roster

| Agent | Owns | Never owns |
|---|---|---|
| orchestrator | QA/FULL/ENRICH routing, dispatch, final state | paper search details |
| creator | all Task Page/Run/Result writes | reviewing its own work |
| reviewer | Plan/Run/Bib/Report gates | searching or creating evidence |
| search worker | one read-only channel/verification batch | relevance, Runs, writes |

## Flow

~~~text
Plan     creator -> reviewer
Build    creator -> reviewer                 optional
Add      creator resolves Trigger -> one Run/Result pair per Subject
Run      creator/type specialist -> reviewer
Report   checker -> Bib builder -> typed root Page synthesis -> reviewer
~~~

`discovery_type` chooses the root article form; Search, Review, and Idea are
derived specialist routes. Only Execute creates Runs, one for each admitted
canonical Subject. Plan, Build, Page synthesis, and Report do not create Runs.

ENRICH follows the same Level-4 law but adds the minimum new Paper Runs to an
existing Task Page. It never appends anonymous source prose.

## Truth gates

~~~text
runs/<RUNNAME>.sh <-> results/<RUNNAME>/runtime.yaml
runtime family: discovery; operation matches paper/source Subject kind
runtime address: bNN.jNN.tNN.rNN and bNNjNNtNNrNN
complete -> <RUNNAME>.md + facts.md + one-entry <RUNNAME>.bib
Card cite key == Bib key
Task Page Evidence Bib == deterministic union of complete Result Bibs
~~~

QA remains a side door governed by haipipe-discovery/fn/qa.md. A consumer never
writes into the Discovery bank.

# Discovery agents

The agents execute the contract owned by haipipe-discovery. They do not define
an alternate folder shape.

## Roster

| Agent | Owns | Never owns |
|---|---|---|
| orchestrator | QA/FULL/ENRICH routing, dispatch, final state | paper search details |
| creator | all Topic/Run/Result writes | reviewing its own work |
| reviewer | Plan/Run/Bib/Report gates | searching or creating evidence |
| search worker | one read-only channel/verification batch | relevance, Runs, writes |

## Flow

~~~text
Plan     creator -> reviewer
Build    creator -> reviewer                 optional
Add      creator resolves Trigger -> one Run/Result pair per Subject
Run      creator/type specialist -> reviewer
Report   checker -> Bib builder -> creator synthesis -> reviewer
~~~

ENRICH follows the same Level-4 law but adds the minimum new Paper Runs to an
existing Topic. It never appends anonymous source prose.

## Truth gates

~~~text
runs/<RUNNAME>.sh <-> results/<RUNNAME>/runtime.yaml
complete -> <RUNNAME>.md + facts.md + one-entry <RUNNAME>.bib
Card cite key == Bib key
Topic Evidence Bib == deterministic union of complete Result Bibs
~~~

QA remains a side door governed by haipipe-discovery/fn/qa.md. A consumer never
writes into the Discovery bank.

1-probe — the PROBE phase (hub + three harvesters)
====================================================

ONE probe pipeline (JL 2026-07-07 harvester ruling). **Evidence work has exactly ONE exit: the
hub.** The three lane workers are the HARVEST step — they transcribe what already landed into
the paper-side working docs. Paper-side may FOLLOW pointers; only a DISPATCHED executor may FIND
things.

```
haipipe-paper-probe (hub)   ① ORGANIZE → ② MATCH → ③ DISPATCH → ④ POINT → ⑤ INTERPRET
  ② MATCH      grep the bank's QA corpus ({tasks,discoveries}/**/QA/*.md), and READ the hits.
               Most sections close HERE (T2 REUSE) — a q-executor is the EXCEPTION.
  ③ DISPATCH   only what MATCH could not close. The section's `q-executor:` block, VERBATIM:
                 Agent(haipipe-task-orchestrator-agent)         internal work
                 Agent(haipipe-discovery-orchestrator-agent)    external evidence
               Their CLEAN CONTEXT is the wall. The SWEEP is ② MATCH, and dispatch
               goes direct.
  ④ POINT      the section's `target:` → the answering QA file <task-folder>/QA/<n>-<slug>.md
  ⑤ INTERPRET  the section's `a-consumer:` → 1-claims.md flips → the lanes pay out:
     haipipe-paper-probe-citation   source anchors → _CITATION_{stage}.md
     haipipe-paper-probe-values     value anchors  → _VALUES_{stage}.md
     haipipe-paper-probe-display    unit links     → _DISPLAY_{stage}.md + tex links
```

The probe FILE (`1-probes/PPNN_<topic>.md`, one file per TOPIC, one SECTION per question;
anatomy owned by `../../../probe/haipipe-probe/SKILL.md`) is the single source of truth: its
`q-executor:` at ORGANIZE, its `target:` at POINT, its `a-consumer:` + lane lines at INTERPRET.
A CLAIM's status is not in it — that lives in `0-lifecycle/1-claims/1-claims.md`.

Enforcement is mechanical (`check-probe-cards.sh`, run at VERIFY and re-run by the CHECK gate):
a `planned` section FAILs (probe-not-run), a `harvest: OWED` lane line FAILs (harvest skipped),
an unresolvable `target:` FAILs, and a markdown table or bibtex in a probe file FAILs. A green
PROBE over any of these is a defect.

Per-stage worker/mode map, seed/claims specifics, strip forms:
`haipipe-paper-probe/ref/per-stage-dispatch.md`. Harvest dispatch + literal acceptance greps:
`haipipe-paper-probe/ref/harvest-acceptance.md`.

Not user-facing: users invoke stage skills (seed, claims, ...); stages call the hub; the hub
dispatches the executor orchestrators and the harvesters.

(The per-section playbooks doc that previously occupied this file was migration debris; it is
archived at `../../_archive/README-sections-playbooks.md`.)

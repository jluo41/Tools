haipipe-data — Changelog
========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.2.0] — 2026-07-04

- deep-audit fixes: Fn-type ownership corrected (HumanFn=Stage 2 with RecordFn, TriggerFn=Stage 3 with CaseFn — dispatcher had them one stage early, contradicting every fn/ doc and shipped template); haipipe-data-external + haipipe-data-remote WIRED into the dispatcher (specialists list, keyword map, aliases — both existed on disk unrouted); README file map rewritten (ref/1-4.md + templates/N-stage/ were fiction); fn-2-cook template paths -> specialist-local templates/config.yaml; fn-2-cook CaseArgs schema aligned to the shipped case template (case_set_version at CaseArgs level, operation blocks); 0-RawStore -> 0-RawDataStore; fan-out summary 5-line; 0-rawdata alias -> raw dashboard Panel 0.
- CONFIRMED by JL 2026-07-05, both arbitrations: Fn ownership (JL: "human fn should go to the Stage 2: Source to Record. it should be in the Record Stage.") and external/remote wiring (JL: "yes, please do for them."). Review thread archived here and removed from SKILL.md.

## [1.1.0] — 2026-06-11

- update notebook section — retire 0_data_nb, add partition params (NUM_PARTITIONS/PARTITION_INDEX/NUM_WORKERS), CLI alternative, MIMIC-IV worked example; add partition mode to fn-2-cook.md for Record/Case/AIData.

## [1.0.0] — 2026-05-31

- baseline metadata added.

Task-type inference — full keyword reference
============================================

The complete keyword lists for Step 3a (3) KEYWORD-INFERRED in ../SKILL.md.
First match (left-to-right in the args) wins. EXPLICIT (positional) and
SCRIPT-INFERRED (imports/content) both outrank keyword inference — see SKILL.md
Step 3a for the full cascade.

```
┌────────────┬─────────────────────────────────────────────────────────────────┐
│ raw        │ raw · ingest · extract table · databricks pull · catalog ·      │
│            │ 0-RawDataStore · database 拿数据                                     │
│ data       │ build · source · record · dataset · cgm ·                       │
│            │ pipeline 1·2·3·4 · fn build                                     │
│ algo       │ smoke · smoke-test · verify algorithm · test algo · algo dev ·  │
│            │ algo class · forward pass · loss class                          │
│ fit        │ train · training · fit · sweep · hyperparam · lr · epoch ·      │
│            │ model size · pretrain · finetune · ft                           │
│ eval       │ eval · evaluate · evaluation · score · scoring · metrics ·      │
│            │ mae · rmse · accuracy · horizon                                 │
│ display    │ figure · table · plot · paper figure · paper table · panel ·    │
│            │ main figure · ablation table                                    │
│ individual │ subject · patient · individual · one user · single subject ·    │
│            │ cgm trace · treatment event · view                              │
│ agent      │ agent · llm · prompt · claude · gpt · tool use · system prompt  │
│ endpoint   │ endpoint · deploy · package · serve · sagemaker · databricks ·  │
│            │ mlflow · Endpoint_Set · inference api                           │
├────────────┼─────────────────────────────────────────────────────────────────┤
│ STATA      │ stata · do-file · .do · cms · case-pipeline · trigger cases ·   │
│ (engine)   │ analysis table · reg · regression · ols · iv · neat · bene_info │
└────────────┴─────────────────────────────────────────────────────────────────┘
```

Stata engine-detect → DELEGATE to `/haipipe-task-for-stata` (it owns stage
disambiguation): `Skill("haipipe-task-for-stata", args="<remaining_args> [--auto]")`.

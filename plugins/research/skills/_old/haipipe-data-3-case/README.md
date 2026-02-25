haipipe-data-3-case
===================

Layer 3: Case Processing -- extracts event-triggered features from RecordSets.

---

Quick Reference
---------------

```
/haipipe-data-3-case load           Inspect existing CaseSet (read-only)
/haipipe-data-3-case cook           Run Case_Pipeline with a YAML config
/haipipe-data-3-case design-chef    Create new TriggerFn/CaseFn via builder
/haipipe-data-3-case design-kitchen Upgrade Case_Pipeline infrastructure
```

---

Layer Diagram
-------------

```
Layer 1: Source          Raw files -> standardized tables
    |
Layer 2: Record          SourceSet -> 5-min aligned patient records
    |
Layer 3: Case    <---    RecordSet -> event-triggered feature extraction
    |
Layer 4: AIData          CaseSet -> ML-ready datasets (train/val/test)
    |
Layer 5: Model           AIData -> trained model artifacts
    |
Layer 6: Endpoint        Model -> deployment packages
```

---

Key Paths
---------

```
Pipeline:    code/haipipe/case_base/case_pipeline.py
Generated:   code/haifn/fn_case/fn_trigger/*.py             (DO NOT EDIT)
             code/haifn/fn_case/case_casefn/*.py             (DO NOT EDIT)
Builders:    code-dev/1-PIPELINE/3-Case-WorkSpace/*.py       (edit these)
Store:       _WorkSpace/3-CaseStore/
Config:      config/test-haistep-ohio/3_test_case.yaml
```

---

Files
-----

```
SKILL.md             Full rules, feature naming, concrete code, MUST DO / MUST NOT
README.md            This file (quick reference)
1-load.md            Rules for inspecting CaseSets
2-cook.md            Rules for running Case_Pipeline
3-design-chef.md     Rules for creating new TriggerFn/CaseFn builders
4-design-kitchen.md  Rules for modifying Case_Pipeline framework
templates/
  config.yaml        Annotated config template
```

---

See Also
--------

- **haipipe-data-1-source**: How raw data becomes SourceSets
- **haipipe-data-2-record**: How SourceSets become RecordSets (input to this layer)
- **haipipe-data-4-aidata**: How CaseSets become ML-ready datasets

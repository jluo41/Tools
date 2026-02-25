haipipe-data-4-aidata
=====================

Layer 4: AIData Processing -- converts CaseSets into ML-ready datasets.

---

Quick Reference
---------------

```
/haipipe-data-4-aidata load           Inspect existing AIDataSet (read-only)
/haipipe-data-4-aidata cook           Run AIData_Pipeline with a YAML config
/haipipe-data-4-aidata design-chef    Create new TfmFn/SplitFn via builder
/haipipe-data-4-aidata design-kitchen Upgrade AIData_Pipeline infrastructure
```

---

Layer Diagram
-------------

```
Layer 6: Endpoint           Deployment packaging
    |
Layer 5: Model              Model training reads AIDataSet splits
    |
Layer 4: AIData  <---       CaseSet -> ML-ready datasets (train/val/test)
    |
Layer 3: Case               RecordSet -> event-triggered feature extraction
    |
Layer 2: Record             SourceSet -> 5-min aligned patient records
    |
Layer 1: Source             Raw files -> standardized tables
```

---

Key Paths
---------

```
Pipeline:    code/haipipe/aidata_base/aidata_pipeline.py
Asset:       code/haipipe/aidata_base/aidata_set.py
Generated:   code/haifn/fn_aidata/entryinput/*.py           (DO NOT EDIT)
             code/haifn/fn_aidata/entryoutput/*.py           (DO NOT EDIT)
             code/haifn/fn_aidata/split/*.py                 (DO NOT EDIT)
Builders:    code-dev/1-PIPELINE/4-AIData-WorkSpace/*.py     (edit these)
Store:       _WorkSpace/4-AIDataStore/
Config:      tutorials/config/test-haistep-ohio/4_test_aidata-cgm-tedata.yaml
```

---

Files
-----

```
SKILL.md             Full rules, config pattern, concrete code, MUST DO / MUST NOT
README.md            This file (quick reference)
1-load.md            Rules for inspecting AIDataSets
2-cook.md            Rules for running AIData_Pipeline
3-design-chef.md     Rules for creating new TfmFn/SplitFn builders
4-design-kitchen.md  Rules for modifying AIData_Pipeline framework
templates/
  config.yaml        Annotated config template
```

---

See Also
--------

- **haipipe-data-1-source**: How raw data becomes SourceSets
- **haipipe-data-2-record**: How SourceSets become RecordSets
- **haipipe-data-3-case**: How RecordSets become CaseSets (input to this layer)
- **haipipe-nn-0-overview**: How AIDataSets feed into model training (Layer 5)

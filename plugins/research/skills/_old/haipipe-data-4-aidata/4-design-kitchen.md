Subcommand: design-kitchen
==========================

Purpose: Upgrade AIData_Pipeline infrastructure (code/haipipe/aidata_base/).
This is advanced -- most users do not need this.

Only use this when the pipeline framework itself needs changes, not when
you just need a new TfmFn (use design-chef for that).

---

What You Edit
=============

```
code/haipipe/aidata_base/
+-- aidata_pipeline.py    Pipeline orchestrator (run, split, transform)
+-- aidata_set.py         AIDataSet asset class (save, load, I/O)
+-- aidata_utils.py       Utility functions
+-- builder/
    +-- tfmfn.py           TfmFn dynamic loader (input + output transforms)
    +-- splitfn.py         SplitFn dynamic loader
```

These files are **EDITABLE** (not generated). Changes take effect immediately.

---

Architecture
============

The AIData layer uses a **three-class architecture**:

```
+--------------------------------------------------+
|  AIData_Pipeline  (aidata_pipeline.py)            |
|  - __init__(config, SPACE, cache_combined_case)   |
|  - run(case_set, ...): Full transform pipeline    |
|  - Split: df_tag -> split_ai column tagging       |
|  - Input: case features -> model-ready format     |
|  - Output: case features -> labels/targets        |
|  - Vocabulary: builds CF_to_CFVocab + feat_vocab  |
+------------------+-------------------------------+
                   | uses
+------------------v-------------------------------+
|  TfmFn loader   (builder/tfmfn.py)               |
|  - Dynamic import from code/haifn/fn_aidata/      |
|    entryinput/ and entryoutput/                   |
|  - Loads build_vocab_fn and tfm_fn functions      |
|                                                    |
|  SplitFn loader (builder/splitfn.py)              |
|  - Dynamic import from code/haifn/fn_aidata/split/|
|  - Loads dataset_split_tagging_fn                 |
+------------------+-------------------------------+
                   | produces
+------------------v-------------------------------+
|  AIDataSet  (aidata_set.py)                       |
|  - Inherits from Asset base class                 |
|  - dataset_dict: Dict[str, HF_Dataset]            |
|  - CF_to_CFVocab: per-CaseFn vocabulary           |
|  - feat_vocab: feature vocabulary                 |
|  - HuggingFace Datasets format (Parquet)          |
|  - save_to_disk / load_from_disk / load_asset     |
+--------------------------------------------------+
```

**Three-class pattern:** Pipeline + Fn Loaders (Tfm + Split) + Asset Set

---

Key Contracts
=============

**Pipeline -> Fn Loader contract:**

- TfmFn loader provides: `tfm_fn`, `build_vocab_fn` (input), or `tfm_fn` (output)
- SplitFn loader provides: `dataset_split_tagging_fn`
- Pipeline calls `build_vocab_fn(InputArgs, CF_to_CFVocab)` during __init__
- Pipeline calls input `tfm_fn(case_features, InputArgs, CF_to_CFvocab, feat_vocab)` per case
- Pipeline calls output `tfm_fn(case, OutputArgs)` per case
- Pipeline calls `dataset_split_tagging_fn(df_tag, SplitArgs)` once

**Pipeline -> AIDataSet contract:**

- Pipeline creates AIDataSet with dataset_dict, CF_to_CFVocab, feat_vocab
- AIDataSet saves cf_to_cfvocab.json and feat_vocab.json at root (NOT in vocab/)
- AIDataSet.load_from_disk(path=..., SPACE=...) restores everything

**AIDataSet -> Model Layer contract:**

- Model layer reads dataset_dict splits ('train', 'validation', 'test-id', 'test-od')
- Model layer reads feat_vocab for architecture configuration
- Model layer reads CF_to_CFVocab for token decoding

---

When To Use This
================

- **Adding** new split strategies beyond the SplitFn interface
- **Modifying** the vocabulary building mechanism
- **Adding** new serialization formats (beyond Parquet)
- **Changing** the transform pipeline execution order
- **Adding** progressive enrichment features
- **Modifying** HuggingFace Dataset integration
- **Changing** how pipeline.run() dispatches processing paths

---

MUST DO
=======

- **Present** plan to user -> get approval
- **Maintain** backward compatibility with existing TfmFn/SplitFn files
- **Test** thoroughly with existing transforms and splits
- **Keep** the Asset I/O contract: load_from_disk(path=..., SPACE=...)
- **Keep** AIDataSet naming: `<aidata_name>/@<aidata_version>`
- **Preserve** dataset_dict interface (Dict[str, HF_Dataset])
- **Preserve** vocab file contract: cf_to_cfvocab.json and feat_vocab.json at root
- **Activate** .venv and run `source env.sh` before testing

---

MUST NOT
========

- **NEVER break** the Asset I/O contract (save/load must remain compatible)
- **NEVER change** stage-to-stage interface without updating Case and Model layers
- **NEVER modify** code/haifn/ (that is generated code -- use builders)
- **NEVER change** input tfm_fn signature: (case_features, InputArgs, CF_to_CFvocab, feat_vocab)
- **NEVER change** output tfm_fn signature: (case, OutputArgs)
- **NEVER change** split fn signature: dataset_split_tagging_fn(df_tag, SplitArgs)
- **NEVER change** build_vocab_fn signature: (InputArgs, CF_to_CFVocab)
- **NEVER change** split output format without updating all SplitFn builders
- **NEVER introduce** a vocab/ subdirectory (files are at root)

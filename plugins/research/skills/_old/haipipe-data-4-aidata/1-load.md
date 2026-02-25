Subcommand: load
================

Purpose: Inspect existing AIDataSet assets (read-only).

Use this when you need to understand ML-ready datasets, verify splits,
check feature dimensions, or debug data quality issues.
This subcommand applies to any domain -- any AIDataSet, any transform or split method.

---

What To Read
============

AIDataSets live under `_WorkSpace/4-AIDataStore/`:

```
_WorkSpace/4-AIDataStore/
+-- <aidata_name>/
|   +-- @<aidata_version>/
|       +-- train/                HuggingFace Dataset (Parquet format)
|       +-- validation/
|       +-- test-id/
|       +-- test-od/
|       +-- cf_to_cfvocab.json   Per-CaseFn vocabulary
|       +-- feat_vocab.json      Feature vocabulary from build_vocab_fn
|       +-- manifest.json
+-- ...
```

To see what actually exists:
```bash
ls _WorkSpace/4-AIDataStore/                               # available AIDataSets
ls _WorkSpace/4-AIDataStore/<aidata_name>/                 # versions
ls _WorkSpace/4-AIDataStore/<aidata_name>/@<version>/      # splits and vocab
```

**Directory naming:** `<aidata_name>/@<aidata_version>/`

**CRITICAL:** Vocabulary files are **cf_to_cfvocab.json** and **feat_vocab.json**
at the root of the AIDataSet directory. There is NO vocab/ subdirectory.

---

Load Pattern (Correct API)
===========================

```python
source .venv/bin/activate
source env.sh

python -c "
from haipipe.aidata_base.aidata_set import AIDataSet

# Load existing AIDataSet -- pass full path, not set_name + store_key
aidata_set = AIDataSet.load_from_disk(
    path='_WorkSpace/4-AIDataStore/<aidata_name>/@<aidata_version>',
    SPACE=SPACE
)
# or equivalently:
aidata_set = AIDataSet.load_asset(
    path='_WorkSpace/4-AIDataStore/<aidata_name>/@<aidata_version>',
    SPACE=SPACE
)

# Inspect splits via dataset_dict
for split_name, dataset in aidata_set.dataset_dict.items():
    print(f'{split_name}: {len(dataset)} samples')
    print(f'  Features: {dataset.column_names}')
    sample = dataset[0]
    for key, value in sample.items():
        if hasattr(value, '__len__'):
            print(f'  {key}: len={len(value)}')
        else:
            print(f'  {key}: {type(value).__name__}')
    print()

# Inspect vocabulary files
print('CF_to_CFVocab:', list(aidata_set.CF_to_CFVocab.keys()))
print('feat_vocab keys:', list(aidata_set.feat_vocab.keys()))

# Pretty print summary
aidata_set.info()
"
```

**WRONG -- this API does NOT exist:**

```python
# WRONG: load_from_disk does NOT accept set_name= or store_key=
aidata_set = AIDataSet.load_from_disk(set_name='...', store_key='...')
```

---

What cf_to_cfvocab.json Contains
=================================

Per-CaseFn vocabulary mapping. Each CaseFn has vocab_size, tid2tkn, tkn2tid:

```json
{
  "CGMValueBf24h": {
    "vocab_size": 407,
    "tid2tkn": ["<pad>", "<unk>", "<masked>", "<s>", "<e>", "0", "1", ...],
    "tkn2tid": {"<pad>": 0, "<unk>": 1, ...}
  },
  "CGMValueAf24h": {
    "vocab_size": 407,
    "tid2tkn": [...],
    "tkn2tid": {...}
  }
}
```

---

What feat_vocab.json Contains
==============================

Feature vocabulary built by the input transform's build_vocab_fn.
Structure depends on the input_method used:

```json
{
  "window_build": { "..." },
  "tetoken_config": { "..." },
  "tetoken_model_config": { "..." },
  "singlevalue_timestep": { "..." },
  "singletoken_timestep": { "..." }
}
```

---

Inspection Checklist
====================

1. **Split existence**: Verify train, validation, test-id exist (test-od optional)
2. **Sample counts**: Check train >> validation >= test splits
3. **Feature dimensions**: Verify input sequence lengths match config
4. **Column names**: Check expected features are present in dataset_dict
5. **Data types**: Verify numeric columns are float/int, not string
6. **Vocabulary**: Check cf_to_cfvocab.json and feat_vocab.json at root
7. **Label distribution**: Check output labels are balanced (if classification)
8. **Missing values**: Check for unexpected None/NaN in features
9. **Manifest**: Check manifest.json for lineage back to CaseSet

---

Quick Inspection Commands
=========================

```bash
# List available AIDataSets
ls _WorkSpace/4-AIDataStore/

# List versions for a dataset
ls _WorkSpace/4-AIDataStore/<aidata_name>/

# List splits and files
ls _WorkSpace/4-AIDataStore/<aidata_name>/@<aidata_version>/

# Check file sizes
du -sh _WorkSpace/4-AIDataStore/<aidata_name>/@<aidata_version>/*

# Read manifest
cat _WorkSpace/4-AIDataStore/<aidata_name>/@<aidata_version>/manifest.json

# Read vocabulary files (NOT in a vocab/ subdirectory)
cat _WorkSpace/4-AIDataStore/<aidata_name>/@<aidata_version>/cf_to_cfvocab.json
cat _WorkSpace/4-AIDataStore/<aidata_name>/@<aidata_version>/feat_vocab.json
```

---

MUST DO
=======

- **Activate** .venv and run `source env.sh` before loading
- **Use** `load_from_disk(path=..., SPACE=...)` or `load_asset(path=..., SPACE=...)`
- **Check** cf_to_cfvocab.json and feat_vocab.json at the AIDataSet root
- **Inspect** dataset_dict keys to understand available splits

---

MUST NOT
========

- **NEVER modify** loaded data or any files in _WorkSpace/4-AIDataStore/
- **NEVER assume** data exists -- check first with ls or try/except
- **NEVER load** without activating .venv and sourcing env.sh
- **NEVER use** `load_from_disk(set_name=..., store_key=...)` -- that API does not exist
- **NEVER assume** a vocab/ subdirectory -- vocab files are at root level

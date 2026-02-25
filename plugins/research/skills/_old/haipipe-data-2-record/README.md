haipipe-data-2-record
=====================

Layer 2: Record Processing -- converts SourceSets into temporally-aligned
structured records. In the CGM domain, records are aligned to a 5-minute
time grid. The HumanRecords mapping is domain-configurable.

---

Quick Reference
---------------

```
/haipipe-data-2-record load           Inspect existing RecordSet (read-only)
/haipipe-data-2-record cook           Run Record_Pipeline with a YAML config
/haipipe-data-2-record design-chef    Create new HumanFn/RecordFn via builder
/haipipe-data-2-record design-kitchen Upgrade Record_Pipeline infrastructure
```

---

Common Commands
---------------

```bash
# 1. Activate environment
source .venv/bin/activate && source env.sh

# 2. Discover available configs, RecordSets, and registered Fns
ls config/                                   # find existing configs
ls _WorkSpace/2-RecStore/                    # find existing RecordSets
ls code/haifn/fn_record/record/              # find registered RecordFns

# 3. Run Record_Pipeline via CLI (replace with your config path)
haistep-record --config <your_config>.yaml

# 4. Load and inspect (Python) -- replace with actual RecordSet name
from haipipe.record_base import RecordSet
record_set = RecordSet.load_from_disk(path='_WorkSpace/2-RecStore/<RecordSetName>', SPACE=SPACE)
record_set.info()

# 5. Access data (example illustrative -- list keys first to find actual names)
for key in record_set.Name_to_HRF:
    print(key)                               # string = Human, tuple = Record
human  = record_set.Name_to_HRF['<HumanFnName>']            # string key
record = record_set.Name_to_HRF[('<HumanFnName>', '<RecordFnName>')]  # tuple key
```

---

Key Paths
---------

```
Pipeline:    code/haipipe/record_base/record_pipeline.py
Asset:       code/haipipe/record_base/record_set.py
Generated:   code/haifn/fn_record/human/*.py               (DO NOT EDIT)
             code/haifn/fn_record/record/*.py               (DO NOT EDIT)
Builders:    code-dev/1-PIPELINE/2-Record-WorkSpace/*.py    (edit these)
Store:       _WorkSpace/2-RecStore/
Config:      config/test-haistep-ohio/2_test_record.yaml
```

---

Files
-----

```
SKILL.md           Full rules, Name_to_HRF pattern, MUST DO / MUST NOT
README.md          This file (quick reference)
1-load.md            Rules for inspecting RecordSets
2-cook.md            Rules for running Record_Pipeline
3-design-chef.md     Rules for creating new HumanFn/RecordFn builders
4-design-kitchen.md  Rules for modifying Record_Pipeline framework
templates/
  config.yaml      Annotated config template
```

---

See Also
--------

- **haipipe-data-1-source**: How raw data becomes SourceSets (input to this layer)
- **haipipe-data-3-case**: How RecordSets become CaseSets (output of this layer)
- **haipipe-data-4-aidata**: How CaseSets become ML-ready datasets

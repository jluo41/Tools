haipipe-data-0-overview
=======================

Architecture map and navigation hub for the haipipe system.

---

Quick Reference
---------------

```
/haipipe-data-0-overview    Read SKILL.md -- architecture + navigation
```

This skill has no subcommands. Read SKILL.md in full when invoked.

---

The 6-Layer Pipeline
--------------------

```
Layer 1: Source    Raw files      ->  SourceSet       /haipipe-data-1-source
Layer 2: Record    SourceSet      ->  RecordSet       /haipipe-data-2-record
Layer 3: Case      RecordSet      ->  CaseSet         /haipipe-data-3-case
Layer 4: AIData    CaseSet        ->  AIDataSet       /haipipe-data-4-aidata
Layer 5: Model     AIDataSet      ->  ModelInstance   /haipipe-nn-*
Layer 6: Endpoint  ModelInstance  ->  EndpointSet
```

---

Three-Package System
--------------------

```
haipipe    Pipeline framework       code/haipipe/          EDITABLE
hainn      ML models                code/hainn/            EDITABLE
haifn      Production functions     code/haifn/            GENERATED (DO NOT EDIT)
```

Builders (edit these):  code-dev/1-PIPELINE/<N>-WorkSpace/

---

Key Discovery Commands
----------------------

```bash
# What Fns are registered?
ls code/haifn/fn_source/          # Layer 1 SourceFns
ls code/haifn/fn_record/human/    # Layer 2 HumanFns
ls code/haifn/fn_record/record/   # Layer 2 RecordFns
ls code/haifn/fn_case/fn_trigger/ # Layer 3 TriggerFns
ls code/haifn/fn_case/case_casefn/ # Layer 3 CaseFns
ls code/haifn/fn_aidata/entryinput/ # Layer 4 Input Tfms
ls code/haifn/fn_aidata/entryoutput/ # Layer 4 Output Tfms

# What data exists?
ls _WorkSpace/1-SourceStore/
ls _WorkSpace/2-RecStore/
ls _WorkSpace/3-CaseStore/
ls _WorkSpace/4-AIDataStore/
ls _WorkSpace/5-ModelInstanceStore/
```

---

Universal Prerequisites
-----------------------

```bash
source .venv/bin/activate    # ALWAYS first
source env.sh                # ALWAYS second
```

---

Files
-----

```
SKILL.md    Full architecture, design principles, current structure, skill index
README.md   This file (quick reference)
```

---

See Also
--------

- **haipipe-data-1-source** through **haipipe-data-4-aidata**: Layer-specific skills
- **haipipe-nn-0-overview**: ML model system overview

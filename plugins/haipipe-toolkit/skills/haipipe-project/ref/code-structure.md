Track A: Code Development Structure (code/ + code-dev/)
=========================================================

Two sub-tracks:

  A1 -- Pipeline functions (SourceFn, RecordFn, CaseFn, TfmFn, SplitFn)
       Developed in: code-dev/1-PIPELINE/    Generated to: code/haifn/

  A2 -- ML models (Algorithm, Tuner, Instance)
       Developed in: code/hainn/

---

Builder Pattern (A1)
=====================

NEVER edit code/haifn/ directly. Edit code-dev/ builder, then run it.

  code-dev/1-PIPELINE/
  +-- 1-Source-WorkSpace/   -> code/haifn/fn_source/    (SourceFn, HumanFn)
  +-- 2-Record-WorkSpace/   -> code/haifn/fn_record/    (RecordFn)
  +-- 3-Case-WorkSpace/     -> code/haifn/fn_case/      (TriggerFn, CaseFn)
  +-- 4-AIData-WorkSpace/   -> code/haifn/fn_aidata/    (TfmFn, SplitFn)
  +-- 5-Instance-WorkSpace/ -> code/haifn/fn_model/     (ModelInstanceFn)
  +-- 6-Endpoint-WorkSpace/ -> code/haifn/fn_endpoint/  (EndpointFn)

---

ML Model Layout (A2)
=====================

  code/hainn/
  +-- algo/{family}/algorithm_{name}.py
  +-- tuner/{family}/tuner_{name}.py
  +-- instance/{family}/instance_{name}.py
  +-- instance/{family}/configuration_{name}.py
  +-- nn/                       <- shared neural net blocks

  Families: tsforecast, mlpredictor, tefm, tediffusion, bandit

---

When to Create Track A Stubs
==============================

  New dataset/modality?       -> SourceFn/RecordFn stubs (code-dev/)
  New feature engineering?    -> CaseFn/TfmFn stubs
  New model architecture?     -> algo + tuner + instance stubs (code/hainn/)
  Purely experimental/reuse?  -> Track A not needed

---

Stub File Locations
====================

Pipeline Fn stubs:
  code-dev/1-PIPELINE/{N}-*-WorkSpace/build_{dataset}_{layer}.py

ML model stubs:
  code/hainn/algo/{family}/algorithm_{name}.py
  code/hainn/tuner/{family}/tuner_{name}.py
  code/hainn/instance/{family}/instance_{name}.py
  code/hainn/instance/{family}/configuration_{name}.py

---

code/INDEX.md -- Codebase-Wide Registry
========================================

Location: code/INDEX.md (shared across ALL projects).
Read BEFORE creating any new Fn or model -- reuse first.

  ## Pipeline Functions (code/haifn/)
  | FnClass | Stage | Dataset | Location | Projects Using | Status |

  ## ML Models (code/hainn/)
  | ModelClass | Family | Tuner | Location | Projects Using | Status |

  Status: stub | wip | done

Update after: creating stubs, implementing, or reviewing.

---

Skill Handoff
==============

  Stage 1-4 Fns    ->  /haipipe-data design-chef {stage}
  Stage 5 models   ->  /haipipe-nn
  Stage 6 endpoints ->  /haipipe-end

---

Review Checklist for Track A
=============================

  [ ] Builder exists in code-dev/ for each declared stage
  [ ] Generated code/haifn/ has Fn class (not just stub)
  [ ] For new models: algo, tuner, instance, configuration files exist
  [ ] code-dev/ builder and code/haifn/ output in sync

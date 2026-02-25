haipipe-data-1-source
=====================

Layer 1: Source Processing -- converts raw data files into standardized SourceSets.

---

Quick Reference
---------------

```
/haipipe-data-1-source load           Inspect existing SourceSet (read-only)
/haipipe-data-1-source cook           Run Source_Pipeline with a YAML config
/haipipe-data-1-source design-chef    Create new SourceFn via builder pattern
/haipipe-data-1-source design-kitchen Upgrade Source_Pipeline infrastructure
```

---

Key Paths
---------

```
File / Directory                                        Purpose
------------------------------------------------------  -----------------------------------
code/haipipe/source_base/source_pipeline.py             Pipeline orchestrator
code/haifn/fn_source/*.py                               Generated SourceFns (DO NOT EDIT)
code-dev/1-PIPELINE/1-Source-WorkSpace/*.py              Builder scripts (edit these)
_WorkSpace/1-SourceStore/                                Output store
tutorials/config/test-haistep-ohio/1_test_source.yaml   Example config
```

---

Files
-----

```
SKILL.md             Full rules, schemas, MUST DO / MUST NOT
README.md            This file (quick reference)
1-load.md            Rules for inspecting SourceSets
2-cook.md            Rules for running Source_Pipeline
3-design-chef.md     Rules for creating new SourceFn builders
4-design-kitchen.md  Rules for modifying Source_Pipeline framework
templates/
  config.yaml        Annotated config template
```

---

See Also
--------

- **haipipe-data-0-overview**: Architecture map and decision guide
- **haipipe-data-2-record**: How SourceSets become RecordSets
- **haipipe-data-3-case**: How RecordSets become CaseSets
- **haipipe-data-4-aidata**: How CaseSets become ML-ready datasets

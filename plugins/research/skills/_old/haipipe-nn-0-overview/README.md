haipipe-nn-0-overview
=====================

Architecture map, decision guide, and model registry for the NN pipeline.
Read this FIRST before any other haipipe-nn skill.

---

Quick Reference
---------------

- **4-Layer Architecture**: Algorithm (1) -> Tuner (2) -> Instance (3) -> ModelSet (4)
- **Decision Tree**: domain_format -> single/multi Tuner -> Optuna? -> save format
- **Add New Model**: Create Tuner -> Create Instance + Config -> Register -> Write YAML
- **Model Registry**: 7 model types across 5 families (see SKILL.md for full table)
- **YAML Templates**: One per model type (TSForecast, S-Learner, TEFM-Tuner, TEFM-Direct)
- **Reference Implementation**: tsforecast (cleanest 4-layer separation)

---

Files
-----

```
SKILL.md    Full architecture diagram, decision tree, add-new-model checklist,
            complete model registry, YAML config templates, family comparison
README.md   This file (quick reference)
```

---

See Also
--------

- **haipipe-nn-1-algorithm**: Algorithm diversity and the "never import above Tuner" rule
- **haipipe-nn-2-tuner**: The universal Tuner contract (5 abstract methods)
- **haipipe-nn-3-instance**: The orchestrator contract (5 abstract methods, config, registry)
- **haipipe-nn-4-modelset**: Packaging, YAML config, pipeline flow, versioning

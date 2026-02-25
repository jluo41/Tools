haipipe-nn-4-modelset
=====================

Layer 4: ModelSet/Pipeline -- packages trained Instances into complete assets.

---

Quick Reference
---------------

- **ModelInstance_Set**: Asset subclass with save/load/remote sync
  - asset_store_type = 'MODELINSTANCE'
  - Contains: model_instance, training_results, evaluation_results, examples_data
  - Directory: model/ + training/ + evaluation/ + examples/ + manifest.json
  - Run versioning with @run-v000X subdirectories

- **ModelInstance_Pipeline**: Config-driven orchestrator
  - Training mode: Config -> Init -> Fit -> Evaluate -> PreFn -> Examples -> Package -> RETURN
  - Inference mode: Load existing -> get_model_instance() -> predict
  - Pipeline RETURNS ModelInstance_Set -- caller calls save_to_disk()
  - Uses load_model_instance_class() for string -> class resolution

- **PreFnPipeline**: Feature pipeline attached to model before saving
  - Created from AIDataSet, travels with the model
  - Saves prefn_config.json + vocabulary files in model/ folder

- **YAML Config**: Drives ModelInstance_Pipeline (see haipipe-nn-0-overview for templates)

---

Two API Levels
--------------

```
Asset API (ModelInstance_Set):
  save_to_disk()           load_asset(name, SPACE)    push_to_remote()

HuggingFace API (model_instance, nested):
  save_pretrained(dir)     from_pretrained(dir, SPACE)
```

---

Files
-----

```
SKILL.md    Full pipeline flow, YAML config, directory structure, versioning,
            lineage, PreFn, example generation, usage patterns, MUST DO / MUST NOT
README.md   This file (quick reference)
```

---

See Also
--------

- **haipipe-nn-0-overview**: Architecture map, decision guide, YAML templates
- **haipipe-nn-1-algorithm**: What algorithms are and their diversity
- **haipipe-nn-2-tuner**: How to wrap an algorithm into a Tuner
- **haipipe-nn-3-instance**: How Tuners are managed by Instances

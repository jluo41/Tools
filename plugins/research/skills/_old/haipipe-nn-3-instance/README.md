haipipe-nn-3-instance
=====================

Layer 3: Instance -- the orchestrator contract for managing Tuners.

---

Quick Reference
---------------

- Inherits from ModelInstance (code/hainn/model_instance.py)
- Set MODEL_TYPE class attribute (goes into metadata.json)
- Implement 5 abstract methods: init(), fit(), infer(), _save_model_base(), _load_model_base()
- Store Tuners in self.model_base dict (keys: 'MAIN' or action/variant names)
- Use Tuner Registry (dict or if/elif) for lazy-loading by name string
- Create matching @dataclass Config inheriting ModelInstanceConfig
- Config MUST have: ModelArgs, TrainingArgs, InferenceArgs, EvaluationArgs
- Register in model_registry.py: MODEL_TYPE -> (InstanceClass, ConfigClass)
- Reference implementation: TSForecastInstance (cleanest pattern)
- NEVER import raw algorithms -- delegate everything to Tuners

---

Three Composition Patterns
---------------------------

1. **Single Tuner**: model_base = {'MAIN': tuner}
2. **Single Tuner + Encoding**: one model, treatment/context as input feature
3. **Multiple Tuners**: one tuner per treatment arm / variant

---

Files
-----

```
SKILL.md    Full contract, 3 patterns, config class, registry, HF-style API,
            concrete example, known deviations, MUST DO / MUST NOT
README.md   This file (quick reference)
```

---

See Also
--------

- **haipipe-nn-0-overview**: Architecture map, decision guide, YAML templates
- **haipipe-nn-1-algorithm**: What algorithms are and their diversity
- **haipipe-nn-2-tuner**: The universal Tuner contract (5 abstract methods)
- **haipipe-nn-4-modelset**: Packaging, pipeline flow, versioning

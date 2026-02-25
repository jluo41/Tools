haipipe-nn-2-tuner
==================

Layer 2: Tuner -- the universal wrapper contract for any algorithm.

---

Quick Reference
---------------

- Inherits from ModelTuner (code/hainn/model_tuner.py)
- Set domain_format class attribute ("nixtla", "sparse", "tensor", "hf_clm", ...)
- Define transform_fn() as STANDALONE function at TOP of file
- Implement 5 abstract methods: get_tfm_data(), fit(), infer(), save_model(), load_model()
- Save to model_{key}/ subfolder with best_params.json + tfm_args.json
- ONLY layer that imports external algorithm libraries
- Known deviation: MLPredictor tuners don't inherit ModelTuner (legacy)

---

Files
-----

```
SKILL.md    Full contract, file template, 5-case dispatch, Optuna pattern,
            save/load pattern, known deviations, MUST DO / MUST NOT
README.md   This file (quick reference)
```

---

See Also
--------

- **haipipe-nn-0-overview**: Architecture map and decision guide
- **haipipe-nn-1-algorithm**: What algorithms are and their diversity
- **haipipe-nn-3-instance**: How Tuners are managed by Instances
- **haipipe-nn-4-modelset**: How Instances are packaged into assets

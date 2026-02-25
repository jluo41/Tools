haipipe-nn-1-algorithm
======================

Layer 1: Algorithm -- any external ML library that does the actual computation.

---

Quick Reference
---------------

- Algorithms are external libraries (xgboost, neuralforecast, transformers, ...)
- Each algorithm is wrapped by exactly ONE Tuner (Layer 2)
- The Tuner file is the ONLY place that imports the algorithm
- Instance (Layer 3) and Pipeline (Layer 4) NEVER import algorithms
- Six domain formats: nixtla, sparse, tensor, hf_clm, llmapi, custom

---

Files
-----

```
SKILL.md    Full rules, diversity table, domain formats, serialization,
            concrete code examples, MUST DO / MUST NOT
README.md   This file (quick reference)
```

---

See Also
--------

- **haipipe-nn-0-overview**: Architecture map and decision guide
- **haipipe-nn-2-tuner**: How to wrap an algorithm into a Tuner
- **haipipe-nn-3-instance**: How Tuners are managed by Instances
- **haipipe-nn-4-modelset**: How Instances are packaged into assets

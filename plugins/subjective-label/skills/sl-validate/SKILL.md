---
name: sl-validate
description: "Compatibility alias for sealed final evaluation. Use when a user says /sl-validate, asks whether the guideline or weak models are good enough, or invokes the legacy public-dataset validation command; route project validation to /sl-evaluate and keep optional external datasets explicitly separate."
---

# Compatibility alias: validate → evaluate

Invoke `/sl-evaluate` with the same project path and compatible arguments.

Explain that confirmatory validation now uses a sealed target-population test labeled by
the human after `G*` freezes. If the user explicitly requests a public dataset, use the
optional external-validation protocol in `/sl-evaluate` and `ref-datasets.md`; do not
call it project convergence, a human ceiling, or an autonomy license.

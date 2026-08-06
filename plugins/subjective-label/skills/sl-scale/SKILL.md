---
name: sl-scale
description: "Compatibility alias for validated corpus completion. Use when a user says /sl-scale or asks to batch-label the remaining corpus with the legacy scale workflow; route to /sl-complete and require sealed-test qualification, risk routing, terminal reconciliation, final audit, and provenance."
---

# Compatibility alias: scale → complete

Invoke `/sl-complete` with the same project path and compatible arguments.

Explain that scaling now requires a production route that passed sealed evaluation and
ends with probability audit and provenance. Do not use unvalidated k-NN inheritance,
classifier thresholds, or weak-model majority as a fallback.

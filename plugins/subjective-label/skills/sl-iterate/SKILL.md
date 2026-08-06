---
name: sl-iterate
description: "Compatibility alias for the revised human-grounded calibration command. Use when a user says /sl-iterate, asks for another subjective-labeling iteration, or refers to the legacy iterate workflow; route to /sl-round and explain the new sealed-prelabel, blind-human, checkpoint semantics."
---

# Compatibility alias: iterate → round

Invoke `/sl-round` with the same project path and arguments.

Tell the user that an iteration is now a checkpointed calibration round:
`C_t → sealed P_t → B_t → blind Human-AI Session → D_t/G_t`.

Do not run the retired persona-majority workflow, auto-resolve “noise,” promote model
agreement to gold, or use public-dataset kappa as convergence.

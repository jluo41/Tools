---
status: open
created: 2026-06-23
context: Paper-SuitableMessageForRx-JAMANO — user has limited knowledge of the lifecycle stages
fixed_in: ""
---
The user (a domain expert, not a paper-lifecycle expert) does not know what each stage IS FOR. Quote: "in each stage, I am not sure what is the purpose for this stage, I have limited knowledge on it, why we use this stage, why it is important, and what we want to get?"

Right now each stage skill jumps straight into illuminate/elicit/edit and ASSUMES the user knows why seed vs pitch vs claims vs narrative vs display vs minimap exist and how they differ. They are similar-sounding to a newcomer (seed question vs pitch one-minute story vs claim ledger all overlap). The skills never teach the WHY before doing the work.

Two requested fixes:
1. Every stage should open with a short, plain-language "why this stage" teaching block: what this stage is, why we do it, why it matters to the final paper, and what concrete artifact/decision we want out of it (the "what we want to get"). Aim it at a user with limited lifecycle knowledge.
2. The stage strip should ALSO carry the current stage's purpose — not just the stage name. e.g. the strip / closing block should say something like "claims 🔥 — pin the 1 primary + 3 supporting claims each tied to evidence" so the one-line status itself teaches what the current stage is doing and why.

Fix: Add a per-stage one-line "purpose" string (the why + the wanted output) to each stage skill and to the stage-strip / closing-block renderer, and have explain mode expand it into a few sentences. Honor the existing 2026-06-23_use-diagram-ascii-for-explanations preference when teaching.

---
status: fixed
created: 2026-06-22
context: haipipe-paper lifecycle (pitch/claims/surprise etc.); felt on Paper-Personality-Opioid-MedJournal when the agent started grepping two-part logs / variables to verify the C2 "patients already on opioids" claim
fixed_in: "paper ref/evidence-routing.md v2.0.0"
---
这个不是你要做的事情，应该留给 probe 去做，你可以列一下计划，之后合适的时候 trigger probe 去做，我觉得这算是一类问题吧，你看看如果加上 feedback 里去，遇到这种情况，应该怎么去丢给 probe 去处理。 现在没有证据，可以先加上 红字 进行解释之类的。

Distilled ask (this is a CLASS of situation):
- When paper-lifecycle work hits a claim or wording whose support needs NEW evidence, data/variable inspection, or an analysis that does not exist yet (e.g. "is the intensive margin really about patients ALREADY on opioids? do we need the bene_bf14d baseline-MME variable?"), the paper layer must NOT dig into the data, scripts, do-files, logs, or variable definitions to verify or design the analysis. That is the evidence layer's job.
- The paper owns the STORY; probe (and task) own the EVIDENCE. Grepping metrics.json / two-part logs / variable defs to settle a claim is overstepping the layer boundary.

Handoff protocol when a paper hits an evidence gap (what to do INSTEAD of digging):
1. STOP investigating the data. Do not grep do-files, re-derive variables, or design the estimation.
2. Mark the claim in the artifact with a visible RED caveat so the gap is obvious in the compiled PDF and the wording is clearly provisional, e.g. `\textcolor{red}{\textbf{[NEED PROBE]} ...}` (load xcolor). Propose a reusable `\needprobe{...}` macro as a shared lifecycle convention.
3. Record a delivery NEED (per ../ref/delivery-need.md) and a short probe PLAN: the claim under test, what the probe must decide (definitions, populations, variables), and the expected output/verdict.
4. Route to /haipipe-probe at the appropriate time (not necessarily now). The paper TRIGGERS probe; it does not run the analysis.
5. When the probe returns a verdict, backfill it into the claim/pitch and remove the red caveat.

Why:
- Paper sessions kept sliding into data forensics (two-part logs, bene_bf14d, recipient definitions) to settle a claim. That blurs the paper/evidence boundary, is slow, and produces ad-hoc analysis the evidence layer should own and audit.

Where it touches:
- haipipe-paper-pitch / -claims / every stage skill: add an "evidence gap -> probe" rule: when a claim needs new evidence, flag with a red [NEED PROBE] caveat + record a need + draft a probe plan; never investigate the data in the paper layer.
- a shared red-flag convention (`\needprobe{...}`) so evidence gaps render consistently across lifecycle tex.
- ../ref/delivery-need.md: "claim needs a verdict / robustness / a new analysis or variable" is always a PAUSE -> route to probe, never resolved in-paper.

Fix:

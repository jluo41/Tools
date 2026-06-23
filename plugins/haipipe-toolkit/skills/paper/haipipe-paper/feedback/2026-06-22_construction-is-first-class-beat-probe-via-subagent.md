---
status: open
created: 2026-06-22
context: haipipe-paper narrative/Methods stage on Paper-Personality-Opioid-MedJournal; the narrative had only a thin "Setting: N≈766k" line and no account of HOW the analytic cohort is built, and the user wanted the construction probe dispatched to a subagent so the paper main line keeps moving
fixed_in: ""
---
"有一项，就是数据集的构建，我觉得应该好仔细说说，应该开一个 probe，这个 probe 去看对应的 stata 的 code，然后生成 report，这样我们才能用。"
"这个你开个 subagent 去跑吧，我们主线有主线的任务。"

Distilled ask (a CLASS of situation):
- Dataset/cohort CONSTRUCTION is a first-class narrative/Methods beat, not a one-line "Setting" aside. The narrative must carefully account for HOW the analytic cohort is built: the inclusion/exclusion funnel with N at each step, the unit definition (e.g. "first-pair"), the exposure→outcome linkage, the exposure window, and how each outcome/flag/control is computed. That account is what makes the results usable and reproducible, and it is exactly what the venue's reviewers scrutinize.
- The paper layer must NOT read the build code itself to write that account (same boundary as paper-evidence-gap-route-to-probe). It routes to a CONSTRUCTION PROBE that reads the build CODE (Stata cms/case/data do-files) + aggregated logs and emits a construction report. PHI guardrail: code + aggregated logs only, never raw CMS data.
- Heavy evidence probes (ones that read a lot of code/logs and write a report) must be DISPATCHED TO A SUBAGENT (background), not run inline on the paper main line. The main line keeps doing paper work; the subagent returns the report, which is then folded into Methods + Table 1.

Handoff protocol when the narrative/Methods needs the build documented:
1. Add a "Cohort construction" beat to narrative/Methods, marked [GAP] / [NEED PROBE] until the report lands.
2. Record the delivery need with the PHI guardrail and the exact source folders (the A=cms / B=case / C=data stage task-folders).
3. Open the probe (/haipipe-probe plan), then run it via a BACKGROUND subagent. Do not block the main line on the code-reading.
4. When the construction report returns, fold it into Methods + Table 1 and flip the beat to [READY].

Why:
- Construction is the reproducibility spine; JAMA-style reviewers judge cohort definition hard. A thin "Setting" line is not enough.
- Running the code-reading probe inline stalls the paper session; the user explicitly wants the main line free while the probe runs.

Where it touches:
- haipipe-paper-narrative / -minimap: narrative + Methods must carry a dedicated cohort-construction beat tied to a construction probe.
- haipipe-paper orchestrator + -enter: when an evidence probe is heavy (code/log reading + report), recommend dispatching it to a subagent / background, not inline.
- ../ref/delivery-need.md: "section needs the build documented" -> construction probe, run off-main-line.

Fix:

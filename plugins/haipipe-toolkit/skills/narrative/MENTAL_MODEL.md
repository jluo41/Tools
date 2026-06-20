The Three-Layer Pyramid — Mental Model
=======================================

Read this BEFORE writing your first narrative, or when something feels
like it could live in tasks/, probes/, or narratives/ and you're not sure.


TL;DR
=====

```
📖 ARGUE  (narrative)  "why does this matter?"         curate + judge readiness
📊 CLAIM  (probe)      "does the hypothesis hold?"     test + validate
💼 DO     (task)       "did this run work?"            execute + measure
```

If you can ask "did this RUN work?" — it's a task.
If you can ask "does this HYPOTHESIS hold?" — it's a probe.
If you can ask "is this STORY ready to publish?" — it's a narrative.


The Pyramid
===========

```
                       📖 ARGUE (narrative)
                      "this is the story worth telling"
                     curates which facts matter + angle
                    ─────────────────────────────────────

                  📊 CLAIM (probe)              📊 CLAIM
                 "X beats Y, p=0.018"          "Z doesn't hold"
                one hypothesis tested          one hypothesis tested
               ─────────────────────────────────────────────────────

             💼 DO (task)    💼 DO     💼 DO     💼 DO     💼 DO
            "MAE=24.6"    "MAE=23.9" "MAE=24.8" ...       ...
            one run        one run    one run
```

Each level adds interpretation:
- DO = raw measurement (no opinion)
- CLAIM = validated statement (statistical test, reviewer-checked)
- ARGUE = editorial selection (which claims matter, what angle, what's missing)


Three Lifecycles, Three Time Scales
=====================================

```
💼 DO      hours     Plan → Build → Execute → Report
📊 CLAIM   weeks     Design → Materialize → Harvest → Judge
📖 ARGUE   months    Idea → Discovery → [Probes&Tasks → Insights → Fill → Ignite]* → Handoff
```

ARGUE contains N × CLAIM contains N × DO. The narrative is the outermost loop.
Each CLAIM loop runs inside the narrative's Probes & Tasks stage.
Each DO lifecycle runs inside a probe's Materialize stage.


Who Produces, Who Files, Who Curates
======================================

```
Layer     Produces                 Files to insight?    Reads insight?
────────  ───────────────────────  ─────────────────────  ────────────────
💼 DO     metrics.json             ❌ NO                  ❌ NO
📊 CLAIM  probe.yaml (verdict)     ❌ NO                  ❌ NO
📖 ARGUE  narratives/ (story)      ✅ YES (sole writer)   ✅ YES (for Fill)
```

Tasks produce evidence. Probes produce verdicts. The narrative decides what
becomes permanent knowledge. insight has ONE writer: the narrative.


Where A through N Live
=======================

```
📖 ARGUE layer  — "why does this matter?"
    narrative     📖 the editor       story + claims + ignite
    discover      🔍 the eyes         landscape + literature filter
    paper         📰 the typesetter   render story → paper (OUTPUT)
    application   💬 the translator   deliver to audiences (OUTPUT)

📊 CLAIM layer  — "does the hypothesis hold?"
    probe         📊 the judge        test one hypothesis
    insight       🧠 the memory       store validated DIKW

💼 DO layer     — "did this run work?"
    project       🏗️ the skeleton     scaffold project structure
    task          💼 the hands        execute code → metrics
    1_data…4_indiv  🔧 the pipeline     what the hands build
```


The Research Loop
==================

```
ARGUE identifies gap → "we need to know X"
  │
  ▼
CLAIM tests X → "X is confirmed (or refuted)"
  │
  │ needs runs
  ▼
DO runs the experiment → "MAE = 24.6"
  │
  │ metrics produced
  ▼
ARGUE harvests → files DIKW to insight → rechecks claims
  │
  ├── NO (gaps remain) → back to CLAIM
  └── YES (all filled) → Handoff → Paper + Application
```

ARGUE is the engine. It drives the loop by identifying what's missing.
Without ARGUE, you have scattered facts and completed experiments but no
direction. ARGUE says "we need K06 about OOD generalization" and the
loop spins to fill it.


Handoff — Multiple Outputs
============================

When Ignite = YES, the ignited narrative feeds BOTH paper and application:

```
📖 Ignited narrative (curated K/W + angle + claims)
     │
     ├──→ 📰 paper           "render for academics" (venue-specific LaTeX)
     ├──→ 💬 G_app report      "brief stakeholders"
     ├──→ 💬 G_app message     "tell patient/clinician"
     └──→ 💬 G_app ui          "design the feature"
```

1 narrative : N outputs. Same truth, different audiences.


Common Confusions — FAQ
========================

**Q: A task produced interesting metrics. Should I file a D card?**
A: No — the task just produces metrics.json. The narrative's Insights stage
   decides whether those metrics are worth filing as a D card.

**Q: A probe confirmed a claim. Should it file a K card?**
A: No — the probe updates probe.yaml with the verdict. The narrative's
   Insights stage reads the confirmed claim and files the K card.

**Q: Who writes to insights/?**
A: Only the narrative (Insights stage). Tasks and probes never touch insights/.

**Q: Can I have a probe without a narrative?**
A: Yes — probes can run independently for ad-hoc hypothesis testing.
   But without a narrative to harvest the results, K cards won't be filed
   to insight, and the results won't feed a paper.

**Q: Can I have a narrative without probes?**
A: Yes — if all claims are already in the literature (discover confirms them),
   the narrative can go straight to Ignite with lit-sourced K cards, no probes needed.

**Q: Where does discover fit?**
A: It's the narrative's eyes. Used in two stages:
   - Discovery (Stage 2): position the angle in the landscape
   - Probes & Tasks (Stage 3): filter each GAP — is the answer in the literature?

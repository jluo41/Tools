---
name: haipipe-individual-inference-judge
description: "LLM-as-judge evaluator for prediction-interpretation Reports. Consumes the report.json produced by haipipe-individual-inference-report and scores it against a rubric persona (e.g. patient-comprehension, safety-review) via claude_agent_sdk. Each judge persona defines its own rubric dimensions, scoring rules, and verdict thresholds — pluggable, can live outside the plugin. Builds on haipipe-individual-inference-report. Use to score reports in CI batches, doctor pre-review, persona ablation studies, or red-team safety checks. Trigger: judge a report, score interpretation, evaluate report, /haipipe-individual-inference-judge."
argument-hint: --report-dir <path> --persona <name_or_path> [--model X]
allowed-tools: Bash, Read
---

Skill: haipipe-individual-inference-judge
=======================================

LLM-as-judge for the dual-layer Reports produced by
`haipipe-individual-inference-report`. Same SDK + persona pattern, applied
to evaluation instead of generation.

```
  📨 Report          ⚖️  judge persona       🤖 Claude SDK
  (report.json)      (rubric, weights)       (Haiku via OAuth)
       │                    │                       │
       └────────┬───────────┴───────────────────────┘
                ▼
           📜 Judgment{rubric_dimensions, issues, verdict, summary}
```

Sibling progression in `5_individual/`:

| Skill | Adds | Output |
|-------|------|--------|
| `haipipe-individual` | (data load) | ctx |
| `haipipe-individual-inference` | + payload + POST | forecast |
| `haipipe-individual-inference-report` | + audience persona + LLM | Report |
| `haipipe-individual-inference-judge` | + judge persona + LLM | **Judgment** |

---

Layout
-------

```
src/
  judge_report.py       SDK call, <judgment> XML extract, parse
  judgment_schema.py    pydantic Judgment model
  persona_loader.py     resolve judge persona name|path → system_prompt

personas/                 ← shipped reference judges
  patient-comprehension/  ←  scores readability/tone/jargon/length
  safety-review/          ←  scores hypo/hyper flag, no insulin dose, no Rx

scripts/
  judge_report_cli.py   end-to-end CLI: report.json + judge persona → judgment

tests/
  (smoke against the report.json from 18/patient-friendly/<ts>/)
```

---

Quickstart
-----------

Assuming you already produced a report (sibling skill):

```
python Tools/plugins/haipipe-toolkit/skills/5_individual/haipipe-individual-inference-judge/scripts/judge_report_cli.py \
    --report-dir _WorkSpace/7-AgentWorkspace/reports/18/patient-friendly/<TS>/ \
    --persona patient-comprehension
```

Output: `<report-dir>/judge_<persona>/`

```
judgment.json    structured payload (Judgment pydantic)
response.xml     raw <judgment> block from the LLM
meta.json        telemetry: judge_persona, model, cost, session_id
```

You can run multiple judges against the same report — each writes into
its own `judge_<persona>/` subfolder so no clobbering.

---

Judge persona system
---------------------

Same convention as report personas. Folder with three files:

```
<judge-persona>/
├── persona.yaml      rubric + target_audience + model
├── system.md         system prompt for the judge
└── schema.md         <judgment> XML schema spec
```

`--persona` accepts a name (resolved under shipped/) or an absolute path
to any folder on disk. External judge libraries (clinical IRB rubrics,
Samsung-internal red-team panels, ablation rubrics for research) live
outside the plugin.

Required fields in `persona.yaml`:
- `rubric`            (label, e.g. `safety-review`, `patient-comprehension`)
- `target_audience`   (who the report under judgment was written for)
Optional: `model`, `dimensions` (advisory list of dimension names),
`weights`, anything else.

---

Output schema (XML the judge emits)
------------------------------------

```xml
<judgment>
  <rubric_dimensions>
    <dimension>
      <name>...</name>
      <score>1-5</score>
      <reasoning>...</reasoning>
    </dimension>
    <!-- one per dimension, schema-defined per persona -->
  </rubric_dimensions>

  <issues>
    <issue>
      <severity>info|warning|critical</severity>
      <location>"nl" | "interpretation.actions[2]" | ...</location>
      <issue>brief description</issue>
      <suggestion>optional concrete fix</suggestion>
    </issue>
  </issues>

  <overall_verdict>pass | warn | fail</overall_verdict>
  <overall_score>4.2</overall_score>
  <summary>One paragraph synthesis.</summary>
</judgment>
```

`pydantic Judgment` enforces:
- score 1-5 (int)
- overall_score 0.0-5.0 (float)
- severity ∈ {info, warning, critical}
- overall_verdict ∈ {pass, warn, fail}

---

Failure modes
--------------

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `no <judgment>...</judgment> block` | Judge LLM wrote prose around XML | Tighten persona system.md; check `response.xml` |
| `pydantic.ValidationError` on Judgment | Score outside 1-5 or unknown verdict | Check schema.md; persona must constrain enum strictly |
| Judge marks safe report as `fail` | rubric is too strict for the report persona | Match judge-rubric to report-audience pair |
| `FileNotFoundError: No report.json at ...` | --report-dir wrong | Pass either the dir or the json file path |

---

Reuses
------

- `haipipe-individual-inference-report` produces the input (`report.json`)
- `claude_agent_sdk` for the LLM call (subprocess of `claude` CLI)
- Pattern reference: `Physician-SPACE/.../A3_cross_family_judge/run_sdk_judge.py`
  (where the original XML-block + ResultMessage + idempotent-skip pattern
  was first proven; this skill adapts it to the haipipe per-individual layer)

---

Future
------

- `--all-personas` flag to fan out across every shipped judge in one call
- per-batch driver (separate skill, not under 5_individual) for cohort eval
- inter-judge agreement metrics (Cohen's κ across judges) for the same
  report — useful for rubric calibration

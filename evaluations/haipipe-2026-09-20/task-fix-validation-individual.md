# Fresh-context Individual / Endpoint validation

Scope: static source inspection only, starting from root AGENTS.md and the realistic request supplied by the parent. No Python was executed, no tests or models were run, no endpoints/network were called, and no patient data was inspected. Repository files were read only. The repository already contains many user edits and active parallel edits.

Selected skills: `haipipe-individual` for cached Subject slices; `haipipe-individual-inference` for client payload and invocation; `haipipe-individual-inference-report` for report evidence format; `haipipe-individual-inference-judge` for judging the existing bundle; `haipipe-end-deploy-local`, `haipipe-end-input2src`, and `haipipe-end-src2input` for the deployed wrapper and wire pair. No new deployment or endpoint construction is required by the request.

## Static command plan (not executed)

The illustrative chosen project is `/private/tmp/haipipe-individual-validation/project`. It must already contain the configured global stores and the saved report. These paths are placeholders for the command walkthrough; no stores or report files have been manufactured.

```sh
skill_root=/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/task
project_root=/private/tmp/haipipe-individual-validation/project

python "$skill_root/4_individual/haipipe-individual/fn/build_sample_individuals.py" \
  OhioT1DM 559 --workspace "$project_root/_WorkSpace" --force

python "$skill_root/4_individual/haipipe-individual-inference/scripts/test_individual_predict.py" \
  --workspace-root "$project_root" \
  --individual UserGroup-OhioT1DM/Subject-559 \
  --platform sagemaker \
  --endpoint-model endpoint_cgm_patchtst_ohio/v0001 \
  --endpoint-url http://127.0.0.1:8765/invocations \
  --single-window --json

python "$skill_root/4_individual/haipipe-individual-inference-judge/scripts/judge_report_cli.py" \
  --report-dir "$project_root/_WorkSpace/7-AgentWorkspace/reports/559/patient-friendly/SAVED_RUN" \
  --persona safety-review
```

The inference command selects the illustrative advertised endpoint model `endpoint_cgm_patchtst_ohio/v0001`. Replace that `--endpoint-model` value with the actual packaged endpoint mapping. Both inference and report CLIs now accept `--endpoint-model`; report `--model` separately controls its composing LLM.

The builder now exits nonzero for any requested subject error or unsupported dataset; successful per-subject results remain `built`/`skipped_fresh`. In inference `--json` mode, the payload diagnostic now goes to stderr and the forecast JSON goes to stdout.

## Data flow and confirmed branches

1. Builder `--workspace` is the `_WorkSpace` directory, unlike inference/report `--workspace-root`, which is its parent project. Ohio Subject 559 selects cohort 2018, global SourceSet `OhioT1DM/@OhioT1DMxmlv250302`, RecSet `OhioT1DM_v0RecSet`, and PatientID values `ohio-559_train` / `ohio-559_test`.
2. Refresh filters existing global parquet outputs, strips wrapper and partition paths, and writes `A-User-Store/UserGroup-OhioT1DM/Subject-559`. It copies Ohio raw XML files when present; it does not rerun SourceFn/RecordFn. `--force` bypasses reuse. Without it, spec/builder/input stat fingerprint and output stat inventory must both match. Build staging and replacement preserve the old cache when ordinary construction fails; a subject lock serializes writers.
3. The loader resolves explicit project, then environment, then nearest cwd ancestor containing `_WorkSpace`. Absolute Subject paths resolve directly; ambiguous shorthand is rejected. It loads the available configured source tables and sorts/filter-validates CGM timestamps. It does not read the individual's RecStore for inference.
4. `build_payload` serializes CGM as ElogBGEntry and optional Ptt as Patient; the trigger uses the last CGM row. SageMaker places `models`, `TriggerName_to_CaseTriggerList`, and `inference_form` at top level. Databricks wraps the record in `dataframe_records`. The local FastAPI server forwards the chosen payload to `Endpoint_Set.inference()` unchanged. Local HTTP does not require SageMaker SigV4 merely because the package uses a SageMaker wire pair. The included requests client does not implement direct AWS SageMaker Runtime transport.
5. The saved report bundle is `report.json`, `forecast.json`, and `meta.json`. Report generation stores the selected response (already sliced if `--single-window` was used), the two file hashes, and model/window indices. Judge checks the hashes and selection before the LLM call, supplies raw forecast plus deterministic facts as extra context, and compares the last returned window's count, five-minute-step horizon, min/max/mean, and exact threshold flag. A deterministic summary/flag mismatch forces `fail` after the LLM response. Legacy missing binding caps a model `pass` at `warn`. Evidence verification is not clinical validation and cannot establish chronology without window timestamps.

## Final follow-up status after root changes

The final follow-up review re-read the previously outstanding quickstart, chronology, provenance, JSON-output, and rounding sources, and reconfirmed the report binding and builder failure status. It remained static: no Python, tests, endpoint calls, models, or patient data. Statuses below describe the current source actually read.

All paths below are repository-relative under `plugins/haipipe-toolkit/skills/task/`.

| Original finding | Current status | Source evidence |
| --- | --- | --- |
| 1. Hash differs from judged file | Resolved; reconfirmed | `4_individual/haipipe-individual-inference-judge/scripts/judge_report_cli.py:57-58` passes the actual path. `4_individual/haipipe-individual-inference/src/forecast_evidence.py:50-57` hashes that path and checks its parsed object against the judged object. |
| 2. Missing bound forecast downgraded to legacy | Resolved; modern binding marker added | `forecast_evidence.py:40-49` reads existing metadata first, raises when a v1 bundle has no evidence_binding, and raises when a declared binding lacks forecast.json. `make_report_cli.py:113` emits `schema: haipipe-report-bundle/v1`. True missing metadata / absent unmarked legacy binding remains unavailable. |
| 3. Refresh errors exit 0 | Resolved; reconfirmed | `4_individual/haipipe-individual/fn/build_sample_individuals.py:441-444,464-468` records unknown datasets as errors, returns 1 when any result failed, and passes that status through SystemExit. |
| 4. Endpoint model cannot be selected | Resolved | Inference CLI `:35-38` and report CLI `:48,69` expose and pass `--endpoint-model`. Report metadata `:115` records the selected endpoint model. |
| 5. Input2Src dual-format conflict | Resolved | `3_end/haipipe-end-input2src/ref/concepts.md:295` now requires only the selected platform shape and matching pair roundtrip. |
| 6. Quickstart executes wrapper in place | Resolved | Inference SKILL `:63-66` and report SKILL `:70-73` now prefer the existing deployment and require copying the reference wrapper to the canonical serving Task for a new deployment. |
| 7. Report chronology stronger than evidence | Resolved, including persona follow-up | `4_individual/haipipe-individual-inference-report/src/compose_report.py:93-116,190-193` labels the anchor unverified and explicitly prohibits a now/last_obs_dt claim without evidence. Client `:43-48` and both CLI single-window help strings agree. Report `personas/patient-friendly/system.md:2,8-17` now describes a selected trajectory and requires unverified timing to be stated without claiming the next two hours. Judge `personas/safety-review/system.md:9,14` now refers to the selected last-returned window. |
| Raw-materialization provenance | Resolved | `4_individual/haipipe-individual/fn/build_sample_individuals.py:386-388` sets raw_materialized from the copied-file count, separately records raw_copy_requested, and records missing raw paths. A partial copy is distinguishable through the missing-path list and copied count. |

The two additional gaps are also resolved in the final read:

- **JSON stdout: resolved.** `4_individual/haipipe-individual-inference/scripts/test_individual_predict.py:40,46-48` sends diagnostics to stderr in JSON mode and writes only forecast JSON to stdout.
- **Threshold evidence before rounding: resolved.** `4_individual/haipipe-individual-inference-report/src/compose_report.py:109-114` computes expected_safety_flag from the unrounded trajectory using the same strict threshold comparisons as `forecast_evidence.py:25-26`. `compose_report.py:181-193` includes it in the prompt and instructs preservation. A synthetic 69.999 / 300.001 crossing is therefore still represented by the correct flag even when displayed extrema round to 70.0 / 300.0. This conclusion follows from static source inspection, not an executed numeric test.

Direct report binding remains coherent on this final read: the CLI forwards the exact supplied report path; the evidence loader checks that file's hash and parsed-object identity before comparing selected raw forecast facts. Builder failure propagation also remains coherent: per-subject errors and unsupported datasets produce status 1 through SystemExit. The modern schema marker prevents a v1 report with a removed binding from silently entering legacy mode. The final persona reread also confirms that chronology wording now agrees with the composer and evidence layer. No new implementation logic conflict was found in these fixes.

## Original findings (historical detail; statuses above supersede these)

All paths below are repository-relative under `plugins/haipipe-toolkit/skills/task/`.

1. **Report hash can refer to different bytes than the judged report.** `4_individual/haipipe-individual-inference-judge/scripts/judge_report_cli.py:49-57` loads the supplied file and then passes only its parent to `load_ground_truth`. `.../src/judge_report.py:224-231` accepts any existing file name. `4_individual/haipipe-individual-inference/src/forecast_evidence.py:46-49` always hashes sibling `report.json`. A directory containing a valid bundle and `edited-report.json` can therefore judge the edited JSON with `verified_binding` based on the original report's bytes, provided its forecast summary/flag are unchanged. Bind the actual selected file bytes, or reject noncanonical file inputs explicitly.

2. **A missing file in a bound bundle becomes legacy mode.** `4_individual/haipipe-individual-inference/src/forecast_evidence.py:39-45` returns unavailable when forecast.json is absent before reading meta.json. Thus deleting forecast.json while retaining a binding is not rejected as broken evidence; the CLI proceeds to the LLM and only caps `pass` at `warn`. Inspect the available meta binding first and distinguish incomplete modern bundles from true legacy reports.

3. **Refresh failure exits successfully.** `4_individual/haipipe-individual/fn/build_sample_individuals.py:449-459` catches all per-subject exceptions, logs an error summary, and returns normally. With a preserved older cache, `refresh && inference` can use stale inputs after a failed refresh. Return a nonzero status when any requested subject fails, including unsupported datasets.

4. **The endpoint model mapping cannot be selected by the shipped CLIs.** `4_individual/haipipe-individual-inference/src/build_payload.py:31,63-69` supports a model argument, but the inference CLI never exposes/passes it; the report CLI likewise omits it when constructing the endpoint payload. The inference skill's failure table tells users to pass the correct model id. That repair is not available through the documented CLI interface, and report `--model` has a different meaning.

5. **Input2Src instructions still conflict on legacy formats.** `3_end/haipipe-end-input2src/ref/concepts.md:38-43` requires one platform shape and explicitly rejects a dual decoder, while line 295 (`MUST DO` item 6) requires both dataframe_records and legacy flat. Replace that requirement with same-platform validation or an explicitly named separate legacy implementation.

6. **Quickstarts conflict with the local wrapper's copy requirement.** The inference and report SKILL quickstarts run the skill's serve_local.py path directly. `3_end/haipipe-end-deploy-local/SKILL.md:128-141` says it is reference-only and must first be copied to the serving Task. This scenario already has a deployed endpoint, so following the quickstart's deployment step is unnecessary, but the linked instructions disagree.

7. **Report prompt asserts chronology that the evidence layer does not verify.** `4_individual/haipipe-individual-inference-report/src/compose_report.py:93-102,192-198` calls the last returned window most recent and tells the model it is anchored at `last_obs_dt`. `4_individual/haipipe-individual-inference/src/forecast_evidence.py:63-65` correctly says chronology is not independently established without timestamps. The prompt's stronger claim can label a historical last-valid segment as a current forecast; carry the same limitation into report composition unless timestamps establish the anchor.

Additional small provenance issue: `build_sample_individuals.py:324-328,382` sets `raw_materialized` from the requested raw-copy flag even if neither Ohio raw file exists and zero files were copied. The manifest can claim raw materialization while the raw projection is absent.

Initial review also found inference SKILL wording saying one dataframe_records payload works everywhere and only endpoint_url differs. A later read showed that wording had already been corrected by concurrent parent edits, so it is not listed as an outstanding finding.

## Result

The intended command/data flow is supported by the skills and shipped Python. All seven original findings, the raw-materialization provenance issue, and the two follow-up gaps are resolved in the final static source review. No outstanding issue remains among these scoped findings. No runtime compatibility, parquet schema parity, endpoint roundtrip, model prediction, patient report quality, or actual forecast chronology was verified.

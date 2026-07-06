# SKILLSET_REVIEW — 0_connect bucket

Reviewed: 2026-07-05 · Scope: `Tools/plugins/haipipe-toolkit/skills/0_connect/` (3 skills, 23 files: food-to-description, meal-cam-logger, whoop-connect) · Reviewer: haipipe-skill-diagnose
Status: DIAGNOSED, awaiting user eyeball before any fix (改前必报).

Inventory: all 3 SKILL.md have valid YAML frontmatter with `name` == folder. whoop-connect and meal-cam-logger carry version + last_updated + CHANGELOG pointer + CHANGELOG.md; food-to-description is missing the CHANGELOG pointer, the CHANGELOG.md file, and the `summary:` field (E1). The bucket has no orchestrator/root doc of its own; the nearest root doc is `../STRUCTURE.md`.


## Part 1 — Root causes (先看这个)

1. ① 🚚 搬家没改地址 — 5 findings (A1-A5): the bucket's skills were authored in other homes (WellDoc-SPACE Linux server, old `Tools/plugins/health/` plugin) and moved here without repointing paths; two skills are unrunnable on this host as documented.
2. ② 📄 路由层失真 — 1 finding (B1): STRUCTURE.md still claims venue playbooks live under `0_*`; they live under `paper/_venue` and `application/_venue`.
3. ③ ⚔️ 内部矛盾 (doc↔code) — 9 findings (C1-C9): the heaviest class. food-to-description's documented entry point crashes on import (C1, verified by execution); meal-cam's documented launch flag does not exist (C2); the whoop redirect URI in the doc contradicts the listener code (C6); stage-3 scope, resumability, and the daily-sync claim are all overclaimed relative to shipped code (C4, C5, C8).
4. ④ 🪝 跨workspace耦合 — 1 finding (D1): whoop-connect hardcodes another workspace's absolute machine path inside the shared toolkit.
5. ⑤ 📇 契约缺件 (metadata contract gaps) — 1 finding (E1): food-to-description missing CHANGELOG machinery. (New class: fits none of ①-④.)

Totals: 17 findings = 🔴 9 · 🟡 7 · 🟢 1 ; [M] 10 · [J] 7.


## Part 2 — Findings by class

### ① 🚚 搬家没改地址 (migration debris)

- [ ] **A1** 🔴 `[M]` meal-cam-logger launch command points at a dead plugin home: `meal-cam-logger/SKILL.md:60` runs `Tools/plugins/health/skills/meal-cam-logger/scripts/meal_cam_loop.py`; `Tools/plugins/health/` does not exist (script actually lives in this bucket). Fix: repoint to `Tools/plugins/haipipe-toolkit/skills/0_connect/meal-cam-logger/scripts/meal_cam_loop.py`.
- [ ] **A2** 🔴 `[J]` meal-cam-logger launch prelude `meal-cam-logger/SKILL.md:57` does `cd /home/jluo41/WellDoc-SPACE` and sources its `.venv`/`env.sh`; that Linux home does not exist on this host, so the documented Phase 1 crashes at the first line. Fix: choose the canonical runtime home (repo-root-relative resolution vs a named workspace) and rewrite the snippet; owner must pick, since the toolkit is shared across workspaces.
- [ ] **A3** 🔴 `[J]` food-to-description USDA DB is a hardcoded foreign absolute path: `food-to-description/utils/constants.py:12` sets `USDA_DB = /home/jluo41/WellDoc-SPACE/_WorkSpace/ExternalStore/@v1215/usda_fdc/usda_nutrition.sqlite` (absent on this host) and `food-to-description/SKILL.md:185` repeats it. Fix: resolve via the HAIToolLib asset-root pattern (env `HAIPIPE_TOOL_LIB` / walk-up to `_WorkSpace/HAIToolLib/`, graceful fallback); owner to confirm the asset's new home.
- [ ] **A4** 🟡 `[M]` food-to-description example dataset path is from the old workspace: `food-to-description/SKILL.md:235` cites `_WorkSpace/1-SourceStore/Shanghai/@ShanghaiV260419/Diet.parquet`, which does not exist in this workspace. Fix: label it explicitly as a WellDoc-SPACE example or drop the line.
- [ ] **A5** 🟡 `[M]` food-to-description references a skill that exists nowhere in the toolkit: `food-to-description/SKILL.md:233` and `food-to-description/SKILL.md:245` cite `end-to-end-roadmap` (zero hits outside these two lines). Fix: delete the See-Also bullet and rewrite the specialist-tail `next:` line.

### ② 📄 路由层失真 (routing drift)

- [ ] **B1** 🟡 `[M]` `STRUCTURE.md:70` says `0_*` holds "utilities, connectors, venue playbooks"; venue packs actually live at `paper/_venue` and `application/_venue`, and `0_connect`/`0_utils` hold connectors and utilities only. Fix: drop "venue playbooks" from the `0_*` row.

### ③ ⚔️ 内部矛盾 (doc ↔ code contradictions)

- [ ] **C1** 🔴 `[M]` food-to-description's entire documented CLI is dead on arrival: `food-to-description/pipeline.py:20` imports `from stages import stage_1_decompose` (through line 23) but `stages/__init__.py` exports nothing and the modules are named `1_decompose.py` etc. (leading digit, not importable by that name). Verified: `python3 -c "from stages import stage_1_decompose"` raises ImportError. Every command in `food-to-description/SKILL.md:105`-135 crashes. Fix: alias in `stages/__init__.py` via importlib (`stage_1_decompose = importlib.import_module(".1_decompose", __name__)`, x4).
- [ ] **C2** 🔴 `[M]` meal-cam-logger documented launch flag does not exist: `meal-cam-logger/SKILL.md:62` passes `--interval 5` but `scripts/meal_cam_loop.py:32`-47 defines only `--source/--fps/--cooldown-sec/--max-gap-sec/--output-dir/--model`; argparse exits with "unrecognized arguments". The Phase 1 user prompt (`meal-cam-logger/SKILL.md:48`) also asks for a "capture interval" that maps to nothing. Fix: rewrite the launch snippet and prompt in fps/cooldown/max-gap terms (code beats prose).
- [ ] **C3** 🔴 `[M]` `--status` documented as standalone but the code requires the positional input: `food-to-description/SKILL.md:133`-135 says `python pipeline.py --status`; `food-to-description/pipeline.py:265`-269 makes `input` required, so the command errors before reaching the status branch at `pipeline.py:302`. Fix: document `python pipeline.py <input.parquet> --status`, or make `input` optional (`nargs="?"`) since the status branch never reads it; doc fix is the minimal mechanical option.
- [ ] **C4** 🔴 `[J]` Stage-3 scope contradiction: `food-to-description/SKILL.md:71`-87 and `diagram/00-pipeline-flow.txt` (stage-3 box) say Claude reranks WEAK+MISS cases (35.4%+1.7%, the "62.8% → 90-95%" claim), but `food-to-description/pipeline.py:180`-184 selects only foods whose `fdc_id is None` (retrieval returned zero candidates ≈ MISS only); WEAK foods keep their rank-1 match and are never reranked, and the classify() result at `pipeline.py:143` is used only for counters. The status example "1,676/1,676 reranked" (`SKILL.md:161`) matches neither reading. Fix options: (a) track classification and rerank WEAK too, matching the doc and the historical run numbers, or (b) rewrite doc + diagram to MISS-only and retire the 90-95% claim. Evidence leans (a): the 1,676 figure implies WEAK was reranked in the run that produced the documented metrics.
- [ ] **C5** 🔴 `[J]` "Resumable" is overclaimed: `food-to-description/SKILL.md:127`-130 and `SKILL.md:212` (Design Choice 3) promise resume via `--from-stage`, but the food→fdc_id mapping lives only in memory (`pipeline.py:33`); a fresh process resuming at stage 3 sees an empty dict, logs "no weak/miss cases", and stage 4 writes zero-filled nutrition. Statusline persists status strings only, not data. Fix options: persist the mapping under `~/.food-description/`, or delete the resume claims and the `--from-stage` flag. Someone must pick.
- [ ] **C6** 🔴 `[J]` whoop redirect URI scheme contradiction: `whoop-connect/SKILL.md:64` tells the user to register `http://localhost:8080/callback`, but the listener the skill launches sends `https://localhost:8080/callback` (`jluo41-repo/Health-Sync/whoop/whoop_listen.py:27`); a user following the doc gets an OAuth redirect_uri mismatch. Evidence that the code is the truth: `tokens.json` exists in that repo, so the https value has succeeded against the real app registration. Fix: change SKILL.md to `https://` (external code stays untouched, it is outside this bucket).
- [ ] **C7** 🟡 `[M]` meal-cam-logger doc describes the retired v0.1 design: frontmatter description (`meal-cam-logger/SKILL.md:3`), Phase 2 (`SKILL.md:89`-96), and the output format (`SKILL.md:125`-145, `## Foods` with per-detection bullets) describe per-frame vision calls + string dedupe, but `scripts/meal_cam_loop.py:1`-13 is "v0.3 — episode-driven": local MediaPipe bite detection, one vision call per episode, `## Episodes` lines with bite counts, and a `mediapipe` dependency the doc never mentions. Fix: rewrite Overview/Phase 2/output-format sections to v0.3 behavior (code beats prose).
- [ ] **C8** 🟡 `[J]` whoop daily-sync claim is not implemented: `whoop-connect/SKILL.md:32` and `SKILL.md:124` tell the user "data will now sync automatically every morning at 7am", but no phase schedules anything; `Health-Sync/whoop/README.md:30` says to add the cron job manually via `/jobs`. Fix options: add a real Phase 3 scheduling step (create the job, then confirm), or soften the message to "say sync whoop anytime; I can also set up a daily 7am job if you want". Someone must pick.
- [ ] **C9** 🟢 `[M]` alias count stale: `food-to-description/SKILL.md:204` says "17 Shanghai→USDA manual mappings"; `utils/alias_dict.py` ALIAS has 19 entries (AST-verified). Fix: say 19, or "~20" to stop the drift.

### ④ 🪝 跨workspace耦合 (cross-workspace coupling)

- [ ] **D1** 🟡 `[J]` whoop-connect hardcodes another workspace's absolute machine paths throughout: `whoop-connect/SKILL.md:87`, `SKILL.md:94`-96, `SKILL.md:113`, `SKILL.md:141`-143 all point at `/Users/jluo41/Desktop/OpenClawServer/jluo41-repo/Health-Sync/whoop` and `/Users/jluo41/Desktop/OpenClawServer/env.sh`. They exist and work on this machine today, but the shared toolkit becomes machine-bound. Fix: introduce a resolvable root (env var with the current path as documented default), or accept machine-binding deliberately and record that in the SKILL.md; owner call.

### ⑤ 📇 契约缺件 (metadata contract gaps)

- [ ] **E1** 🟡 `[M]` food-to-description frontmatter misses the bucket's metadata contract: `food-to-description/SKILL.md:4`-9 has version + last_updated but no `summary:`, no CHANGELOG pointer comment, and no `CHANGELOG.md` on disk (both sibling skills have all three). Fix: add `summary:`, the `# version history: ./CHANGELOG.md` pointer, and a baseline CHANGELOG.md.


## Part 3 — Coverage honesty (what was NOT audited)

- `Health-Sync/whoop/*.py` (external repo, outside bucket): only `whoop_listen.py` was grepped for the port/redirect values feeding C6; auth/refresh/sync logic not audited.
- `meal-cam-logger/scripts/bite_detector.py`: header + public API (`is_bite_event`, `close`) spot-checked against the loop's usage; MediaPipe threshold logic not line-audited.
- `meal-cam-logger/scripts/test_bite_detector.py`, `test_identify_food.py`: not read.
- `food-to-description/stages/*.py` bodies: import blocks and public signatures checked (all four have `__main__` test blocks and self-insert `sys.path`, so direct-run works); retrieval/rerank internals not line-audited.
- `food-to-description/utils/usda_db.py`, `utils/statusline.py`: grep-level only (STATUS paths, dashboard method confirmed).
- No end-to-end runtime execution: only an import smoke test (which is what confirmed C1). The USDA DB and input parquets are absent on this host, so stages 2-4 cannot be exercised here.

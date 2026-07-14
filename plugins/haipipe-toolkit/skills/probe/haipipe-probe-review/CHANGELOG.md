haipipe-probe-review — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `probe/CHANGELOG.md`.


## [2.2.0] — 2026-07-14 — the last two dead doors in the probe bucket

Fixed
- **G1's instrument still wrote into retired artifacts.** `probe-caveats-checklist.txt` (LIVE — cited from SKILL.md G1) opened: "Walked by Judge (structural gate) before a verdict is committed. Each YES becomes a caveat in verdict.md and an entry in probe.yaml.verdict.caveats." Both files were retired 2026-07-05 with the probe-folder era, and the instruction directly contradicted this skill's own contract (the reviewer **writes nothing, anywhere**). An agent walking the checklist would have tried to commit caveats into two nonexistent files — or into the bank, a LAW-1 violation. The header now says: walked at **G1**, before the **G3 judgment is returned**; each YES is a caveat **line in the RETURNED TEXT**, which the **CALLER** transcribes into the claim's entry in `0-lifecycle/1-claims/1-claims.md` (the only home of a claim's status) and, where relevant, into the probe section's `reading:`. The closing "But…" prompt lost "before committing the verdict" the same way. Both dead filenames deleted.
- **G2 led with a command that cannot run.** The body's first G2 instruction was `python …/g2_integrity_check.py <evidence artifact paths>` — but the script takes a probe FOLDER positional and reads `probe_folder/evidence.md` + `probe_folder/probe.yaml` (g2_integrity_check.py:539-545), both retired. Handed a QA file / `sources.md` / a `results/` CSV it exits early (`evidence.md not found`) and audits nothing, so the deterministic half of the integrity gate never ran on the shapes the current model produces. The gap was DISCLOSED in a footnote, but the footnote came AFTER the command — so the command is what an agent tried first. **Inverted:** G2 now leads with the manual source-by-source walk (which IS G2 today), keeps the >95 / 80–95 / <80 thresholds, and carries an explicit ⛔ ban on invoking the script on current shapes. The script survives for legacy folder-era probes only; the `--doc/--sources` refit stays a flagged follow-up.

Unchanged: every gate's judgment. G1's checklist items, G2's five fraud patterns and thresholds, G3's six steps, the confidence scale, and the `associational | causal` guard.

## [2.1.0] — 2026-07-14 — the last dead pointer, and a readable body

Fixed
- **The status vocabulary was still attributed to a retired artifact.** The G3 section read "Verdict vocabulary is the PPNN card's (anatomy: `../haipipe-probe/SKILL.md`)" — but the PPNN *card* is retired (it is a probe FILE now), and the vocabulary no longer lives in the probe SKILL at all. It is the CLAIM LEDGER's (`0-lifecycle/1-claims/1-claims.md`), which is where this judgment lands. A reader who followed that pointer to find the vocabulary would not have found it.
- Return-contract key `verdict:` → `status:`. `supported | refuted | inconclusive` is transcribed by the caller into `1-claims.md`, whose field is `status` — the return is now shaped so the caller copies rather than translates, and the retired word "verdict" is gone from the live contract. (No caller depended on the key: the paper/application PROBE workers describe the return by its VALUES, not its keys.) A DISCOVERY's own `verdict.md` terminal file is a different, executor-native thing and is untouched.

Changed (readability — the goal of the pass, not a side effect)
- Body recast in house ASCII headers (`===` / `---` / `**bold**`), matching its just-rewritten sibling `haipipe-probe/SKILL.md` 8.0.0. It was the last `##`-header skill body in the probe bucket.
- New 10-second orientation at the top — **Owns / Invoked / Writes** — plus one diagram of the whole path: the answered QA file → the PROBE worker's INTERPRET → this reviewer (fresh context) → the caller's `1-claims.md`. Previously a reader had to get to line 27 to learn who invokes this, and to line 132 to learn where the judgment goes.
- 产审分离 is now EXPLAINED, not just asserted: it holds without the gateway because the EXECUTOR assembled the evidence in its own clean session and a SEPARATE fresh-context reviewer grades it.

Unchanged: every gate. G1's checklist, G2's five fraud patterns + the >95 / 80–95 / <80 thresholds + the deterministic `g2_integrity_check.py`, G3's six steps, the confidence scale, and the `associational | causal` guard are all exactly as they were.

## [2.0.0] — 2026-07-14 — the judgment survives; its CALLER and its LANDING SITE move

Ruling: `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` v3 (APPROVED by JL 2026-07-14), R1 + R7 + CC-6. Companion to haipipe-probe 8.0.0.

Fixed
- **THE JUDGMENT SURVIVES; ITS LANDING SITE AND ITS CALLER BOTH MOVED.** This skill was untouched by the redesign and still said the judgment "lands in the 1-probe-plans/PPNN card's `## Verdict`", dispatched "by the gateway, FULL mode only". R7 deleted the `## Verdict` block and the `verdicted` state; R1 retired `1-probe-plans/`; the gateway is archived. A consumer following this skill wrote its judgment into a folder and a block that no longer exist, and `1-claims.md` was never flipped — the claim silently stayed GAP.
- The judgment now lands in the consumer's `0-lifecycle/1-claims/1-claims.md` (per-claim, per-consumer, PRIVATE), and the caller is the paper/application PROBE-phase worker's INTERPRET step, for a `mode: full` section. Judgment CONTENT (G1/G2/G3, supported|refuted|inconclusive, confidence, claim_type) is UNCHANGED.

## [1.0.1] — 2026-07-06

Fixed (fresh-subagent smoke test on the Paper-PhyPatSim bench: reviewer shell correctly loaded this skill — used the fraud categories + 95% bar that exist nowhere else — and returned the full contract; judgment `supported` with clean scope carve-outs)
- KNOWN GAP documented: `g2_integrity_check.py` CLI is still folder-era (expects a probe folder with evidence.md + probe.yaml; exits early on folderless refs), so the manual fallback carries G2 until a `--doc <file> --sources <paths...>` refit; the fallback line in the G2 return is now required wording.

## [1.0.0] — 2026-07-06

Added (JL ruling: the reviewer agent may be called by the gateway, but the PROCESS must be governed by a skill — "haipipe-probe-review可以被新的agent call，但是我们还是需要一个skill来规范流程")
- New skill: the G1/G2/G3 judgment rulebook, extracted verbatim-in-substance from haipipe-probe-reviewer-agent 2.1.0 (which becomes a thin shell that invokes this headless and returns the output).
- Instruments migrated here from `../agents/`: `g2_integrity_check.py` (deterministic G2) + `probe-caveats-checklist.txt` (G1 confound checklist) — the skill owns its own docs.
- Direct invocation allowed only with a complete spec (claim + on-disk refs); the normal path is gateway full mode. Light mode never judges.

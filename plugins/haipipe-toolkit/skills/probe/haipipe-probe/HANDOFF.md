Handoff — probe file redesign (2026-07-19)
==========================================

For whoever continues the "C-P-E-Skill-Update-Probe-Template" work (JL co-design).
The DESIGN is settled and `ref/probe-template.md` is REWRITTEN to it.
The SYNC (constitution anatomy + `check-probe-cards.sh` ×2) is NOT done — that is the next task.
⚠️ Do not run `check-probe-cards.sh` against a new-format probe file until the checker is rewritten; the formats do not match yet.


What the probe file IS now (the settled model)
----------------------------------------------

A probe file is one TOPIC's list of Q-EXECUTORS (it used to be read as a list of Q-consumer sections).
It is Q-executor-oriented — the q-executor is the entity; the consumers hang off it.

1.  ENTRY = one Q-executor, id `QX<n>`, topic-local (QX1, QX2 … within the file).
    THREE id layers, none crosses the wall, all bound by PATH:
      stage doc  Q-consumer   → Q-Seed-1 / Q-Claim-6   (consumer-local)
      probe file Q-executor   → QX1 / QX2              (topic-local)
      bank       QA file       → QA/<n>-<slug>.md       (task-folder-local)
    Only the q-executor's TEXT crosses the wall — never any id.

2.  MANY-TO-ONE: one q-executor may serve SEVERAL Q-consumers (many consumer questions reduce to
    the same executor question — this is reuse made structural). The entry lists them under
    `### q-consumer`, and COPIES IN each consumer's ORIGINAL question (review-only, never dispatched)
    so the entry is self-contained and the strip (Q-consumer → q-executor) is visible.

3.  NO `## Why`. The stake lives in each Q-consumer, in the stage doc — not in the probe file.
    (Same logic as dropping a duplicated q-consumer field: consumer-side things stay consumer-side.)

4.  ANSWER = `a-executor`: a COPY of the answering QA file's answer, held in the probe entry as the
    consumer-side SINGLE SOURCE OF TRUTH. The a-consumer (the per-consumer interpretation) is NOT
    here — it moves to each stage doc (station ②). The answer chain is copy-then-anchor at each hop:
      QA answer → a-executor (probe) → a-consumer (stage doc, `[source: PP<NN>]`) → stage content
    Each hop is a real copy anchored to the previous → self-contained AND traceable (JL: "chain of
    thought … later we can track which part is correct"). `target` is the anchor back to the QA file.

5.  `bank` field = the DRAFT-time verdict on the bank, four values (richer than the old EXISTS/NONE):
      reuse — a results folder already answers it; just harvest.
      run   — the task folder + code exist; needs a run.
      code  — the task folder exists but code needs a change first.
      new   — nothing exists; create a task folder.
    `state` (planned|commissioned|answered|read|answered-local|failed) stays as the LIVE lifecycle,
    derived from disk. `bank` = the plan; `state` = where it is now.

6.  RENAME: `serves:` → `q-consumer` (JL: no coined words). `match:` → `bank`. `a-consumer:` (in the
    probe file) → `a-executor`.

7.  FORMAT (JL picked "version B"): entry `## QX<n> — <title>`, then FOUR `###` subsections —
      ### q-executor    (the question + Deliverable/Accepted)
      ### q-consumer    (bulleted list, each bullet = id + copied original question)
      ### bank binding  (route / bank / target / state, each as `**field**: value`, no indentation)
      ### a-executor    (the copied answer)
    Big fields get their own `###`; the four short scalars are grouped under `### bank binding`.
    No `- field:` lines, no `|` block scalars, no indentation.

8.  PHASE MODEL (settled earlier this session, already in the constitution v9.2.0/9.3.0 and the paper
    DRAFT worker + seed skill): DRAFT authors the WHOLE probe plan — ① ORGANIZE + ② MATCH run at
    DRAFT (a read-only bank grep is legal, LAW 1), so ONE human gate reviews draft + probe plan
    together. PROBE runs ③ DISPATCH + ④ POINT + ⑤ INTERPRET forward. `route` and the bank verdict
    are AUTHORITATIVE — the executor executes them, does not re-decide (decision "A"). v9.3.0 adds a
    fresh-context DRAFT self-review before the gate.


What changed on disk this session
---------------------------------

DONE:
- `ref/probe-template.md` — FULLY REWRITTEN to the model above. This file is now the target spec.
- `SKILL.md` — v9.2.0 (probe plan into DRAFT) + v9.3.0 (DRAFT self-review). NOTE: its "The probe file"
  anatomy still describes the OLD fields (serves/match/a-consumer/## Why, `## Q` sections). The new
  template SUPERSEDES that; the anatomy is the main thing to sync (see below).
- `CHANGELOG.md` — 9.1.0, 9.2.0, 9.3.0 entries.
- `../../paper/2-phase/0-draft/haipipe-paper-draft/SKILL.md` — DRAFT authors the plan.
- `../../paper/1-lifecycle/0-seed/haipipe-paper-seed/SKILL.md` — DRAFT/PROBE reattributed.


PENDING — the SYNC task (start here)
------------------------------------

1.  CONSTITUTION `SKILL.md` — rewrite the core to the new model:
    - "The probe file" anatomy → Q-executor entry, `QX<n>`, four `###` subsections, the field set
      above (q-executor / q-consumer-list-with-copies / route / bank / target / state / a-executor).
    - "THE FOUR FORMS" + "The answer's three stations" → relabel station ① from "probe a-consumer"
      to "probe a-executor (a copy)"; a-consumer now lives in the stage doc (station ②).
    - Drop `## Why` from the anatomy; state moves the stake to the stage-doc Q-consumer.
    - Bump version, add CHANGELOG entry.

2.  `check-probe-cards.sh` — TWO copies, rewrite the parser:
      paper: `../../paper/2-phase/1-probe/haipipe-paper-probe/check-probe-cards.sh`
      app:   `../../application/2-phase/1-probe/haipipe-application-probe/check-probe-cards.sh`
    - Section detection: `## QX<n>` entries + `### ` subsections (was `## Q` + `- field:`).
    - Parse `**field**:` lines under `### bank binding`; parse `### a-executor` body.
    - `--stage` gate: grep the `### q-consumer` bullets for the `Q-<Stage>` id (was `- serves:`).
    - DROP `no-why-section` / `multiple-why-sections` (no `## Why` anymore).
    - Rename in every code path: serves→q-consumer, match→bank, a-consumer→a-executor.
    - Keep the QA-file / state-line contract UNCHANGED (that is bank-side, not touched here).

3.  STAGE SKILLS still naming old probe fields — re-grep and fix (seed skill references `a-consumer`,
    `target`, etc.; the paper DRAFT worker mentions `match`). Search: `grep -rn "a-consumer\|serves:\|## Why\|match:" ../../paper`.

4.  APPLICATION FAMILY (parallel session's lane) — mirror everything: app DRAFT worker, app PROBE
    worker, `application/haipipe-application/SKILL.md`, and any app-side probe template. Leave a note
    in `../../../diagram/260718-qconsumer-nosidecar/` (that folder already coordinates paper↔app).

5.  EXISTING PP probe files on disk (real papers) — migrate to the new format, or note that only
    new files use it.


Open notes / risks
------------------

- This is a FORMAT-BREAKING change. Nothing must run the old checker on a new-format file, or vice
  versa, until step 2 lands. Do constitution + both checkers together.
- `bank` vs `state` overlap is intentional (plan vs live status); revisit only if it proves noisy.
- Heading style: the probe FILE uses markdown `#`/`##`/`###` (JL approved version B). The template's
  GUIDANCE sections use `====`/`----` (that is the template doc's own structure, not the file's).
- JL wanted to try filling a REAL probe file by hand from the new template before the checker is
  rewritten — that is a fine next step and a good test of the template's usability.

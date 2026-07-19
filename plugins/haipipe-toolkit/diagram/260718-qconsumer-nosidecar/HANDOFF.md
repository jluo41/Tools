haipipe-application — Session Handoff (2026-07-18)
===================================================

Topic: (1) align the Q-consumer question format across all 9 lifecycle stage templates, and (2) move to a NO-SIDECAR harvest workflow.
Scope: APPLICATION family only. The PAPER family is being mirrored separately by JL — the two share the probe constitution + a forked checker, so they must converge.
Status: all changes ON DISK, UNCOMMITTED. Checker syntax verified (`sh -n` passes).
Read first for the model: `Tools/plugins/haipipe-toolkit/skills/probe/haipipe-probe/SKILL.md` (the probe constitution — it wins over any stage skill).


Context (why this happened)
---------------------------

Started as `/haipipe-application` work on the seed stage for `designs/Project-Application-SMSDesign/applications/01_sms_young_male`, but pivoted to fixing the STAGE TEMPLATES first (a bad template propagates to every intervention). That intervention is still UNSCAFFOLDED — the original task, deferred.


Decisions (the durable contract)
---------------------------------

D1 — Question id = `## Q-{Token}-<n>`.
The `Q-` prefix LEADS, so every id reads as a question and can never be confused with a `## Description <n>` entry.
Tokens, one per stage: **Seed · Desc · Theme · Claim · Advice · Venue · Pitch · Narr · Disp** (e.g. `## Q-Claim-1`, `## Q-Disp-1 · materialize U<nn>`).

D2 — Q-consumer block shape (in the stage doc) = `## Q-{Token}-<n> · <title>` + `Ask:` (what the question wants) + `Why:` (which content/claim raised it + what breaks if unanswered) + (after APPROVE) a `→ 1-probes/PPnn` pointer.
There is NO `Answer:` field. Per the constitution, the stage-doc Q-consumer holds only the QUESTION + a POINTER; the ANSWER lives in the probe file's `a-consumer:`, and the STAKE lives in the probe file's `## Why`.

D3 — Templates = SKELETON; rules live in SKILL.md.
Dropped the top "How to use: copy to … replace <…>" line from every template (it never survives into a filled doc; the copy/replace mechanic is the DRAFT worker's job).
Decided AGAINST `<!-- HOWTO -->` instruction tags — the per-section how-to prose stays as-is; only the Q-consumer was normalized.

D4 — Seed: `Kill criteria` section REMOVED (unhelpful at seed stage; 6 content sections → 5).
`EVALUATION.md` reservoir line updated: seed has NO reservoir (too early for considered-and-dropped wisdom); the ladder rungs keep theirs (1a Waivers · 1b Parked · 1c Declined · 1d Rejected).

D5 — Descriptions (1a) restructured.
`Datasets` / `DS<n>` → a single `Dataset` section that LISTS one or many sources/files (not limited to one).
`D<n>` bullets → `## Description <n> · <topic>` SUBSECTIONS (spelled out where DEFINED; cited downstream by the short id `D<n>` — the footnote model: define full, cite short).

D6 — NO SIDECAR (the big one).
Retired `_VALUES_` / `_CITATION_` / `_DISPLAY_` / `_DESCRIPTIONS/` docs AND the `values:` / `sources:` / `displays:` harvest lanes.
The answer's numbers/citations now land INLINE in the probe SECTION's `a-consumer:`, each anchored `[→ <the section's target QA file>]`.
The fabrication guard MOVED, it did not die: the checker already verifies the section's `target:` is `answered` + non-superseded (PASS 1 R19/R20) — that on-disk QA file IS the anchor; no second transcription.
Checker PASS 2 (the sidecar-doc loop) REMOVED. The `harvest: OWED` guard is KEPT as a harmless defensive catch (no lanes are written, so it never fires; it would catch a legacy/stray lane line).

D7 — Scope = application only. JL is mirroring paper. The shared checker fork (`check-probe-cards.sh`) and the constitution must stay in step; the constitution keeps the harvest-lane fields OPTIONAL for other families, and application simply opts out.

D8 — Working style (behavioral, saved to auto-memory `feedback_concise_single_proposal`): give ONE recommendation and act, not an options menu; keep replies short.


Files changed (application family)
-----------------------------------

Stage templates + SKILLs + CHANGELOGs (versions bumped, all last_updated 2026-07-18):
- 0-seed 4.3.0 · 1a-descriptions 2.4.0 · 1b-themes 2.4.0 · 1c-claims 7.3.0 · 1d-advice 1.8.0 · venue 3.3.0 · 2-pitch 5.3.0 · 3-narrative 5.2.0 · 4-display 4.6.0.
- 1a-descriptions also: `Dataset`/`## Description` restructure + `ref/interrogation-battery.md` synced.
- Fixed a stray `</content></invoke>` artifact at the end of the display SKILL.

Probe layer:
- `2-phase/1-probe/haipipe-application-probe/SKILL.md` v3.1.0 — ⑤ INTERPRET harvests inline; "Harvest — no sidecar" section replaces the venue-hook lanes; T1 whitelist, VERIFY, return contract updated.
- `check-probe-cards.sh` — PASS 2 removed (syntax verified).
- `ref/harvest-acceptance.md` — rewritten to the no-sidecar rule.
- `ref/per-stage-dispatch.md` + `haipipe-application/fn/probes.md` + `2-phase/README.md` — lane/sidecar wording → no-sidecar.

Docs:
- `wiki/03-intervention-lifecycle.md` + `README.md` — dropped the retired sidecar mentions from the folder contract.
- `EVALUATION.md` — reservoir line (D4).


Open items / next steps
------------------------

1. UNCOMMITTED — commit as one application-family commit when ready.
2. PAPER mirror — JL is applying the same two changes to the paper family; verify the paper checker fork matches (PASS 2 removed) so the two don't drift.
3. `01_sms_young_male` is still unscaffolded — resume with `/haipipe-application enter designs/Project-Application-SMSDesign/applications/01_sms_young_male` (get-or-create), then the seed stage.
4. MINOR: the stage-doc Q-consumer still carries `Why:` (the constitution shows title + intent only). Left as a light extension — decide conform-vs-keep in a later pass.


How a fresh session picks this up
---------------------------------

- The MODEL is the probe constitution: `skills/probe/haipipe-probe/SKILL.md`. Stage-doc Q-consumer = question + pointer; probe file (`1-probes/PPNN`) = q-executor + target + a-consumer (the answer's home); QA file in the bank = the real anchored answer.
- Stage templates: `skills/application/1-lifecycle/*/*/ref/*-template.md`; each SKILL.md sits alongside.
- Harvest: inline in `a-consumer:`, anchored to `target:`. No sidecar docs exist.

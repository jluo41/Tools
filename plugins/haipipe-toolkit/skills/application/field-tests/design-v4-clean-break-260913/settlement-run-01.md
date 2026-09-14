# Design v4 clean-break field test · run 01 settlement

Field desk: Codex thread `01a09aab-a31d-7161-9d2f-be54a6d0be50`.
Target: DrFirst `B00_DesignBoard-R2Messages-260821` (read-only).
Baseline: Design v4.0.0 as installed in Physician-SPACE.

## Ledger settlement

| Row | Settlement | Transcript/disk evidence |
|---|---|---|
| E1 | MATCH | Loaded the three commissioned Design skills plus required Folder/Run references. |
| E2 | MATCH | Stopped currentness at `design/DU01…DU18/` and reported the v4 lanes absent. |
| E3 | SKILL GAP | Performed no migration or write, but called PageX “invalid/read-only migration history”; this language reintroduces a compatibility concept forbidden by the clean break. |
| E4 | MATCH | Reported Page `rp00` separately from `rd01_generate_*` and `rd02_verify_*`. |
| E5 | MATCH | Did not infer Commission release, verification, or adoption from old accepted rows. |
| E6 | MATCH | Stopped after one bounded next action; transcript contains read-only shell commands only. |

Auxiliary field-method observation: the returned FRICTION LOG mostly listed
target debt rather than ambiguity/wrongness/contradiction/missing law in the
skill instructions. The next commission must say that target defects belong in
status and only instruction defects belong in the friction log.

## Scorecard

- Time: `2026-09-13 08:09:09 EDT` to `08:10:41 EDT` = 1m32s field audit.
- Tokens: unavailable from the surfaced task receipt; no estimate recorded.
- Format: separate Design and Design-Page frontiers; no writes; current checker
  independently reports 18 `retired-design-shape` findings on the target.
- Semantic: 5 MATCH, 1 SKILL GAP, 0 EXPECTATION GAP.
- Friction severity: one high-severity compatibility-language leak; one
  field-method classification observation.
- Tax: one additional fresh run is required because the first report used a
  forbidden compatibility label after otherwise applying the clean break.
- Rate: one real legacy DS Folder audited in 1m32s; grade = repair, not close.

## Required repair

Strengthen the Design clean-break law so unsupported bytes are never described
as readable/read-only/migration history. Add a mechanical contract test, then
run a fresh field desk on a different real slice.

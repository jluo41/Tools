# Page setup Result · Reviewer comments on version 1

- Page Face: `CM01-review-0110.md`
- Content source: `draft/evidence/materials/q01_review-0110.md`
- Shape: `draft/CM01-review-0110-draft-v0.1.md` (present).
- Draft authority: `draft/CM01-review-0110-draft-v0.1.md` (present).
- Coverage: 3 sections; 3 reader-move Bullets; 3 source sentences.
- Static delivery: `../delivery/CM01-review-0110/web/index.html`
- Mechanical gate: **PASS**.
- Coverage check: every Outline Bullet has embedded Draft prose and an explicit evidence decision.
- Mode: create-semantic-records.
- Run status: **complete**.
- Human gate: Shape/content acceptance remains open.

Audited artifact paths and saved times are recorded in `checks.json`; rerun setup after changing a checked artifact.

## Setup checklist

| Check | Status | Gate | Evidence or next action |
|---|---|---|---|
| `source_configuration` · Source/configuration | **pass** | blocking | Page Face `CM01-review-0110.md` resolves through page.toml with explicit state and owner. |
| `input_preservation` · Input preservation | **pass** | blocking | The imported editable copy reads the same as `q01_review-0110.md`. |
| `opening` · Opening | **pass** | blocking | Opening is Page-specific, non-placeholder prose that names the Page or its subject. |
| `outline_structure` · Outline | **pass** | blocking | Shape has 3 divisions, 3 paragraphs, 3 Bullets, and one Evidence decision per Bullet. |
| `paragraph_global_order` · Page-global paragraph order | **pass** | blocking | Paragraph identities form one uninterrupted P1–P3 Page sequence. |
| `content_draft_mapping` · Bullet ↔ Content Draft | **pass** | blocking | All 3 Bullets have nonempty Content Draft records. |
| `semantic_role_syntax` · Semantic role syntax | **pass** | blocking | All 3 Bullets use a recognized semantic role label. |
| `bullet_head_readability` · Bullet-head readability | **pass** | blocking | All 3 setup Bullet heads are complete 4–24 word provisional reader moves without clipping or planner imperatives. |
| `content` · Content | **pass** | blocking | Bound editable Content `draft/evidence/materials/q01_review-0110.md` is nonempty. |
| `aims_structure` · Backstage Aims | **deferred** | informational | The minimal Page Face keeps targets in Folder/Run records rather than rendering an Aims section. |
| `static_delivery` · Static website | **pass** | blocking | `../delivery/CM01-review-0110/web/index.html` is a marked Page export and contains all 1 current source/assets. |
| `semantic_role_judgment` · Semantic-role judgment | **untested** | informational | Role labels are mechanically valid, but an agent or person must review whether each role fits its reader move. |
| `outline_logic_judgment` · Bullet-only argument review | **untested** | informational | An agent or person must read the Bullet heads without the Content Draft and confirm that the argument remains intelligible, ordered, and complete. |
| `aim_targets` · Aim targets | **deferred** | informational | Targets are recorded, but setup cannot certify that the substantive targets are achieved. |
| `human_shape_approval` · Human Shape approval | **deferred** | informational | The generated Shape remains unapproved until a person accepts it. |
| `human_content_acceptance` · Human Content acceptance | **deferred** | informational | Candidate prose exists, but setup does not mark it accepted. |
| `hosting` · Hosted Page | **n/a** | informational | Setup requested a static build, not a live listener or deployment. |

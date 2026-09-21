# Migrate a single-chain Insight Page to item Runs

Keep the public entry and installed skill path. Application I2/I3/I4/I5
Folders keep their own contracts; this concerns task-side research Pages.

1. Read the old Page, sources, and consumers. Preserve topic, data scope,
   evidence, limitations, and result dates.
2. Keep its Folder/Page address. Add `insight-layout: items-v2` and stable
   `insight-instance:`; declare snapshots in `workflow/insight.yaml`.
3. Preserve an existing `rNN_<descriptive-stem>` as readable items-v1 history.
   For new work, identify the reusable normal R ticket and allocate an
   `riNN_<descriptive-stem>` binding to it and the intended dataset snapshot.
4. Do not fabricate execution from prose. When historical receipts establish
   the contract, register an imported Result with original provenance and an
   explicit import/review receipt. Otherwise keep readable legacy material
   and mark the item proposed or needing evidence. Migration is not a rerun.
5. Reshape Content to Origin / Instance and Scope / Insight Items / Synthesis /
   Reusable Findings; retain DIKW inside the item and old navigation anchors.
6. Map old Page/RF references to exact instance/item/version/RF only after
   verification. Never match an RF by text or by selecting `latest`.
7. Update consumer bindings and recheck their context. The I1/I5 bridge and
   its person's signature remain; migration does not mint one.
8. Run the item checker and Page checks. A Page without `items-v2` remains
   readable under its recorded old contract; do not claim it is migrated or
   automatically rewrite unrelated live Pages.

Published Results and signatures remain immutable. Active instructions and
examples use the new model; changelogs preserve the previous contracts.

## 1.2.0 allocation and evidence finalization

New `bind` calls create an immutable `binding.yaml` and planned receipt, with
no final input until evidence arrives. Use `freeze` once to seal v001. An older
frozen input, including a prematurely empty v001, remains byte-for-byte intact;
finalize the corrected evidence under the next explicit version of the same RI.
Changed base R, dataset, question, target or acceptance instead needs a new RI.

Old recipe packets with `execution` retain their historical audit dialect. New
freezes require separate `producer_execution` and `consumer_insight_execution`,
producer Ticket/hash and complete receipt/hash; see `task-calls.md`. Reused
accepted support needs no fabricated recipe call, but a new freeze still binds
its real Ticket/hash and completed native receipt/hash in `supporting_results`. Existing published Results
and base R tickets are never rewritten by migration. No project-specific
producer adapter or external installed skill is changed by this source update.

New freezes mark `evidence_contract: haipipe.insight-evidence/v1`. Read-only
audit preserves the earlier evidence dialect for frozen packets without that
marker, including packets with `binding_sha256`. Allocation hashes do not select
evidence-validation rules. Upgrade through a new explicit version, never by
changing old inputs or their hashes. Unknown evidence-contract markers fail
visibly. Earlier packets still owe their original source-owner acceptance;
legacy audit does not confer new current-use approval.

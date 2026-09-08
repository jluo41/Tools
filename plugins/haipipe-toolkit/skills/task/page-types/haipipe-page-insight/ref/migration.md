# Migrate a single-chain Insight Page to item Runs

Keep the public entry and installed skill path. Application I2/I3/I4/I5
Folders keep their own contracts; this concerns task-side research Pages.

1. Read the old Page, sources, and consumers. Preserve topic, data scope,
   evidence, limitations, and result dates.
2. Keep its Folder/Page address. Add `insight-layout: items-v1` and stable
   `insight-instance:`; declare snapshots in `workflow/insight.yaml`.
3. Map its old question to `r01_<descriptive-stem>`, inheriting the old
   `insight-target:`. New questions in that topic become sibling items.
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
8. Run the item checker and Page checks. A Page without `items-v1` remains
   readable under its recorded old contract; do not claim it is migrated or
   automatically rewrite unrelated live Pages.

Published Results and signatures remain immutable. Active instructions and
examples use the new model; changelogs preserve the previous contracts.

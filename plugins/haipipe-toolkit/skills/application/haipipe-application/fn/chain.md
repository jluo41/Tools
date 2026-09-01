# `chain` · open or extend one D→I→K→W chain for one question

A question spans four pages on the InsightBoard. This verb opens the next level, never all four at once.

1. Resolve the InsightBoard and require one registered question id: `QD<n>`, `QI<n>`, `QK<n>` or `QW<n>` from the matching register `MT01`-`MT04`. A question not yet registered is registered first, through the `question` verb, on the register facing its target rung; a Brief-raised need arrives the same way and keeps the register's id from then on.
2. FIRST search the Task/Insights Board for a settled `page-type: insight` Page
   whose question covers this need. A match is reusable evidence, never Design
   authority. It may take the **pre-climbed external-parent bridge** only when
   all of these are true:
   - `scope: task`, `insight-target: wisdom`, and no `application:` or `serves:`;
   - CHECK is closed against current source versions;
   - one exact `RF<n>@<version>` traces `D → I → K → W → RF` inside that Page.

   For a valid match, register or resume one `QW<n>` row in MT04, record the
   exact Task Page/RF version and one local I5 Wisdom Folder on that row, and
   PageX-bind the RF from the local W Folder. Run I5 there: cite rather than
   copy the Task K/W/RF rows, test them against this Application's audience,
   context, and decision, write local counsel and forbidden overreach, then
   stop at `signed: ⬜`. A person may sign the resulting **Application-owned**
   Design Handoff; GI6 then settles the QW row. No local I2-I4 Folder is minted
   because their evidence authority remains inside the already-complete Task
   chain. This is a bridge over a pre-climbed parent, not a skipped epistemic
   rung, and the Task RF never binds directly to Design.

   An incomplete, stale, below-Wisdom, or untraceable Task Page cannot use the
   bridge. It may be cited as input to the normal local climb, but it cannot
   close a rung by itself.
3. Read the question's Queue row on its register to see how far the chain has climbed, then open only the NEXT level. On a rung-major board:
   - no D yet → `1-D-data/D<NN>-<slug>/` with `folder-kind: data`
   - D settled, no I → `2-I-information/I<NN>-<slug>/` with `folder-kind: information`
   - I settled, no K → `3-K-knowledge/K<NN>-<slug>/` with `folder-kind: knowledge`
   - K settled, no W → `4-W-wisdom/W<NN>-<slug>/` with `folder-kind: wisdom`
   On a partition-major board (`ref/partition.md`) the rungs live inside partition groups: resolve the owning group from the question's Queue CELL (its column names the partition; a dot cell routes to the X group), then open `<group>/<L><rung letter><NN>-<slug>/` with the partition letter prefixed to the page id. The phase-owned Folder contracts are the same four.
4. Load `haipipe-folder`, `haipipe-page`, `haipipe-insight-workflow`, then the matching phase contract. Load `haipipe-plugin-probe` for a D Folder commissioning missing evidence and `haipipe-plugin-pagex` for the producing Folder or any accepted parent.
5. Cite the parent page and the parent ROWS by id. Never restate a parent's content: a D page's counts are cited, not copied.
6. Update the question's Queue row on its register with the new page id and state.
7. Run the Page workflow until CHECK settles or holds the page.

A chain may legitimately stop. A question that reaches K and no further is answered as far as the evidence allows; its register's Queue row shows that, and a DesignBoard simply cannot bind it, because only a W page carries a Design Handoff.

Return the page path, its level, the parent rows it cites, the register Queue row, and whether the chain can climb further.

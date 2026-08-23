# `chain` · open or extend one D→I→K→W chain for one question

A question spans four pages on the InsightBoard. This verb opens the next level, never all four at once.

1. Resolve the InsightBoard and require one registered question id: `QD<n>`, `QI<n>`, `QK<n>` or `QW<n>` from the matching register `MT01`-`MT04`. A question not yet registered is registered first, through the `question` verb, on the register facing its target rung; a Brief-raised need arrives the same way and keeps the register's id from then on.
2. FIRST search the Task/Insights Board for a settled `page-type: insight` page whose question covers this need. If one exists, bind it through PageX and stop: a consumer-neutral chain already answered this, and reopening it locally duplicates the work.
3. Read the question's Queue row on its register to see how far the chain has climbed, then open only the NEXT level:
   - no D yet → `1-D-data/D<NN>-<slug>/` with `page-type: data`
   - D settled, no I → `2-I-information/I<NN>-<slug>/` with `page-type: information`
   - I settled, no K → `3-K-knowledge/K<NN>-<slug>/` with `page-type: knowledge`
   - K settled, no W → `4-W-wisdom/W<NN>-<slug>/` with `page-type: wisdom`
4. Load `haipipe-page`, `haipipe-page-for-task`, then the matching level contract. Load `haipipe-plugin-probe` for a D page reaching a task folder, `haipipe-plugin-pagex` for any level citing the one below it.
5. Cite the parent page and the parent ROWS by id. Never restate a parent's content: a D page's counts are cited, not copied.
6. Update the question's Queue row on its register with the new page id and state.
7. Run the Page workflow until CHECK settles or holds the page.

A chain may legitimately stop. A question that reaches K and no further is answered as far as the evidence allows; its register's Queue row shows that, and a DesignBoard simply cannot bind it, because only a W page carries a Design Handoff.

Return the page path, its level, the parent rows it cites, the register Queue row, and whether the chain can climb further.

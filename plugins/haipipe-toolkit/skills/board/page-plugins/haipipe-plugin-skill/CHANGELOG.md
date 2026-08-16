# haipipe-plugin-skill · Changelog

## 0.2.0 · 2026-08-16
- FLATTENED on JL's ruling ("maybe we don't need to have these concept …
  we just need to show these skills and the user can drag and rank them
  themselves"): the uses/designs relations, the aligned ✓ with drift dates,
  and the ↑ designs upgrade came out whole. The store is now a ranked list
  (`- <name>`, order = the person's rank), the ✕ tombstone survives as
  ` · removed`, the drag saves through the new /_board/skill-order route,
  and /_board/skill-verify is gone. Old-grammar stores read cleanly and
  migrate on the next write.

## 0.1.1 · 2026-08-15
- The card's NAME now stages the skill as its own 🔍 Skill tab, the whole
  split, and the view walks the page's skills with ← and → in card order
  (JL 260815: "the whole split should be the skill, like the display split,
  with ← and →"); the inline lazy-iframe expansion it replaces lived one hour.

## 0.1.0 · 2026-08-15
- Initial draft, round 2 of the thin-door migration (JL 260815): every live QPf plugin gains its skill; delta-only over haipipe-plugin.

## 0.2.1 · 2026-08-16
- Agents joined the list (JL 260816: "我们的 Skill 其实也是包括 Agent 相关的"): an `agents/<name>-agent.md` is a first-class 🤖 row with the same rank, ✕, and note; its open door is the live markdown view, and the ← → walk stays skills-only. First consumer: QPf9, ranking the collector and bank-door agents its probe cards crossed through.

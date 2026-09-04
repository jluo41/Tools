## 0.4.2 · 2026-09-03

- Stop presenting a freshly seeded sequence as an already completed human
  ranking: the header now says `drag to rank · refresh appends`.
- Remove the misleading Page-log-derived `last moved` label from the Skills
  surface; the plugin has no auditable rank-gesture timestamp.

## 0.4.1 · 2026-09-03

- Expand the seed index from the host `haipipe-toolkit/skills` tree to every
  installed `Tools/plugins/*/skills` tree and plugin-level agent directory.
- Preserve the existing modest scan law: only literal names written by the
  Page are appended, and only a person may rank them.

## 0.4.0 · 2026-09-03

- Move the sole ranked Skills store and generated editor to
  `outline/skill/<stem>{.md,-skill.html}`.
- Keep the former sibling `skill/` readable only for migration; every writer
  now lands in the canonical nested lane.

## 0.3.0 · 2026-09-03

- Move the ranked Skills surface into Outline → Page Records → Skills.
- Keep `skill/<stem>.md` as the sole primary store and remove the duplicate
  top-level Plugin picker row; compatibility writer and reader routes remain.

## 0.2.1 · 2026-08-16

- **Agents joined the list (JL 260816)**: an `agents/<name>-agent.md` is a
  first-class 🤖 row — same rank, same ✕; its open door is the live markdown
  view, because no SKILL.md folder stands behind it. The scan-seed matches
  against real SKILL.md folders AND agent definitions, and never invents.
- *(Entry reconstructed 260819 from the 0.2.1 frontmatter summary and commit
  432bd718 — the bump shipped without its CHANGELOG entry; agree.py caught the
  disagreement.)*

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

---
name: haipipe-plugin-probe
description: >-
  The probe/ plugin of a Board page: the page's evidence questions asked ONCE, each a card cited by id from the prose, shown in the 🚪 tab as the display split's strip: one card fills the pane, chips name the ids. Owns only the material contract — where a probe card lives in the page folder and how the page cites it; the crossing protocol itself (stake stripping, Q-executor, the QA bank) is haipipe-probe's and is never restated here. Loads haipipe-plugin for the four-facet contract. Trigger: probe plugin, probe card, evidence question, cite a probe, probe tab, asked once cited by id, /haipipe-plugin-probe.
metadata:
  version: "0.1.1"
  last_updated: "2026-08-16"
  summary: "The tab took the display split's structure (JL 260816); storage aligned to QPf9's PP<NN>-<slug>/card.md folders; 1-probes retired upstream."
---
# /haipipe-plugin-probe · asked once, cited by id

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
**LOAD `haipipe-probe` for the crossing itself.** This file owns only the material delta: what sits in the folder and how prose points at it.
It is the thinnest skill of the set on purpose: two layers already own most of what probe is, and a third copy would drift.

## 🗂 Storage · one card per question, id-addressed

```text
<page>/probe/
└── PP<NN>-<slug>/       one evidence question, numbered per page (QPf9 §1)
    └── card.md          the question · state: raised → working → bound ·
                         binding: → the answering QA file, by PATH
```

PRIMARY material: a card is authored when the question is raised and completed when the answer lands; it is never regenerated.
A question is asked ONCE: a second card for the same unknown is the failure the id exists to prevent, and the prose cites the id (`probe: <id>`) rather than restating the answer.

## ⚙️ Writer · the probe loop lands it, nothing else does

The card's lifecycle follows the probe layer's five-step loop: the page raises the stake-bearing question, the dispatch strips the stake, the bank answers into its own QA file, and the card binds to that file by path.
No board route writes a card today; the loop's owner does, and this plugin only says where the result lives.

## 📡 Surface · the display split's structure, probe's filling

The 🚪 tab (`live/plugview.py`, `plug_probe`) takes the display split's structure whole (JL 260816): a horizontal strip of blocks, one card filling the pane, shift right for the next, a chip row naming every PP id, and per-card anchors so a citation lands on the card it names.
The filling is probe's own: the state badge, the question, the binding, and the card folder's tree; an open question is visible before it is forgotten.
The tab renders; it never dispatches, because sending a question out is a deliberate act on the page, not a button reflex.

## 📂 Files

- `../../haipipe-board/live/plugview.py`
  The 🧪 list view.
- `../../../probe/haipipe-probe/SKILL.md`
  The crossing protocol this plugin defers to whole.
- `../../haipipe-plugin/ref/roster.md`
  The row this skill expands.

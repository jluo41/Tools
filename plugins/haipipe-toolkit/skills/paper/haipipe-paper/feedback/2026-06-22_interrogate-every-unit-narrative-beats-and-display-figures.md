---
status: fixed
created: 2026-06-22
context: haipipe-paper, after setting up per-beat subagent review of the narrative on Paper-Personality-Opioid-MedJournal; user generalizing the discipline to the display stage
fixed_in: "haipipe-paper-narrative v1.3.0 + haipipe-paper-display v1.4.0"
---
"so in the narrative 我们拷打每一个 item，在 display 里，我们拷打每一个图或者表。"

Distilled ask (a CROSS-STAGE principle):
- The "interrogate every unit" discipline ("拷打") is symmetric across lifecycle stages. In the NARRATIVE stage we grill every beat/item: an independent subagent judges each one's inclusion/necessity (keep / move / demote / cut) with a sharp comment rendered in SMALL FONT; the drafting agent does not self-author the justification (self-authored "why it's here" comes out limp).
- The DISPLAY stage must apply the SAME discipline to every figure and every table: each display unit is interrogated by an independent subagent for whether it earns its place (keep / merge / move-to-Supplement / cut), what job it does, whether it is the RIGHT form (table vs figure vs forest vs flow diagram), and whether it maps to exactly one claim (main vs Supplement). The verdict is rendered as a small-font editorial comment on the display unit.
- Generalization: any lifecycle stage that enumerates discrete units (narrative beats, display figures/tables) subjects every unit to an independent per-unit review, not a self-graded one.

How to apply:
- narrative (haipipe-paper-narrative): per-beat subagent review (keep/move/demote/cut + small-font comment) [already in motion].
- display (haipipe-paper-display + renderers): add a per-figure / per-table subagent interrogation step. For each display unit: does it earn inclusion, is it the right form, does it map to exactly one claim, main vs Supplement. Render the verdict in small font alongside the unit (e.g. in 0-displays/<unit>/README.md or the display gallery), same as the narrative beats.
- The drafting agent integrates verdicts + recompiles; the subagent JUDGES, never authors (builder != judge).

Why:
- Self-authored "why this is here" comes out limp; an independent interrogation per unit is sharper and catches units that do not earn their place. The same nice-to-have failure mode (keeping marginal figures/tables) afflicts the display stage, so the same fix applies.

Where it touches:
- haipipe-paper-narrative: per-beat interrogation (small-font comments).
- haipipe-paper-display + the display renderers (-display-table / -display-figure / -display-diagram / -display-illustration): add a per-figure/per-table interrogation step with small-font verdicts.
- a shared lifecycle convention worth stating once: "interrogate every unit via an independent subagent review, render the verdict in small font."

Fix:

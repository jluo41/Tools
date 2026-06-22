---
status: fixed
created: 2026-06-22
context: pitch stage. Responsible skills: haipipe-paper-structure-pitch (canonical pitch structure) and the scaffolded 1-pitch.tex stub emitted by haipipe-paper-folder / scripts/init_paper_layout.py (pitch_tex).
fixed_in: "2026-06-22 revision pass (init_paper_layout.py pitch_tex + haipipe-paper-structure-pitch template)"
---

Reporter (JL): 这个 pitch 写得不行。一个 pitch 应该有 hook、有 surprise、有
implication(so-what)、然后有什么证据支持,诸如此类。现在这个不达标。可以看看我们
pitch 相关的 skill 是怎么写的。

Detail: the canonical pitch skill (haipipe-paper-structure-pitch) does carry
Hook / Surprise / So What / Why Believe / Still Fragile. But the scaffolded
`0-lifecycle/1-pitch/1-pitch.tex` stub from init_paper_layout.py (`pitch_tex`) is
weaker: its sections are One-Minute Pitch / Hook / Surprise / Why Believe /
Still Fragile, which OMITS the implication (so-what) section and does not make
"evidence support per point" explicit. A user scaffolding a fresh paper gets the
weak stub, not the fuller structure.

Fix (2026-06-22): added an Implication (so-what) section to both the scaffold
`pitch_tex` (init_paper_layout.py) and the pitch skill template, and made
"Why Believe" demand evidence per point (cite a source per claim). The pitch
backbone is now Hook -> Surprise -> Implication -> Why-Believe(evidence) ->
Still-Fragile -> Next-Evidence-Move, emitted in the sentence-format layout.

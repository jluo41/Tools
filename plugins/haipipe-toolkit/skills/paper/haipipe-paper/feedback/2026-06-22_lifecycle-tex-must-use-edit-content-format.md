---
status: open
created: 2026-06-22
context: lifecycle stage tex generators (haipipe-paper-structure-{seed,pitch,claims,narrative,display,minimap}); format defined by 3-write-edit/haipipe-paper-edit-content + 3-write-edit/_shared/{paragraph-indexing,sentence-format}.md
fixed_in: ""
---
然后lifecycle的paper里，生成这个tex的时候，要符合 Tools/plugins/haipipe-toolkit/skills/paper/3-write-edit/haipipe-paper-edit-content定义的格式，----Pn.Sn---- 的sentence 然后% 当作sentence 分割符  这个也写到feedback里

Distilled ask:
- When a lifecycle stage skill GENERATES a tex (0-lifecycle/*/*.tex), the prose must already be emitted in the canonical edit format, not as freeform wrapped paragraphs.
- Required format (from 3-write-edit/_shared/sentence-format.md + paragraph-indexing.md):
  - paragraph banner: % Para [<file-slug>.<para-slug>] <Role> -- <one-line point>  (three comment lines)
  - one sentence per line, each preceded by  %% ---- Pn.Sm ----
  - a lone  %  line may separate sentences
  - Pn restarts per file, Sm restarts per paragraph
- Rationale: every generated tex (lifecycle contracts included, not only 0-sections/) should share the same sentence-indexing standard so it is editable/trackable by the 4-edit cycle from the moment it is created.

Suggested fix direction (later revision pass):
- Bake the banner + %% ---- Pn.Sm ---- emission into the templates of haipipe-paper-structure-seed/pitch/claims/narrative/display/minimap so newly generated lifecycle tex is born conformant.
- Tables (tabularx) get a banner but no per-sentence Pn.Sm tags (a table is not a sentence stream).

Note: the existing lifecycle of Paper-Personality-Opioid-MedJournal was retro-fitted to this format on 2026-06-22 (format-only, words unchanged) as a one-off; this feedback is about making the GENERATORS emit it by default.

Fix:

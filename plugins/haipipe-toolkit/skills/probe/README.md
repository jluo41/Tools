# Probe

Probe is the shared evidence-acquisition family for a consumer Page.

```text
Probe
├─ PageX      accepted Board Page → exact file/scope binding in OUTLINE
└─ QA Probe   Task/Discovery → QA-bank crossing at LAND (outbound rows only; `haipipe-probe` retired 260901 into `_old/`)
```

The family has one router, `haipipe-probe`, and two Page-local surfaces:

| Lane | Contract | Storage |
|---|---|---|
| PageX | `../board/page-plugins/haipipe-plugin-pagex/SKILL.md` | `<page>/pagex/` |
| QA Probe | `../board/page-plugins/haipipe-plugin-probe/SKILL.md` | `<page>/probe/` |

A THIRD file completes the QA lane and is not listed above because it is not a
surface: `../board/page-workflows/haipipe-page-probe/SKILL.md` is the Board
Page's LAND **cycle** (`haipipe-page-evidence` §🚪) — when a card may be created, how `PP<NN>` is allocated,
and the run receipt. Three files, three altitudes, and each owns exactly one:

```text
  haipipe-probe          the CROSSING   family-wide · paper, application, page
  haipipe-page-probe     the PHASE      board-page only · when, and by whom
  haipipe-plugin-probe   the STORAGE    board-page only · what lands on disk
```

The crossing is stated ONCE, in the router. Until 260821 the phase file restated
§①②③ near-verbatim and had grown a sixth bullet mark that no mark authority
carries; that is why the rule is written here.

PageX is grouped here conceptually but remains a Page plugin physically. This
keeps plugin discovery and the existing Board tab stable. The lanes never share
records: PageX does not create QA cards, and QA Probe does not search Pages.


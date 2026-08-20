# Probe

Probe is the shared evidence-acquisition family for a consumer Page.

```text
Probe
├─ PageX      accepted Board Page → exact file/scope binding in OUTLINE
└─ QA Probe   Task/Discovery → QA-bank crossing in PROBE/EVIDENCE
```

The family has one router, `haipipe-probe`, and two Page-local surfaces:

| Lane | Contract | Storage |
|---|---|---|
| PageX | `../board/page-plugins/haipipe-plugin-pagex/SKILL.md` | `<page>/pagex/` |
| QA Probe | `../board/page-plugins/haipipe-plugin-probe/SKILL.md` | `<page>/probe/` |

PageX is grouped here conceptually but remains a Page plugin physically. This
keeps plugin discovery and the existing Board tab stable. The lanes never share
records: PageX does not create QA cards, and QA Probe does not search Pages.


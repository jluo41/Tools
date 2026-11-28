# Numbering

Part of hai-studio's topic contract (`ref/topic-contract.md`).

## Blueprint bands

The shared ordered registry is
`examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/studio-bands.json`.
The Studio page, structure diagram and `new_topic.py` read this file. Work Blocks (Blueprint) use the same band names
and order; their own `bands:` lines do not rename the shared groups. Empty bands are omitted from the page.

| Numbers | Band | Content |
|---|---|---|
| s01–s09 | Block Structure | One structure for each actual Block type |
| s11–s19 | Block Job UI Preview | Live Block, Job and Task views |
| s21–s29 | Report | Report definitions |
| s31–s39 | UI Plugin | Shared page components |
| s41–s49 | Task Procedure | Task methods owned by their Task types and skills |
| s51–s69 | Skills | Skills used by the Block and its shared mechanisms |
| s71 onward | Studio Type | Shared type requirements or theme-specific type definitions |
| s81–s89 | Theme Guide | The theme's way of working |
| s99 | Guide | Guidance for the particular Block |

A Band is a group, a Studio Type defines content, and a Studio topic holds an actual instance. These are distinct.
A theme may bind each of its Bands to exactly one Studio Type, so the Band names the type (Knowledge does: hai-knowledge A07).
The type definitions are numbered in one run from s71, with no gaps, continuing past s79 (s80, s81 … up to s98)
when there are more than nine: s71 Block Structure, s72 Block Job UI Preview, s73 Report, s74 UI Plugin, s75 Skills,
s76 Theme Guide, then Knowledge's Band types s77 Resources, s78 Methods, s79 Applications, s80 Questions
(hai-knowledge A07). A topic named `sNN-studio-type-*` is in the Studio Type band whatever its decade. Their numbers are identifiers, not a requirement to fill every slot.
A type's `band:` field states where its instances belong; it does not define the group's name.

A Blueprint references a shared type rather than copying its definition. It authors its own type only when the
content contract differs. A type topic presents the top views and left tabs of its instances; its right side states
requirements from `elements.md`. The actual instance shows the real content. Type-definition topics themselves
need no further recursive type definition.

## Actual work

Actual Work Blocks show their own Studio topics, grouped by their configured bands or tags. They do not need a
Studio Type group. The ordinary topic writer's bands are concept (s01–s09), level (s11–s19), report (s21–s29),
server (s31–s39), procedure (s41–s49), run/skills (s51–s59), slides (s61–s69), and guide (s81–s89).
Task methods belong to the relevant Task type and its owning skill. Common page usage belongs to `workbench`;
theme-specific guidance belongs to Theme Guide. A concrete s99 Guide remains useful when it explains its Block.

1. Take the next free number in the selected band; use `--nn` when selecting an explicit identifier such as s99.
2. Preserve topic identifiers and folders. A group's removal does not remove its topics or permit reusing their IDs.
3. Use two digits, a dash and a short kebab name: `s21-report`.

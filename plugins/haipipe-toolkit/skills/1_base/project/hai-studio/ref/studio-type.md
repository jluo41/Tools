# Writing a Studio Type

Part of hai-studio's topic contract (`ref/topic-contract.md`). Rule: CONSTITUTION.md A06.

A Studio Type is a topic that says what every topic of one kind must show. It sits in its Block's Studio Type band.
A type and its topics have the same top buttons and the same left tabs; only the right side differs.

```text
              top buttons        left tabs          right side
the type      the same           the same           what this part must show
a topic       the same           the same           the real thing
```

## Where a type lives

```text
a blueprint Block's Studio Type band      sNN-studio-type-<name>/elements.md     designed, discussed, shown
          │ types_deliver.py
          ▼
this skill                                 gallery/<name>/elements.md               kept; found by name in any SPACE
          ▲
a topic                                    "check_type": "<name>"                 names it
```

1. **Designed in a blueprint Block.** The type topic shows the type as its topics will look, with the requirement
   on the right; it is where the type is changed.
2. **Kept in this skill, in its gallery folder.** `types_deliver.py` copies each type's `elements.md` to
   `gallery/<name>/`; the type topic's `delivery/render.yaml` records it. `ls gallery/` lists every type. Never
   edit a kept `elements.md`. Beside it the folder holds what is written here: `TYPE.md` (how a topic of the type
   is built), `scripts/` and `tests/` (what writes and checks one), `example.md` (a real topic and its picture).
3. **Named by a topic.** The name is the type topic's folder name after `sNN-studio-type-`, so renumbering a type
   topic changes nothing for its topics.
4. **Which copy is read.** In a SPACE that holds the blueprint, the type topic; anywhere else, the kept copy.
   `types_deliver.py --check` fails when the two differ, when a kept type has no blueprint, and when two blueprints
   deliver one name.

## The four questions

Answer them in order; the answers are the type.

1. **Top: what is there several of?** The things a reader picks between first: the skills of a Skills topic, the
   pages of a UI preview, the views of a structure.
2. **Left: what are the parts of one of them?** Under their real names: a file's name, a folder's name with its
   slash, a page part's name. Never an alias.
3. **Right: what does one part show, and where does it come from?** The source decides who writes a topic of the
   type: content read from disk is written by a script; anything else is written by hand.
4. **Which names are fixed?** A name every topic shares is written plainly (`SKILL.md`). A name each topic fills in
   is written in 〈 〉 (`〈skill〉`, `〈folder〉/`).

## The file

`elements.md` in the type topic. One `## ` heading per top button, one `### ` heading per left tab under it.

```text
## 〈top button〉
what:  〈what it is, one sentence〉
why:   〈why a reader needs it〉
from:  〈the file, folder or page the right side reads〉

### 〈left tab〉
what:  …
why:   …
from:  …
must:
- 〈one thing a topic must show here〉
- 〈another〉
> 〈a line of the pattern tree, indented by two spaces per level〉
check: 〈how a person or a script verifies it〉
```

| Line | Feeds |
|---|---|
| `## ` and `### ` | the type's own top buttons and left tabs, and the Check button's groups |
| `what:`, `why:`, `from:` | the requirement page on the type's right side |
| `must:` and its `- ` lines | the "Must show" list; a Check criterion each |
| `> ` lines | the Pattern tree on the requirement page: folders and files as a tree, `# ` after a name for a note |
| `check:` | the Check button's "how to verify" line |
| `  | words` after a name on a `> ` line | that tree line's hover |
| `build:` (before the first `## `) | the hai-studio scripts that build a topic of the type, run by `type_follow.py follow <topic>` |
| `when:` | the part is there only in that case (`when: the skill has a ref/`); without it every topic must have the part |
| `skills:` on a `## ` | skill folders whose `SKILL.md` become that button's real left tabs |
| `base:` | before the first `## `: a SPACE-relative folder whose `elements.md` this type starts from; its buttons come first, the type's own tabs go before the base's |

## A base type

Types that share parts write them once in a base type, a folder with an `elements.md` and no topic:
`base-types/learning/` holds Page's last tab Try explaining, and Draw, Map and Slides. A type names it on a
`base:` line and writes only its own parts; a part it writes again replaces the base's.

```text
base-types/learning   Page › Try explaining · Draw · Map · Slides
   ▲ base:
a learning type       Page › its own tabs, then Try explaining
```

## After writing it

```text
type_requirements.py <type topic>            the requirement pages and the type's own studio-views.json
type_requirements.py <type topic> --check    exit 1 when a page is stale
placeholder_check.py examples                no bare slot name
types_deliver.py                             the type kept in this skill, under its name
```

## A topic of the type

```text
type_follow.py new <type name> <topic>         the type's buttons and tabs, each still showing its requirement
type_follow.py follow <topic> [...]            build it as the type says, rebuild its Check view, then check
type_follow.py check <Block or topic> [...]    what differs from the type; exit 1 on any ❗
```

1. **Start it from the type.** `new` writes the topic's `studio-views.json` from the type and names it
   (`"check_type": "<name>"`). Where only the kept copy is there, the requirement pages are written into the
   topic's own `delivery/requirements/`. The topic reads as its type does from the first minute. A type whose topics a script writes
   (Skills topics, `skills_views.py`) uses that script instead.
2. **Replace each part with the real thing.** A part that still points into the type reads `⬜ still shows the
   requirement`; a name still in 〈 〉 reads `⬜ not settled`. Neither fails: the topic follows, it is not finished.
3. **Hold it to the type.** `check` reads only the type's `elements.md` and the topic's views file, so a new type
   needs no new code. It fails on a missing button or tab the type lists without `when:`, on one the type does not
   list, and on a wrong order. A name the type writes in 〈 〉 stands for zero or more real names.
4. **The Check button** (`check_views.py <topic>`) lists the type's criteria with how to verify each, and claims no
   result (`ref/check-view.md`).
5. `python plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/checks/run.py --target <topic>` runs the follow check with the others.

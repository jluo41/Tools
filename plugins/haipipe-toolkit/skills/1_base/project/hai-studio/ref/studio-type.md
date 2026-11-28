# Writing a Studio Type

Part of hai-studio's topic contract (`ref/topic-contract.md`). Rule: CONSTITUTION.md A06.

A Studio Type is a topic that says what every topic of one kind must show. It sits in its Block's Studio Type band.
A type and its topics have the same top buttons and the same left tabs; only the right side differs.

```text
              top buttons        left tabs          right side
the type      the same           the same           what this part must show
a topic       the same           the same           the real thing
```

No list of types is kept in this skill. Each kind of Block has its own set; open the band to see them.

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
instances: 〈selector of the topics of this type〉

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
| `when:` | the part is there only in that case (`when: the skill has a ref/`); without it every topic must have the part |
| `skills:` on a `## ` | skill folders whose `SKILL.md` become that button's real left tabs |
| `instances:` | where the type's topics are found on the Block page |

## After writing it

```text
type_requirements.py <type topic>            the requirement pages and the type's own studio-views.json
type_requirements.py <type topic> --check    exit 1 when a page is stale
placeholder_check.py examples                no bare slot name
```

## A topic of the type

```text
type_follow.py new <type topic> <topic>        the type's buttons and tabs, each still showing its requirement
type_follow.py check <Block or topic> [...]    what differs from the type; exit 1 on any ❗
```

1. **Start it from the type.** `new` writes the topic's `studio-views.json` from the type's own and names the type
   (`check_type`). The topic reads as its type does from the first minute. A type whose topics a script writes
   (Skills topics, `skills_views.py`) uses that script instead.
2. **Replace each part with the real thing.** A part that still points into the type reads `⬜ still shows the
   requirement`; a name still in 〈 〉 reads `⬜ not settled`. Neither fails: the topic follows, it is not finished.
3. **Hold it to the type.** `check` reads only the type's `elements.md` and the topic's views file, so a new type
   needs no new code. It fails on a missing button or tab the type lists without `when:`, on one the type does not
   list, and on a wrong order. A name the type writes in 〈 〉 stands for zero or more real names.
4. **The Check button** (`check_views.py <topic>`) lists the type's criteria with how to verify each, and claims no
   result (`ref/check-view.md`).
5. `python plugins/haipipe-toolkit/checks/run.py --target <topic>` runs the follow check with the others.

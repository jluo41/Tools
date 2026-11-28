# Design Method Book

One channel's method collection, serving one or more Design Boards. Each Job is one method type.
Signed versions of that type live inside its Job.

## Job / Task Organization

Drawn as b17's folder tree (`delivery/structure/build_organization.py`, trace 261127/1305): Structure and Draw
show the naming rules. Structure embeds the corresponding real DesignMethodBook-Example records beside each rule and includes the live Block. The Book stops at Job name.

```text
Design Method Book
└── 〈Method family〉       Job group · optional
    └── M0x · 〈method〉    Job name   (its signed versions mK.md are files in the Job, not Tasks)
```

**Job group:** the Job's authored `family:`, else its method's family from the method registry
(`hai-design-method/methods/M0x-*/method.md`): M01 is Goal Only, M02 Internal.

**Job name:** `〈method id〉 · 〈method title〉`, read from each method Job's `method` and `title`. M01 and M02 are
different method types, never versions of each other. The stored folders and versions:

```text
DesignMethodBook-Example/
├── j01_M01-goal-only/
│   └── m2.md
└── j02_M02-overall-performance/
    └── m1.md
```

No Task level: the five steps inside a recipe describe Board execution, and signed versions and proposals are
records. A new Board goal or inputs version does not create another Book Job.

## Main

The embedded Method Main presents the method brief, its signed versions and their recipe steps,
evidence from the Boards using those versions, and proposals for improving that type. Main
keeps the Method Book title and route. The example shows these current records through the
shared renderer. There is no selected execution Task or execution Run panel to invent here.

Proposals in `proposals/<slug>.md` are backlog records. Signing and taking in a proposal yields
the next version of its method type. Board execution evidence links back to the Board's actual
Job, Task and Run owners. Book proposals are not Studio topics by default.

## Studio organization

The general structure allows a Block-owned Studio topic beside its method Jobs, and a
Job-owned topic beside that method's versions when the method needs a design discussion.
Block topics belong to the Method Book; method topics belong to the Method type Job that uses
their delivery. These are ownership rules, not a claim that both example levels have topics. No Task-owned branch
is drawn because this Book has no execution Task contract.

This type's structure Studio has Structure, Draw and Skills on top. Each Structure entry includes its real example; the named example entry embeds the live Block. Shared left tabs
select entries within a view; one entry fills the content width. Skills stays in this Studio.

Studio Band names and order are read from b17's s71–s79 definitions through its shared builder. Empty Bands on a real Block remain omitted by the shared page.

## Sources

- Contract: `plugins/haipipe-toolkit/skills/3_theme/design/hai-design/ref/design-ladder.md`, The Design Method Book.
- Method owner: `plugins/haipipe-toolkit/skills/3_theme/design/hai-design-method/SKILL.md`.
- Reader and Main: `plugins/haipipe-toolkit/servers/workbench-design/design_reader.py` and `design_jobs.py`.
- Example 1: `examples/Project-Ladder/design/DesignMethodBook-Example/`, rendered live inside Structure.
- The older five-Task proposal in s05 is historical, not the current Book contract.
- The previous workbench drawing remains in `design-workbench-ui.excalidraw` beside this topic's face;
  the existing Guide reference continues to open it.

### Evidence and unresolved schema

`hai-design/ref/design-ladder.md:26–30,77–89` and `hai-design-method/SKILL.md:24–29`
explicitly define one Job per method type. The two Job faces above contain `method`, `title`,
`versions` and the matching frozen version file. `design_jobs.py:25–30,126–155` groups method Jobs
and renders versions inside Main. The older s05 five-Task proposal conflicts with this implemented
contract and remains historical; implementing method-development Tasks requires a new decision.

There is no separate serialized `job_type` enum in these method faces. “Method type” is the
contract role, while M01/M02 are registered identities. No absent Task types or names are invented.

Recheck both Studios with `python delivery/structure/build_organization.py --check` from this blueprint Block.

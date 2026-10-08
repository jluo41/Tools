Method folders: one design method per group of Design Folders
==============================================================

A DesignBoard may compare design methods. Each method is one group folder,
`2-Design-M<NN>-<slug>/`, with a frozen `method.md` card and one Design Folder per Brief task.
In the Block -> Job -> Task -> Run hierarchy the method plays the Job, the Design Folder the
Task, and a Generate Run is one design unit.

A board with no method folders keeps the plain `2-Design/` and reads exactly as before. A
board may hold both; the plain group then reads as "no method stated".


The tree
--------

```text
<board>/
├── board.md
├── design-goal.md                    the goal every method shares
├── 0-BR-brief/BR00-brief/BR00-brief.md
│                                     the TASKS, one row each; its folder cell names the task's
│                                     Design-NN folder, the same name under every method
├── 1-IN-inputs/                      when used: the input packets methods point to, frozen
├── 2-Design-M01-<slug>/              one method
│   ├── method.md                     the method card (below)
│   ├── Design-01-<audience>-<job>-<venue>/    the Brief's task 1, made by this method
│   └── Design-02-…/
├── 2-Design-M02-<slug>/
│   ├── method.md
│   └── Design-01-…/                  the same task 1, made by method M02
└── 2-Design/                         optional: folders made before methods were stated
```

Each Design Folder keeps the standard shape (`haipipe-design` SKILL.md § Folder shape): its
Page, `draft/`, `scripts/config/`, `runs/`, `results/`. Nothing inside a Design Folder changes.


The method card, `method.md`
----------------------------

One Markdown page: a `# ` title, an optional lead paragraph, then the design unit's three
steps as `## ` sections, in this order. The workbench shows the three sections side by side
above the method's tasks.

```markdown
# M01 · <method name in plain words>

<one or two sentences: what this method is for>

## ① See input

- goal: `design-goal.md`
- packet: `1-IN-inputs/<IN-id>/<IN-id>.md` · sha256 <hash>
- may not see: <what is kept from this method>

## ② Conduct process

- reasoning: direct · freestyle · element-wise, and its budget
- maker: <one model snapshot, or agents with roles, or a person with an agent>
- count: <N designs per unit>

## ③ Check output

- rules: <the hard and semantic checks every method shares>
- grounding: only what ① lets this method see
- predict: <what is predicted, frozen before the trial>
```

The title's first word is the method key, `M<NN>`, the same as the folder's. With no card the
workbench names the method from its folder (`M02 · overall performance`) and says the card is
missing.


The rules
---------

1. **One method per folder, frozen once.** `method.md` is settled before the first Generate
   Run under it, and each Run's config cites it. A change to a method after anything was
   generated is a new folder, `M<next>`, never an edit, so every design traces to exactly one
   method.
2. **Task numbers are the Brief's, shared by every method.** `Design-01` is the Brief's task 1
   under every method, so comparing methods is reading one task across the method folders. A
   method may skip a task; it never renumbers one. A task opened first under a method takes the
   next free number, and the Brief's folder cell records it once.
3. **The Brief lists tasks only.** With method folders the Brief's `method` column is not
   read; the folder says the method. The column stays for boards with only `2-Design/`.
4. **Inputs by reference.** `method.md` points to its input packet by path and hash; it never
   copies one, so a nesting check (each richer packet contains the one before) runs over the
   packets themselves.
5. **Checks stay inside the method.** A method's Verify grounds only on what its ① lets it see;
   a checker never brings another method's insight into a design, and never picks winners.
6. **New questions are new folders.** Varying only the process later (the same packet, another
   reasoning style) is one more `M<NN>` folder beside the others; earlier folders are kept.
7. **Resources per design come later.** A Design Folder will name the resources it used; until
   that contract exists, `method.md` ① is the record of what the method could use.


What the workbench reads
------------------------

```text
Board › Design Tasks    one View per method folder, no All View (the first method opens). Under
                        each method, the design unit's three steps as its own row of Views, each
                        with its part of method.md on top; ② opens:
                          ① See input      the packet(s) the card names, read from 1-IN-inputs/,
                                           and design-goal.md, folded
                          ② Designs        task by task, each design's message and its reason
                                           (the Generate result's rationale.yaml)
                          ③ Check output   task by task, each design's Verify state and its
                                           predicted click-through (rationale.yaml forecast)
                        A task the method has not designed shows "not designed this way yet" and a
                        New Design Folder button that opens it under that method.
Board facts band        … · N methods · …
Page header band        the Design-NN id, then the method's title from ../method.md
Board csv               a `method` column after `folder`
Short links             /_board/design?folder=M02/Design-01 names one method's folder; a bare
                        Design-01 under several methods answers with a page listing them.
                        /w/<board>/m02-design-01 opens that method's page.
```

The writer for every file here is unchanged: the Brief's owner writes the Brief, the Design
Folder owners write the folders, the Design Runs write their Results. The workbench writes only
through New Design Folder, which opens a folder under the method it is clicked in.

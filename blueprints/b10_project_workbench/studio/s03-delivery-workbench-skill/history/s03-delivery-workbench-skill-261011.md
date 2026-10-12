s03 · Delivery: its workbench and its skill
===========================================

New on 261010 (JL: "have a s03 delivery-workbench-skill"); s03 was the Guide's old number, free since it
became s31 (261007). The Studio's twin is s02-studio-workbench-skill.

**Tags:** `Structure` · `UI`

**Stage:** shaping

**Topic:** the Delivery seen from both sides: its workbench (the Delivery view at the right end of the
top row, Studio | Block · Job · Task | Delivery, opened from every level) and its skill
(`/haipipe-delivery`). Jobs and Tasks make outputs; only the Block keeps them, in its one `delivery/`;
each subfolder leads back to the Job or Task folder that made it. A Report stays with each level
(s09-D02); what is handed over lives once, at the Block (s09-D05).

**Feeds:** `reports/` q07_workbench_mapping · q08_workbench_base


Files
-----

```text
s03-delivery-workbench-skill/
├── s03-delivery-workbench-skill.md            this face
├── s03-delivery-workbench-skill.excalidraw    two frames: the idea (makers, delivery/, storage, screen); In Tools
├── s03-delivery-workbench-skill.png           its preview
├── .s03-delivery-workbench-skill.seed.json    generated snapshot for preserving marks
└── build_s03_delivery_workbench_skill.py      the builder (moved from s09's frame 2)
skill: Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-delivery/
```


In Tools
--------

Where its skill and code sit, under `Tools/plugins/haipipe-toolkit/`. The drawing's "In Tools" frame
reads the same off the disk on every build: the skill's folder as it is, its version, and each
function looked up in its file (JL 261011: "show what are the skills related folders in the Tools").

```text
skills/1_base/project/
├── haipipe-studio/     s02 Studio
├── haipipe-delivery/   s03 Delivery   ◀ this topic
├── haipipe-related/    s04 Related
├── haipipe-report/     s05 Report
└── haipipe-run/        s06 Run
servers/workbench/frame.py                        delivery_parts · _delivery_row · delivery_by_source
skills/1_base/page/haipipe-draft/src/common.py    delivery_owner · delivery_dir · delivery_source
```


Decided
-------

s03-D01 · Delivery has one physical owner, the Block: Jobs and Tasks keep no `delivery/` of their own;
    their outputs sit under their source address, `delivery/jNN_<job>/tNN_<task>/<lane>/` (carries
    s02-D14 and s09-D05 on; JL 261010).
s03-D02 · The path is the link: each subfolder leads back to its source, `delivery/jNN_<job>/` to the
    Job folder and `delivery/jNN_<job>/tNN_<task>/` to the Task folder; `delivery_source()` and
    `delivery_dir()` in haipipe-draft/src/common.py map one to the other (JL 261010: "track the
    subfolder to link to the job folder and job/task folder").
s03-D03 · One skill owns the rule: `/haipipe-delivery`, beside haipipe-studio and haipipe-report;
    haipipe-block, haipipe-report, haipipe-cowork and haipipe-draft-delivery point to it instead of
    each keeping a copy. How a file is built stays with its lane owner (JL 261010: "should we have a
    skill named /haipipe-delivery? ... just as we have the /haipipe-studio").
s03-D04 · Delivery sits at the right end of the top row and opens like Studio: only it selected, the
    work row hidden, the level buttons keep the way back (s02-D18; JL 261010).
s03-D05 · A delivery folder keeps its source's name, `delivery/jNN_<job>/` (and `tNN_<task>/` under
    it); no `dNN-<send>/` card and no `dNN_jNN_<job>/` prefix (JL 261011: "could this be still the
    today's version or to make it like dNN_j01_vXXXX?"). A send is one row of one table,
    `delivery/delivery.md` (date · for · from · status), so a resend or a second reader is a row, not
    a copy, and Status turns `sent` only by a person. Why: the path stays the link (s03-D02) with
    nothing to strip; a paper's version Job already names the send (`j01_v1009_nmi`); and `dNN` is
    already a design in the design theme (b12, `run-generate-d<NN>`). Like `related/related.md` for
    what came in (b10 s01-D34), `delivery/delivery.md` lists what went out. Swept 261011: the s01
    screens and the s11 · s12 · s13 mock screens show parts by source, and `run-delivery-<dNN>`
    is `run-delivery-<lane>`, as haipipe-run already names it.
s03-D06 · From a Job or Task, the top row's Delivery opens the Block's Delivery, as Studio opens the
    Block's Studio: a Job or Task has no Studio, Related or Delivery of its own (JL 261011, "apply it
    to all the workbench"). A source row, Block · jNN · tNN, comes first with the open Job or Task
    picked, and each source's part shows inside it. This refines s09-D05's "the Job and Task views
    show their own part": the part is now a pick inside the Block's Delivery, not a separate page.
    Built by the b16 session in servers/workbench/frame.py (render's Delivery mode).


Open
----

1. Settled 261011 by s03-D05 (named by source, one row per send). Was: each delivery is one dNN card named by the send,
   `delivery/dNN-<send>/`, with a face `dNN-<send>.md` (For · From · Status · Files); the parts keep
   their source folder inside it; Status turns `sent` only by a person, never by a build. Today the
   folders are named by source (`delivery/j01_v1009_nmi/`): rename now, or at the next send?
2. A Report's own build (`delivery/reports/qNN_<topic>/`): a row in `delivery.md` too?
3. Do Delivery rows take the Studio's groups (Current and tags), the same code?
4. Built 261011 (b16 session): the Block's own Delivery ends with "By source" (part · from · files),
   one row per Job and Task part, each linking back to its folder (s03-D02).
5. A deliverable that pulls from several Blocks (a meeting deck): its own Block, as a paper Board is?

(write here, or mark the drawing in red)

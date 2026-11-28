s12 · Block Job UI Preview: Blueprint
=====================================
view: overview
emoji: 📐

**Stage:** shaping

**For:** a blueprint Block's page (a Block that plans a tool: its Jobs of design, code and skills), looked at on this Block, b17_theme_work

**Delivery type:** ui

**UI preview:** Job · blueprint

**Covers:** the blueprint Block page, one of its Jobs and one Task, as the server renders them

**Excluded:** a Job and its Tasks as work code (s11, the Work Job UI preview); the Block's folder and organization (s02, Work Block (Blueprint) Structure)

**Why:** does a blueprint Block page show what each Job builds and where its code and rules live, at a glance?

**Topic:** A Blueprint UI Preview: its Page shows the live pages of blueprint/b17_theme_work, its Block, the j12 side pane Job and its t03 pane speed Task, so a change to the blueprint pages shows here on the next open.

**Feeds:** none


Files
-----

```text
s12-blueprint-job-preview/
├── s12-blueprint-job-preview.md     this face
├── s12-blueprint-job-preview.html   the list of views: Page, the live pages of blueprint/b17_theme_work
├── s12-blueprint-job-preview.excalidraw   its drawing, with its .png
├── build_s12_blueprint_job_preview.py draws it from the Block's folders
├── delivery/ui/job-row-builds.html    its quick page
└── studio-views.json                  its views, written by s72's build_type_pages.py
```


Decided
-------

- s12-D01 · The Block Job UI Preview band has a Blueprint Job UI preview beside work, cowork and discovery (JL 261127: "you should also add the studio for the blueprint JOb UI Preview as well")


Open
----

(write here, or mark the drawing in red)

Checklist
---------

- ✅ Page-Job · job-rows
- ✅ Page-Job · job-overview
- ✅ Page-Job · job-tasks
- ✅ Page-Job · job-findings
- ✅ Page-Task · task-rows
- ✅ Page-Task · task-overview
- ✅ Page-Task · task-runs
- ✅ Page-Task · task-findings
- ✅ Job types
- 🙋 Job types · group types: no file says which Job group is of which type
- ✅ Task types
- 🙋 Task types · group types: no file says which Task group is of which type
- ✅ QuickHtml
- ✅ Draw

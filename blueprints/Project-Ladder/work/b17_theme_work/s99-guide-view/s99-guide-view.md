s99 · Guide view: how to use this Block's page
==============================================
view: overview

**Tags:** `Block UI`

**Stage:** shaping

**For:** a 🧭 Guide section on a work Block's focus page, an item of the section menu beside Report, Jobs, Studio, Interactions, Decisions, Things to Know, Checklist, Timeline and Skills (the shared list, `servers/workbench/page/job_task_views/work_frame.py` `SHARED`), as a screen preview in `delivery/ui/`, for JL to agree before the code draws it

**Delivery type:** ui

**UI preview:** Guide

**Covers:** how this theme's pages are used (the levels and the steps, from `servers/workbench-work/guide/guide.yaml` and `guide/method.md`); how to read this Block (its Topic from `board.md`, each Job's goal by band, which Job to read first, where the 🙋 waits are)

**Excluded:** the theme's Guide shared by every Block (Description, Method, RoadMap; s31-s39); the Jobs section's rows and Main (s11-work-job-preview)

**Why:** a person opening a Block for the first time: what is this page for, and where do I start?

**Topic:** s99 is the Block's own Guide, one per Block, always last. It reads two things in one section: the theme's way of working, said once at the level it acts on (Block, Job, Task), and this Block's own map, drawn from its face and its Jobs' faces, ending at what waits on the reader. The preview draws it over `blueprints/Project-Ladder/work/b01_example_work`, the work theme's example Block.

**Feeds:** `servers/workbench/page/job_task_views/work_frame.py` (`SHARED`), after JL looks at this preview


Decided
-------

- A UI preview topic: its page `s99-guide-view.html` lists its views; Guide is a quick view (Studio › Effect) until the section is in the code, then a live view over b01_example_work takes its place under Page and Guide fades (`class="old"`).
- Inside the section, top-view-left-tab-right-content: two left tabs, Reading this Block first, then Using work pages.

Open
----

- Where 🧭 Guide sits in the menu: the preview puts it after 🧰 Skills, last before Files.
- Whether Reading this Block is written by hand in a face field or read from the Jobs' faces each time (the preview reads them).
- The same section on a Job page (its Tasks, which to read first) and on other themes.

Files
-----

- `s99-guide-view.html`: the topic's page; Studio lists its views as left tabs
- `delivery/ui/guide.html`: the quick view, the 🧭 Guide section as it would read on b01_example_work

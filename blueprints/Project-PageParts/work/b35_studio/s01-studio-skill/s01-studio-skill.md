s01 · What a Studio is, and what each sNN delivers
==================================================

**Stage:** shaping

**Tags:** Studio

**For:** a deck, and the haipipe-studio skill: SKILL.md's opening (what a Studio is; one sNN, one idea, one delivery; the kinds table; where an sNN sits and how many; how it lives from a chat to closed) and the `For:` line `new_topic.py` writes on every new face (JL 261030: "so each studio with a clear delivery, right? either skills or draft, or display"); for anyone who opens an sNN.

**Delivery type:** skill

**Covers:** what a Studio is; what an sNN hands over (a deck, and one thing); the kinds of sNN by level; the kinds of Block; where an sNN sits and the limits per level; how it lives (stages, passes); the `For:` line; the five parts of an sNN's drawing; how every Theme uses the Studio (its kinds, where the render writes, who renders)

**Excluded:** an sNN's page and the Block map (s02); its mind map and leaf drawings (s03); slide rules (b34-s02); building other Blocks' deliveries

**Topic:** one sNN, one idea, one delivery. An sNN starts as one open idea and ends in what it hands over: a deck, always, and the thing the deck is about. JL 261030: "studio: from idea to delivery"; "what I mean is one studio, one idea and one delivery"; "so one studio should link to a delivery, this is the outcome oriented"; "delivery could be: slide (a must) and the associated skills, code, or figures, draft, etc.". The kinds come from a scan of every `studio/` topic and `delivery/` folder in the eight SPACEs on 261030: 825 sNN (and 184 old `s00-background-and-index` sNN), 157 `delivery/` folders. The drawing has five parts: Idea; Now, this Block's Studio as it stands, read from the faces (JL 261030: "should we have another area for the current studio structure things?"); Design (the biggest: "for this idea, we can design many things, and will change it a lot along the way"), holding proposals only: A the rule, B the kinds of sNN by level, C the kinds of Block; Process; Delivery.

From b35 s02 (what-is-a-studio), merged 261030: what a Studio is, what it holds, how it lives and ends, and how it sits beside `related/` and `delivery/`. JL 261029: "I want to have a slide about how to define a studio ... I am not sure about it." The rules so far are spread over haipipe-studio, haipipe-related and haipipe-delivery, and two of them disagree; this topic puts the open choices side by side, one idea per slide. In one line (261030, b35-s01): a Studio runs from idea to delivery.

From b35 s03 (topic-lifecycle), merged 261030: the life of one Studio topic: a chat on a level makes it, each later chat is a pass, its stage walks explore → shaping → agreed → closed, and only the agreed version is copied to `delivery/`. JL 261029: "I want the slides to draw what is the life cycle of the studio, from the very begining, to the end, and close it". Two steps are not settled: who may say agreed, and what a closed topic leaves behind.

**Feeds:** haipipe-studio SKILL.md and `scripts/new_topic.py`; haipipe-delivery (a row for a delivery that is not a file).


Files
-----

```text
s01-studio-skill/
├── s01-studio-skill.md            this face
├── s01-studio-skill.excalidraw    its drawing
├── build_s01_studio_skill.py     its builder: redraws the drawing and its preview from disk
├── s01-studio-skill.mindmap.md    its mind map, a drawing per leaf in map/
├── s01-studio-skill.ideas.md      the open ideas, one per slide
├── s01-studio-skill.slides.json   each slide's content and leaf
├── map/<leaf id>-<words>.excalidraw  one drawing per leaf
├── result/                 working output; merged sNN kept whole under result/merged-*/
└── delivery/               the agreed version: deck/ (stays) and skill/ (renders into haipipe-studio SKILL.md); render.yaml
```


Decided
-------

s01-D01 · One sNN, one idea, one delivery: an sNN starts as one open idea and ends in its own delivery, named first on its face in a `**For:**` line (JL 261030: "what I mean is one studio, one idea and one delivery"; "studio: from idea to delivery").

s01-D02 · A delivery is a deck, always, and the thing the deck is about: skills or code, a figure, a draft, a data table, a server package; the thing gives the sNN its type (JL 261030: "delivery could be: slide (a must) and the associated skills, code, or figures, draft, etc.").

s01-D03 · In b35 this sNN comes first (JL 261030: "I think the s01 should be the studio-delivery-type"); a Block's delivery is the deliveries of its sNN together, listed in its board.md `## Deliveries`.

s01-D04 · The 184 old `s00-background-and-index` and `s00-overview` folders, and their 44 `runs/run-draw-s00/`, are removed from WellDoc, Knowledge, Physician and REACH: moved to the Trash (`~/.Trash/s00-cleanup-261030/`, with a tar backup), and the list lines naming them taken out of 35 board and README faces (JL 261030: "yes you should do it"). 42 faces still link to them inside a sentence or table, for each page's owner.

s01-D05 · One `studio/` per Block, one sNN numbering; each topic names the level it hangs from in its face, `**At:** j01` (b17, j01 or j01.t03) (JL 261029: "in this way, sNN should be bNN sNN, or tNN sNN"). Replaced by s01-D12 on 261030. (Was b35 s02-D01, merged 261030.)

s01-D06 · A topic's address is `bNN.jNN-sNN` (dots for the ladder, a hyphen before the topic, e.g. `b17.j01-s07`); the folder stays `sNN-<topic>/` (JL 261029: "it should be b17.j01-s07"). (Was b35 s02-D02, merged 261030.)

s01-D07 · Never write an address alone: the address, a colon, each level's short name (folder name without its number, first three words) joined by dots, then ` @ ` and the topic, `-` inside a name as `_`: `b17-s04:theme_work @ workbench_page_structure`, `b17.j01.t03-s09:theme_work.tables.cut @ which_cut_first` (JL 261029: "nvery just give the bNNjNN index"; "let's do b17-s04:theme_work @ workbench_page_structure"). (Was b35 s02-D03, merged 261030.)

s01-D08 · The main things are four: Block `bNN`, Job `jNN`, Task `tNN` and Studio topic `sNN`; a Run `rNN` sits inside its Task. An open topic (explore or shaping) is a decision a person owes; Work rows say how many, "N open topics waiting on you" (JL 261029: "so we just have the bNN jNN tNN and sNN, they are the main things"; "more sNN, means for that item, more human to intervene"). (Was b35 s02-D04, merged 261030.)

s01-D09 · A Studio topic is where we go round with a person on one thing (an open question, a figure, a deck) until it is good: each round is a pass, "agreed" is the person saying it is good, and the agreed version leaves for `delivery/`. A Task's figure gets a topic at that Task, `**At:** j01.t03` (JL 261029: "一个 task 他画图放到 studio 因为我们是要给这个人说话嘛 ... 我们要看这个图弄得好不好 然后就要不停地改"). (Was b35 s02-D05, merged 261030.)

s01-D10 · A topic has its own `result/`: what we made while thinking (mock pages, trial pictures, extra drawings and their builders), messy is fine; the top of the topic stays small. A Task Run's output stays in the Run's `result/` and the topic only shows it (JL 261029: "studio 应该也要有 results"). (Was b35 s02-D06, merged 261030.)

s01-D11 · `delivery/` gets only the clean version, and only after rounds in the Studio: a Task's result goes round with the person, and the agreed version is copied out with its version number (JL 261029: "delivery 可能是从 task 的 results 来 ... 肯定是在我们 studio 腻歪几轮之后，才能够到 delivery"). (Was b35 s02-D07, merged 261030.)

s01-D12 · No `studio/` folder: each sNN sits directly beside the Jobs or Tasks of the level that uses its delivery (a Block's beside its `jNN_`, a Job's beside its `tNN_`, a Task's beside `runs/`), one sNN numbering per Block, and at most 9 at a Block, 5 at a Job, 3 at a Task (JL 261030: "we don't have the studio/sNN, we just have sNN, along side with jNN, to make it visible directly"; "we might have many sNN, but we need to control the numbers"). (Was b35 s02-D08, merged 261030.)

s01-D13 · One picture holds the whole life: a chat on any level (Block, Job, Task) makes the topic; it holds Items, Mind map, Slides and passes; each later chat adds a pass; the agreed version goes to `delivery/`, then the topic closes. The picture is b35-s01's slide 07 (JL 261029: "I want one slide to show the whole picture", from JL's ladder sketch). (Was b35 s03-D01, merged 261030.)

s01-D14 · An sNN hands over through its own `delivery/`: the agreed version goes there (its deck, which stays, and the thing), then a render writes the thing out to where it is used; for s01, `delivery/skill/` renders into haipipe-studio's SKILL.md between `<!-- render b35-s01 <block> -->` markers (`render_delivery.py`), and `new_topic.py` is built by j01 t02 (JL 261030: "studio/sNN/delivery, this is the delivery, and then we do the render, to render the delivery out, to that area, like the haipipe-studio").

s01-D15 · The Studio is the same in every Theme; a Theme plugs in only by its kinds of delivery, where the render writes, and which skill renders, and that Theme's own skill renders (haipipe-paper-assemble a paper, haipipe-design-delivery a release), never haipipe-studio; the table is `delivery/skill/themes.md` (JL 261030: "how could the haipipe-studio skill will be adopted to different theme?"; "okay, good, please go ahead and do it").

s01-D16 · excalidraw-studio owns an sNN's five-part drawing (Idea, Now, Design, Process, Delivery; `five_parts.py`); excalidraw-job, -task and -story draw only its Design part (JL 261031, b35 r01 Q1: A).

s01-D17 · No `studio/` folder anywhere: an sNN sits under its Block, Job or Task folder, and every loose drawing left in a `studio/` becomes an sNN; then `studio/` is deleted (JL 261031, b35 r01 Q2: C, "We will not have the studio anymore, we will just use the sNN under the block, or job or task folder"). It confirms s01-D12.

s01-D18 · A topic's Process part shows each Run under its Task with its status, agent and skill from its run.yaml (JL 261031, b35 r01 Q3: A, "Yes, we should do it").


Open
----

1. Are these the kinds of sNN, each with what it hands over: story → the claim and its Sections, paper version → full paper in Word and PDF, question → report page, table contract → data table, display → figure, section → written Section, run plan → server package or code, design → skill or tool change, ask → letter or meeting note?
2. Is an sNN's deck its own slides only, or also gathered into one Block deck in an s61 topic, as b11 and b12?
3. Code, a data table and a server package leave no `delivery.md` row: add a row that names where it went?
4. Must `For:` be filled before an sNN leaves explore?
5. Process as a real Job: make `b35_studio/j01_studio_delivery_type/` with Tasks t01 to t05 and their Runs, as the drawing shows, so each tick comes from disk?
6. Is each kind on its level: Block (story, question, design, ask), Job (run plan, table contract, paper version: the whole paper, Word and PDF), Task (display, section: a paper's Section, its draft Task)? Only 44 of 641 sNN carry an `**At:**` line today.
7. The kinds of Block (Data, Algorithm, Model, Analysis, Endpoint, Tool, Paper, Discovery, CoWork, Labeling), each with what it hands over and its s01 kind: does every Block list what it hands over in its board.md `## Deliveries`?
8. Is "a Studio" one topic (`sNN-<topic>/`) or all of a Block's topics (`studio/`)? (from b35 s02, what-is-a-studio)
9. Who says a topic is agreed: only JL, or the person the topic is for? (from b35 s03, topic-lifecycle)
10. Is a closed topic kept, folded in `studio/`, or deleted once its answer is in Report and `delivery/`? (from b35-s01) (from b35 s03, topic-lifecycle)
11. When does the "Send to delivery" button turn on, and what does it copy? (from b35 s03, topic-lifecycle)

(write here, or mark the drawing in red)

Delivery preview
----------------

**Target delivery:** An executable Studio guide with a creation checklist and worked example.

**Reader:** Agents and people starting a Studio.

**State:** review prototype; not accepted or released.

- [Open delivery](delivery/web/index.html)
- [Main delivery Draw](delivery-design.excalidraw)
- [Draw preview](delivery-design.png)
- [Explanation slides](delivery/deck/index.html)
- [Delivery contract](delivery/web/contract.html)

The source is `../scripts/delivery-specs.json`; `../scripts/build_delivery_previews.py` generates the review package. Earlier drawings remain unchanged.

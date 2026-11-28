# A proposal topic: one section, drawn so it can be written

Part of hai-studio's topic contract (`ref/topic-contract.md`).


A topic that works on one section of a proposal or a paper draws five frames in two rows. The worked
example is b21_event_cgm's s03 for SHIFT Task 2.1. The first row is the thinking, each frame one screen; the second row is the long reads,
each one frame that grows down (`canvas.reads_down`).

```text
row 1   ① the idea workflow        ② why and the plan        ③ the proposal figure
          one screen, one flow        one screen                one screen, caption beside
row 2   ④ the draft today, marked up        ⑤ the section written out
          one frame, read down                one large frame, read down
```

1. **① The idea workflow**: one connected flow from the inputs through the steps and the model to its
   use, every loop drawn closed (in s03 the data loop, the model-improvement loop, and the red loop that
   stops when there is no gain). The checks that would show it works sit beside it; each open question
   is red, inside the box it is about. The words are cut short until it fits one screen.
2. **② Why and the plan**: the lab's own papers it builds on (each one's status and what it gives this
   section), a small sketch of what the model sees, and the plan in order.
3. **③ The figure**: the proposal's picture, its change notes and caption in a column beside it.
4. **④ The draft today, marked up**: the shared draft is only read, printed to PDF, and each related
   passage is cut from its own page in the draft's order. A numbered red box on the passage, an arrow to
   a note: its title, `Change:` the wording we propose, `Why:`, and in red `Ask the team:` with the name
   of who can answer. The frame closes with every open question again, by who can answer.
5. **⑤ The section written out**: every part of the template as a section map read left to right:
   paragraph (its job), point (role and gist), Text (our wording), Evidence. Rules below.

The section written out: the bullet points sit close to each other; on the right side the evidence is free in
style, may take several columns, and is joined to the text by lines:

1. **Tight text**: text rows sit 8 px apart; the evidence never pushes them apart.
2. **Free evidence**: cards in two columns on the right, each beside the first text it supports; a line
   joins text and card and goes around other cards, never through one.
3. **No long lines**: a later text more than about one screen (1,400 px) from its card gets a one-line
   card naming the item ("full card above") instead of a long line.
4. **The card**: `E<nn> · VALUE|CITE|DISPLAY · label`, what it needs, where it comes from. Black when
   traced to a published paper or a repo file; dashed red while it waits, with its ask and who answers.
5. **The figure is evidence**: a DISPLAY item whose full card holds the picture and its caption, at the
   figure's own row. The frame closes with every waiting ask, by who can answer.

Where the words live: every word is in the face, in yaml blocks the builder reads (s03: `idea`,
`workflow_figure`, `draft_changes`, `task21_section`, `task21_evidence`); the builder only lays them out,
so a wording change is a face edit and a rebuild. A draft change finds its passage by `anchors` (a start
and an end phrase, each found exactly once in the draft): when the draft is edited the boxes move on the
next rebuild, and a phrase found twice or not at all stops the build. The written-out section prints its
word count against the template's page budget. Our wording reaches the shared file by a person, never by
an agent.

What went wrong on the way, so it is not done again:

```text
❗ one 9,200 x 5,650 px idea frame        "This is too huge"            ✅ fits one screen
❗ the whole drawing scaled to 20%         words 6 px, 3 px at 50%       ✅ words stay 20 px
❗ the written-out cut into 9 frames,       "should be one large frame"   ✅ one frame, read down
   the draft into 4
❗ evidence stacked under each point       text rows spread apart        ✅ evidence laid out on its own
```

The builders to copy from (in the SPACE that holds the worked example, `<world>/Project-<Name>/cowork/b21_event_cgm/studio/`):
`s03-related-work-structure/idea_frame.py` draws ① and ②; `draft_pages.py` ④; `task21_section.py` ⑤, with
its line routing (`evidence_route`); `build_s03_related_work_structure.py` reads the face and the draft,
draws ③ and sets the rows; `_build/draw_kit.py` and `_build/word_pdf.py` are the level's helpers.

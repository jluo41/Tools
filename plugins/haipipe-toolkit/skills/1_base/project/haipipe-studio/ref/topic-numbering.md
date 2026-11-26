# Numbering

Part of haipipe-studio's topic contract (`ref/topic-contract.md`).


```text
s00       none              retired 261029: Report › MindMap shows the Block; numbers start at s01
s01-s09   concepts          what the level is, its trees and words
s11-s19   levels            Block · Job · Task, one topic each
          (b17, the work theme Block: Job UI Previews, one per theme, s11 work · s12 cowork · s13 discovery;
           ref/ui-preview-topic.md)
s21-s29   runs and skills   the Runs, the buttons and the skills that own them
s31-s39   Guide             the theme's Guide: Description · Method · RoadMap Draw · Related Paper
s41-s49   Task procedures   one per Task type of a theme: its steps, Runs, disk, tabs, prompts (sNN-task-<type>-procedure)
s51-s59   server            how the screens are served
s61-s69   slide drafts      a proposed deck: its logic flow and its slides, before the deck is built
s99       Block Guide       how to use this Block's page; one per Block, always last, a UI preview topic
```

1. **Next free in its band**: `new_topic.py --band <band>` takes the lowest free NN there.
   s99 is never in a band: it is made by hand with `--nn 99`. It is this Block's own Guide; s31-s39
   design the theme's Guide (Description, Method, RoadMap), shared by every Block of the theme.
2. **Never reused**: a number stays with its topic; a renumbering is written into the face
   of the Block (a "Renumbered" note), never done silently.
3. **Two digits**, then a dash and a short kebab topic: `s21-run-skill`.

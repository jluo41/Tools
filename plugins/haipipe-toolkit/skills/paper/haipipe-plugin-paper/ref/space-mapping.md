# Paper Plugin · Workflow × Space mapping

This is the reader-facing mapping for `haipipe-plugin-paper`. Spaces are UI
projections; the paths below are authority or receipt addresses, not new
Paper Plugin stores.

| Run-Type / record | Setup | Ideation | Story | Run | Delivery |
| --- | --- | --- | --- | --- | --- |
| `paper.setup` | `action · SetupPlan · board.md + Paper root` | `read · Idea/Story folders` | `read · StoryA folder` | `register · SessionSpec · explicit setup` | `read · delivery config` |
| `paper.ideation.generate` | `—` | `action · IdeaPool · A1-Story/Story00-ideation/` | `—` | `run · IdeaGeneration · native receipt` | `—` |
| `paper.ideation.test` | `—` | `review · PressureTest · Story00` | `—` | `run · IdeaPressureTest · native receipt` | `—` |
| `paper.ideation.select` | `—` | `action · Admission · Story00` | `route · StoryHandoff · StoryA` | `run · IdeaAdmission · native receipt` | `—` |
| `paper.story.shape` | `—` | `read · admitted Idea` | `action · StorySpine · StoryA C1–C8` | `run · StoryShape · native receipt` | `—` |
| `paper.story.review` | `—` | `—` | `review · ClaimBoundary · StoryA C5` | `run · StoryReview · native receipt` | `—` |
| `paper.story.route` | `—` | `—` | `action · StoryRoadmap · StoryA C6–C8` | `route · Section/Task/Discovery · native receipt` | `read · C8 compile order` |
| `paper.compile` | `read · delivery config` | `—` | `read · C8 compile order` | `run · CompileReceipt · delivery/` | `action · Manuscript · delivery/latex + delivery/word` |
| `paper.round.respond` | `read · Round folder` | `—` | `route · Story or Section` | `run · RoundReceipt · Bc-<desk>-Round/` | `review · Round · Bc-<desk>-Round/ + delivery/word-feedback/` |

The map does not allocate a Run, close a gate, or replace the authority that
owns a cell. Empty cells are intentional.

## Folder tree × Run-Type

The same map seen from disk: which folder each Run-Type reads, writes, or
runs in. The Paper Plugin draws the REAL folder tree of the paper as a nested
explorer in Run Space › Workflow map, matches each real folder to one `slot` here by its shape
(`board.md` · `A1-Story/Story00…` · `A1-Story/Story<Letter>…` · `Ba/Bb/Bc-…`
· `delivery/` · the project's task and discovery homes), and shows that
slot's Run-Types in a right-hand column aligned beside the tree, on the first
folder of the slot (the `holds` column stays here as the map's own record; the
tree shows only names, counts and Run-Types); it also adds a `folder on this
board` column to the map above. The other cells are read as written.

| slot | folder | holds | Run-Types acting here |
|---|---|---|---|
| `board` | `board.md` | Board identity: `dialect: paper`, `paper-root`, the `blocks:` / `discoveries:` claims, Links (venue-page, delivery) | `paper.setup` |
| `story00` | `A1-Story/Story00-<direction>/` | the idea pool: the Page, `outline/<stem>-outline-vN.md` (Ideas ranked), `outline/<stem>-evidence-items.md`, `workflow/selection.yaml`, `handoff/paper-ideation.yaml`, `runs/ridea-NN_<slug>.md` + `results/` | `paper.ideation.generate` · `paper.ideation.test` · `paper.ideation.select` |
| `story` | `A1-Story/Story<Letter>-<desk>-<idea-slug>/` | the Story page C1–C8 with its `haipipe:compile-order` block; `runs/rclaim-NN · rtask-NN · rnarra-NN` + `results/` | `paper.ideation.select` · `paper.story.shape` · `paper.story.review` · `paper.story.route` · `paper.round.respond` |
| `main` | `Ba-<desk>-Main/` | one `S-<desk>-Main-<N>-<Title>/` per Section: the Page, `outline/` (plan, evidence items), `runs/` + `results/` (rp-, re-, rd), `delivery/latex · word · web/` | `paper.story.route` · `paper.compile` · the Page workflow (haipipe-page) |
| `appendix` | `Bb-<desk>-Appendix/` | one `S-<desk>-Appendix-<L>-<Title>/` per appendix, same shape as Main | `paper.story.route` · `paper.compile` · the Page workflow (haipipe-page) |
| `round` | `Bc-<desk>-Round/` | one `RD<NN>-<desk>-<slug>/` per feedback batch: `feedback/` · `sent/` · `released/` · `delivery/` | `paper.round.respond` |
| `delivery` | `delivery/` | `paper-build.toml`, `build.py`, `build-manifest.json`, `display-register.md`, `latex/` (master.tex, sections/, appendices/, displays/, the PDF), `word/`, `word-feedback/` | `paper.setup` · `paper.compile` · `paper.round.respond` |
| `tasks` | `<project>/tasks/` | the Task home (`task/` on older projects): `bNN_<block>/jNN_<job>/tNN_<task>/` with `runs/` + `results/` + `scripts/`; the Execution Supporting Runs Evidence Items cite | `paper.story.route` · Supporting Runs |
| `discoveries` | `<project>/discoveries/` | the Discovery home: `bNN_<evidence board>/jNN_<inquiry>/tNN_<task page>/` with `discovery.yaml`, `runs/rNN_*.sh` + `results/`; the Discovery Supporting Runs Evidence Items cite | `paper.story.route` · Supporting Runs |

A folder that is missing on a board is shown as ⬜ with its pattern; the map
never creates it.

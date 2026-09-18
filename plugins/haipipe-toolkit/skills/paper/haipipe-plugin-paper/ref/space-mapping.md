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

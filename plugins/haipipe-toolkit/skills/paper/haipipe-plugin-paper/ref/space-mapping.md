# Paper Plugin · Run Specs and controls × Space

Read `haipipe-paper-workflow/ref/run-workflow.md` for the canonical definition.
This map is its presentation by Space; each parameterized Spec must be bound
to a real target before commissioning. Control rows do not count as Runs.
The map neither allocates a Run nor closes a gate. Setup Apply remains a
preview until its writer is implemented and an authorized application succeeds.

| Spec / control | Setup | Ideation | Story | Run | Delivery |
| --- | --- | --- | --- | --- | --- |
| `idea.<idea>` | — | candidate discussion | selected handoff pointer | native ridea Ticket/Result | — |
| `claim.<story>.<claim>` | — | — | C5 support judgment | native rclaim Ticket/Result | — |
| `obligation.<story>.<row>` | — | — | C7 obligation judgment | native rtask Ticket/Result | — |
| `narrative.<story>.<section>` | — | — | C8 telling judgment | native rnarra Ticket/Result | — |
| `support.<target>` | native owner | generation/test dependencies | C6/C7 obligations | Task/Discovery/selected owner receipt | — |
| `structure.<page>` | Page owner | selected Ideation structure | selected Story/Section structure | native RP | — |
| `write.<page>.<scope>` | Page owner | selected prose | selected Story/Section prose | native RP | — |
| `evidence.<page>.<item>` | Page owner | typed bindings | typed bindings | native RE and Supporting Results | — |
| `deliver.<page>.<format>` | declared target | Page surface receipt | Page surface receipt | native RD | one Page artifact |
| `compile.<paper>.<build>` | validated config | — | selected C8 order | compile Ticket/Result | current build manifest |
| `response.<round>` | frozen base build | — | routed repairs | response Ticket/Result | response and frozen answer build |
| `paper.setup` | control: preview/apply | — | — | no automatic Run | config location |
| `paper.ideation.select` | — | control: sole human I3 | G0 handoff validation | no selection wrapper Run | — |
| `paper.story.route` | — | — | control: G1/dependencies/G2 | native Spec references | compile-order pointer |
| `paper.section.route` | — | — | control: G3 release per C8 row | selected Section Specs | — |

## Folder tree × Spec or control

The renderer matches real folders to these slots. Missing folders are shown
as missing; the map never creates them. Stored records remain with their owners.

| slot | folder | holds | Specs / controls acting here |
|---|---|---|---|
| `board` | `board.md` | Board identity and paper-root; aggregate Runtime references | `paper.setup` |
| `story00` | `A1-Story/Story00-<direction>/` | Ideation Page, source projection and sole I3/handoff pointers | `idea.<idea>` · `support.<target>` · `structure.<page>` · `write.<page>.<scope>` · `evidence.<page>.<item>` · `deliver.<page>.<format>` · `paper.ideation.select` |
| `story` | `A1-Story/Story<Letter>-<desk>-<idea>/` | C1–C8, judgment records and compile-order block | `claim.<story>.<claim>` · `obligation.<story>.<row>` · `narrative.<story>.<section>` · `structure.<page>` · `write.<page>.<scope>` · `evidence.<page>.<item>` · `deliver.<page>.<format>` · `paper.story.route` · `paper.section.route` |
| `main` | `Ba-<desk>-Main/` | Main Section Pages, RP/RE/RD and accepted bindings | `structure.<page>` · `write.<page>.<scope>` · `evidence.<page>.<item>` · `deliver.<page>.<format>` · `paper.section.route` · `compile.<paper>.<build>` |
| `appendix` | `Bb-<desk>-Appendix/` | Appendix Section Pages and native work | `structure.<page>` · `write.<page>.<scope>` · `evidence.<page>.<item>` · `deliver.<page>.<format>` · `paper.section.route` · `compile.<paper>.<build>` |
| `round` | `Bc-<desk>-Round/` | one RD Page per feedback batch, ledger and frozen builds | `response.<round>` · `structure.<page>` · `write.<page>.<scope>` · `deliver.<page>.<format>` |
| `delivery` | `delivery/` | config, build manifest and generated outputs; commissioned compile records | `paper.setup` · `compile.<paper>.<build>` · `response.<round>` |
| `tasks` | `<project>/tasks/` | native Task Tickets, Results and receipts | `support.<target>` · `paper.story.route` |
| `discoveries` | `<project>/discoveries/` | native Discovery Tickets, Results and receipts | `support.<target>` · `paper.story.route` |

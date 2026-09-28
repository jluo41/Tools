# Paper Run cards

What the Paper workbench shows in each Space's Runs panel: one card per paper
Run type, each with the button a person sees and the prompt that button
copies. The Run Specs themselves stay in `run-workflow.md`; the owning skills
keep their authority.

A `🔘 BUTTON` line is `label · Space · ticket pattern · views <names>`. The
pattern is a regular expression on the ticket file name; `-` means the button
only copies a prompt, because its runs live with another owner. `views` names
the tabs or views the button shows in (none = every view of the Space).
`💬 PROMPT` is the text the button copies; `{page}` is the Page the run sits
on, `{target}` the selected idea, row or Section, `{paper}` the paper folder.

Section runs are the Section Page's own runs (`haipipe-page-workflow/ref/run-cards.md`),
shown under three buttons, one per Page Space.

## `paper.judgment.idea` · `ridea-NN_<slug>`

🔘 BUTTON   Idea review · Ideation · ^ridea-
💬 PROMPT   /haipipe-paper-ideation review {target} on {page}: judge this idea against its evidence and record its rationale, limits and next question as a new version.

## Idea generation and tests · owned by `haipipe-ideation`

🔘 BUTTON   Generate ideas · Ideation · -
💬 PROMPT   /haipipe-ideation-generate {page}: propose new candidate ideas for this paper and write each one as an Idea Card.

🔘 BUTTON   Test idea · Ideation · -
💬 PROMPT   /haipipe-ideation-test {page} {target}: run the novelty and pressure tests on this idea and record the Result on its card.

## Story writing · the Story Page's own `rp-` runs

🔘 BUTTON   Story revise · Story · ^rp- · views spine
💬 PROMPT   /haipipe-page run {page} rp-sec: revise {target} of the Story; keep its C1–C8 contract and change no row another Page owns.

## `paper.judgment.claim` · `rclaim-NN_<slug>`

🔘 BUTTON   Claim review · Story · ^rclaim- · views questions
💬 PROMPT   /haipipe-paper-story review {target} on {page}: judge this C5 claim against its evidence, boundaries and open risks; research it needs is a separate run.

## `paper.judgment.obligation` · `rtask-NN_<slug>`

🔘 BUTTON   Task review · Story · ^rtask- · views roadmap
💬 PROMPT   /haipipe-paper-story review {target} on {page}: review this C7 obligation and its study plan; commission supporting work only after its G1 release.

## Supporting work · Task and Discovery runs, owned by their homes

🔘 BUTTON   Supporting runs · Story · - · views roadmap
💬 PROMPT   /haipipe-paper-story route {target} on {page}: name the Task or Discovery run this row needs, then hand it to that owner.

## `paper.judgment.narrative` · `rnarra-NN_<section>`

🔘 BUTTON   Narrative review · Sections · ^rnarra- · views table narrative
💬 PROMPT   /haipipe-paper-story review the C8 row of {target} on {page}: check its moves, claims, displays and cut rule against the Section's current draft.

## Section Page runs · Draft, Evidence and Delivery Spaces of each Section

🔘 BUTTON   Draft runs · Sections · - · views table
💬 PROMPT   /haipipe-page run {target} from Draft: continue this Section's Draft in its own Page workbench.

🔘 BUTTON   Evidence runs · Sections · - · views table evidence
💬 PROMPT   /haipipe-page evidence {target}: land and verify this Section's open Evidence Items, then bind their Results.

🔘 BUTTON   Delivery runs · Sections · - · views table
💬 PROMPT   /haipipe-page build {target}: build this Section's LaTeX and Word outputs from its accepted Page, then run its checks.

## `paper.compile` · the manuscript build

🔘 BUTTON   Build · Delivery · - · views preview artifacts
💬 PROMPT   /haipipe-paper-assemble build {paper}: regenerate delivery/ from the Section Pages in compile order, then write build-manifest.json.

🔘 BUTTON   Check · Delivery · - · views checks
💬 PROMPT   /haipipe-paper-assemble check {paper}: audit the last build against its manifest and name every stale page, unresolved reference and failed check.

## `paper.response` · one Round Page per feedback batch

🔘 BUTTON   Response · Delivery · ^rp-|^rd\d+_ · views rounds
💬 PROMPT   /haipipe-paper-round respond {target}: answer each routed concern once, link the checked versions and freeze the answer build.

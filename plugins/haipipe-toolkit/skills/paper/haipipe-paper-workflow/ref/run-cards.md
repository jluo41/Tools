# Paper Run cards

What the Paper workbench shows in each Space's Runs panel: one card per paper
Run type, each with the button a person sees and the prompt that button
copies. The Run Specs themselves stay in `run-workflow.md`; the owning skills
keep their authority.

A `🔘 BUTTON` line is `label · Space · ticket pattern · views <names>`. The
pattern is a regular expression on the ticket file name; `-` means the button
only copies a prompt, because its runs live with another owner. `views` names
the tabs or views the button shows in (none = every view of the Space).
`🧩 SKILL` names the skill(s) that do the work; the Runs panel shows them on every
run of that button (JL 260928: each run says which skill it uses).
`💬 PROMPT` is the text the button copies; `{page}` is the Page the run sits
on, `{target}` the selected idea, row or Section, `{paper}` the paper folder.

Section runs are the Section Page's own runs (`haipipe-page-workflow/ref/run-cards.md`),
shown under three buttons, one per Page Space.

## `paper.judgment.idea` · `ridea-NN_<slug>`

🔘 BUTTON   Idea review · Ideation · ^ridea-
🧩 SKILL    haipipe-paper-ideation
💬 PROMPT   /haipipe-paper-ideation review {target} on {page}: judge this idea against its evidence and record its rationale, limits and next question as a new version.

## Idea generation and tests · owned by `haipipe-ideation`

🔘 BUTTON   Generate ideas · Ideation · -
🧩 SKILL    haipipe-ideation-generate
💬 PROMPT   /haipipe-ideation-generate {page}: propose new candidate ideas for this paper and write each one as an Idea Card.

🔘 BUTTON   Test idea · Ideation · -
🧩 SKILL    haipipe-ideation-test
💬 PROMPT   /haipipe-ideation-test {page} {target}: run the novelty and pressure tests on this idea and record the Result on its card.

🔘 BUTTON   Select idea · Ideation · -
🧩 SKILL    haipipe-ideation-select
💬 PROMPT   /haipipe-ideation-select {page} {target}: put this idea and its venue to the person as the G0 choice; on yes, hand it to the Story.

## Story writing · the Story Page's own `rp-` runs

🔘 BUTTON   Story revise · Story · ^rp- · views spine
🧩 SKILL    haipipe-paper-story · haipipe-writing
💬 PROMPT   /haipipe-page run {page} rp-sec: revise {target} of the Story; keep its C1–C8 contract and change no row another Page owns.

## `paper.judgment.claim` · `rclaim-NN_<slug>`

🔘 BUTTON   Claim review · Story · ^rclaim- · views logic-work
🧩 SKILL    haipipe-paper-story
💬 PROMPT   /haipipe-paper-story review {target} on {page}: judge this C5 claim against its evidence, boundaries and open risks; research it needs is a separate run.

## `paper.judgment.obligation` · `rtask-NN_<slug>`

🔘 BUTTON   Task review · Story · ^rtask- · views logic-work
🧩 SKILL    haipipe-paper-story
💬 PROMPT   /haipipe-paper-story review {target} on {page}: review this C7 obligation and its study plan; commission supporting work only after its G1 release.

## Supporting work · Task runs and Discovery runs, owned by their folders

A question (a T or D row) is answered by runs in its folder: a Task folder under
`task/` or a Discovery folder under `discoveries/`. Each run shows under the
button of its owner.

🔘 BUTTON   Task runs · Story · - · views logic-work
🧩 SKILL    haipipe-task
💬 PROMPT   /haipipe-task {target}: create or continue the Task folder (BJTR) that answers this question on {page}, write its address on the row, and build its run tickets; JL presses Run.

🔘 BUTTON   Discovery runs · Story · - · views logic-work
🧩 SKILL    haipipe-discovery
💬 PROMPT   /haipipe-discovery {target}: create or continue the Discovery folder (BJTR) that answers this question on {page}, write its address on the row, and add its Paper Runs.

## `paper.judgment.narrative` · `rnarra-NN_<section>`

🔘 BUTTON   Narrative review · Sections · ^rnarra- · views table narrative
🧩 SKILL    haipipe-paper-story
💬 PROMPT   /haipipe-paper-story review the C8 row of {target} on {page}: check its moves, claims, displays and cut rule against the Section's current draft.

## Section Page runs · Draft, Evidence and Delivery Spaces of each Section

🔘 BUTTON   Draft runs · Sections · - · views table
🧩 SKILL    haipipe-paper-section · haipipe-page-writing
💬 PROMPT   /haipipe-page run {target} from Draft: continue this Section's Draft in its own Page workbench.

🔘 BUTTON   Evidence runs · Sections · - · views table evidence
🧩 SKILL    haipipe-page-evidence
💬 PROMPT   /haipipe-page evidence {target}: land and verify this Section's open Evidence Items, then bind their Results.

🔘 BUTTON   Delivery runs · Sections · - · views table
🧩 SKILL    haipipe-page-delivery
💬 PROMPT   /haipipe-page export {target}: rerun this Section's Delivery Runs (run-delivery-webpage, _latex, _word); say which files changed.

🔘 BUTTON   Page check · Sections · ^rp-check-|^run-check- · views table
🧩 SKILL    haipipe-page-check
💬 PROMPT   /haipipe-page-check {target}: judge the Section's current built version against its C8 row, evidence and venue; route CLOSE or name what must change.

## `paper.compile` · the manuscript build

🔘 BUTTON   Build · Delivery · - · views preview artifacts
🧩 SKILL    haipipe-paper-assemble
💬 PROMPT   /haipipe-paper-assemble build {paper}: regenerate delivery/ from the Section Pages in compile order, then write build-manifest.json.

🔘 BUTTON   Check · Delivery · - · views checks
🧩 SKILL    haipipe-paper-assemble
💬 PROMPT   /haipipe-paper-assemble check {paper}: audit the last build against its manifest and name every stale page, unresolved reference and failed check.

## `paper.coverletter` · the submission cover letter

🔘 BUTTON   Cover letter · Delivery · - · views cover
🧩 SKILL    haipipe-paper-assemble
💬 PROMPT   /haipipe-paper-assemble coverletter {paper}: draft or revise the "Cover letter" division on the submission Round page from the approved Abstract and Story, rebuild delivery/ so run-delivery-coverletter writes the letter PDF and DOCX, and report its checks.

## `paper.response` · one Round Page per feedback batch

🔘 BUTTON   Response · Delivery · ^rp-|^rd\d+_ · views rounds
🧩 SKILL    haipipe-paper-round
💬 PROMPT   /haipipe-paper-round respond {target}: answer each routed concern once, link the checked versions and freeze the answer build.

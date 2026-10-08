# Paper Run cards

What the paper workbench shows in each level's Spaces: one card per button, each with the prompt that button
copies. The cards follow the paper ladder (`haipipe-paper/ref/paper-ladder.md`; b16 Q05, JL 261007): a Board
(Block), a version (Job), a Section Task. The Run Specs stay in `run-workflow.md`; the owning skills keep their
authority.

A `🔘 BUTTON` line is `label · <Level> › <Space> · ticket pattern · views <names>`. Level is `Block` or `Job`;
Space is one of the six (Description · Idea Studio · Audience Report · Work Details · Runs · Delivery). The pattern
is a regular expression on the Run's name, `run-<type>-<target>` (no date; a folder in `runs/` as `haipipe-run` has it); `-` means the button only
copies a prompt, because its Runs live with another owner. `views` names the third-row views the button shows in,
lowercase-kebab (`draft-main`, `cover-letter`); none = every view of the Space. `🧩 SKILL` names the one skill that
does the work (JL 260928: each run says which skill it uses). `🤖 AGENT` names who does the run and `✍️ SIGNS` what
the person signs on it, or `none`; the three lines match the button's row in `workbench-paper/ref/workbench-table.md`,
which `table-workbench --check --cards` checks (JL 261003). `🏷 RUN` names the Run the button makes, `run-<type>-<target>` with its target as a placeholder: the Runs panel
shows it as the button's name and the label in small under it (JL 261007: "for all the soft run, the name of them
will be run-xxxx-xxx"; haipipe-run `ref/run-types-by-space.md`). Where a paper button does a base button's job it
makes the base Run and names the base skill: run-face-*, run-add-<jNN>, run-add-<tNN>, run-draw-<sNN> (haipipe-studio),
run-ask-<qNN> (haipipe-question), run-report-<qNN>, run-figures-<qNN>, run-check-<qNN> (haipipe-report),
run-delivery-<target>. `💬 PROMPT` is the text the button copies; `{folder}`
is the Board or version folder the frame shows, `<target>` the row picked.

A label may show at two levels (Ask a Question, Check the rules): each is its own card with the same skill, agent
and sign. A Section's own buttons are the Page workflow's (`haipipe-page-workflow/ref/run-cards.md`); a version
shows them under four buttons in Work Details. The base frame adds its own (Add a topic, Redraw a topic).


## Block › Description · the paper's face, venues, resources and related work

🔘 BUTTON   Update the Board · Block › Description · ^run-face-board · views scope
🏷 RUN      run-face-<board>
🧩 SKILL    haipipe-paper
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper update the face of {folder}/board.md: its spine, close, which telling it tells now (story-current) and its target; keep the session as a pass of runs/run-update-board.md.

🔘 BUTTON   Add a venue · Block › Description · ^run-add-venue- · views scope venue
🏷 RUN      run-add-venue-<venue>
🧩 SKILL    haipipe-paper-venue
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper-venue add <venue> to {folder}: write venues/<venue>/call.md from the venue's own call (dates, limits, format, review rules, the link and the day it was read) and keep the author kit as shipped in venues/<venue>/kit/.

🔘 BUTTON   Check the rules · Block › Description · ^run-check-venue- · views venue
🏷 RUN      run-check-venue-<venue>
🧩 SKILL    haipipe-paper-venue
🤖 AGENT    haipipe-page-check-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper-venue check {folder} against venues/<venue>/call.md: reread the call, mark what changed since the day it was read, and list every limit, format or review rule the paper breaks.

🔘 BUTTON   Add a resource · Block › Description · ^run-add-resource- · views resources
🏷 RUN      run-add-resource-<slug>
🧩 SKILL    haipipe-paper
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper add a resource to {folder}'s Resources: what it is, its kind, what the paper uses it for, and its link.

🔘 BUTTON   Add a related item · Block › Description · ^run-add-related- · views related
🏷 RUN      run-add-related-<slug>
🧩 SKILL    haipipe-paper
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper add a related item to {folder}/related/related.md: its group (the research question it bears on), key, who, year, title, venue, kind, why here, and the deep read it links.

🔘 BUTTON   Read a paper · Block › Description · - · views related
🏷 RUN      rNN_<author><year>_<subject> (discovery)
🧩 SKILL    haipipe-discovery
🤖 AGENT    haipipe-discovery-orchestrator-agent
✍️ SIGNS    the source check
💬 PROMPT   /haipipe-discovery read <paper> for {folder}: one deep read, its Result card, facts, BibTeX and its drawing; then link the read from related/related.md.


## Block › Idea Studio · the studio topics

🔘 BUTTON   Redraw · Block › Idea Studio · ^run-draw-
🏷 RUN      run-draw-<sNN>
🧩 SKILL    haipipe-studio
🤖 AGENT    haipipe-studio-agent (new)
✍️ SIGNS    none
💬 PROMPT   /haipipe-studio redraw {folder}'s studio topics (a pass of run-draw-<sNN> each): rerun each topic's build_*.py so every drawing follows the current telling, then check it in the Idea Studio; a person's marks on a drawing are kept.


## Block › Audience Report · Ideation, Narrative, the research questions, Related Questions

🔘 BUTTON   Ask a Question · Block › Audience Report · ^run-ask- · views ideation related-questions
🏷 RUN      run-ask-<qNN>
🧩 SKILL    haipipe-question
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-question {folder}: one question a reviewer, a coauthor, an editor or a reader will ask of this paper; register it in board.md ## Questions with group: <who asks>, and its folder reports/qNN_<topic>/.

🔘 BUTTON   Generate ideas · Block › Audience Report · ^run-generate-ideas · views ideation
🏷 RUN      run-generate-ideas
🧩 SKILL    haipipe-ideation-generate
🤖 AGENT    haipipe-ideation-agent (new)
✍️ SIGNS    none
💬 PROMPT   /haipipe-ideation-generate {folder}: propose new candidate ideas for this paper into studio/s01-ideation/, each written as the question it asks, and register each as a Question with group: ideation.

🔘 BUTTON   Test idea · Block › Audience Report · ^run-test-idea- · views ideation
🏷 RUN      run-test-idea-<idea>
🧩 SKILL    haipipe-ideation-test
🤖 AGENT    haipipe-ideation-agent (new)
✍️ SIGNS    none
💬 PROMPT   /haipipe-ideation-test {folder} <target>: run the novelty and pressure tests on this idea and record the Result in its report.

🔘 BUTTON   Idea review · Block › Audience Report · ^run-paper-idea- · views ideation
🏷 RUN      run-paper-idea-<slug>
🧩 SKILL    haipipe-paper-ideation
🤖 AGENT    haipipe-board-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper-ideation review <target> of {folder}: judge this idea against its evidence and record its rationale, limits and next question as a new pass of runs/run-paper-idea-<slug>.md.

🔘 BUTTON   Select idea · Block › Audience Report · ^run-select-idea- · views ideation
🏷 RUN      run-select-idea-<idea>
🧩 SKILL    haipipe-ideation-select
🤖 AGENT    haipipe-ideation-agent (new)
✍️ SIGNS    the admitted idea (G0)
💬 PROMPT   /haipipe-ideation-select {folder} <target>: put this idea and its venue to the person as the G0 choice; on yes, open its telling as studio/sNN-story-<telling>/.

🔘 BUTTON   Story revise · Block › Audience Report · ^run-revise-story- · views narrative
🏷 RUN      run-revise-story-<telling>
🧩 SKILL    haipipe-paper-story
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    the Story version
💬 PROMPT   /haipipe-paper-story revise <target> of {folder}'s current telling (its studio topic's face and its Board Questions): what the story says, how it is drawn and how it is told; change no row another owner holds.

🔘 BUTTON   Narrative review · Block › Audience Report · ^run-paper-narrative- · views narrative
🏷 RUN      run-paper-narrative-<slug>
🧩 SKILL    haipipe-paper-story
🤖 AGENT    haipipe-board-reviewer-agent
✍️ SIGNS    release of one Section (G3)
💬 PROMPT   /haipipe-paper-story review the Narrative row of <target> in {folder}: check its moves, claims, displays and cut rule against the Section's current draft.

🔘 BUTTON   Review for an audience · Block › Audience Report · ^run-review-audience- · views narrative
🏷 RUN      run-review-audience-<who>
🧩 SKILL    haipipe-paper-story
🤖 AGENT    haipipe-board-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   Read the telling of {folder} as an editor, a reviewer and a member of the public, each in a fresh context (haipipe-journal-fit, haipipe-nature-paper-review): does it attract them? Record each verdict as a narrative Question in board.md ## Questions (group: narrative) with its report.

🔘 BUTTON   Claim review · Block › Audience Report · ^run-paper-claim- · views logic-work
🏷 RUN      run-paper-claim-<slug>
🧩 SKILL    haipipe-paper-story
🤖 AGENT    haipipe-board-reviewer-agent
✍️ SIGNS    the claim state (G2)
💬 PROMPT   /haipipe-paper-story review <target> of {folder}: judge this claim against its evidence, boundaries and open risks; research it needs is a separate run.

🔘 BUTTON   Task review · Block › Audience Report · ^run-paper-task- · views logic-work
🏷 RUN      run-paper-task-<slug>
🧩 SKILL    haipipe-paper-story
🤖 AGENT    haipipe-board-reviewer-agent
✍️ SIGNS    release of Task work (G1)
💬 PROMPT   /haipipe-paper-story review <target> of {folder}: review this Task Roadmap row and its study plan; commission supporting work only after its G1 release.

🔘 BUTTON   Write the report · Block › Audience Report · ^run-report- · views logic-work related-questions
🏷 RUN      run-report-<qNN>
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-report write the report for <target> in {folder}/reports/qNN_<topic>/ (the Page flow, haipipe-page): from the closed Runs of its work, say what they show, which hypotheses hold and which claims follow; cite each Result; set answer-status (open, partial, answered) and never call a hypothesis shown that no Run tests.

🔘 BUTTON   Review the report · Block › Audience Report · ^run-check-q · views logic-work related-questions
🏷 RUN      run-check-<qNN>
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-page-check-agent
✍️ SIGNS    the answer (G2)
💬 PROMPT   /haipipe-report check the report for <target> in {folder}/reports/: check_report.py, then the Page's CHECK in a fresh context: check every number against its cited Result and every "shown" against a Run that tests it; return answered, partial, or back to writing.

🔘 BUTTON   Rebuild report drawing · Block › Audience Report · ^run-figures- · views logic-work related-questions
🏷 RUN      run-figures-<qNN>
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-report rebuild the drawing of <target>'s report in {folder}/reports/qNN_<topic>/ from its ## Figures list (build_report_drawing.py), then its preview.

🔘 BUTTON   Task runs · Block › Audience Report · - · views logic-work
🏷 RUN      rNN_<slug> (a work Task)
🧩 SKILL    haipipe-task
🤖 AGENT    haipipe-task-orchestrator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-task <target>: create or continue the Task folder (BJTR) that answers this question of {folder}, write its address in the question's report, and build its run tickets; JL presses Run.

🔘 BUTTON   Discovery runs · Block › Audience Report · - · views logic-work
🏷 RUN      rNN_<slug> (a discovery Task)
🧩 SKILL    haipipe-discovery
🤖 AGENT    haipipe-discovery-orchestrator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-discovery <target>: create or continue the Discovery folder (BJTR) that answers this question of {folder}, write its address in the question's report, and add its Paper Runs.


## Block › Work Details · the versions

🔘 BUTTON   Open a version · Block › Work Details · ^run-add-j
🏷 RUN      run-add-<jNN>
🧩 SKILL    haipipe-paper
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper open a version of {folder}: python haipipe-paper/scripts/paper_ladder.py version {folder} --desk <desk> --date MMDD --venue "<venue>" (or next --from <version> for a revision), dry run first.


## Block › Runs · the Board's own Runs

🔘 BUTTON   Update the Board status · Block › Runs · ^run-update-status
🏷 RUN      run-update-status
🧩 SKILL    haipipe-paper
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper status {folder}: read each version, Section and Question and write where the paper stands in the face's state line.


## Job › Description · the version's face and its venue

🔘 BUTTON   Update the version · Job › Description · ^run-face-j · views version
🏷 RUN      run-face-<jNN>
🧩 SKILL    haipipe-paper
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper update the face of {folder}: venue, deadline, which telling it tells, state; keep its ## Narrative and ## Questions.

🔘 BUTTON   Check the rules · Job › Description · ^run-check-venue- · views venue-rules
🏷 RUN      run-check-venue-<venue>
🧩 SKILL    haipipe-paper-venue
🤖 AGENT    haipipe-page-check-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper-venue check {folder} against its venue's call.md: limits, format, review rules; list what the version breaks.


## Job › Idea Studio · the version's drawings

🔘 BUTTON   Redraw the paper map · Job › Idea Studio · ^run-draw-
🏷 RUN      run-draw-<sNN>
🧩 SKILL    excalidraw-section
🤖 AGENT    haipipe-studio-agent (new)
✍️ SIGNS    none
💬 PROMPT   /excalidraw-section {folder}: redraw the version's map, its Sections by their one-line job and each Bullet's Evidence Items, from the Draft plans.


## Job › Audience Report · Questions, the draft, Comments, the cover letter

🔘 BUTTON   Ask a Question · Job › Audience Report · ^run-ask- · views questions
🏷 RUN      run-ask-<qNN>
🧩 SKILL    haipipe-question
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-question {folder}: one question this send must answer (why this venue, the writing principles, ready to send, what changed); register it in the face's ## Questions with its report.

🔘 BUTTON   Write the report · Job › Audience Report · ^run-report- · views questions
🏷 RUN      run-report-<qNN>
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-report write the report for <target> in {folder}/reports/qNN_<topic>/ from exact Results (the Page flow, haipipe-page); set answer-status and results-read.

🔘 BUTTON   Review the report · Job › Audience Report · ^run-check-q · views questions
🏷 RUN      run-check-<qNN>
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-page-check-agent
✍️ SIGNS    the answer (G2)
💬 PROMPT   /haipipe-report check the report for <target> in {folder}/reports/: check_report.py, then the Page's CHECK in a fresh context.

🔘 BUTTON   Rebuild report drawing · Job › Audience Report · ^run-figures- · views questions
🏷 RUN      run-figures-<qNN>
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-report rebuild the drawing of <target>'s report in {folder}/reports/qNN_<topic>/ from its ## Figures list (build_report_drawing.py), then its preview.

🔘 BUTTON   Narrative review · Job › Audience Report · ^run-paper-narrative- · views draft-main draft-appendix
🏷 RUN      run-paper-narrative-<slug>
🧩 SKILL    haipipe-paper-story
🤖 AGENT    haipipe-board-reviewer-agent
✍️ SIGNS    release of one Section (G3)
💬 PROMPT   /haipipe-paper-story review the Narrative row of <target> in {folder}: check its moves, claims, displays and cut rule against the Section's current draft.

🔘 BUTTON   Release a Section · Job › Audience Report · ^run-release-section- · views draft-main draft-appendix
🏷 RUN      run-release-section-<tNN>
🧩 SKILL    haipipe-paper-story
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    release of one Section (G3)
💬 PROMPT   Release <target> of {folder} for writing (G3): check its row in the face's ## Narrative is ready, then record the release in that row; a person signs it.

🔘 BUTTON   Add comments · Job › Audience Report · ^run-add-comments- · views comments
🏷 RUN      run-add-comments-<qNN>
🧩 SKILL    haipipe-paper-comments
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper-comments add a batch of comments to {folder}: python haipipe-paper-comments/scripts/review_items.py <board> add <batch folder> --to <version>, dry run first; then split it into points with ids by source and group them into Review Items.

🔘 BUTTON   Route an item · Job › Audience Report · ^run-route-item- · views comments
🏷 RUN      run-route-item-<item>
🧩 SKILL    haipipe-paper-comments
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper-comments route <target> of {folder}: name the Section it lands on and open its run-revise-<item> in that Section, or route it to a Question, a Task or a decline.

🔘 BUTTON   Reply to an item · Job › Audience Report · ^run-reply-item- · views comments
🏷 RUN      run-reply-item-<item>
🧩 SKILL    haipipe-paper-comments
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper-comments reply to <target> of {folder}: write what changed and where, from the closed revise Run, into the item's row and the response letter.

🔘 BUTTON   Write the cover letter · Job › Audience Report · ^run-write-letter- · views cover-letter
🏷 RUN      run-write-letter-<tNN>
🧩 SKILL    haipipe-paper-assemble
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    the letter
💬 PROMPT   /haipipe-paper-assemble coverletter {folder}: write the t31_cover-letter Task one paragraph per row (what we submit · the one-minute story · why this venue · declarations · suggested reviewers if the venue asks), each from the question or rule it answers.

🔘 BUTTON   Check the letter · Job › Audience Report · ^run-check-letter- · views cover-letter
🏷 RUN      run-check-letter-<tNN>
🧩 SKILL    haipipe-paper-assemble
🤖 AGENT    haipipe-page-check-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper-assemble build and check the cover letter of {folder}: its numbers against the manuscript, the venue's required mentions, no causal verbs, no process text, two pages at most.


## Job › Work Details · the Sections, the Appendix and the letters

A Section's Runs are its own Page Runs; these buttons open them from the version.

🔘 BUTTON   Add a Section · Job › Work Details · ^run-add-t · views main appendix
🏷 RUN      run-add-<tNN>
🧩 SKILL    haipipe-paper-section
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper-section add a Section to {folder}: python haipipe-paper/scripts/paper_ladder.py task {folder} t0N_<title> (t2N_ for the Appendix), dry run first, then its row in the face's ## Narrative.

🔘 BUTTON   Draft runs · Job › Work Details · - · views main appendix
🏷 RUN      run-<kind>-<slug> (the Section's)
🧩 SKILL    haipipe-paper-section
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-page run <target> from Draft: continue this Section's Draft in its own Task tab.

🔘 BUTTON   Evidence runs · Job › Work Details · - · views main appendix
🏷 RUN      run-<value|citation|display>-<slug> (the Section's)
🧩 SKILL    haipipe-page-evidence
🤖 AGENT    haipipe-page-evidence-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-page evidence <target>: land and verify this Section's open Evidence Items, then bind their Results.

🔘 BUTTON   Delivery runs · Job › Work Details · - · views main appendix
🏷 RUN      run-delivery-<lane> (the Section's)
🧩 SKILL    haipipe-page-delivery
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-page export <target>: rerun this Section's Delivery Runs (run-delivery-webpage, _latex, _word); say which files changed.

🔘 BUTTON   Page check · Job › Work Details · ^run-check- · views main appendix
🏷 RUN      run-check-<page> (the Section's)
🧩 SKILL    haipipe-page-check
🤖 AGENT    haipipe-page-check-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-page-check <target>: judge the Section's current built version against its Narrative row, evidence and venue; route CLOSE or name what must change.

🔘 BUTTON   Add a letter · Job › Work Details · ^run-add-t3 · views letters
🏷 RUN      run-add-<tNN>
🧩 SKILL    haipipe-paper-section
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper-section add a letter to {folder}: python haipipe-paper/scripts/paper_ladder.py task {folder} t31_cover-letter (t32_response for a revision), dry run first.

🔘 BUTTON   Cover letter · Job › Work Details · ^run-write-letter- · views letters
🏷 RUN      run-write-letter-<tNN>
🧩 SKILL    haipipe-paper-assemble
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    the letter
💬 PROMPT   /haipipe-paper-assemble coverletter {folder}: draft or revise the t31_cover-letter Task from the approved Abstract and the telling, rebuild its delivery, and report its checks.

🔘 BUTTON   Response · Job › Work Details · ^run-write-response- · views letters
🏷 RUN      run-write-response-<tNN>
🧩 SKILL    haipipe-paper-comments
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    every response answered (G5)
💬 PROMPT   /haipipe-paper-comments respond <target> of {folder}: write the t32_response Task item by item, each Review Item answered once with its checked change, and freeze the answer build.


## Job › Runs · the version's own Runs

🔘 BUTTON   Update the version · Job › Runs · ^run-face-j
🏷 RUN      run-face-<jNN>
🧩 SKILL    haipipe-paper
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper update the face of {folder}: venue, deadline, which telling it tells, state; keep its ## Narrative and ## Questions.


## Job › Delivery · the version's build

🔘 BUTTON   Build · Job › Delivery · ^run-delivery-
🏷 RUN      run-delivery-<target>
🧩 SKILL    haipipe-paper-assemble
🤖 AGENT    haipipe-paper-assemble-agent (new)
✍️ SIGNS    none
💬 PROMPT   /haipipe-paper-assemble build {folder}: regenerate the version's delivery/ from its Sections in the face's compile order, then write build-manifest.json.

🔘 BUTTON   Check · Job › Delivery · ^run-check-submission-
🏷 RUN      run-check-submission-<jNN>
🧩 SKILL    haipipe-paper-assemble
🤖 AGENT    haipipe-page-check-agent
✍️ SIGNS    submission readiness (G4)
💬 PROMPT   /haipipe-paper-assemble check {folder}: audit the last build against its manifest and name every stale Section, unresolved reference and failed check.

🔘 BUTTON   Send · Job › Delivery · ^run-send-version-
🏷 RUN      run-send-version-<jNN>
🧩 SKILL    haipipe-paper-assemble
🤖 AGENT    haipipe-paper-assemble-agent (new)
✍️ SIGNS    the send
💬 PROMPT   /haipipe-paper-assemble send {folder}: open the comments report this send will collect into (reports/qNN_<venue>-<MMDD>/, page-type: comments), then freeze the current build into its sent/ with delivery/build.py send qNN; a person signs that this is what went out.

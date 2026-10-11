"""s31 · paper Guide, the Job section: what Guide's four Views say about a paper Job (owned by the -job session).

Imported by build_s31_paper_guide.py, which draws each View's Block · Job · Task sections in b03 s31's card
shapes. This file exports LEVEL (View -> items: c cards, w drawing cards, t lines, m mono lines), ON_DISK
(View -> [(line, meaning)]) and OPEN (["? …"]); a "?" in a title or line draws red.

Read live through paper_guide_live.py, the reader all three levels share, so the drawing shows what Guide
shows today: the Job steps (method.md's **Job · …** table), method cards, drawings (guide.yaml roadmap: Job)
and papers (related/papers.md's level column). Typed here, as the proposal (red): a paper Job is one send,
one deliverable for one venue, sent once and frozen once sent (JL 261007, s12); its types (Manuscript, Grant,
Patent, Talk); the step that opens a send; comments answered by the next send. CHANGES and "✎" lines draw
green: what changed, dated. Placeholders only.
"""
import paper_guide_live as P  # the one shared reader of method.md · guide.yaml · papers.md (s31)

# ── the proposal, typed ──────────────────────────────────────────────────────────────────────
# the Job types: (folder, what it delivers, its Tasks, closes on); "?" = not yet agreed
TYPES = [("Manuscript · j0N_v<MMDD>_<desk>/", "one paper sent to one journal, conference or preprint server",
          "Tasks: t00 abstract · t0N_ Main · t2N_ Appendix · t31 cover letter · t32 response   closes: sent + decision"),
         ("? Grant · j5N_grant_<funder>/", "the same Story as a proposal",
          "Tasks: the funder's parts (aims · significance · approach)   closes: submitted + the score"),
         ("? Patent · j5N_patent_<office>/", "the invention as a filing",
          "Tasks: claims · description · figures · abstract   closes: filed"),
         ("? Talk · j6N_talk_<event>/", "the Story as slides", "Tasks: slides · script   closes: given")]
# the six Space cards of a Manuscript Job, in this theme's words
SPACES = [("Description", "the send's face: type · venue · deadline · which Story · from · answers",
           "sub: Version · Venue rules   reads: jNN_v<MMDD>_<desk>.md · venues/<venue>/call.md   runs: Update the version"),
          ("Idea Studio", "optional: a version's own drawings",
           "sub: —   reads: studio/sNN-<topic>/   runs: Draw"),
          ("Audience Report", "the send's questions, each Question │ Work │ Report",
           "sub: Questions · Draft-Main · Draft-Appendix · Comments · Cover letter   reads: ## Questions · comments/"),
          ("Work Details", "its Tasks, grouped by the venue's parts: Main · Appendix · Letters",
           "sub: Main · Appendix · Letters   reads: t0N_<title>/ · t2N_<title>/ · t3N_<letter>/   runs: Add a Section"),
          ("Runs", "the send's own soft Runs, by type",
           "sub: All · narrative · compile · check · delivery   reads: runs/<run>/run.yaml   runs: Run"),
          ("Delivery", "item cards: Manuscript · Letters · Checks; ? Sent once frozen",
           "cards: paper.pdf · paper.docx · cover letter · readiness   reads: delivery/   runs: Build · Check")]
# a step the proposal adds or changes, by its live name ("" = a new step, drawn first)
STEP_CHANGE = {
    "": ("? 4 · Open the send", "type + venue; its rules and parts become the Tasks",
         "where: Block › Work Details › Add a version   methods: By venue fit   signs: the target"),
    "6 · Answer the rounds": ("? 7 · Close on the decision", "comments close it; the next send answers them",
                              "where: reports/qNN_<kind>-<MMDD>/ (type comments) · t32_response   signs: the decision · G5 next")}
NEW_DRAWINGS = [("? the sends of one paper", "j11 → j12 → j13 (answers R1, then re-targets), a type card each",
                 "source: Tools/blueprints/b16_theme_paper/studio/s12-paper-job/   built by: build_s12_paper_job.py   ↗ full size")]
NEW_CARDS = [("? By venue fit ↗", "a new method card", "? the venue's desk taste, from its playbook")]


def method_cards():
    """The live Job steps as short cards (the first clause, the Space, who signs), with the proposal's changes."""
    cards, steps = [STEP_CHANGE[""]], P.steps("Job")
    for step, does, line in steps:
        if step in STEP_CHANGE:
            cards.append(STEP_CHANGE[step])
            continue
        n = int(step.split(" ·")[0]) + 1                     # the new step 4 moves the rest down by one
        where = line.split("where: ", 1)[1].split("   methods:")[0].split(" · run")[0]
        signs = line.split("signs: ", 1)[-1]
        does = does.split(":")[0].split(", each")[0]          # the first clause; the rest is in method.md
        cards.append((f"{n} ·{step.split('·', 1)[1]}", does, f"where: {where}   signs: {signs}"))
    return cards, len(steps)


_cards, _n_live = method_cards()
_papers = P.papers("Job")
LEVEL = {
    "Description": [("t", "? one send: one deliverable, for one venue, sent once; frozen once sent"),
                    ("m", "its types"),
                    ("c", TYPES),
                    ("m", "a Manuscript's six Spaces"),
                    ("c", SPACES),
                    ("m", "skills   paper-section owns · paper-assemble builds · paper-venue rules · paper-comments answers"),
                    ("t", "✎ 261007  names: j0N_v<MMDD>_<desk>/ · t0N_ Main · t2N_ Appendix · t3N_ Letters; no Story Job"),
                    ("t", "✎ 261007  a version carries studio/ · reports/ · runs/"),
                    ("t", "✎ 261007  a comments batch is a report of type comments: reports/qNN_<kind>-<MMDD>/")],
    "Method": [("t", f"the send's steps: {_n_live} in method.md today, one added, one changed (red)"),
               ("c", _cards),
               ("m", "method cards"),
               ("c", P.method_cards("Job") + NEW_CARDS)],
    "RoadMap Draw": [("w", P.drawings("Job") + [(t, s, line, False) for t, s, line in NEW_DRAWINGS])],
    "Related Paper": ([("c", _papers)] if _papers else [("t", "(no Job paper yet)")])
                     + [("t", "? venue fit and peer review: papers to add, level Job (Add a paper)")],
}
ON_DISK = {
    "Description": [("servers/workbench-paper/guide/guide.yaml", ""),
                    ("    levels: Job", "? the send's role and its six Space cards"),
                    ("    job_types: Manuscript · Grant · …", "? a type card each: folder · Tasks · closes")],
    "Method": [("servers/workbench-paper/guide/method.md", ""),
               ("    **Job · one send, for one venue**", "? the steps table: Open the send … Close on the decision"),
               ("servers/workbench-paper/guide/methods/", ""),
               ("    venue/01-by-venue-fit.md", "? a new card, from the venue playbooks")],
    "RoadMap Draw": [("servers/workbench-paper/guide/guide.yaml", ""),
                     ("    roadmap: Job", "the Job's drawings, a card each"),
                     ("Tools/blueprints/b16_theme_paper/studio/s12-paper-job/", "a version's screens; ? the sends")],
    "Related Paper": [("servers/workbench-paper/related/papers.md", "rows with level Job")],
}
OPEN = ["? A paper Job is one send, frozen once sent: a revision is the next Job",
        "? Job types beyond Manuscript: Grant, Patent, Talk",
        "? Step 4 Open the send: the venue's parts become the Tasks (from its playbook)",
        "? A method card By venue fit, and papers for it"]

CHANGES = ["the Story is not a Job (the Story type card is gone)",
           "the Story becomes studio topics and Board Questions (Q04); §8 is the version face's ## Narrative",
           "a version is j0N_v<MMDD>_<desk>/, its Tasks t0N_ · t2N_ · t3N_ (was j1N_v<N>_<venue>/ · S-<desk>-…)",
           "comments: a batch is not a Task; t32_response in the next send answers it (was ? Q03)",
           "comments are a report of type comments, reports/qNN_<kind>-<MMDD>/ in the answering version",
           "Audience Report: Questions · Draft-Main · Draft-Appendix · Comments · Cover letter (was the §8 Narrative)",
           "Delivery: item cards (was LaTeX · Word · Cover letter · Sent tabs) · haipipe-paper-round renamed -comments"]

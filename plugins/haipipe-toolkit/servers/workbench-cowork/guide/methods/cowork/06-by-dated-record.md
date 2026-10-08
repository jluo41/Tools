By dated record
===============

One CoWork method card. The CoWork workbench shows it in the shared Guide › Method; its
papers are the rows of `../../../related/papers.md` whose `group` is `by dated record`. A claim names
its source in brackets; "(ours)" marks the workbench's own judgment.

family: Record: How do meetings and decisions stay findable?
move: Write each meeting as a dated note, and move every decision it makes into design/, so the note records what was said and design/ holds what is now true.
comes from: Hall et al. 2018, science of team science
reads: the meeting · the job pages it touched
returns: meetings/YYYY-MM-DD-<topic>.md and the changed design/ note
test now: T5 dated
test in use: T5 dated


What the literature says
------------------------

rationale: Collaborations across disciplines and organizations need institutional structures and policies that have not kept pace with demand, which the science of team science studies [Hall 2018]; a shared written record is one such structure we can keep ourselves (ours).
context: The science of team science, a field that studies how science teams work [Hall 2018].
steps: 1. Date the note. 2. List who was there and what was decided. 3. Move each decision to design/. 4. Update the Jobs it changes.
strengths: A new member can read the notes in order and know why the design is as it is (ours).
limitations: Notes can drift from decisions; the decision's home is design/, not the note (ours).


Applied to AI
-------------

agent: haipipe-cowork-agent (planned) writes the note from the person's input.
steps: 1. Take the person's notes. 2. Write the dated note. 3. Move the decisions. 4. Stop for the person.
returns: the meeting note and the design/ change.
verify: Every decision in the note appears in design/ (T5).
risk: An agent may record a decision nobody made; the person agrees the list (ours).
evidence on ai: No study tests agents writing meeting records (ours).
skill: haipipe-cowork

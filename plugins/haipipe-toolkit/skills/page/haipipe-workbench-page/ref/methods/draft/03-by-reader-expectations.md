By reader expectations
======================

One draft method card. The Page workbench shows it in the shared Guide › Method,
under Draft methods; its papers are the rows of `../../page-papers.md` whose
`group` is `by reader expectations`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Draft: What will the Page say, and why?
move: Write each sentence where its reader looks for things: the known in the topic
  position at the start, the new and important in the stress position at the end,
  subject and verb close together.
comes from: Gopen & Swan 1990, the science of scientific writing
reads: one paragraph's Bullets · their Evidence Items
returns: the paragraph's sentences, one per Bullet
test now: T0 covered
test in use: T4 independent


What the literature says
------------------------

rationale: Readers take much of a sentence's meaning from where things sit in it, not
  only from the words; putting information where readers expect it makes complex science
  clear without simplifying it [Gopen 1990].
context: Scientific writing, read by readers who interpret structure as well as content
  [Gopen 1990].
steps: 1. Start the sentence with what the reader already has. 2. Keep the grammatical
  subject close to its verb. 3. End on the new point the Bullet makes. 4. Write one
  sentence per Bullet.
strengths: The rules can be checked sentence by sentence by someone who did not write it
  (ours).
limitations: They govern sentences and paragraphs, not whether the Page's argument
  holds; that is the logic tree's work (ours).


Applied to AI
-------------

agent: A writing agent drafts each paragraph from its Bullets and Evidence Items, then
  the Page adopts the Draft.
steps: 1. Read the paragraph's Bullets and bound values. 2. Write one sentence per
  Bullet. 3. Adopt the Draft into the Page's Content.
returns: the Draft section of the plan, then the adopted Page sentences.
verify: Folder health checks every Draft equals its Page sentence (T0); the checker
  reads for clarity (T4).
risk: A model writes fluent sentences that may move the point away from the stress
  position, or add a claim no Bullet makes (ours).
evidence on ai: No study tests these rules on agent-drafted Pages (ours).
skill: haipipe-page-writing

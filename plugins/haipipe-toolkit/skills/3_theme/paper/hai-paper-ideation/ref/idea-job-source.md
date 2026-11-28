# Paper from an Idea Job

The source contract is
[hai-ideation's Idea Block](../../../../1_base/ideation/hai-ideation/references/idea-block.md).
Read it before creating or rebinding a Paper from an idea. This adapter owns
Paper presentation; it does not select ideas or move their source records.

## Apply a handoff

1. Read the source Job's manifest, Card, exact semantic revision, immutable
   selection and handoff. Run the source gate for that Job. Selection must
   identify the person, idea, target/category, accepted risks and destination.
2. Resolve the selected `paper_block` and `story_path` relative to the source
   Job. Check existing destination/origin links before allocating anything.
   A repeated handoff reuses its destination. A conflicting existing origin
   is unresolved; do not overwrite it or create an unrequested duplicate.
3. Use `hai-paper`'s scaffold to create/bind the destination. A Paper owner
   may also handle an explicit early-Paper request with provisional content;
   that request does not pass G0 or authorize a selected verdict.
4. Write `ideation-origin.yaml` with SPACE-relative Job, identity, immutable
   selection/handoff paths and consumed revision. Its schema is in the source
   contract. After creation, verify these links and the source's selected
   destination resolve back to each other. Preserve the original receipts.
5. Put ordinary Markdown links to the source Job, reviewed Card and human
   receipt on `s01-ideation/`'s face. Existing readers can follow those links.
   Apply the standard Page projection workflow; only real dispatch receipts
   can mark working/release/delivery surfaces current.

By default one selected Idea Job produces one Paper Block. A Paper's versions
remain Jobs inside that Paper. Its Story explains the chosen argument; its
Section Tasks write the manuscript. The Idea Job keeps evaluations, rejected
approaches, evidence pointers and the decision trail.

If scientific inputs change after selection, refresh the source Job and return
through its human gate before a new handoff. Retain the old Paper origin and
selection as history; the current origin points to the newly accepted snapshot.
An explicit split/merge names every contributing Job and human decision. It
does not delete sources or silently turn two ideas into one paper.

## Read an existing Paper

When `ideation-origin.yaml` exists, follow its sources before semantic edits;
project the selected idea and its paper-specific framing. Do not create a
second authoritative Card in Paper. Source links are useful content, not
internal implementation labels for the page.

When it is absent, read the existing `s01-ideation/` or legacy
`A1-Story/Story00-ideation/` portfolio as before. Do not infer, move or create
an Idea Job merely to make the new file exist. A requested migration is a
separate operation with an identity/path map and preserved historical links.

The origin file is a skill contract; this content update does not implement a
new server reader or Idea Board UI. Keep source links in faces for the current
workbench. Related stays in both Idea and Story; Story by Section stays in
both Story and Displays. Empty sections and progress tallies remain governed
by the shared UI Constitution.

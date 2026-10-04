ask-questions — Changelog
========================

## [0.2.0] — 2026-10-03

- Moved from `skills/0_utils/` to `skills/question/` (JL 261003: "put all the question
  related skills into here").
- Follow response-format 0.17.0: the question is the section's last line, the Related
  question; the Session form is gone; a proposed question is a topic on the owning board,
  with its folder offered in Summary and Next. Question records now point to
  `haipipe-question`, not `haipipe-task`.

## [0.1.2] — 2026-10-03

- Follow response-format 0.13.0: a section's question sits at the end of its
  heading as `(Q: <address>)`, not in a footer line.

## [0.1.1] — 2026-10-02

- Follow response-format's fully bold related Question footer at the section's
  bottom, preserving useful diagrams and an independent closing summary.
- Update the refinement example to the latest placement and emphasis choices.
- Fresh-context use confirmed the new footer presentation with recorded questions.

## [0.1.0] — 2026-10-02

- Identify and refine session questions, match normally written sections to
  recorded Block questions, and propose independent new questions.
- Ask clarifications only when missing information materially affects the
  answer or next action; retain known corrections and existing question identity.
- Use response-format for title-adjacent associations and an independent closing
  summary; route explicitly requested record and Report writing to Task and Page.
- Fresh-context use confirmed recorded question matching, distinction between
  Blocks with equal Q ids, proposed candidates and unregistered Session questions.

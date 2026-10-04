---
name: ask-questions
description: >-
  Identify and refine questions in an ongoing conversation, associate normally
  written response sections with existing Block questions, and propose distinct
  new questions. Ask focused clarifications when missing information would
  materially change the answer or next action. Use for tracing a long session
  to questions, matching sections to Q records, or shaping candidate questions;
  ordinary chat remains driven by the user's input. Trigger: ask questions,
  session questions, question association, propose a question, 提问, 追问, 问题归属.
metadata:
  version: "0.2.0"
  last_updated: "2026-10-03"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Ask Questions

Help the user advance the questions that arise in conversation and make their
answers traceable. Start with the user's current input and relevant earlier
clarifications. Form a useful reply in the normal discussion order, then
associate its sections with questions. A Board's question order does not determine
the reply's content, section order, or an extra layer of Question headings.

For presentation in this workspace, read
[response-format](../response-format/SKILL.md). It owns the exact reply shape:
scan points, a useful sketch when possible, explanation and any changed files,
and each ordinary section's ONE question as its last line, the Related question
(`**Related question:** [<Board> QNN "<short question>"](<question file>): <why>`, or
`(proposed) <Board> "<short question>": <why>`). The final Summary and Next has none.
Question matching follows drafting; the line makes that association visible without
interrupting the normal discussion. What a board question is and how big it should be
(a topic, not a decision) is [haipipe-question](../haipipe-question/SKILL.md).

## Understand the question before asking

Use what the user has already said. Distinguish their explicit question from a
candidate inferred by the assistant. Preserve the original intent and absorb
later corrections into the current understanding. Do not repeat a clarification
the session has already resolved.

A follow-up usually refines the same question: a new condition, example,
correction or next step does not automatically create a new Q. Propose a separate
question when it needs an independently useful answer or a different piece of
work. Keep questions neutral enough to admit an unexpected answer.

When a Block or Report is supplied or already known, read its relevant question
records to establish the actual wording, owner and report target. Match by the
decision or understanding sought, not just a shared keyword. Read enough context
to distinguish related questions without making an exhaustive Board search a
prerequisite for ordinary chat. There is no Session form: when no recorded question
fits, propose one on the board that owns the work.

## Associate normally written sections

Use the forms defined by response-format:

- **Recorded question:** its stable id, specific wording and actual record link.
  Preserve the owning Block and Project context. Q ids are local to a Block;
  Project / Block / Q01 distinguishes two different Q01 records.
- **Proposed question:** a topic no recorded question covers, on the board that
  owns the work, written `(proposed) <Board> "<short question>"` without minting an
  id. Lift a narrow ask to the topic it belongs to (`haipipe-question` § A question
  is a topic); the narrow ask goes in the section's Why. Present it as a proposal,
  and offer its folder in Summary and Next.

Several sections may advance the same Q, but each section answers exactly one
question; content that serves two questions is split into two sections. Preserve the normally written sections and their order.
Attach associations to those sections rather than rebuilding the reply as a
Board inventory. No Related question belongs on Summary and Next.

Use only known ids and existing link targets. Where a path was supplied but has
not been verified, identify it as supplied or intended and avoid presenting it
as a verified link. Source pointers to earlier messages are useful when available;
otherwise identify the relevant user statement in words. Do not invent message
permalinks.

## Ask when the answer needs it

First separate what is already known from what is missing. Ask a clarification
when its answer would materially change the recommendation, ownership required
for a requested save, scope, or next action. Otherwise proceed with the available
context and make any consequential assumption clear.

Keep the clarification focused. When useful, offer a few meaningful choices and
a recommendation. State the question being advanced and explain briefly how the
missing information affects it. Use the available user-input tool when appropriate,
or ask in chat when that is the available interface. Continue independent work
while waiting; a missing required answer remains unresolved.

Asking a person for information and associating a section with a Question are
different actions. A Related question line gives the reader context; it does not imply
that the user must answer another prompt.

## Continue into a Report when requested

A board's questions live in `reports/qNN_<topic>/`, beside `studio/`.
Associate an existing Q with its actual record path, including an older layout
when that is where the record lives. Question attribution alone creates no folders,
allocates no stable ids, and changes no answer or Page state.

For an explicit request to create or maintain question records, read
[haipipe-question](../haipipe-question/SKILL.md) and its
[Block Questions contract](../haipipe-question/ref/block-questions.md);
for Report writing also read
[haipipe-page](../../page/haipipe-page/SKILL.md). Those owners govern question
identity, work references and the Report's writing flow. Check the actual owner
tooling against the requested destination before using a creation helper; a chat
placement convention is not proof that older tooling supports that path.

When authorized to save, synthesize the question's current understanding and
answer, preserve significant clarifications and their available sources, and
carry forward evidence, limits and next actions. A Report should be independently
readable. Recording a question is separate from reaching an answer; execution
completion is separate from both the answer's status and the Page's acceptance.

## Small example

The user first asks how replies can be traced in a long session, then specifies
that the question belongs on the section's last line and names a board's question.
This is a refinement of the same question. If the board already has a topic such as
"How are questions recorded and answered?", link it, and let the Why say what this
section settles. If no record covers it, propose that topic on the board that owns the
work, without allocating an id, and offer its folder. Keep the user's discussion order in the reply.

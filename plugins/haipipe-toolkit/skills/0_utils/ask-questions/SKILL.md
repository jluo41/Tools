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
  version: "0.1.1"
  last_updated: "2026-10-02"
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
then a fully bold Related question footer at the bottom of each ordinary section.
Bold the question wording as well as its label and any linked id. The final
Summary and Next has no Question or ownership line. Question matching follows
drafting; the footer makes that association visible without interrupting the
normal discussion. Preserve meaningful diagrams alongside the footer.

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
prerequisite for ordinary chat. If the owner is unknown, continue with a Session
question; locating a Block is necessary only when the requested work depends on it.

## Associate normally written sections

Use the forms defined by response-format:

- **Recorded question:** its stable id, specific wording and actual record link.
  Preserve the owning Block and Project context. Q ids are local to a Block;
  Project / Block / Q01 distinguishes two different Q01 records.
- **Session question:** the unregistered question raised by the user. Use its
  actual wording or a faithful concise formulation, without minting an id.
- **Proposed question:** a distinct new candidate raised during the discussion.
  State the ask, its source or reason, and the target Block when known. Present
  it as a proposal rather than an accepted user decision or recorded question.

Several sections may advance the same Q. One section may support several Qs or
Projects when the content warrants it; show enough ownership context to keep
the links unambiguous. Preserve the normally written sections and their order.
Attach associations to those sections rather than rebuilding the reply as a
Board inventory. No Question association belongs on Summary and Next.

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
different actions. A Question line gives the reader context; it does not imply
that the user must answer another prompt.

## Continue into a Report when requested

The agreed Block placement is `report/Q01`, `report/Q02`, alongside `studio/`.
Associate an existing Q with its actual record path, including an older layout
when that is where the record lives. Question attribution alone creates no folders,
allocates no stable ids, and changes no answer or Page state.

For an explicit request to create or maintain Block records, read
[haipipe-task](../../task/haipipe-task/SKILL.md) and its
[Block Questions contract](../../task/haipipe-task/ref/block-questions.md);
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
that associations belong at the section's bottom and the whole question should
be bold, while useful diagrams remain. This is a refinement of the same
question. If an existing Block Q asks how to make replies traceable, link it.
If no record is known, use a Session question. If the discussion exposes a
separate need to decide when Reports should be saved, propose that question
without allocating an id. Keep the user's discussion order in the reply.

# The Bullet · the Outline's primary unit

> Part of the Structure Run (`structure.md`); read it before SHAPE writes or changes a Bullet.

**Highest-priority revision boundary.** Any edit to existing Draft Space
text must load `haipipe-draft-writing` (`ref/writing.md`) and obey its surgical-revision rule. The object
the person names sets the boundary: a sentence request edits only that Content
preview sentence; a Bullet request edits only that Bullet; neither authorizes
changes to neighboring Bullets, sentences, paragraph logic, transitions, or
Evidence bindings. Edit both sides only when the person requests both, or when
one cannot remain valid without the other; disclose the latter before treating
it as part of the patch. A paragraph-wide or structural rewrite requires
explicit approval. When scope is ambiguous, make the smaller edit and leave
any broader proposal in Discussion rather than applying it.

SHAPE now shapes both the plan and its candidate prose. In the Draft Space,
read the left-column Bullet/Evidence beside the right-column Draft, then read
the assembled paragraph. Draft and revise those candidate sentences
during the human discussion, even at v0 or before all Evidence is ready. Mark
missing factual material explicitly. The source and write protocol are
`workbench-task-draft/ref/content-preview.md`; load it for this work.
The candidate stays as the Bullet's Draft in the selected
`draft/<stem>-draft-v<G>.<S>[.<E>].md`, written Draft-first: the sentence
on the dash line, the planned point in `Point:` (`plan-grammar.md` § Draft-first
Bullets). Collaborative writing uses
`../../haipipe-draft-workflow/ref/interactive-writing-run.md`: the current Writing
Run saves each human exchange as a Step, without another Run per edit or
paragraph. CONTENT later adopts explicitly agreed wording without redrafting.

**Paragraph-focused handoff.** Follow the routine writing packet in
`../../haipipe-draft/ref/user-check-packet.md`; that shared contract controls
review-window size, final link placement and low-latency completion.

 When the person and AI are revising one
paragraph, every response after an applied revision must return the live
**Draft Space** link and the complete assembled Draft paragraph
as it reads after that save, in Bullet order and including unchanged sentences.
Render the chat copy through the same reader-facing projection as the live
`Read paragraph`: preserve ordinary manuscript citations, but replace every
raw pending placeholder such as `[E05-VALUE-headline-association pending]`
with its compact parenthetical wall label such as `(Evalue05.Headline)`. Never put
the full technical Evidence id, pending-status prose, chip, or card inside the
paragraph handed to the person; those details belong in Evidence Space.
Changed sentences, a diff, or a summary may accompany the paragraph but may
not replace it. Reproduce the saved Draft rather than silently polishing a
second copy in chat, and show the declared review window (normally one to three complete
paragraphs), never unrelated Section text. Continue to return the **Evidence Space** link where
the live-Board handoff below requires it. Keep this routine handoff compact:
the complete saved passage, a brief change explanation, then the
Draft Space, Evidence Space, and Current Run links at the very end.
Do not append the Outline table, PDF, or section-wide material unless the person
requests a formal review or those artifacts were themselves changed.

A **Bullet** is one planned reader move with a stable `C<n>.P<m>.B<k>` address.
It is smaller than a paragraph and more durable than a sentence: a Section Page
realizes exactly one Bullet as exactly one sentence, while another Page type may use
one or more sentences. Its source head may use the legacy imperative job form,
or the clearer Point form `[Role]` followed by one concise substantive planning
statement. Neither form is final manuscript prose.

In Section rehearsal, revise Bullet and candidate sentence together, starting
from either side. During `PROPOSE`, the Outline producer and the whole-Page
Structure Run propose one context-specific functional `[Role]` for every new
Bullet, using the Structure list's flow, paragraph move, neighboring Points, and
the Page's subject as the basis. The tag is a proposal for human review, not a
fixed taxonomy: the producer may use `Phenomenon`, `Example`, `Mechanism`,
`Translation`, or another clear role when the argument calls for it. Do not
invent a generic `[Boundary]` role; a limitation belongs in the Point's actual
meaning only when the logic requires it. Split independent points, merge
redundant ones, and review evidence bindings rather than hiding several
sentences in one row. Keep edits in the same unapproved working Shape after
the first protected fork; ordinary saves do not create versions or approvals.
The precise reader/save boundary is `ref/content-preview.md` under the Outline
workbench. Published Page Content and PDF remain unchanged until CONTENT promotion.

```text
Bullet
├── Address       stable C.P.B identity
├── Head          planned reader move
├── Note          bounded rationale or constraint
├── Evidence      one explicit decision: typed Item(s), or none with reason
└── Realization   CONTENT-written Page sentence(s), linked with realizes:
```

The reader-facing Point form is presentation-only and remains Markdown
authoritative:

```markdown
- B1 · [Phenomenon] Physician behavior varies within clinical settings.
  Note: Clinical settings = clinical decision contexts
  Note: Focus: differences among physicians facing comparable situations
  Transition: illustration: general pattern → specific example
```

The Outline renderer shows `[1 · Phenomenon]` before the statement, turns the
short Note/Annotation/indented-dash lines into dash annotations, and places one
`→ [relation]` between adjacent Points for `Transition:`. It does not print
`Core statement:` or `Note:` labels, invent a role for a legacy head, or turn a
transition into an extra Bullet/Sentence. The 4–11-word check excludes the
`s<n> ·` slot and `[Role]` metadata and applies to the concise statement.

For new or edited Bullets, the statement must be plain subject–verb planning
language, not a command to the future writer. In a new or rewritten
`PROPOSE` output, every Bullet carries one proposed `[Role]`. The label is
contextual and open-ended rather than a controlled vocabulary; it should name
what that Point does in the current logic flow (`[Phenomenon]`, `[Example]`,
`[Mechanism]`, `[Translation]`, or another honest label). Do not use a generic
`[Boundary]` role. A human may revise or remove a proposed role during SHAPE;
legacy plans remain readable with the neutral fallback until they are
re-proposed. Do not start
the visible head with planner imperatives such as `Open with`, `Explain`,
`Introduce`, `Name`, `Connect`, `Ask`, `Keep`, `Return`, `Hand`, or `State`.
Keep rationale and scope as short dash annotations; use `Transition:` for the
single relation arrow between adjacent Points. Existing imperative heads are
compatibility input only and are not silently rewritten; migrating them
requires a new unapproved Shape and human review.

The Bullet is the shared unit across Draft Space and Evidence Space.
SHAPE revises its intended move; SURVEY maps what supports it without changing
its meaning; LAND and EMBED return ready material; CONTENT alone writes its Page
prose. Evidence Items serve a Bullet—they do not become competing outline rows.
Paragraphs and divisions are presentation groups only: they own no Evidence
Item and confer no evidence on their Bullets. A Bullet may not inherit an
Evidence Item from a sibling Bullet. When two Bullets depend on the same paper
or upstream Result, each owns its own claim-level Evidence Item and both items
may reuse the same source or Supporting Run.

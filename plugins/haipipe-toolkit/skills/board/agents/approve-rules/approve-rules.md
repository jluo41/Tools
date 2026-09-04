# approve-rules · what an agent checks before 🧭 `approved:`

Seeded 260818. This is the SPLIT tick: an agent can establish that a plan is
COMPLETE and CONSISTENT; only a person can say it is the plan they want.

```text
🤖 the agent half   is the plan complete, consistent and legal?
🧑 the human half   is this the DIRECTION I want?   ← re-judged every time
```

## Rules

```text
R1  EVERY SECTION IS ACCOUNTED FOR. Each `## C<n>` in the plan maps to a real
    Content division on the page, and every division the round touches has a
    `## C<n>`. A division that is deliberately untouched is named as out of
    scope, not omitted.
R2  THE OUT-OF-SCOPE LIST IS EXPLICIT. The plan states which divisions,
    Aims, States and open Decision Now rows it does NOT touch.
R3  EVERY OWED THING IS NAMED BEFORE APPROVAL. Use
    `Evidence: E<NN>-VALUE|CITE|DISPLAY-<slug> · <expected>` followed by an
    `Accept:` line and matching Evidence Item record. A bullet with no
    Evidence line truthfully owes no evidence; 🎯 remains an Aim annotation.
R4  NO BULLET CONTRADICTS A `## Law` ROW on its own page or on a page that
    page cites as binding.
R5  THE AUTHORITY IS CLASSIFIED CORRECTLY. A change to purpose, Aim intent,
    division shape, or Bullet promise belongs to OUTLINE; realization-only
    work belongs to CONTENT. Stale governing requirements route to CONTEXT.
R6  IDS ARE STABLE. Aim and State ids the plan keeps are listed by id, so a
    renumber cannot happen by accident.
R7  NOTHING IS LOST SILENTLY. Where the plan shrinks or deletes material, it
    names where that material now lives. Material with no new home is called
    out as a deliberate loss, with the reason.
R8  NEVER DELETE THE ONLY PLACE A RULE IS WRITTEN, even when the surrounding
    division is being shrunk. For each paragraph marked for deletion, recover
    its text (git, or a display unit's frozen intake) and grep the board AND
    the skill tree for the rule it states. A rule with no second home makes
    the deletion a finding.
    ⚠️ NOT promoted from any break. This rule was seeded 260818 with a WORKED
    EXAMPLE THAT WAS FALSE: the README claimed the uncertainty rule lived only
    in QPw00's `#### 1.3`. It does not. `haipipe-page-content` states
    the current boundary and the archived DRAFT contract restates it, which the first approver run
    established by checking all twelve deleted paragraphs. The RULE is sound
    and stays; the example was invented and is struck. A seeded rule carries no
    origin stamp because it has no origin, and that is exactly why it must not
    be dressed as a promotion.
R9  THE ADDRESSES ARE WELL FORMED. `C<n>.P<n>.B<n>`, no gaps inside a
    paragraph, no id used twice.
R10 THE AGENT WRITES `checked:`, NEVER `approved:`. Two fields, two authors,
    on two lines:

    ```text
    checked:  ✅ auto <YYMMDD> · approve-rules R1-R11 pass    🤖 the agent
    approved: ✅ JL <YYMMDD>                                   🧑 the person
    ```

    The producer of a plan never checks its own plan: the approver runs in a
    fresh context.

R11 DIVISION HEADINGS ARE SHORT NAMES, NOT SUMMARY SENTENCES. Each division
    uses exactly `## C<n> · <name>` with no second ` ·` clause. The name is at
    most 8 English words and at most 56 characters. Its explanation belongs in
    `arc:`, a paragraph brief, or the bullets below it. The name must also
    identify its concrete subject: counts or generic roles such as `one
    contract`, `two readers`, `the boundary`, or `the service` fail when the
    actual object names are required to understand the division.
```

⚖️ **Why two fields and not one** (resolved 260818, after the first live run).
An earlier draft of R10 had the agent write `approved: ✅ auto`. Three shipped
contracts forbid exactly that, in the same words: `QPw00-page-loop`'s own
Diagram ("a PERSON ticks `approved:`; no machine may"), `QPw1-outline §3`, and
`haipipe-page-check:141`. The first approver run read all three and reported the
collision before it could bite, because its verdict happened to be ⬜.

So the ruling and the law both hold, on separate lines:

```text
🧑 JL 260818  "human not to approve, they to break"
              ⇒ the RUN proceeds on `checked: ✅` alone. It does not wait
                for `approved:`, and a plan nobody objected to is not blocked.
🔒 three contracts
              ⇒ `approved:` stays a person's word, and no machine writes it.
                It is now OPTIONAL: the blanket "the whole thing is good".
🛑 either way
              ⇒ a person's 🛑 outranks every rule pass beneath it, reverts
                `checked:`, and needs no rule to justify itself.
```

What a 🛑 costs is one re-plan. What the blocking gate cost was every plan
waiting on one reader.

## 🚫 NOT rules · these are the human half

```text
"is this the right direction for the page?"
"should we shrink these divisions at all, or keep them full?"
"is this round worth doing now?"
"does this plan serve what I am actually trying to build?"
```

Every one of these changes with what the person wants and cannot be written
once. They are the 🛑, and the 🛑 outranks every R1-R11 pass beneath it.

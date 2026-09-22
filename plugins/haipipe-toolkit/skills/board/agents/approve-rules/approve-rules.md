# approve-rules · what a reviewer checks before 🧭 `approved:`

Seeded 260818. This is the SPLIT tick: a reviewer can report structural checks
and evidence-bound readings against this frozen contract; only a person can
approve the plan's direction.

```text
🤖 the reviewer half   are deterministic checks complete, and what do the
                        cited passages show under the frozen semantic rules?
🧑 the human half   is this the DIRECTION I want?   ← re-judged every time
```

## Rules

Each rule has a judgment class even when this legacy list does not yet encode
it per row:

- **deterministic**: exact structure/string/hash/predicate recomputed from the
  pinned artifact by a named checker;
- **semantic**: a reviewer compares cited evidence to a frozen criterion and
  records the relevant passage, finding, and uncertainty; a fresh context can
  improve independence but does not make the reading mechanically certain;
- **human decision**: direction, preference, waiver, release, or acceptance
  chosen by the named person. An agent may prepare options, never write this
  decision.

Classify each new rule and state its scope. A semantic criterion must include
an observation method and at least one pass, fail, and not-verifiable boundary
example. If the artifact or criterion does not support a decision, report
`not verifiable`; do not manufacture a verdict or retry the unchanged input.

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
    in QPw00's `#### 1.3`. It does not. `haipipe-page-writing` states
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

## Check result and workflow release

R1–R11 determine the machine `checked:` result. They do not release CONTENT
or satisfy a person-reserved gate. Follow `README.md` for the check/release
boundary and the canonical Page Outline gate. A checked v0 plan can support
permitted evidence work while human approval is owed; CONTENT remains held.
A person's 🛑 stays durable and reopens the affected check. Historical
two-field discussions are recorded in `../CHANGELOG.md`.

## 🚫 NOT rules · these are the human half

```text
"is this the right direction for the page?"
"should we shrink these divisions at all, or keep them full?"
"is this round worth doing now?"
"does this plan serve what I am actually trying to build?"
```

Every one of these changes with what the person wants and cannot be written
once. They are the 🛑, and the 🛑 outranks every R1-R11 pass beneath it.

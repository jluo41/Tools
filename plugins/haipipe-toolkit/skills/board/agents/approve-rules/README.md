# approve-rules · what a machine may pass, and what it may never judge

Rules and judgments have three different owners. Keep deterministic checks,
evidence-based semantic assessments, and human preferences distinct. Writing a
criterion down makes its scope visible; it does not make every criterion
mechanically decidable or transfer a person's choice to an agent.

```text
                   ⚙️ DETERMINISTIC           🤖 SEMANTIC ASSESSMENT       🧑 HUMAN DECISION
question           exact bytes satisfy a      what does the cited          is this the scope,
                   declared predicate?       evidence show under this    tradeoff or direction
                                             frozen criterion?           the person chooses?
result             recomputable pass/fail    criterion-level reading,    preference, release,
                                             evidence, uncertainty       acceptance or refusal
authority          rule + checker            trained/authorized reviewer  named person
```

The machine may claim deterministic pass/fail only when the predicate is
recomputed from the pinned input with a declared checker. A semantic rule may
be assessed by a reviewer, but the record must name the frozen criterion,
observed evidence, limits and any unresolved disagreement; `checked: auto` does
not turn it into a mechanical proof. A human preference or release decision
remains with the named person. An agent asked "is this display good overall"
must return a bounded finding or `not verifiable`, not an overall quality claim.

## The four files

```text
approve-rules.md   🧭 an OUTLINE plan, before prose is written
display-rules.md   🖼 a DISPLAY unit, before it is accepted
cite-rules.md      📚 a BIBEX entry, before it is verified
value-rules.md     🧮 a VALUE Evidence Item's accepted Result
```

## How they grow

Every 🛑 remains a durable, artifact-scoped steer and preserves the person's
own words. It is not automatically promoted to a reusable rule. Promotion
requires a separate explicit authorization naming scope and judgment class.

```text
🧑 🛑 JL · "B4 keeps #### 1.3. the uncertainty rule lives ONLY there."
            │
            ▼
🗂 the artifact retains the steer; the approver records it as a candidate
   rule with original locator. No rules file changes until the person
   explicitly approves its cross-artifact scope and class.
```

An authorized promotion keeps `promoted <date> from <whose break> on <what>` and
links the person's scope/class decision. A candidate stays a candidate until
that authorization exists.

## What a pass looks like · TWO FIELDS, TWO AUTHORS

The agent writes `checked:` and ONLY `checked:`. Every other tick on this board
is a person's word, and no machine writes one (ruled 260818, `approve-rules.md`
R10; corrected here 260821, where the single-field shape below had survived the
ruling that retired it).

```text
checked: ✅ auto · deterministic <YYMMDD> · <input hash> R1-R<n> pass
checked: ✅ auto · semantic <YYMMDD> · <criterion id> · <evidence> · pass|finding|not-verifiable
checked: ⬜ auto · <date> · <criterion id> · <evidence> · R4 fails: <the exact rule>
```

**Which human field each `checked:` sits under**, per artifact:

```text
artifact   🤖 the agent writes        🧑 the person writes       rules file
──────────────────────────────────────────────────────────────────────────
outline    checked:  ✅ auto …        approved: ✅ JL <YYMMDD>   approve-rules.md
display    checked:  ✅ auto …        accepted: ✅ JL <YYMMDD>   display-rules.md
cite       checked = {auto <YYMMDD>}  verified = {JL <YYMMDD>}   cite-rules.md
value      checked:  ✅ auto …        accepted: ✅ JL <YYMMDD>   value-rules.md
```

The cite row uses `=` and braces because a bibtex entry has no `key: value`;
the field's host syntax always wins.

**A check records what kind of judgment occurred; the owning Run Spec controls
release.** A passing `checked:` never substitutes for a person-reserved gate. The caller resolves
the Folder/Page owner and current mode before continuing work. The approver
does not dispatch the next Run or grant workflow release.

For Page Outline work, follow
[the Content-release gate](../../../page/page-workflows/haipipe-page-outline/SKILL.md).
A checked `v0.*` plan may proceed through permitted SURVEY, LAND and EMBED
work in copilot or auto. CONTENT remains held until its required human approval
is durably recorded. Auto may record review debt but cannot treat it as approval.
Other artifacts use their own Run Spec's acceptance and human-gate contract;
this rule pack does not make all human fields optional or mandatory.

Report the deterministic checks, semantic findings, permitted next work, and
next unmet human gate separately.
If owner context was not supplied, report permitted next work and unmet gate
as `not evaluated`; workflow release remains `not granted by this check`.
A person's 🛑 outranks a machine pass, reopens the affected check, and remains
on the artifact. Silence never supplies a required approval or Folder ruling.

# Context record · `outline/<stem>-context.md`

This generated record is the PREPARE snapshot used by SHAPE and later Page
phases. It is a projection over source authorities, never a replacement for
them.

```markdown
# <stem> · context
page: <stem>
kind: context · generated · PREPARE resolves sources; source files remain authoritative
generated: YYYY-MM-DDTHH:MM:SS±HH:MM

### CTX1 · Page identity and ownership
- **Status**: resolved
- **Page**: <repo-relative path>
- **Folder kind**: <kind> · source <path or resolver step>
- **Folder owner**: <exact workflow or canonical family skill name>
- **Page Face owner**: <exact phase, canonical family, or legacy Page-Type skill name>
- **Current authority**: CONTEXT

### CTX2 · Purpose and scope
- **Status**: resolved | missing | conflicting
- **Question**: <the Page question>
- **Audience**: <intended reader>
- **Covered here**: <scope>
- **Covered elsewhere**: <bounded related addresses or none>
- **Sources**: <path#locator; version/hash>

### CTX3 · Policy, structure, and style
- **Status**: resolved | missing | conflicting
- **Outline policy**: <exact skill/path#locator>
- **Expected structure**: <exact skill/path#locator>
- **Narrative/style policy**: <exact skill/path#locator or none>
- **Requirements**: outline/<stem>-requirement.md#<record ids> or none
- **Sources**: <every governing authority and version/hash>

### CTX4 · Related information
- **Status**: resolved | missing | conflicting | not-applicable
- **Rows**: <F ids and one-hop related Page scopes>
- **Packet**: <pagecontext.py invocation or durable packet path>
- **Sources**: <exact Page fragments and version/hash>

### CTX5 · Feedback and open decisions
- **Status**: resolved | missing | conflicting | not-applicable
- **Feedback**: <record ids and landed/open state>
- **Discussion**: <open D ids or none>
- **Human decisions**: <durable signed locations or none>
- **Sources**: <exact record paths>

### CTX6 · Planning and evidence readiness
- **Status**: resolved | stale | not-applicable
- **Plan**: <version, approval state, path or none>
- **Evidence Items**: <count and state tally or none>
- **Run receipts**: <relevant current receipts or none>
- **Next authority**: OUTLINE | CONTEXT | HOLD
- **Sources**: <paths and version/hash>
```

Rules:

1. The six `CTX` ids are stable and ordered.
2. `Status` is about context resolution, not Page completion.
3. Every summarized rule has an exact source address.
4. A missing or conflicting required row makes `Next authority: HOLD` or
   `CONTEXT`; it never disappears from the record.
5. Regenerate the whole file. Never hand-edit it and never put person-reserved
   approval inside it.

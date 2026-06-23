---
status: open
created: 2026-06-23
context: JAMANO claims restructuring session — venue fit analysis for JAMA flagship
fixed_in: ""
---

When restructuring claims for JAMA flagship, the most useful framing device was sitting in the target editor's chair and asking the question THEY ask:

JAMA flagship: "What should a physician do differently Monday morning?"

This single question instantly filtered which claims were strong (C3 unreachable patients — yes, the MD can act on this) vs weak (C4 click→auth deepening — the MD doesn't control the messaging system).

Every venue has an equivalent "editor's chair" question. Capture these per-venue so they can be baked into the _venue/playbook-* packs and used during /haipipe-paper claims to pressure-test claim structure before writing.

Candidates (to be refined and added to each playbook):

**Clinical medicine:**
- JAMA flagship: "What should a physician do differently Monday morning?"
- NEJM: "Does this change the standard of care for a common condition?"
- Lancet: "Does this affect global health policy or resource allocation?"
- JAMA Network Open: "Is this methodologically rigorous and clinically relevant, even if the scope is narrower?"
- JAMA Internal Medicine: "Does this change how internists think about a common practice?"
- BMJ: "Will a GP in Manchester read this and change how they practice?"

**Information systems / management:**
- Management Science: "Does this change how a decision-maker allocates resources or designs a system?"
- ISR: "Does this advance theory about how information systems create value or change behavior?"
- MISQ: "Does this reshape how we understand the relationship between IT and organizations?"

**Multidisciplinary science:**
- Nature: "Is this a finding that scientists outside the field will talk about at dinner?"
- Science: "Does this overturn or establish a principle?"
- PNAS: "Does this matter to the National Academy — broad significance across disciplines?"

**Health policy / operations:**
- Health Affairs: "Does this change how payers, regulators, or health systems should act?"
- JAMA Health Forum: "Does this change how health systems operate or deliver care?"

**Behavioral / social science:**
- Psychological Science: "Does this change how we understand human behavior?"
- PNAS (social science track): "Is this a behavioral finding with policy implications?"

Fix: Add an "Editor's Chair Question" field to each _venue/playbook-* pack. The claims skill (/haipipe-paper claims) should surface it when the venue is pinned, and use it as a litmus test: every primary claim must have a clear answer to the editor's chair question, or the claim needs restructuring.

<!-- TEMPLATE (follow, don't ship). Fill 0-lifecycle/1-work/1b-claims.md from this skeleton: replace every <…>, and each `<!-- RULE: … -->` comment is guidance to FOLLOW then DELETE — a RULE comment never appears in the finished doc. Delete this top line too. -->
1b-claims: <paper title> (venue-free claim/evidence inventory)
==============================================================

Date: YYYY-MM-DD
Status: DRAFT
This ledger plans what evidence to collect, commissions the work, and tracks results as they return.


Hypotheses (venue-neutral)
--------------------------
<!-- RULE: venue-neutral statements of what the paper tests. The same H1 can become RQ1 for a different venue — that reframing happens in PITCH, not here. One `- **H<n> (role)**` + statement, one sentence per line. -->

- **H1 (core).**
<hypothesis statement, one sentence per line.>

- **H2 (boundary).**
<hypothesis statement.>

- **H3 (mechanism).**
<hypothesis statement.>


Claims
------
<!-- RULE: each claim is a short sub-item — the testable statement, its current status, and the questions that settle it. Status vocabulary: `supported` / `weak` / `GAP`. No inline study design — the thinking lives in the Q-consumer. The `Evidence:` line LISTS every Q-Claim-<n> that bears on this claim — a claim is settled by SEVERAL small questions from different angles (fit, eval, robustness, placebo, …), never one; each question's Answer carries its verdict + `[source: PP<nn>]`. AGGREGATION: the status is `supported` only when the claim's required angles CONVERGE at REVISE — one favorable question is not a supported claim; any `GAP`/`weak` angle holds it below `supported`. The same Q-Claim-<n> may appear under more than one claim. Keyed on `H<n>`. -->

**C1 - <title> (H1, core) - <status>**

<Claim statement, one sentence per line.>
Evidence: [Q-Claim-1] [Q-Claim-2] [Q-Claim-3]

**C2 - <title> (H3, mechanism) - <status>**

<Claim statement.>
Evidence: [Q-Claim-4] [Q-Claim-5]

**C3 - <title> (H2, boundary) - <status>**

<Claim statement.>
Evidence: [Q-Claim-5] [Q-Claim-6]


Q-consumer
----------
<!-- RULE: the evidence questions this stage raises — one `## Q-Claim-<n>` block per question, uniform Description / Reason / Answer (the PROBE stage collects every stage's Q-consumer through one pipeline, so the shape is shared across all stages).
     · ANSWERABLE + SPECIFIC — each question is a CONCRETE check a task/discovery can answer with a definite result. Decompose a big claim into SEVERAL such small questions, each a different angle (fit, eval, robustness, placebo, IV, external, …); name the angle in the title, e.g. "· physician-clustered SE (eval)". NEVER a broad, ambiguous question like "is the effect real?".
     · M:N — a claim is settled by several questions, and a question may settle several claims. Cite each question in the `Evidence:` line of EVERY claim it bears on (forward link); `Reason` names which `C<n>`(s) it settles — possibly more than one (back link). If one question needs another's answer first, say so in its `Reason`.
     · Description = the specific thing it checks. Reason = which `C<n>`(s) it settles + why it matters. Answer = empty in DRAFT; PROBE fills it with the verdict + `[source: PP<nn>]`.
     · Route (task/discovery) + approver are decided at APPROVE, into the probe file — not here. At REVISE each Answer feeds the status of every claim it settles. -->

## Q-Claim-<n> · <question title — name the angle, e.g. main coefficient (fit)>
Description: <the specific, answerable check — one sentence per line>
Reason: <which `C<n>`(s) it settles, and why it matters if unanswered>
Answer: <empty in DRAFT — PROBE fills it: the verdict + [source: PP<nn>]>

<!-- second worked example, showing M:N — one question settling TWO claims. Numbering is
     sequential in the real file; the gap here is only to show the ids are independent. -->

## Q-Claim-<m> · <question title — e.g. metformin placebo null (placebo)>
Description: <the specific check.>
Reason: <settles C2 and C3 — a shared angle bearing on two claims.>
Answer: <filled at PROBE.>

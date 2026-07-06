# Claims: <Paper Title> (venue-free claim/evidence inventory)

Date: <YYYY-MM-DD>
Status: <one line -- e.g. DRAFT (first pass); most claims GAP because core run not done>

Venue-FREE evidence inventory. This is the pure claim/evidence ledger; venue-specific framing (RQ wording, Editor's Chair Test, [primary] designation) lives in pitch, the cover letter.

Status vocabulary: `supported` / `weak` / `GAP`. Probe needs are marked inline as `[NEED PROBE] <what evidence is missing>`.

**No tables.** This ledger is prose only -- one bulleted hypothesis list and one `###` subsection per claim. Never render claims, evidence, or the hypothesis-claim alignment as a markdown table.

## Hypotheses (venue-neutral)

Venue-neutral statements of what the paper tests. The same H1 can become RQ1 worded for different venues; that reframing happens in pitch, not here.

- **H1 (core).** <venue-neutral hypothesis statement>
- **H2 (boundary).** <hypothesis>
- **H3 (mechanism).** <hypothesis>

> CC: <optional structural question for the author, e.g. keep H3 separate or fold into H1?>

## Claims

Each claim is its own subsection: the claim, its hypothesis, its evidence status, and the route to settle it. No matrix, no table -- the subsections ARE the index.

Heading convention: `### C<n> - <short title> (<H>, <role>) - <status>`, where `<role>` is core / boundary / mechanism / input / positioning / feasibility / supplement. For a pure support claim (input / positioning / feasibility) that does not test one hypothesis, use its most-related H or `-` in the `<H>` slot, e.g. `(- , input)`.

Each subsection is a paragraph carrying four slots: (S1) the claim + its verdict, (S2) the verified statistic with spec and N, (S3) a one-line interpretation, (S4) the source file + caveat. For `weak`/`GAP` claims, state the gap and the route instead of a statistic. Never cite a "planned Table" as evidence.

### C1 - <short title> (H1, core) - supported

<claim statement>. <verified statistic, spec, N>. <one-line interpretation>. Source: <real file>; <caveat if any>.

### C2 - <short title> (H3, mechanism) - weak

<claim statement>. <why current evidence falls short>. <route: probe / task / discovery>. [NEED PROBE] <what the probe must test>.

### C3 - <short title> (H2, boundary) - GAP

<claim statement>. No evidence yet. [NEED PROBE] <what the probe must test>. Route: <task / discovery, then probe>.

> CC: <optional structural question, e.g. are C4/C5/C6 inputs/positioning/feasibility rather than contributions -- keep as claim sections or move to a short "Inputs and Feasibility" block?>

## Discussion-Only Interpretations (optional)

Interpretive findings that belong in Discussion, not Results. Explicitly marked to prevent creep into Results claims.

- **D1. <label> (interpretive):** <description>. No direct measurement; interpretive frame only.

## Robustness (optional)

Reported as a design strength in Methods, not claimed as a finding.

<sensitivity analyses: clustering, alt specs, multiple testing, exclusion criteria>

## Pending Evidence

To be buffered as probe plans in `_PROBE/` during the PROBE phase.

- MUST-HAVE: <GAP claims that block submission>.
- STRONGLY RECOMMENDED: <claims that pre-empt reviewer objections>.
- EXPLORATORY: <supplement analyses held from main claims>.

## Hypothesis-Claim Alignment

A paragraph (not a table) that maps each hypothesis to the claims that carry it, names support claims by role, and checks for orphan claims (no H) and unanswered hypotheses (claims all GAP). No venue framing.

<e.g. H1 (core) is carried by C1. H2 (boundary) is carried by C3. H3 (mechanism) is carried by C2. C4/C5/C6 are support claims: input, positioning, feasibility. C7 is an optional supplement. Every claim maps to a hypothesis or a support role, and every hypothesis has a claim.>

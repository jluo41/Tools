# Claims: <Paper Title>

Date: <YYYY-MM-DD>

Venue-FREE evidence inventory. This is the pure claim/evidence ledger; venue-specific framing (RQ wording, Editor's Chair Test, [primary] designation) lives in pitch, the cover letter.

Status vocabulary: `supported` / `weak` / `GAP`. Probe needs are marked inline as `[NEED PROBE] <what evidence is missing>`.

## Hypotheses

Venue-neutral statements of what the paper tests. The same H1 can become RQ1 worded for different venues; that reframing happens in pitch, not here.

- **H1.** <venue-neutral hypothesis statement>
- **H2.** <hypothesis>
- **H3.** <hypothesis>

## Claim-Evidence Matrix

One row per claim, status at a glance. The matrix is the index; the per-claim subsections below carry the evidence.

| ID | Claim | Status |
|---|---|---|
| C1 | <claim, as the paper states it> | supported |
| C2 | <claim> | weak |
| C3 | <claim> | GAP |

## Per-Claim Detail

One subsection per claim. Each is a paragraph with four slots: S1 claim + verdict, S2 verified statistic (spec, N), S3 one-line interpretation, S4 source file + caveat. For `weak`/`GAP` claims, state the gap and the route instead of a statistic. Never cite a "planned Table" as evidence.

### C1. <short title> (supported)

<claim statement>. <verified statistic, spec, N>. <one-line interpretation>. Source: <real file>; <caveat if any>.

### C2. <short title> (weak)

<claim statement>. <why current evidence falls short>. <route: probe / task / discovery>. [NEED PROBE] <what the probe must test>.

### C3. <short title> (GAP)

<claim statement>. No evidence yet. [NEED PROBE] <what the probe must test>.

## Discussion-Only Interpretations (optional)

Interpretive findings that belong in Discussion, not Results. Explicitly marked to prevent creep into Results claims.

- **D1. <label> (interpretive):** <description>. No direct measurement; interpretive frame only.

## Robustness (optional)

Reported as a design strength in Methods, not claimed as a finding.

<sensitivity analyses: clustering, alt specs, multiple testing, exclusion criteria>

## Pending Evidence

Probes/tasks not yet run, with the dependency chain.

- **<probe id> (<label>, <status>):** <what it will test>. <which claim it upgrades>.
- **Exploratory (supplement):** <analyses held from main claims>.

## Hypothesis-Claim Alignment

Maps hypotheses to claims; checks for orphan claims (no H) and unanswered hypotheses (claims all GAP). No venue framing.

| H | Hypothesis | Claims | How claims test this hypothesis |
|---|---|---|---|
| H1 | <hypothesis> | C1, C2 | <how the claims provide evidence for/against H1> |
| H2 | <hypothesis> | C3 | <how> |
| H3 | <hypothesis> | C4 | <how> |

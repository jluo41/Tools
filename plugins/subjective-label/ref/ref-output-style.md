# Reference: rendered output contract

Human-facing artifacts should make the active semantic and operational state visible
without becoming a second source of truth. Machine-readable records remain canonical.

## 1. Principles

1. **Lead with the result.** State status, active gate, and consequential evidence first.
2. **Separate evidence types.** Audit, challenge, final-test, external, and production
   metrics never share an unlabeled score column.
3. **Show provenance.** Every label count identifies human-confirmed, machine-accepted,
   unresolved, excluded, or invalid provenance.
4. **Pair canonical and rendered views.** Render inspectable Markdown from manifests,
   events, scorecards, and checkpoints; never hand-edit it as authority.
5. **Layer policy detail.** Preserve the full guideline and provide a compact cheatsheet.
6. **Expose uncertainty and holds.** Do not hide failed gates, missing capabilities,
   invalidated tests, or unresolved items behind a green summary.

## 2. Required rendered views

- `REPORT.md`: current lifecycle state, open gate, latest closed policy and gold, risk,
  holds, and next valid action;
- `gold/cumulative.md`: human-confirmed H/L/N and seven-region examples with reasons and
  checkpoint provenance;
- policy cheatsheet: class signals, boundary tests, procedure, and escalation rules;
- round report: batch composition, blind adjudication, audit/challenge metrics, policy
  diff, regression, coverage, risk, and stopping decision;
- evaluation summary: registered candidate scorecards on `T*`, baseline uplift, held-out
  executor result, intervals, errors, cost, and invalidation status;
- production report: route shares, terminal dispositions, risk queue, cost, and failures;
- final-audit report: design, weighted error, intervals, protected strata, repairs,
  provenance shares, and accepted limitations.

## 3. `REPORT.md` template

```markdown
# {project} — {construct}

status **{state}** · round **{round/phase}** · policy **{G_t}** · human gold **{D_t_n}**

| gate | evidence | result |
|---|---|---|
| quality | audit {metric + interval} | {pass/fail/pending} |
| stability | comparable audit improvement | {value; streak} |
| coverage | H/L/N + seven regions + strata | {pass/fail} |
| risk | unresolved and critical errors | {pass/fail} |
| sealed test | {reserved/frozen/released/valid/invalid} | {custodian} |

holds: {none or concise capability list}
next: **{one valid command or human decision}**
```

Keep the dashboard compact, but do not impose a line limit that removes material risk.

## 4. Round report template

```markdown
# Round {t} — {closed/open/held}

result: **{checkpoint decision}** · policy **{G_prev} → {G_t}** · gold **+{n}**

| slice | selected | human changed prelabel | final unresolved |
|---|---:|---:|---:|
| audit | ... | ... | ... |
| challenge | ... | ... | ... |
| consensus audit | ... | ... | ... |

policy diff: {semantic/procedural/casebook/wrapper summary}
regression: {pass/fail and affected prior gold}
stopping: quality {x} · stability {x} · coverage {x} · risk {x} · human {x}
```

## 5. Policy cheatsheet template

```markdown
# {construct} — decision cheatsheet (`{policy_id}`)

| class | positive signal | exclusion | canonical contrast |
|---|---|---|---|
| H | ... | ... | ... |
| L | ... | ... | ... |
| N | ... | ... | ... |

boundary order: {ordered tests}
uncertainty: {when to mark uncertain, escalate, or remain unresolved}
```

Examples should be compact and generalized. If verbatim text is retained, link it to
its authorized corpus record and avoid turning the casebook into a memorized training
set.

## 6. Scorecard template

```markdown
# Executor scorecard — {executor/run}

test **{T_star checksum}** · policy **{G_star checksum}** · validity **{valid/invalid}**

| evidence | score | interval | floor/result |
|---|---:|---:|---|
| absolute headline | ... | ... | ... |
| uplift vs minimal instruction | ... | ... | ... |
| held-out-family comparison | ... | ... | ... |

class/region/stratum errors: {link}
stability: {repeats}
cost and latency: {values}
```

## 7. Anti-patterns

- reporting consensus as gold or `NONE` as uncertainty;
- mixing challenge-set improvement with representative quality;
- claiming convergence from a single aggregate score;
- exposing sealed prelabels before the human-first event;
- exposing `T*` labels before executor predictions close;
- hiding invalidation, exclusions, or unresolved records;
- presenting similarity or confidence as semantic truth;
- shortening the guideline by deleting necessary boundary logic instead of layering it.

## 8. Implementation boundary

If a renderer cannot derive a view from canonical v2 artifacts, label the view `HOLD`
or `legacy`; do not fabricate fields or silently translate old panel metrics into the
new contract.

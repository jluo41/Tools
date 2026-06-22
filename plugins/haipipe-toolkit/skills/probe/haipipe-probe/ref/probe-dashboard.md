# Probe Dashboard

This defines the behavior of `/haipipe-probe` with no arguments and the panel
rendered by `/haipipe-probe <probe>`.

The dashboard is a derive-from-disk preflight. It orients the session before the
Probe Console or any lifecycle step acts.

## Golden Rule

```text
Never report a step as done because probe.yaml says so.
A step is done only when its expected artifact resolves on disk.
When stored status and disk disagree, disk wins and the gap is flagged DRIFT.
```

## Lifecycle Frontier

The dashboard uses the current probe lifecycle:

```text
Plan -> Gather -> Read -> Judge -> Return
```

The frontier is the first step whose disk predicate fails.

| Step | Done when | Next action if frontier |
|---|---|---|
| `Plan` | `probe.yaml` exists and has `claim` + `evidence_plan` | `/haipipe-probe plan ...` |
| `Gather` | required evidence refs/calls are present and linked/requested artifacts resolve or are explicitly pending | `/haipipe-probe gather <probe> ...` |
| `Read` | `evidence.md` exists and `probe.yaml.result` is present | `/haipipe-probe read <probe>` |
| `Judge` | `verdict.md` exists and `probe.yaml.verdict` is present | `/haipipe-probe judge <probe>` |
| `Return` | `return.md` exists and `probe.yaml.return` has a final status | `/haipipe-probe return <probe>` |

Glyphs:

```text
OK       done
ACTIVE   current frontier
TODO     not reached
DRIFT    stored state claims progress but disk predicate fails
BLOCKED  explicit blocker
```

## Shallow Check

For each active probe folder:

1. Read `probe.yaml`.
2. Extract path-like refs from `source`, `evidence_refs`, `calls`, `result`,
   `verdict`, and `return`.
3. Resolve refs against the project root.
4. Mark missing refs as drift if stored state depends on them.
5. Do not parse heavy artifacts or run integrity audits here.

Path-like refs include project-relative paths starting with:

```text
tasks/
discoveries/
insights/
probes/
paper/
applications/
```

## Render Skeleton

Same shape as the paper dashboard panel (header + one-line story + a lifecycle
progress bar), so paper and probe read consistently. probe's "story" is the claim.

### Single probe (Console / `/haipipe-probe <probe>`)

```text
📊 <P.id>  ·  <slug>   [⚠ drift]

  Claim: <one plain sentence: what this probe claims + scope/caveat>

  进度  Plan ─ Gather ─ Read ─ Judge ─ Return
         <g>    <g>      <g>    <g>      <g>
                ▶️ 这里(<one-clause why this is the frontier>)
```

### Project level (no-arg `/haipipe-probe`)

Header, then one compact panel per probe, then un-probed evidence (per the
"Un-probed evidence" rules above; nag only GAPs, not STANDALONE).

```text
📊 haipipe-probe  ·  <PROJECT>  ·  <DATE>

  <P.id>  <slug>
    Claim: <one line>
    进度  Plan <g> ─ Gather <g> ─ Read <g> ─ Judge <g> ─ Return <g>   [⚠drift]
          ▶️ 这里(<why>)

  Un-probed evidence:
    GAP (claim-bearing, no probe): <list or none>   -> /haipipe-probe file ...
    standalone (prep/display, fine): <count or short list>
```

Glyphs (derive-from-disk; first non-✅ rung = frontier):

```text
✅ done       the step's disk predicate passes
▶️ frontier   the first failing step; annotate "← 这里"
⬜ todo       not reached
⚠ drift      stored verdict claims progress but the disk predicate fails
```

Worked example (P.0605, derived from disk):

```text
📊 P.0605  ·  discretion-gradient   ⚠ drift

  Claim: 亲和度↑ 阿片处方强度,随临床自由裁量下降而衰减;腰背痛(高裁量)强,
         癌痛(指南锁死)近零。(待真实数据)

  进度  Plan ─ Gather ─ Read ─ Judge ─ Return
         ✅    ▶️       ⬜     ⬜      ⬜
               ← 这里(5/5 证据路径断:R01_Regression → R01_Reg 改名)
```

Frontier = Gather: Plan is ✅ (probe.yaml has claim + evidence_plan), but the 5
arm paths do not resolve on disk, so Gather fails first. ⚠ drift because the
stored verdict says mechanics=confirmed while those paths are gone.

Keep the render concise. The dashboard is an orientation panel, not a report.
Detailed evidence belongs in `evidence.md`; claim verdicts belong in `verdict.md`.

## Writes

No-arg dashboard may write generated project-level orientation:

```text
probes/_index.md
```

Opening a specific console writes:

```text
.probe-console.yaml
probes/<probe>/status.md
```

Generated files should be overwritten from disk state. Do not treat them as
hand-authored source of truth.

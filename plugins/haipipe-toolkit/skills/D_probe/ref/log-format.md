Probe Daily Log — Format
==============================

Location: `probes/<NN>_<slug>/logs/<YYYY-MM-DD>.md`
Owner:    Auto-appended by D_probe skills + manually edited by user/Claude.
Status:   Append-only narrative; never overwrite past days.


Why daily (not single log.md)
------------------------------

A long-running probe may span weeks. A single `log.md` becomes
unwieldy; a daily file:

- "What happened on E02 on 2026-05-24?" → open `logs/2026-05-24.md`
- "How did E02 evolve over the week?" → ls `logs/`, read chronologically
- Diff-friendly in git (today's edits don't churn the whole history)
- Aligns with how research actually unfolds (one decision per day, not 1 file)


File structure
--------------

```
# Probe <NN> — <slug> — <YYYY-MM-DD>

## HH:MM — <action> [<skill>]
<one-paragraph description>

## HH:MM — <action> [<skill>]
<...>
```

Each entry: timestamp + action + (optional) which skill or who wrote it,
then a 1-paragraph description.


Action keywords (vocabulary for "action" field)
------------------------------------------------

```
created           probe yaml first written
linked            run(s) attached to an arm
unlinked          run removed from an arm
aggregated        result block computed
re-aggregated     after excluding seed, fixing bug, etc.
claim-written     final claim sentence composed
reviewed          structural QA pass
verdict           Codex semantic verdict obtained
proposed          explore suggested next steps from this expmt
note              free-form thought (user or Claude)
discussed         chat or pairing session yielded a decision
linked-evidence   figure/table from a display task attached
status-change     status field went from A → B (e.g., pending → confirmed)
postmortem        probe closed (refuted / abandoned); lessons noted
```


Examples
--------

```markdown
# Probe 02 — lhm_vs_baseline — 2026-05-24

## 14:30 — created [design new]
Hypothesis: LHM-A test-id MAE lower than baseline by ≥ 0.5 mg/dL.
Discussed with Claude: pilot at N=3 paired seeds. Confound risk: LHM has
~1.2× params — flagged as ⚠️.

## 16:00 — linked [design link]
Baseline arm: run_seed42_baseline, run_seed7_baseline, run_seed13_baseline.
All status=ok; headlines 24.45 / 24.78 / 24.57.

## 18:30 — linked [design link]
LHM arm: run_seed42_lhm, run_seed7_lhm, run_seed13_lhm.
Note: run_seed7_lhm MAE = 22.10 vs others 23.91/24.04. Possible outlier.

## 19:30 — aggregated [result aggregate]
mean_std_paired_t on MAE_test_id.
Δ=-0.68, p=0.018, sign 3/3 negative. status=confirmed.
Caveat: outlier-excluded aggregate pending.

## 20:00 — note [user]
Need to re-aggregate excluding seed7. Will do tomorrow.
```

```markdown
# Probe 02 — lhm_vs_baseline — 2026-05-25

## 09:00 — re-aggregated [result aggregate --exclude-seeds 7]
Without seed7: Δ=-0.42, p=0.052 (marginal). status downgraded to
confirmed-pending-validation.

## 09:30 — reviewed [review probe]
Structural: 0 errors, 2 warnings (scale confound not in caveats;
outlier-excluded analysis now present).
Action: add caveat for +20% params.

## 09:45 — verdict [review claim]
Codex: claim_supported = partial; confidence = medium.
Suggested revision: weaken claim to "modest improvement on test-id,
needs param-matched re-test".

## 10:00 — claim-written [result claim]
Final: "LHM-A shows a modest 0.4-0.7 MAE improvement on test-id
(N=3 seeds, paired-t p=0.018-0.052 depending on outlier inclusion);
confound: +20% params; needs param-matched re-test for full confirmation."

## 11:00 — status-change [user]
status: confirmed → confirmed-pending-validation
Reason: outlier sensitivity + param confound.
```


Who writes what
----------------

```
created            — design new (auto)
linked / unlinked  — design link / unlink (auto)
aggregated / re-aggregated — result aggregate (auto)
claim-written      — result claim (auto)
reviewed           — review probe (auto)
verdict            — review claim (auto, via Codex MCP)
proposed           — explore propose (when invoked, auto)
linked-evidence    — design link-evidence (auto)
note               — user / Claude (manual)
discussed          — user / Claude (manual)
status-change      — any skill that changes status: field
postmortem         — user (manual, when closing probe)
```


Atomic append
-------------

Each entry is appended to today's file via:

```bash
DATE=$(date +%F)
HHMM=$(date +%H:%M)
LOG="probes/<NN>_<slug>/logs/${DATE}.md"

# Init file if missing
if [ ! -f "$LOG" ]; then
  mkdir -p "$(dirname "$LOG")"
  echo "# Probe <NN> — <slug> — $DATE" > "$LOG"
  echo "" >> "$LOG"
fi

# Append entry (with flock to be safe if concurrent)
(
  flock -x 200
  echo "## $HHMM — <action> [<skill>]" >> "$LOG"
  echo "<description>" >> "$LOG"
  echo "" >> "$LOG"
) 200>>"$LOG.lock"
```


Manual edits welcome
---------------------

Unlike runlog (which was machine-aggregated and easily clobbered), this
file is intended for human editing too. Add notes, discussion summaries,
links to chat transcripts, etc., freely. Skills only APPEND; they never
rewrite past entries.


Cross-day discovery
-------------------

```bash
# All days for this probe, chronological:
ls probes/02_lhm_vs_baseline/logs/

# Today's log across all probes:
find probes -path "*/logs/$(date +%F).md"

# Search all probe logs for a keyword:
grep -rn "outlier" probes/*/logs/
```


Difference from B_project's defunct runlogs/
---------------------------------------------

```
B_project/runlogs/<DATE>-runlog.md     (DELETED 2026-05-24)
  was: per-task daily index + LLM narrative of runs
  why deleted: "today's runs" wasn't a real research question

D_probe/<ID>/logs/<DATE>.md       (THIS file)
  is:  per-probe daily narrative of design decisions
  why kept: probes evolve over days; daily slicing matches research
            cadence ("what did we decide about E02 today")
```

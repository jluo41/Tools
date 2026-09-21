[CRASH] The supplied nightly-report trace fails while summarizing empty input because `report.py:6` divides by zero.

## 🔍 What Failed

The unit is the isolated report script, the job name is `nightly-report`, and the step is `summarize input values`. The exact error is `ZeroDivisionError: division by zero`. No remote Run ID was supplied.

## 🧠 Why

`/tmp/interaction-validation-lb40b3lu/report.py:6` originally contained `average = sum(values) / len(values)`. The supplied input is `[]`, so its length is zero and the division stops report creation. Generic mode applies; no environment-specific profile covers this fixture.

## 🛠️ What I Changed, Where, And Why

**WHERE**

```text
/tmp/interaction-validation-lb40b3lu/
  report.py :6 CANONICAL; no copies configured
```

**WHAT**

```python
# was
    average = sum(values) / len(values)
# now
    average = sum(values) / len(values) if values else None
```

The supplied fixture's empty-input policy uses an unavailable average, serialized as `null`. This guard preserves the non-empty calculation and does not validate nonnumeric inputs.

- CARRY: No transfer or deployment mechanism was supplied or verified; no remote copy is claimed.
- GATE: No local gate available. Source inspection, Python AST syntax parsing and report-shape checks passed; no report execution or remote rerun was performed.

## 📄 The Report I Wrote

Issue `unassigned`: `/tmp/interaction-validation-lb40b3lu/register/empty-input-report.md`.

- Symptom: preserved the exact supplied trace.
- Cause: empty input makes the denominator zero.
- Fix: empty averages become `None`, serialized as `null`.
- Scope: one canonical line, no copies or other register artifacts.
- Not affected: input parsing, count, and non-empty arithmetic.
- Gate rule: `--`; no checker exists for this fixture.

The diagnosis outcome is fixed because a local canonical edit was made. Remote verification remains unperformed.

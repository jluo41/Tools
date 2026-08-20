# a-executor

The auditor is `src/page_lifecycle.py`, run over every file under `_runs/` on 260819; re-run the same day at EVIDENCE after the 260819-1813 run landed.
Verbatim output, not summarised:

```
260805-0216-QB8e     FAIL (2)
  page-path-stale            run         `page` records a path that no longer resolves
  artifact-version-mismatch  run         current source/render identity ≠ recorded

260818-1510-QPw00    FAIL (1)
  artifact-version-mismatch  run         current source/render identity ≠ recorded

260818-1543-QPw00    FAIL (2)
  checked-version-mismatch   receipt[2]  CHECK must leave one identical version_before/version_after/checked_version
  artifact-version-mismatch  run         current source/render identity ≠ recorded

260819-1813-QPw00    FAIL (10)
  max-steps-exceeded         run         6 receipts exceed max_steps=1
  receipt-after-terminal     receipt[1]  receipt follows HOLD
  receipt-after-terminal     receipt[2]  receipt follows HOLD
  receipt-after-terminal     receipt[3]  receipt follows HOLD
  version-continuity         receipt[3]  version_before must equal the preceding receipt's version_after
  receipt-after-terminal     receipt[4]  receipt follows HOLD
  missing-artifacts-list     receipt[5]  artifacts must be a list
  human-gate-contract-mismatch receipt[5]  receipt human_gate.required must match the raw-material packet
  receipt-after-terminal     receipt[5]  receipt follows HOLD
  artifact-version-mismatch  run         current source/render identity ≠ recorded
```

**4 runs stored, 4 FAIL, 0 PASS. 15 findings, 8 distinct codes.**

The codes are not equally serious, and the distinction matters:

- `artifact-version-mismatch` fires on all four and is EXPECTED. It compares the page as it stands now against the identity recorded when the run finished, and every one of these pages has been edited since. It says the receipt is old, not that the run was wrong.
- `page-path-stale` fires on the oldest run because the page was later renamed. The auditor recovered by searching for the file's basename, which is why it degraded to a named finding instead of a false "artifact missing".
- `max-steps-exceeded` and `receipt-after-terminal` fire on the 260819-1813 run because that run's receipt file is a shared APPEND surface for the day's HOLD passes: each pass parks at HOLD and the next agent appends after it, and the auditor reads that as steps past a terminal route. That is RECORDED DEBT of the append convention, confirmed here, not repaired: the receipt shape has no multi-pass vocabulary yet.
- `version-continuity` on the same run is the same debt seen from the version chain: concurrent passes do not hand each other `version_after`.
- `missing-artifacts-list` and `human-gate-contract-mismatch` fire on that run's last receipt, appended by the main session for the C3/C4/C5 division rotation: its `artifacts` field is not a list and its `human_gate.required` does not match the packet. Shape debt of a hand-written receipt on the shared append surface, confirmed here, not repaired.
- `checked-version-mismatch` at `receipt[2]` of 260818-1543 is the real one. CHECK is required to leave `version_before`, `version_after` and `checked_version` identical, because a judge that reports on a version it did not read is the one failure the receipt exists to catch. That receipt violates it, and no reasoning had predicted it: it was found by running the auditor.

**So the loop's own audit claim is half-earned.** The machinery exists and it caught a genuine contract violation in the board's own history. What is missing is any run that PASSES: the passing half of `A14.1`'s "both a passing and a failing test" has no stored example.

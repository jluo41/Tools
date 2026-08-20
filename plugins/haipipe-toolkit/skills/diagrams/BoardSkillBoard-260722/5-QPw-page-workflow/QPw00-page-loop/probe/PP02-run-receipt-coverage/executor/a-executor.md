# a-executor

Read from disk on 260819; re-pulled the same day at EVIDENCE after the 260819-1813 run landed.

**4 runs are stored, holding 15 receipts between them.**

```
260805-0216-QB8e    5   CHECK · REVISE · CHECK · REVISE · CHECK      → CLOSE
260818-1510-QPw00   1   OUTLINE                                      → HOLD
260818-1543-QPw00   3   DRAFT · REVISE · CHECK                       → HOLD
260819-1813-QPw00   6   OUTLINE · PROBE · OUTLINE · OUTLINE · PROBE · OUTLINE → HOLD
```

**Phases covered: 5 of 7**: OUTLINE, DRAFT, PROBE, REVISE, CHECK.
**Never executed under the contract: 2**: EVIDENCE, COMPILE.

The first run is the only closed one, and every one of its five receipts is CHECK or REVISE: it exercised the judge/repair edge and nothing else. The two 260818 runs are single-pass and cover one new phase each. The 260819-1813 run is the first to hold PROBE receipts: the PREPARE loop's dispatch half has now run under the router, and its receipt file doubles as the day's shared append surface, one HOLD per pass.

So the loop has been driven end to end zero times. No stored run contains an EVIDENCE or a COMPILE receipt, which means the phase that lands evidence on disk has still never been executed by the router, only by hand.

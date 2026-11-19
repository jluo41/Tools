# The haistack report

Every `/haistack` run writes one report per article, so anyone can read later why the rule exists and why
it will hold (JL 261118: "for each time, we should have a report").

## Where

`<owner skill>/constitution/A<NN>-<slug>.md`, beside the owner's `CONSTITUTION.md`. The article links it:
`**Report:** constitution/A<NN>-<slug>.md`. `constitution.py --check` marks ❗ any article whose report is
missing.

## The six parts, in this order

```markdown
# A<NN> · <the rule, a few words>

> "<JL's words, verbatim>" (JL <YYMMDD>, <where>)

## 1. Need
What JL needs, in his terms: what he wants to see or do, and on which screen or file.

## 2. Now
What the current skill, code or page actually does today, with file:line and what the real output showed
(a screenshot, a command's output). Read and run it; never describe it from memory.

## 3. Gap
Why the current setup cannot meet the need: the missing rule, the missing field, the writer that never
looks, the check that does not exist. Name the cause by file and line, not the symptom.

## 4. Methods
The ways it could be fixed (2 or 3), each with what it costs and what it leaves open, and which one was
chosen and why. A method that fixes only the instance JL saw is listed and rejected.

## 5. Update
What was changed: each file, one line each, and every case from the article's Cases with ✅ or ⬜.
The Run line and its real output.

## 6. Never again
Why the chosen method stops the same problem next time: which writer can no longer produce it, which
check fails if it comes back, who reruns that check and when (`/haistack sweep`, a test, a builder
assert). What would still let it return, if anything, stays here as an open risk.
```

## Rules

1. **Real evidence**: Now and Update quote real output; a report written before the check ran is not one.
2. **Short**: a report fits one screen per part; the detail lives in the files it names.
3. **Reopened article**: a new dated `## Reopened <YYMMDD>` part is added to the same report, saying
   which case was missed and why the old Run line did not see it.

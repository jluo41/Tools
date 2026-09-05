# Page Division Writing Result

One `Page · Division Writing` Run returns a candidate that can be judged and
promoted independently.

```text
results/<RUNNAME>/
├── candidate.md   exactly one `### <n> · <name>` Content division
├── trace.md       Bullet → sentence(s) → Evidence Result/source mapping
└── runtime.yaml   neutral haipipe-run receipt
```

`trace.md` uses one row per plan Bullet:

| Plan address | Candidate locator | Evidence Items/Results | Status | Finding |
|---|---|---|---|---|
| `C2.P1.B3` | `candidate.md#sentence-4` | `E04-CITE-… → pj…r01` | covered | none |

The Result is accepted only when:

1. every target Bullet has a candidate locator;
2. every factual claim names a folded Evidence Result or an allowed static
   source from the frozen Local Input;
3. no candidate sentence exceeds the approved claim strength;
4. the Page Face owner and narrative/style checks pass;
5. `runtime.yaml` records the exact Context, plan, evidence, and prior Page
   versions.

Promotion into `<page>.md` is a separate CONTENT authority step and records the
Run id. An accepted Result may exist without being promoted; a promoted
division may not claim a different Result silently.

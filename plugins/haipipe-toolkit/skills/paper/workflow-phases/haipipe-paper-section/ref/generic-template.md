# Generic Section Page outline

Use this explicit fallback when the selected venue has no current template for
the Section kind. Record that fallback in `structure-source`; never convert this
generic outline into an invented venue rule.

## Section contract

```yaml
page-type: section
section_kind: <kind>
narrative-row: <row id and version>
reader-question: <one question>
entry-state: <reader state on entry>
exit-state: <reader state on exit>
claim-ids: [<exact Narrative ids>]
venue-allocation: <binding rules; pack observations labeled separately>
structure-source: ref/generic-template.md · <why: ABSENT BY DESIGN or MISSING>
evidence-allowlist:
  pagex: [<accepted Page and scope>]
  probe: [<PP ids and values>]
  citations: [<bibex keys>]
  displays: [<unit ids and accepted versions>]
transition-in: <join from prior Narrative row>
transition-out: <join to next Narrative row>
```

## Opening

Orient the reader to the Section's question, order, and governing limitation.
Do not restate the paper abstract or preview evidence that has not landed.

## Move outline

Create only the moves required by the current Narrative row. For each move:

```text
reader move
claim ids advanced
exact proposition established
PageX/probe/citation/value/display bindings
expected prose or display placement
transition to the next move
known limitation or unresolved obligation
```

The final move must deliver the declared exit state and transition-out without
introducing a new claim.

## Exit check

- Every move traces to the current Narrative row.
- Every consequential statement has inspectable support or remains visibly open.
- Probe used the PageX lane for accepted Pages and the QA lane for
  Task/Discovery; their durable records remain distinct.
- Venue rules and pack observations are not conflated.
- The compiled output reflects the accepted Page version.

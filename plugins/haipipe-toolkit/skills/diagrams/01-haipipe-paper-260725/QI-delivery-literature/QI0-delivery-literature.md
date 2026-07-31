# Delivery: Literature
state: ✅ RULED
owner: JL
method: bind discovery-returned sources to manuscript sentences without letting the paper invent bibliography entries

## Question
How does literature travel from the bank into a sentence and its delivered formats?

## Boundary
- ✅ Covered here
  Literature questions, source verification, sentence citations, and bibliography bindings.
- ↪ Covered by Work
  Commissioning the discovery.
- ↪ Covered by QC1
  The citation marker and evidence card itself.

## Diagram
```text
Work probe → discovery answer → S-page sentence → citation marker → bibliography
```

## Content
| Field | Contract |
|---|---|
| Lifecycle | After Work and before Value and Display in the Delivery reading order. |
| Authority | S-page prose plus the discovery answer bound through `1-probes/`. |
| Projects to | Sentence citations and format-specific bibliography rendering. |
| Skills | `haipipe-paper-probe`, evidence checks, and format adapters. |
| Consumes | Verified literature returned by discovery. |
| Gate | The cited source supports the exact sentence and the bibliography key is human-approved. |
| Open gaps | Word export has no `.bib` and must preserve an explicit citation field or baked reference. |

## Items to Finish
- [x] Preserve QC1 as the detailed citation contract.

## Where we are
The Delivery overview now places Literature after bank-growing Work.

## Files
- `QC1-sentence-citation.md`

## Law
An agent may search and verify bibliography evidence; it never invents or silently writes a bibliography entry.

## Glossary
- **Literature binding**: the inspectable path from a sentence marker to the source that supports it.

## Log
260729 · Literature placed after Work in the accepted Delivery order.

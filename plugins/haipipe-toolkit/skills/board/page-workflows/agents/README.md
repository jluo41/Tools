# Page workflow actors

One actor owns each current Page phase. Every producer reads
`../haipipe-page-workflow/ref/producer-contract.md`; CHECK remains an
independent fresh-context judge.

```text
haipipe-page-context-agent     00 CONTEXT · PREPARE
haipipe-page-outline-agent     01 OUTLINE · SHAPE, SURVEY
haipipe-page-evidence-agent    02 EVIDENCE · LAND, EMBED
haipipe-page-content-agent     03 CONTENT · WRITE
haipipe-page-check-agent       04 CHECK · CHECK; also CONTENT's cold pre-check
```

The old `haipipe-page-draft-agent` and `haipipe-page-revise-agent` remain
compatibility identities for stored receipts. New dispatch uses the CONTENT
agent. `_old/haipipe-page-probe-agent` remains historical.

## Stand-in rule

Agent types register at session start. If a new type is unavailable in the
running session, dispatch a general-purpose stand-in whose first action is to
read the exact phase agent file as its identity and then the shared producer
contract. The receipt names the phase-role agent, not the stand-in.

# Page workflow actors

Actors implement the selected Run or controller operation; the legacy Run names below are dispatch coordinates, not Workflow units. Every producer reads
`../../haipipe-page-workflow/ref/producer-contract.md`; CHECK remains an
independent fresh-context judge.

```text
haipipe-page-context-agent     context · PREPARE
haipipe-page-structure-agent     structure · SHAPE, SURVEY
haipipe-page-evidence-agent    evidence · LAND, EMBED
haipipe-page-writing-agent     writing · WRITE
haipipe-page-check-agent       check · CHECK; also CONTENT's cold pre-check
```

The board family's four agents moved here when `skills/board` was retired (JL 261005):

```text
haipipe-board-reviewer-agent   the BASE of haipipe-page-check-agent: cold read, route, never edit
haipipe-page-approver-agent    one artifact against one numbered rule pack (approve-rules/); checked: auto
haipipe-page-auditor-agent     packet builder and receipt keeper of one Page workflow pass
haipipe-page-creator-agent     producer base: stands in only when a current producer is missing
```

Historical DRAFT/REVISE/COMPILE receipt tokens are interpreted by the
lifecycle auditor. They do not retain callable agent identities; every current
writing dispatch uses the CONTENT agent. Retired actors live only in Git
history.

## Stand-in rule

Agent types register at session start. If a new type is unavailable in the
running session, dispatch a general-purpose stand-in whose first action is to
read the exact owner agent file as its identity and then the shared producer
contract. The receipt names the owner-role agent, not the stand-in.

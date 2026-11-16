# Page workflow actors

Actors implement the selected Run or controller operation; the legacy Run names below are dispatch coordinates, not Workflow units. Every producer reads
`../../haipipe-draft-workflow/ref/producer-contract.md`; CHECK remains an
independent fresh-context judge.

```text
haipipe-draft-context-agent     context · PREPARE
haipipe-draft-structure-agent     structure · SHAPE, SURVEY
haipipe-draft-evidence-agent    evidence · LAND, EMBED
haipipe-draft-writing-agent     writing · WRITE
haipipe-draft-check-agent       check · CHECK; also CONTENT's cold pre-check
```

The must-check gate's reading agents (2026-11-15). `haipipe-paper/scripts/must_check.py` runs the scripts and
prints which of these to dispatch, each in a fresh context, none reading text it wrote:

```text
haipipe-draft-eval-structure-agent    S1, S2: paragraph jobs and slots against § 8.3 and venue examples
haipipe-draft-eval-paragraph-agent    D1: paragraph logic, blind, 0-10, a fix under 8
haipipe-draft-eval-sentence-agent     D1: sentence logic, read, ai; the scope guard's reading half
haipipe-draft-ab-reader-agent         D2: blind A/B pairs, easier and same meaning; writes no text
haipipe-draft-evidence-value-agent    a VALUE item proposed for each number no item covers
haipipe-draft-evidence-cite-agent     the cited paper read against its sentence; a person verifies
haipipe-draft-evidence-display-agent  the sentence's claim read against the display's headline and caption
haipipe-draft-consistency-agent       one version: one term one meaning, one claim one wording, counts
```

`haipipe-draft-writing-agent` also writes D2's rewrites and adopts only the pairs the A/B reader kept.

The board family's four agents moved here when `skills/board` was retired (JL 261005):

```text
haipipe-block-reviewer-agent   the BASE of haipipe-draft-check-agent: cold read, route, never edit
haipipe-draft-approver-agent    one artifact against one numbered rule pack (approve-rules/); checked: auto
haipipe-draft-auditor-agent     packet builder and receipt keeper of one Page workflow pass
haipipe-draft-creator-agent     producer base: stands in only when a current producer is missing
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

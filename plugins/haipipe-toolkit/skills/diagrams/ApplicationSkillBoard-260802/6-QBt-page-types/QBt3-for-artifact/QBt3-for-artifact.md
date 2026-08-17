# Application Artifact: one independently reviewable delivery unit
state: 🟡 PARTIAL · fresh-context grain passed · open: render, stale acceptance
page-type: artifact
artifact-kind: sms
artifact-unit: specimen
owner: JL

## Opening
Where does concrete intervention content live, and what exactly does a person accept?

One Artifact Page executes one Intervention component row and owns its copy, local trace, visible render, and version-bound acceptance. Neighboring units split only when one can pass while another fails; comparison arms reviewed together remain divisions on the same Page.

**Covered here**: Artifact grain, rendering, trace, and acceptance.

**Covered elsewhere**: Intervention owns global strategy; Deploy ships only accepted versions.

## Writing Style
Show concrete content separately from explanation. Name handoff and render versions whenever acceptance is discussed.

## Diagram
**Artifact authority**: one handoff produces one reviewable version before deployment.

```text
Intervention row ─▶ authored unit ─▶ visible render ─▶ acceptance ─▶ deploy
```

## Content

### 1 · Unit contract
**Unit identity**: one handoff names one review grain.
```text
artifact-kind + artifact-unit + intervention-row + venue
```
The unit carries one audience job, current handoff, venue constraints, and safety rails.

### 2 · Authored content
**Concrete output**: the user-visible material is separate from its rationale.
```text
content version → exact copy / interface content
```
Concrete copy or interface content lives here rather than in the Intervention map.

### 3 · Variants and arms
**Review grain**: comparable arms stay together and vary one declared dimension.
```text
invariant core | arm A variable | arm B variable
```
Arms remain together when comparison is the review unit; each names the one variable it changes.

### 4 · Trace
**Local lineage**: every substantive move reaches settled knowledge.
```text
content move → Intervention principle → Insight K/W row
```
Every substantive move reaches an Intervention principle and settled Insight Page.

### 5 · Render and preview
**Visible version**: review points to one exact rendering of one exact content version.
```text
content v<n> → render v<n> → preview path
```
The Page points to the exact visible version under review.

### 6 · Acceptance
**Acceptance lock**: approval binds both input and visible output versions.
```text
reviewer + date + handoff version + render version → accepted
```
Acceptance names reviewer, date, handoff version, and render version; any changed input reopens it.

## Aims

### A4 · Trace
- A4.1 · Claim audit reaches settled Insight Pages without entering Task folders.
  **Done when:** a rendered specimen passes the trace check.

### A6 · Acceptance
- A6.1 · Changed handoff or render invalidates prior acceptance.
  **Done when:** a known-stale fixture fails before a fresh version passes.

## States

### A4 · Trace
- ⬜ A4.1 · No rendered specimen exists yet.

### A6 · Acceptance
- ⬜ A6.1 · Known-stale negative fixture not yet exercised.

## Files

### 📋 Contracts
- `../../../../application/page-types/haipipe-page-for-artifact/SKILL.md`
  The Page Type contract this specimen exercises.
- `../../../../application/haipipe-application/fn/artifact.md`
  The Application door procedure.

## Log
260817 · Fresh Application agent kept jointly reviewed SMS variants on one Artifact Page, deferred a separable renal Artifact until warranted, and bound future acceptance to both handoff and render versions.
260817 · Opened as the Application unit Page: concrete content, render, and version-bound acceptance.

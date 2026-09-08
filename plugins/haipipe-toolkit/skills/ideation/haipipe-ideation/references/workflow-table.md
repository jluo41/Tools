# Ideation workflow table

This is the concise Phase × Run map for the semantic ideation layer. The
ideation unit uses BJTR for its durable container, while Task and Discovery
own every addressable Run.

| ID | Phase / cycle | Purpose | Authoritative writes | L4 Run profile | Exit / next route | Human gate |
|---|---|---|---|---|---|---|
| `i0.scope` | SCOPE | Freeze one direction, question, boundary, and decision rule. | `ideation.yaml`, direction face | none | Identity and scope agree → `i1.bundle` | Resolve material ambiguity |
| `i1.bundle` | BUNDLE | Collect and freeze internal Task plus external Discovery pointers. | `bundle/evidence-bundle.yaml`, bundle receipt | none; reads owner Results/QA | Every input has owner path, status, locator, and role → `i2.search` or `i3.synthesize` | Approve a consequential evidence boundary when needed |
| `i2.search` | SEARCH / REUSE | Reuse adequate Discovery Results or request missing source-map/source-reading work. | `workflow/` request/return receipts; no Discovery mutation | Discovery `paper-analysis` / `source-analysis` × `N_admitted`; Task Run × `N_missing_internal` | Returned owner Results are paired and valid → `i1.bundle` | None; citation verification remains owner-side |
| `i3.synthesize` | SYNTHESIZE | Separate observations from inference and write the direction plus a dynamic compared candidate set. | `cards/direction.yaml`, `cards/iNN_*.yaml`, human face | none | Every material claim traces to bundle IDs; gaps are explicit → `i4.pressure` | None |
| `i4.pressure` | PRESSURE-TEST | Test claims against closest work and feasibility; route gaps to owners. | card revisions plus pressure-test receipts | New/changed work uses owner Task/Discovery Run contracts; no ideation Run | Claim-level novelty and feasibility states are truthful → `i5.select` or `i2.search` | Accept a named risk only at selection |
| `i5.select` | SELECT | Record which cards, if any, a person chooses and why; comparison order is not selection. | selection receipt; card state; distinct Story route per selected card | none | Human decision exists → `i6.handoff` or remain open | Required: select, abandon, or defer |
| `i6.handoff` | HANDOFF | Package selected cards and their distinct Story routes for Paper P0 without copying evidence. | `handoff/paper-ideation.yaml` | none | Packet passes handoff assertions → `haipipe-page-ideation` | Required: person/date and accepted risk |

## Run law

The planned external count is `N_admitted canonical Discovery Subjects`; the
planned internal count is `N_missing_internal analyses` only when a Task Run
is actually commissioned. Search calls, card writes, synthesis, pressure-test
passes, and the handoff are not Runs. Actual counts come only from owner-native
Tickets plus valid runtime receipts.

For a Discovery request, the exact chain is:

```text
haipipe-ideation → haipipe-discovery → haipipe-discovery-search
                 → haipipe-run → one canonical Subject per Run
                 → same-stem Discovery Result + one-entry Bib
                 → bundle refresh
```

For internal feasibility:

```text
haipipe-ideation → haipipe-task qa (reuse)
                 or haipipe-task / haipipe-run (new bounded analysis)
                 → owner Result/QA receipt → bundle refresh
```

The four Run tests, exact Ticket/Result pairing, `supersedes:` rule, and Bib
authority remain those of `haipipe-run` and the owning Task/Discovery dialect.
The workflow cannot close a card claim by counting a search hit or a model
opinion as a Run.

## Handoff assertions

The packet is ready only when:

- one Direction Card and a dynamic set of one or more stable Idea Cards are named;
- each selected card's Core Claims have claim-level novelty readings and
  direct evidence paths, with unverified work marked as such;
- feasibility has a Task-owned receipt or an explicit, reasoned waiver;
- all cited Discovery Results point to their direct Card and one-entry Bib;
- unresolved gaps and hard limits are visible;
- a person has recorded selection, date, accepted risk, and one distinct Story
  route per selected card;
- the packet contains paths and IDs only, so Paper can bind its own pages and
  citations without duplicating owner artifacts.

An absent selection is not a failed search. It leaves the ideation unit open or
routes it back to `i2.search`, `i3.synthesize`, or `i4.pressure`.

---
name: haipipe-insight-wisdom
description: >-
  InsightBoard Folder contract for Wisdom: contextual
  counsel from a bounded Knowledge claim plus the signed Design Handoff that
  is the only evidence a DesignBoard may bind. Trigger: insight wisdom,
  counsel, design handoff, folder-kind wisdom, /haipipe-insight-wisdom.
metadata:
  version: "1.9.0"
  last_updated: "2026-10-01"
  workflow: haipipe-insight-workflow
  folder_kind: wisdom
  primary_face: page
  page_ruling: domain-gate
  legacy_page_type: wisdom
  group-token: "W"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Page Face (haipipe-page flow): Content one division per need (cite: the Knowledge relied on; judge: counsel, forbidden overreach), then the Design Handoff division"
---

# /haipipe-insight-wisdom · counsel, then hand off

Load `haipipe-folder`, `haipipe-page`, `haipipe-insight`, and the workflow.
Read `../../haipipe-insight/ref/page-v2-adapter.md` before authoring counsel or
exporting the handoff.

## Position

Wisdom answers `QW` from accepted Knowledge pages and crosses to Design
only through a signed handoff. It is the one level that stays a Page Folder
(JL 261001), because a DesignBoard binds its signed handoff by path; it lives
in its partition's folder of the board (`1-full/W<NN>-full-<slug>/`). Data,
Information and Knowledge answers never cross directly. A Wisdom
question's evidence needs are cite (Knowledge needs) and judge only
(`../../haipipe-insight/ref/evidence-needs.md`), so its page has no `runs/`; a compute need on a QW
row is misrouted and becomes a Knowledge successor question.

## Folder Kind

Wisdom says **what the claim means here and what must not be concluded**. It
may counsel `do`, `avoid`, or `leave undecided`; it never writes message copy,
button text, send timing, variants, or another Design artifact.

## Input

One registered QW ask; Application audience/context/decision; source versions;
and unresolved gaps. Its epistemic parent is either named local Knowledge
pages (`<n>-<partition>/K<NN>-<partition>-<slug>/`) with strength, rivals and boundary, or
one exact
`Task Insight instance/item@execution-version/RF<n>` plus Result path,
accepted by the workflow's pre-climbed
external-parent assertion. The second form is evidence input, not a handoff.

## Page Face

The page is a `haipipe-page` Page Face written through that skill's flow
(`../../haipipe-insight/ref/report.md` § The flow). Its Content follows its
needs: the cite needs name the Knowledge relied on, the judge needs give the
counsel and the forbidden overreach, and the last division is the Design
Handoff. Every `W<n>` names the Knowledge page it rests on, by question id
and partition (`← QK2 · full`, the page its register cell names), and cites
the needs it answers (`[QW1.E1]`), bound in the page's `answers.yaml`; on a board made before page tickets, an exact Page
v2 `PARENTS` record for its K page. For a bridge Folder, `Knowledge Cited`
names exact external K/W/RF row ids and the item execution through a Supporting
Result and its local Evidence Run; it does
not copy them or pretend the RF is local K. The handoff carries finding,
strength plus the Knowledge owner's evidence-bound strength basis, boundary,
sources, design consequence, forbidden overreach, gaps, `serves:`, and a final
`signed:` token. Keep the basis short and tied to the cited Knowledge pages; do not
relabel it as a cross-domain probability.

## Task Face

Test applicability against the K boundary; write bounded counsel; construct the
standalone handoff; stop for a person's signature; and reopen the counsel and
signature when a K parent or pooling verdict changes. A new signature is
required whenever the signed payload changes, including its evidence/version
pins even if counsel wording is unchanged. Retain the old signature only as
history; reuse it only for an identical signed payload with current dependencies. For a bridge, verify the selected item's
independent CHECK acceptance, Wisdom target, full DIKWRF trace, source versions,
Question registration, and exact Result pin. Open sibling items do not block it.
Then contextualize it here. Under a valid
POOL verdict, non-template W Folders close by explicit deferral and export no
handoff. Under `UNDETERMINED`, the template W may answer only for the full
extract. An unanswered non-template W may use `🟡 <page> final` only when its
Page states why that partition answer cannot close and what evidence or
decision could change it. This is a licensed non-answer: it has no GI5 pass,
signature, handoff, or Design binding; the Page omits the `SERVES` and `signed:`
rows that identify an exported handoff. The Question owner records its partial
settlement at GI6. If the frozen Workflow can still obtain the needed evidence,
keep the target waiting instead of closing it early.

### Run Profile

Use the parameterized Run Specs in
`../../haipipe-insight-workflow/ref/run-workflow.md`. This Folder kind does
not itself allocate a Run. Declare a bounded Spec per selected Page writing,
evidence, delivery, or supporting computation target; use the worker's native
Ticket, Result, receipt, and close rule. Record each actual Run once in the
Insight Runtime, with its full owner address and exact input versions.
Routine resource updates and GI evaluations remain control records. An accepted
Run Result satisfies only its declared target; Page CHECK/CLOSE and the
Folder's GI conditions still govern citation and register settlement.

## Workbenches

- `outline` required, including semantic parent-row lineage and the
  Supporting/local Result evidence graph for an exact Task item RF parent;
- an applicability gap commissions a decided Supporting Run when computation
  is required; no active PageX or Probe lane;
- `code` forbidden: this Folder contextualizes accepted claims.

## Gate and Closure

GI5 passes only for an exported W handoff after the Page reaches CHECK/CLOSE,
`haipipe-insight-check` finds no overclaim on its cell, counsel stays inside
its exact current Knowledge pages, forbidden overreach is
visible, the handoff reads standalone, and `signed: ✅ <initials> <YYMMDD>`
records a person's decision. `signed: ⬜` is a clean stop, not permission to
infer approval. A bridge also requires the external-parent assertion to remain
current; RF settlement alone cannot pass GI5. A valid POOL deferral and a
licensed `UNDETERMINED` partial-final non-answer do not pass GI5 and export no
handoff. GI6 is the following Question register-settlement act; this Folder
does not perform or rename it.

## Handoff

Export only the signed Design Handoff. A DesignBoard freezes its exact
path/Page-version, signature, and GI6 settlement receipt as input
and never re-derives from Data, Information or Knowledge answers. It creates no PageX lane or synthetic
Run. A deferring W Folder exports only a
pointer to the template handoff. A Task RF never crosses this boundary directly:
the local signed W is the only Design authority.

## Files

- Page and handoff: `<WisdomFolder>/<WisdomFolder>.md`
- Binding: `<WisdomFolder>/answers.yaml` (cite and judge needs only)
- External-parent binding, when used:
  `<WisdomFolder>/draft/<stem>-evidence-items.md` and its Supporting/local Results
- Cross-board binding: the consuming Design Page's Evidence Workspace

For GI5/GI6 receipts and the read-only current Design binding projection, read
[`handoff-record.md`](../../haipipe-insight-workflow/ref/handoff-record.md).

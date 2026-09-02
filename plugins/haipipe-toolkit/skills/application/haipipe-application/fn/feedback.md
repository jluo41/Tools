---
name: haipipe-application-feedback
description: >-
  Utility verb for capturing feedback about the Application skill family and
  routing it to the owning door, workflow, phase-owned Folder contract,
  plugin, or venue reference pack. Merge repeated concerns; list or move
  existing items. This records feedback only and never fixes it in the same
  invocation.
argument-hint: '["<text>" | list [owner] | move <file> <owner>]'
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Feedback · route the concern to its current owner

Capture feedback about the Application machinery, not about the substantive
intervention or artifact it produces. The new architecture has no lifecycle
stage inboxes: ownership follows the Folder model and the native I0-I5/D0-D5
workflows.

## Capture

For /haipipe-application feedback "<text>":

1. Read the named Folder/Board and its current folder-kind or phase when the
   invocation supplies one. Runtime context is a secondary routing signal;
   the feedback words are primary.
2. Apply the cross-cutting guard. A concern about the two-board boundary,
   accepted terminal, or Application-wide routing belongs to
   haipipe-application/feedback/. A concern about the neutral two-face model
   belongs beside haipipe-folder.
3. Otherwise resolve the narrowest current owner using the table below.
4. Read that one inbox. Merge the item when it is the same underlying behavior
   or desired change; same owner alone is insufficient. If a manual capture is
   an ambiguous near-match, ask merge-or-new.
5. On merge, append the reporter's exact new wording under ## Recurrences,
   bump updated and occurrences, and reopen a fixed item as a regression.
   On new, create <YYYY-MM-DD>_<short-slug>.md using the schema below.
6. Report the resolved owner, NEW or MERGED, and file path. Do not implement a
   fix in this invocation.

## Current routing table

    concern                                            owner
    ────────────────────────────────────────────────────────────────────────
    Application crossing, two Boards, accepted stop   haipipe-application
    X0-X3 handoff/routing                              haipipe-application-workflow
    Folder, Page Face, Task Face, phase ownership      haipipe-folder
    shared Page frame or Page-local workflow           haipipe-page / haipipe-page-workflow
    PageX source binding or live Folder navigation     haipipe-plugin-evidence/ref/pagex.md
    optional run/result + supporting files surface     haipipe-plugin-runs

    Insight lane/register/partition/climb              haipipe-insight
    Insight phase order/frontier/GI gates              haipipe-insight-workflow
    I0 scope/source inventory                          haipipe-insight-meta
    I1 question/register/settlement                    haipipe-insight-question
    I2 observations/run/QA binding                     haipipe-insight-data
    I3 rates/contrasts                                 haipipe-insight-information
    I4 claim/strength/rivals                           haipipe-insight-knowledge
    I5 counsel/signed handoff                          haipipe-insight-wisdom

    Design lane/reads/grants/bets                      haipipe-design
    Design phase order/thread/round/GD gates           haipipe-design-workflow
    D0 Brief/roster/need                               haipipe-design-brief
    D1 Card/release/kill                               haipipe-design-card
    D2 Unit/realization                                haipipe-design-unit
    D3 independent verdict/prospect                    haipipe-design-verdict
    D4 Division/render/accept/emit/Principle role      haipipe-design-division
    D5 PageDown/round truth pass                       haipipe-design-pagedown
    design/ thread storage                             haipipe-plugin-design
    render projection                                  haipipe-plugin-render
    venue/channel-specific rail                        application/venue/venue-<name>

Runs presentation is not lifecycle ownership. Route lifecycle, Execute,
progress, or closure issues to the phase's Task Face; route only the optional
Run/Result surface to haipipe-plugin-runs. There is no Task plugin; X2's
`workflow/inbox/application/` is ordinary Task-Face raw material, not a plugin
surface. There is no Application haipipe-page-for-* inbox.

When several words match, choose the owner of the behavior complained about,
not merely the artifact named in the example. For example, "the SMS render
ignored its character rail" routes to venue-sms; "PageX did not show the SMS
Folder's report" routes to PageX.

## Inbox resolution

For a skill owner, locate its current SKILL.md through the installed skill
catalog and use <skill-directory>/feedback/. Do not maintain another hard-coded
path inventory here. For a venue pack, use
application/venue/venue-<name>/feedback/. The Application fallback is
haipipe-application/feedback/.

Create an inbox lazily with this README when it does not exist:

    # <owner> · Feedback Inbox

    Feedback about this owner, routed by /haipipe-application feedback.
    One file per concern: <YYYY-MM-DD>_<slug>.md. Keep fixed files as history.

## One item

    ---
    status: open | fixed
    created: YYYY-MM-DD
    updated: YYYY-MM-DD
    occurrences: 1
    context: <Folder/Board/phase, or general>
    fixed_in: ""
    regressed: ""
    ---
    <feedback in the reporter's exact words>

    ## Recurrences
    - YYYY-MM-DD: <later wording, exact>

    Fix: <added only during a later revision pass>

## List

feedback list [owner] discovers every feedback/ directory under the Application
family plus the current Folder/Page/plugin owners named above, then prints open
items newest-first and grouped by owner. With an owner, read only that inbox.
Folder location is the owner record; there is no duplicate skill field.

## Move

feedback move <file> <owner> resolves the current owner exactly as capture does,
creates the target inbox if needed, and moves the file without changing its
body. Report both old and new paths.

## Resolve later

A later revision sets status: fixed, fixed_in: <version>, and one concise Fix:
line. Never delete the history. A repeated fixed concern becomes status: open
with regressed: <date>.

# Paper Console (the enter/status procedure)

Detail reference for the door's CONSOLE step (`../SKILL.md`, "The CONSOLE step").
Distilled from the retired `haipipe-paper-enter` skill on 2026-08-05 (thin-paper phase 2).
The console derives everything from disk on every run; nothing derived is stored.

## Resolve the paper root

Look upward from the supplied path (default: the current directory) until one of these signatures is found:

```text
0-lifecycle/board.md      the only signature that matters: every paper is Board-first
0-lifecycle/              a paper mid-migration, whose board index is not written yet
<paper>.tex + sections/   a paper that reached the manuscript upgrade
```

`STATUS.md` is NOT a signature. It is retired; a folder that has only a `STATUS.md` is not a paper, it is a leftover.
If no paper root is found, report `status: blocked` and suggest `/haipipe-paper seed "<paper-path>"` or `/haipipe-paper folder "<paper-path>"`.

## Read order

Read only files that exist, in this order:

1. `0-lifecycle/board.md`: the spine; it names every page that exists.
2. The pitch S page (HIGH PRIORITY for the header): its `## Question` lead and one-line pitch become the "what this paper is about" sentence. Absent → "pitch not yet written".
3. The remaining S pages, by family folder; each page's own `state:` line is the primary signal (seed, resources, claims, venue with its PIN on the `state:` line, narrative, display pages).
4. Main and appendix section pages; derive per-section DPRC status from each page's `state:` and disk.
5. `S03-literature/probes/` and `S04-value/probes/`: per entry read its bank-binding `**state**` and whether `#### A-executor` is filled; this drives the phase strip's `probe` glyph.
6. Explicit need records: search for `NEED`, `GAP`, `TODO`, `blocked`, `missing`, `open`.
7. `displays/*/README.md` (one per unit; there is no top-level index), `sections/README.md`, then section/appendix file names and short headers only.
8. The `S-Round-*` pages (there is no stored pointer to a current round).
9. Git state: `git status --short --branch` + `git log --oneline --max-count=3`.

Before every follow-up action, re-read `board.md` and the relevant S pages, then re-derive the frontier, open needs, and gates from disk before routing. A fresh session runs `enter` again.

## The Golden Rule

```text
A stage is done only when its S page resolves on disk with real content
(not the scaffold stub), that page's own `state:` begins `✅`, and its
`## Log` contains the approval receipt for the declared gate.

There is no stored frontier to disagree with. A page's `state:` sits ON the
artifact it describes, so it cannot point at a paper it is not part of.
```

For every stage, `done` is a conjunction: the disk predicate passes, the S page's first state token is `✅`, AND its `## Log` contains a gate row with `Approved = yes`, an actor, and a date. The frontier is the FIRST stage whose conjunction is not satisfied.

Glyphs: `OK` done on disk · `ACTIVE` current frontier · `TODO` not reached · `STALE` the page's own `state:` claims done but its disk predicate fails (the page over-claims about ITSELF; trust disk) · `BLOCKED` explicit blocker. Predicate pass + a non-`✅` gate is BLOCKED at that stage: recommend `/haipipe-paper <stage> check`, never the next stage.

## Frontier predicates (per stage)

```text
seed          seed S page has question / motivations / claim-shape content
resource      resource S page has real Resource Description + Q-consumer content
              (see the resource exemption below)
claims        claims ledger non-empty, each row has a status (anchor `planned` counts;
              unmaterialized evidence is an open need, not a stage fail)
venue         venue S page exists and its `state:` names the pinned outlet
              (`✅ PINNED · <venue> <year>`)
pitch         pitch S page has a one-line pitch
narrative     narrative S page has an arc
display       the display pages map claim -> display and displays/displayNN-<slug>/ units exist
section-edit  the Main section S pages exist and sections/*.tex compile to PDF
review        audits pass and venue checks pass
```

**Resource exemption, `n/a` COUNTS AS PASS (binding).** The resource stage shipped 2026-07-14; a paper whose seed gate closed BEFORE that date passes the resource predicate by exemption, and the frontier walks straight past it to claims. The exemption is per-paper and backwards-only: a paper seeded after 2026-07-14 gets no exemption, and its absent resource page is a real frontier. (The Board may still show an exempt Resource page as not started; do not call that drift.)

## Maturity and need diagnosis

Maturity is inferred from artifacts, separately from the current layer (ladder: `paper-folder-anatomy.md`). Open needs are extracted from: unanswered resource `Q<n>` rows, claims GAP/weak rows, missing display units, sections with incomplete DPRC phases, section comments/TODOs, and the current round page's open items. Classify each with the delivery-need interface (`probe | discovery | task | display | paper-edit`) and route per the door's Delivery Need Routing. A stage whose `.tex` is newer than its `.pdf` is listed under Open Needs (a stale PDF is a defect).

Loopback diagnosis: wording/citation/stale number → section-edit; unclear figure → display; unsupported claim → claims/narrative; the claim's resource cannot carry it → resource; story weak → pitch; every demand unobtainable → seed (resource's `reseed` exit).

## Output

The door's CONSOLE step defines the exact panel (URL first, identity + frontier line, pitch lead, Open Needs, Recommended Next). Print those lines and stop; the board renders everything else. Never render a text dashboard, a stage strip, or an artifacts-read list: the board is the panel.

## Free-form routing

After the panel, route follow-up input by stage keyword (seed / resource / claims / venue / pitch / narrative / display / section-edit / round / rebuttal). If the input does not name a stage, re-derive the frontier from disk and route to it. If ambiguous, ask before acting.

## Copilot policy

Default mode is copilot. The console may automatically read files, summarize the frontier, classify input, draft or revise a stage artifact, plan section work, and suggest routes. It must ask before: costly task/PHI/full-data work; committing or downgrading a claim verdict; editing prose across many sections at once; compiling-to-submit or packaging a submission; opening or closing a revision round destructively; landing a settled claim status in the claims page.

## Session state

Record the console session at the paper/project root as `.paper-console.yaml`:

```yaml
paper_root: <path>
active_paper: <Paper-Name>
updated: <YYMMDD>
```

This file is an identity pointer, not a state cache. Never store frontier, maturity, round, gate, or open-need values here; re-derive them from the Board, S pages, probe entries, and their targets on every action.

## Return contract

Every console reply ends with the closing block defined in `../SKILL.md` ("Closing Block"). Omitting it is a protocol violation; never redefine its shape here.

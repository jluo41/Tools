# haipipe-paper-round · v0.2.0
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
REPLACE THIS PARAGRAPH. Load `haipipe-board-page-for-skill` and write the three slots it names, in its order, in plain words: ❶ what `haipipe-paper-round` is and what it is FOR, ❷ when you reach for it rather than the ONE sibling you would otherwise pick, named, ❸ where it stands, meaning the one thing to know before trusting it.

NEVER open a skill page with a question. This stub used to seed `{name} is a shipped unit: what does it still owe, and is it healthy?`, and on 260802 five pages generated from it all opened with the same rhetorical question in the same four-slot shape, because a skill page DECIDES NOTHING and so has nothing to ask.
Delete these instructions once the paragraph is written; the FIRST BLANK LINE above is the split, and everything below it is the `More details` drawer, written as labelled parts.
`Opening` is the lead section's ONE name on every page kind (JL 260731: "just one single Opening"); `Question` survives only as a legacy alias for pages written before the rename.

## Writing Style
English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram
<!-- haipipe:skill:tree:start b0852e9b13a3d7a0 paper/S10-round/haipipe-paper-round -->

**What `haipipe-paper-round` ships**: every file in the folder, with the one-line purpose each one states for itself.

```
haipipe-paper-round/
  feedback/
    README.md            9 ln  haipipe-paper-round — Feedback Inbox
  CHANGELOG.md          24 ln  haipipe-paper-round — Changelog
  SKILL.md             109 ln  Skill: haipipe-paper-round
```

<!-- haipipe:skill:tree:end -->

**How `haipipe-paper-round` is used**: REPLACE THIS CAPTION with what your figure below actually shows.

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)
Draw how this skill is actually used: the entry point, what it reads,
what it writes, and where it hands off. Delete this fence AND the
caption line above it if the tree is the whole story.
```

## Content
<!-- haipipe:skill:body:start b0852e9b13a3d7a0 paper/S10-round/haipipe-paper-round -->

**haipipe-paper-round** · `0.2.0` · last shipped 2026-07-26

- folder   `paper/S10-round/haipipe-paper-round/`
- tools    Bash, Read, Write, Edit, Grep, Glob, Skill
- summary  Rounds are one-page Board work units: `0-lifecycle/7-round/S-Round-<n>-<vYYMMDD>.md`, with discussion, queue, decisions, applied history, and closing receipt on the same face. History: ./CHANGELOG.md.

### SKILL.md



Skill: haipipe-paper-round
==========================

Rounds are paper working memory expressed in the same Board grammar as every
other lifecycle unit. One round equals one page:

```text
0-lifecycle/7-round/
├── S-Round-0-v260726.md
├── reviewer-letter-v260726.md   # optional received material beside its page
└── ...
```

There is no `latest.md`, `todo.md`, `decisions.md`, `discussion.md`, or
`applied.md`. Those would duplicate the S face and drift.

Page contract
-------------

Each `S-Round-<n>-<vYYMMDD>.md` uses the Board S-page structure:

- `state:` is `🔴`/`🟡` while work remains and `✅` only after close approval.
- `## Content` records source, purpose, accepted decisions, and applied summary.
- `## Items to Finish` is the only queue. Every item names its target.
- `## Discussion` holds raw discussion, anchored comments, and received-letter pointers.
- `## Where we are` is the current concise handoff.
- `## Log` holds dated triage/application events and the close receipt.

Triage routes
-------------

| Item | Target |
|---|---|
| claim unsupported / too strong | `0-lifecycle/1-work/S-Work-1-claims.md`, then that stage's PROBE |
| display missing / stale | DR row in `0-lifecycle/3-display/_DISPLAY_REQUEST.md` |
| paragraph placement unclear | owning `0-lifecycle/4-main/S-Main-*.md` page |
| appendix issue | owning `0-lifecycle/5-appendix/S-Appendix-*.md` page |
| wording / flow / style | owning S page, then its declared REVISE/CHECK sequence |
| citation / value evidence | owning Q-consumer, then that stage's PROBE collector route |
| reviewer response | `haipipe-paper-rebuttal` plus this S-Round page |

Subcommands
-----------

```text
/haipipe-paper round enter [paper-dir]
/haipipe-paper round new [paper-dir] [source/purpose]
/haipipe-paper round triage [paper-dir] [S-Round page]
/haipipe-paper round apply [paper-dir] [S-Round page]
/haipipe-paper round close [paper-dir] [S-Round page]
```


- 0.1 · enter
      Read all `0-lifecycle/7-round/S-Round-*.md` pages. Derive the active round from
      non-green state plus date/unit order; never read or create a stored pointer.
      Show its source, `Where we are`, and open Items. Then open the paper Board at
      that page.

- 0.2 · new
      Confirm source/purpose if missing. Allocate the next unused numeric unit and
      today's `vYYMMDD`; never overwrite an existing page. Create one S page with
      real Question/Boundary/Content/Items/Where/Discussion/Log sections and rebuild
      the Board. Received material is copied or linked beside the page only when the
      user supplied it.

- 0.3 · triage
      Read the page's Discussion and any received letters it names. Add accepted
      decisions to Content and actionable work to Items, each with one target from
      the table above. Triage does not execute the work.

- 0.4 · apply
      Route each selected Item to its owning lifecycle stage. Evidence always enters
      through that stage's Q-consumer and PROBE worker/collector chain. Record what
      changed and which item it closes in this page's `## Log`; keep unresolved work
      visible.

- 0.5 · close
      Require every Item to be checked or explicitly parked with a reason. Present
      the close summary and ask for approval. Only after approval set the first state
      token to `✅` and append the gate receipt with actor/date to `## Log`.
      No round pointer is updated.
      Routing and return
      ------------------
      ```text
      1. First token in {enter,new,triage,apply,close} -> that subcommand.
      2. Else if a non-green S-Round page exists       -> enter.
      3. Else                                          -> ask whether to create a new round.
      ```
      Return the Paper closing block from `../../haipipe-paper/SKILL.md`, deep-linked
      to the active S-Round page. Do not append a second Board status strip.
### The other files

1 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
feedback/README.md       9 ln  haipipe-paper-round — Feedback Inbox
```

<!-- haipipe:skill:body:end -->

## Aims
### P · Page-level health ruling
- P1 · Rule this skill's health.
  **Done when:** `state:` records a human judgment: stable, in flux, needs work, or parked.

## States
### P · Page-level health ruling
- ⬜ P1 · Page generated 260804 1627; nothing ruled yet.

## Log
260804 1627 · page generated from `paper/S10-round/haipipe-paper-round/` by `skillpage.py new`

<!-- haipipe:skill:log:start b0852e9b13a3d7a0 paper/S10-round/haipipe-paper-round -->

Converted from the skill's own `CHANGELOG.md`: 3 releases.

260726 · `0.2.0` · one round, one Board page
      - Replaced the retired `1-rounds/` five-file bundle and `latest.md` pointer
        with `0-lifecycle/7-round/S-Round-<n>-<vYYMMDD>.md`.
      - Moved discussion, queue, decisions, applied history, and close receipt onto
        the owning S page; routes now use the grouped Board families and stage PROBE.
      - Removed the unsupported `argument-hint` frontmatter key.
260724 · `0.1.0`
      Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.0.1; older entries below keep their original numbers).
260719 · `1.0.1`
      - WIKI RETIREMENT — the retired wiki folder's `07-paper-rounds.md` (5 referrers) absorbed here as the **Rounds contract** section; this skill is now its ONE home, and every referrer points at the section instead of the file.
        - Merged into the existing folder-contract block rather than added beside it: the no-nested-branch-level rule (`good: 1-rounds/v260621/` vs `bad: 1-rounds/<branch>/v260621/`), the file-semantics table, the round lifecycle (open → collect → extract → triage → route → record → close), the triage-targets table, and the dashboard rule (`/haipipe-paper enter` MUST surface open round items; round todos are first-class open needs).
        - The `triage` subcommand no longer restates the target list — it points at the contract's Triage targets table. Its stale `0-lifecycle/2-claims` target is corrected to `0-lifecycle/1b-claims`.
        - `Read first:` drops the wiki entry (the contract is in this file now).
      - First CHANGELOG for this skill.

<!-- haipipe:skill:log:end -->

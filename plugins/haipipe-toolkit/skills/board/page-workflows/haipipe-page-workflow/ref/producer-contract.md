# The producer contract · packet, procedure, house rules, return shape

Shared by every phase producer (`page-workflows/agents/haipipe-page-*-agent`)
and by `haipipe-page-creator-agent` when it stands in as the dispatch fallback.
Moved here 260819 from the creator agent's body, because a PRODUCER reading
another agent's file was the one relationship in the roster nobody could hold
in their head (CHECK's judge still reads its reviewer base until the judge ref is
carved out — the one standing exception, recorded, not hidden) (JL: "is this for the board or for the page? I am confused"),
and because shared law belongs in a contract, not in a worker. One copy, here,
loaded like any other ref.

**The STAND-IN rule.** An agent type not yet registered in the running session
is executed by a general-purpose stand-in whose FIRST action is reading the
phase agent's file as its identity, then this contract. The receipt's `actor:`
names the ROLE (the phase agent), and the stand-in signs nothing else.

## The assignment packet

The caller supplies this. If a required field is missing, return `blocked`
naming the field rather than guessing it.

```text
required:
  operation:   create-page | revise-opening | outline | draft | probe |
               evidence | revise | compile
  path:        the exact file path to write, inside its group folder
  id:          the page id (QA3, S-Main-2, ...)
  title:       the short title, unique on this board
  board:       the board folder path, for relative links only
optional:
  opening:     for create-page, the question or stage this page OWNS
  siblings:    for create-page, pages a reader might confuse with this one:
               id, title, and what each owns
  kind:        Q (default) | S
  state:       the starting state line; defaults to 🔴 OPEN
  owner:       defaults to JL for a decision, CC for a stage
  sources:     files this page must read and cite
  constraints: anything the human already ruled that the page must respect
  run_id:      required for draft | probe | revise
  round:       required for draft | revise
  version:     required source:render identity for draft | revise
  intent:      required run-level purpose for draft | revise
  cycle:       required: SHAPE | SURVEY for outline · LAND | EMBED for evidence ·
               WRITE for draft and revise
  probe_path:  required for evidence when an outbound card needs a separate persisted surface
  evidence_units: optional for evidence — the display units whose intake this
               phase must freeze, each `{unit, kind, source}`; the receipt
               returns the renderer that then owes the RENDER step
```

For `create-page`, `opening` and `siblings` are required. `siblings` is the
field that makes parallel writing safe. It is how your
Opening can say what is covered elsewhere without your reading elsewhere, and
it is what stops two agents from claiming the same decision.

For `revise-opening`, the existing `path` is the source of truth. The packet
must carry facts and scope, not a sentence formula. Read the whole target page;
do not read sibling pages and do not change any section other than Opening.

For `draft`, `probe`, and `revise`, `run_id`, `round`, `version`, and `intent`
are required. Treat `sources` and `constraints` as the complete raw-material
boundary. A missing source or undeclared second write routes to HOLD instead of
being guessed.

## Procedure

1. Load the page skill and read the canonical sources above. Do not skip the page spec; the
   section set is not negotiable and a section a renderer does not know renders
   nowhere.
2. For every operation except initial `create-page`, read the target Page from
   first line to last before drafting. For `create-page`, use `siblings` to
   separate ownership without reading sibling pages.
3. Read every file in `sources`. Cite only what you read. A file you could not
   read is named in your return as unread, never quietly dropped.
4. For `create-page`, draft the page in the template's section order. Earn each
   section: empty beats wrong, and a section with nothing to say is left out
   rather than padded. State the scope in Opening against `siblings` without
   creating a separate `## Boundary` section.
5. For `revise-opening`, draft from the page's actual subject and evidence.
   Treat the review questions in the page skill as diagnostic probes, not
   sentence slots. Replace only the Opening body.
6. For `outline`, `draft`, `probe`, `evidence`, `revise` or `compile`, perform
   only the authority named by the loaded phase contract. Three of the six write
   somewhere OTHER than the page body, and writing into the body instead is the
   phase boundary being crossed rather than a stylistic choice:

   ```text
   outline   ─▶ <page>/outline/<stem>-outline-v<N>.md, and NOTHING in the page
                itself. Leave `approved:` UNTICKED: it is a person's.
   probe     ─▶ <page>/evidence/probe/PP<NN>-<slug>/ with card.md,
                consumer/, executor/
                and a proof/ holding only its manifest. Never an answer.
   evidence  ─▶ evidence/bibex/ entries, a card's `state: answered` +
                `target:`, and a frozen evidence/display/ intake/. Leave
                `verified` and `read:` UNTICKED.
   ```

   Stop before the returned route begins. Record a
   non-trivial Page change in Log as part of the produced version; never write a
   later CHECK result into that Log.
7. Self-check the result against the page skill and `writing-rules.md`. Confirm
   the Opening is page-specific and that substituting another page's subject
   would make it false or nonsensical. In `revise-opening`, diff the file and
   confirm nothing outside Opening changed. This check informs the return; it
   does not award a final pass.
8. Write the target to the exact `path` given. During EVIDENCE you may also
   create the declared `probe_path`, a `bibex/` entry landed verbatim from a
   person, and per unit in `evidence_units` its `README.md`, `intake/`,
   `recipe/`, `assets/` and `preview.pdf`: render, pick and build are
   EVIDENCE's since 260819 (the LAND cycle). Never tick `accepted:`, which stays CHECK's.
9. Return the contract below. Do not rebuild, do not run the independent check,
   and do not announce
   that the board is updated: you cannot see the board.

## House rules that fail review if broken

- One sentence per line. The renderer joins lines, so a hard-wrapped sentence
  is visibly broken on the page.
- No em-dashes. Use a colon, semicolon, comma, parentheses, or a new sentence.
- English only.
- Real citations. A file path in `## Files` is a file you read, and every row
  says what that file does for this page.
- The page's own words, not coined labels. Use the board's existing vocabulary.
- ON A Q OR S PAGE, canonical Aims use stable ids (`A3.1`, `P1`) and no checkbox. Every Aim has
  exactly one matching State row with the same id and one allowed status emoji.

## Return contract

```text
actor:    <your own agent name, exactly as dispatched>
status:   ok | blocked | failed
operation: create-page | revise-opening | outline | draft | evidence | revise | compile
phase:    OUTLINE | DRAFT | EVIDENCE | REVISE | COMPILE
cycle:    SHAPE | SURVEY | LAND | EMBED | WRITE   (the pass inside the phase)
path:     <the file written, or none>
id:       <page id>
title:    <title as written>
kind:     Q | S
state:    <the state line written>
sections: <the sections the page earned>
scope:    <the sibling ids this page points at from Opening>
sources:
  read:   <files read and cited>
  unread: <files named in the packet that could not be read, or none>
open:     <what this page leaves for the human to decide, or none>
route:    OUTLINE | DRAFT | EVIDENCE | REVISE | COMPILE | CHECK | HOLD
reason:   <which phase authority was exercised and why this route follows>
reopens_promise: true | false
artifacts: JSON LIST of repo-relative paths, every file written, target
           first; [] when none
evidence:  JSON LIST of exact source locations or artifacts supporting the
           receipt
findings:  JSON LIST of remaining defects; [] when none
human_gate: {"required": <the packet's value>,
             "status": "not-required|pending|passed",
             "evidence": [<paths to the durable ticks>]}
open_questions: <consequential unknowns or none>
self_check:
  canonical_sources_loaded: yes | no
  full_target_read: yes | no | n/a
  opening_page_specific: yes | no
  outside_opening_unchanged: yes | no | n/a
needs:    <what the caller must still do: register in board.md, rebuild, review>
blocked:  <the missing field or unreadable input, when status is blocked>
```

⚠️ **Four of these fields are TYPED, and the auditor enforces the types.**
`artifacts`, `evidence` and `findings` are JSON lists, never prose strings, and
`human_gate.required` must equal the packet's on EVERY step. A step that broke
either shape was auditor-rejected live on 260819: `missing-artifacts-list` and
`human-gate-contract-mismatch` are both `src/page_lifecycle.py` finding codes.

For batch CREATE or `revise-opening`, the caller registers pages as needed, runs
one build/check, and dispatches `haipipe-board-reviewer-agent`. For RUN, the
controller snapshots the version after this receipt and follows its route; only
the reviewer may emit CLOSE.

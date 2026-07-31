# On the second run, what happens to a page a human has edited?
state: 🟡 PARTIAL · Ⓒ+Ⓑ, declared as `on_rerun:` in all 8 contracts; the checker is open in Items
owner: JL
method: find the one rule that already exists in eight versions, pick it, and put it where the writer is

## Question
Every stage will be run more than once. A venue change re-runs pitch, a returned probe answer re-runs revise, a reviewer round reopens whole families, and a re-walk after new evidence is the normal case rather than the exception. So the most consequential question about a stage is not what its first run produces. It is what its second run does to the page a human has already read, argued with, and commented on.

There is no general answer. There are eight specific ones, scattered across seven files, in five different shapes, and the count grew by two when they were re-measured against disk on 260727: page creation silently returns the existing page and writes nothing; the illuminate reference tells a re-walk to surface what is already there and ask keep-or-change rather than overwrite silently; one stage template and all ninety-five venue templates carry a hand-drawn line below which agents may not write; the gate reference says a restart re-runs a phase while READING the reviewer comments; the rebuttal skill says update checkboxes in place; section-edit tells a backfill to preserve every `> USER:` comment exactly where it was, and warns four lines later that a second backward fill would overwrite authored prose with a build product; and the shared prose reference forbids compressing, translating or replacing a `> USER:` line. Every one of them is sensible. The last of them is read by every REVISE worker, so this is not, as it was written, a set of rules that never reaches the place a phase writes. It is worse than that: the two rules that do protect a human comment name a token that appears on no live page.

The reason there are eight is structural, and it is the thing to fix first. A stage declares itself in twenty-four contract fields and NOT ONE of them is about a re-run. A behaviour with no field has nowhere to be declared, so it gets patched wherever somebody was burned, and each patch is invisible to the next author who gets burned somewhere else. `QB3c` is the only other face in this group with the same shape, and its rules are likewise scattered, across three worker contracts. So the ruling below is not really a choice of behaviour. It is a choice of what to declare, and the checker is the easy part afterwards.

What is at risk is specific and is the most expensive content on the board: a `> JL:` comment, a `state:` a human set, a `## Where we are` written after a gate, and prose somebody edited by hand. Two rules in the stage path already try to protect the first of those, and both of them name `> USER:`. On the MISQ paper there are forty-five human comment lines across seven of the forty S pages, every one of them reads `> JL:`, and `> USER:` appears on none of them. `2-phase/USAGE.md:53` is the sentence that makes that legal: it rules `> USER:` canonical and `> JL:` a tolerated alias when reading. So the protection rule and the thing it protects do not share a string, and neither the board's law nor the paper layer's rule can enforce the other.

## Boundary
- ✅ Covered here
  What a re-run does to an existing page, what is protected, and who decides.
- ↪ Covered elsewhere
  Who created the page is `QB2b`; what the phases write is `QB3a` to `QB3d`; who may pass the gate a second time is `QB3d`; ownership of regions on a shared page is `QA8`.

## Diagram
```
   🔁 THE SECOND RUN.   eight rules exist. none of them is general.
   re-measured 260727: two were missing, one had moved, four line
   numbers had drifted.

   ① create-page.py :: existing_face()        def :249 · called :290
        globs  S-<Family>-<unit>-*.md, skipping `_`/`.` folders
        found  ──▶ print the path and RETURN.  ✅ safe, and silent:
                   it neither creates nor warns nor compares
        >1     ──▶ SystemExit "more than one face resolves"

   ② ref/09-stage-illuminate.md:25
        RE-WALK: "surface what is ALREADY there and ask keep / change
        / reframe? ... Do NOT silently overwrite prior choices"
        📍 IT MOVED, AND IT WAS PROMOTED. This began as the
           2026-06-22 feedback note; that file is gone from the tree
           and the rule now sits in a ref doc that `08-stage-gate.md`
           points at twice (:35, :224). No phase worker opens it.

   ③ stages/5-section-edit/template.md:92, and again at :95
        "<!-- Yours. Agents never overwrite below this line. -->"
        📍 1 of 8 stage templates AND 95 of 95 venue templates, which
           is the AUTHORITATIVE template source when one exists.
        ⛔ and it reaches NO page. `template_divisions()` emits
           division titles plus the first `<!-- RULE -->` and nothing
           else, so all 96 copies are compiled out: `## My Notes &
           Feedback` is on 0 of the 40 live MISQ S pages and in 5
           archived flat files under `0-lifecycle/4-main/_archive/`.

   ④ ref/08-stage-gate.md:21
        restart ──▶ the named phase re-runs READING the
                    `> REVIEWER:` comments
        ✅ the closest thing to a general rule, and it is about
           REVIEWER comments only. :26 adds that a human may REOPEN
           any agent-approved gate, and that reopening resets that
           stage's ledger row.

   ⑤ haipipe-paper-rebuttal/SKILL.md:223
        "update checkbox state in place rather than regenerating"

   ⑥ stages/5-section-edit/stage.md:272
        "a second backward-fill would overwrite authored prose with
         a build product"

   ⑦ stages/5-section-edit/stage.md:301            ◀ FOUND 260727
        "preserve every existing > USER: comment EXACTLY where it was"
        📍 was :267 the same morning. FIFTH line-number drift in this
           inventory, and the argument against fixing this with another
           line-keyed rule in another file.

   ⑧ 2-phase/REF/prose-quality.md:34               ◀ FOUND 260727
        "Never compress, summarize, translate, or replace `> USER:`
         or `%% Comments: {USER}` lines. Keep them exactly as written"
        ✅ and ⑧ IS where a phase writes: every REVISE worker is
           required to read it (haipipe-paper-revise/SKILL.md:56).
        ⇒ ⑦ and ⑧ ARE the protection this face was asking for. They
          are also the two that cannot fire. See the token split.

   ── THE TOKEN SPLIT, which is why ⑦ and ⑧ protect nothing ─────────
      the two rules say      > USER:
      the live pages say     > JL:    47 lines, 8 of 40 MISQ S pages
      > USER: on any live S page                       0 occurrences
      (re-counted 260727 pm: 45 lines / 7 pages the same morning, so
       the protected thing is GROWING while the rule cannot see it)
      2-phase/USAGE.md:53    rules `> USER:` canonical and `> JL:` a
                             tolerated alias WHEN READING
      board SKILL.md:475     forbids deleting a `> JL:` line
      ref/writing-rules.md:54  "only added to ... do not erase"
      ⇒ one line, two names, and neither side can enforce the other.
        A grep for either string finds half the evidence, and the
        rule that runs on every REVISE is keyed to the half that is
        not there.

   ── what is actually at risk on an S page ─────────────────────────
      > JL: …            a human comment.  🔒 NEVER deleted (board law)
      state:             a value a human set at a gate
      ## Where we are    written after that gate, about that gate
      ## Content         prose a human edited by hand
      ## Items           checkboxes a human ticked
      ## Log             the GATE LEDGER now lives here (QA6, 260726):
                         who confirmed which gate, when, and why.
                         🔒 the one thing on the page that cannot be
                            re-derived from disk if it is overwritten.
      ⚠️ only ⑦ and ⑧ name any of these, they name the comment line
         alone, and they name it by the wrong string. `state:`,
         `## Where we are`, a ticked box and the GATE row are named
         by nothing at all, and all eight rules predate the Ledger's
         arrival on the page.

   ── QA6 made this SHARPER, not softer, on 260726 ──────────────────
      STATUS.md was retired, so a stale stored frontier can no longer
      lie about a re-run. Good. But `DRIFT` went with it and was
      replaced by `STALE`: an S page whose own `state:` OVER-CLAIMS
      about itself. That is precisely what a bad second run produces,
      and it is now the named failure with no rule to prevent it.

   ── the fork ──────────────────────────────────────────────────────
      Ⓐ REFUSE      a second run stops and reports. A human must
                    say what to reopen. Safest, and slowest.
      Ⓑ DIFF-AND-ASK  compute what would change, show it, then ask.
                    ② has been the written rule since it graduated
                    into a ref doc, and it was never built.
      Ⓒ PROTECTED REGIONS  the page declares what an agent may
                    rewrite; everything else is frozen.  ③ is this
                    idea, drawn by hand, in 96 templates, and
                    compiled out of every page.
      Ⓓ APPEND-ONLY  a re-run never edits; it writes a new revision
                    beside the old and the human merges.

   ── the case that already went wrong ──────────────────────────────
      MISQ seed: the re-run gate at S-Seed-0-seed.md:189 records
      "Approved by an AGENT STANDING IN for the human", and :169
      says so again. The re-run was the occasion; the missing rule
      was the cause.                                        → QB3d
      📍 HALF of it is now answered. The frontier half (a re-run of an
         early stage demoting a later paper) was dissolved by
         CONTRACT.md:170: with no stored frontier, re-running an early
         stage records its gate and changes nothing else. The gate
         ACTOR half is still open, and it is still an open item on
         that page (:157).

   ── WHO READS THIS, AND HOW IT FAILS ─────────────────────────────
      fields   ⛔ NONE. There is no contract field for a re-run.
      reader   ③, and mostly not through the contract. ① is code and
               executes. ⑥ and ⑦ sit in the section-edit contract,
               which a section-edit run does read. ⑧ is required
               reading for every REVISE worker. ② ③ ④ ⑤ are opened by
               nothing in the run path.
      fails    🔇 SILENT, and now in two ways. Four of the eight cannot
               fail, because nothing in the run path reads them. Of
               the two that are read AND are about a human comment,
               neither can fire: ⑦ and ⑧ are keyed to `> USER:` and
               every line they would protect says `> JL:`.
      ⇒ THIS is why eight rules exist. A behaviour with no field has
        nowhere to be declared, so it gets patched wherever somebody
        was burned, and each patch is invisible to the next author.
      to bind  it needs a FIELD before it can need a checker. Whichever
               way the fork below is ruled, the answer lands as one
               declaration: a page-level protected region, or a
               stage-level `on_rerun:`. Ⓒ is the only option that puts
               it on the PAGE, where a human is already looking.
```

## Content
### Why the silence in `create-page.py` is not the answer
Page creation is correctly idempotent: it finds the existing face and returns it. That is exactly right for creation and says nothing about the run. The phases execute afterwards and write into whatever `create-page.py` handed back, so the safe half of the path is the half that was never in danger, and the dangerous half has no rule at all.

### Eight rules is worse than one rule or none
Each of the eight is a local patch on the place where somebody was burned. That is how they should have started. The problem now is that a worker reading its own contract sees at most two of them, so the protection a page gets depends on which stage happens to be running rather than on what the page contains. Section-edit tells a backfill to preserve comments and warns against a second backfill; seed says nothing at all; and the one general-sounding rule, ④, is about reviewer comments during a restart, which is a narrower case than it sounds.

The template guard is the sharpest instance, because it is the most widely written and the least effective. Ninety-six template files carry it, one stage template and every venue template, and `create-page.py` compiles none of them onto a page: `template_divisions()` emits division titles and the first `<!-- RULE -->` and drops the rest. So the guard is stated ninety-six times and reaches zero live pages.

### The board has the rule this needs, and it is written in a different alphabet
A `> JL:` line is never deleted. That is a standing law of the board (`board SKILL.md:475`, `ref/writing-rules.md:54`), it applies to every page regardless of who is writing, and it is the exact shape the stage path is missing. The stage path has already tried to import it twice, at `5-section-edit/stage.md:267` and `2-phase/REF/prose-quality.md:34`, and both times wrote `> USER:` instead, which is the canonical actor id for the paper phase layer (`2-phase/USAGE.md:53`). Forty-five human comment lines on the MISQ pages say `> JL:` and none says `> USER:`, so the imported rule guards a string that is not there. Whatever is ruled here has to close that gap first, because a protection scheme that cannot name what it protects is not a second scheme, it is a null one.

## Items to Finish
- [x] 🔍 Re-measure the scattered rules against disk
      Done 260727. Eight rules, not six: `stages/5-section-edit/stage.md:267` and `2-phase/REF/prose-quality.md:34` were missing from the inventory, and both are the human-comment protection this face was asking for. The 2026-06-22 feedback note no longer exists anywhere in the tree; its rule was promoted into `ref/09-stage-illuminate.md:25`. Four of the six cited line numbers had drifted.
- [x] 🧠 Rule the second run, and where it is DECLARED
      Ruled 260727: **Ⓒ protected regions, with Ⓑ as the behaviour for everything outside them**, declared as `on_rerun: diff-and-ask` in all eight `stage.md` contracts and specified once in `stages/CONTRACT.md` under "The second run". Both halves of the two-decision shape are answered: the behaviour is Ⓑ, which had been the written rule in `ref/09-stage-illuminate.md:25` and never built, and the declaration is a stage field rather than a page marker, because the page-marker version already exists in 96 files and reaches 0 pages.
      Ⓐ was rejected: it would stop the venue-change cascade from ever running unattended, which is most of the value of the lifecycle. Ⓓ was rejected: it doubles the page count.
- [x] 🔧 Make the preservation rules name the token pages use
      Done 260727. Both now match the LANE SHAPE `> <ACTOR>:` rather than one id: `2-phase/REF/prose-quality.md`, which every REVISE worker must read, and `5-section-edit/stage.md`'s backfill step. Neither of the 47 `> JL:` lines was touched, which was the point: rewriting them to `> USER:` would have made one name true everywhere by performing the single edit `board SKILL.md:475` exists to forbid.
- [x] 📐 Name what an S page protects beyond comments
      Done 260727, in the ruling itself. Five things are named and protected, not one: any `> <ACTOR>:` lane, `state:`, `## Where we are`, a ticked box in `## Items to Finish`, and a GATE row in `## Log`. The last is called out as the only item on the page that cannot be re-derived from disk if a run overwrites it (`ref/08-stage-gate.md:205`).
- [x] 🔧 Fix or delete the guard that reaches no page
      Resolved 260727 as NEITHER, which the item did not offer. Protection now keys to constructs that are already on every page, so no marker has to survive template compilation for the rule to hold, and the hand-drawn line in 96 files is superseded rather than implemented or deleted. Deleting it from 96 files is cosmetic and can happen whenever those files are next touched; carrying it onto pages would have added a marker whose only job the ruling already does.
- [ ] 🔧 Teach `create-page.py` and the checker to enforce it
      The ruling is declared and specified; nothing verifies it. Two mechanical pieces: a re-run must diff before writing, and one assertion that no run has changed a protected construct. `on_rerun:` now exists in all eight contracts, so the checker has a field to read, which is what it never had.
- [ ] 🔍 Assert every green S page carries a human GATE row
      `haipipe-paper-enter/SKILL.md:259` already rules that `✅` with no approval receipt is STALE, and nothing asserts it. The evidence is on disk: 40 S pages, each with a `state:` line and a `## Log`. `S-Seed-0-seed.md:189` is the row this catches, because its actor is an agent, and a bad second run is exactly how a green page acquires one.
- [ ] 🔧 Retire or generalise the local rules the ruling replaces
      Seven files hold the eight: `create-page.py`, `ref/09-stage-illuminate.md`, `stages/5-section-edit/template.md` (plus 95 venue copies), `ref/08-stage-gate.md`, `haipipe-paper-rebuttal/SKILL.md`, `stages/5-section-edit/stage.md` (two of them), `2-phase/REF/prose-quality.md`. A local rule that survives the ruling is a local rule that will contradict it later.
- [ ] 🧪 Re-run one stage on the page with 19 comments
      `0-lifecycle/4-main/S-Main-2-introduction.md` carries 19 `> JL:` lines, the most on the paper. Re-run section-edit on it and read what survived. Nobody knows today, which is the finding.

## Where we are
Ruled and declared 260727. `on_rerun: diff-and-ask` is in all eight `stage.md` contracts, the rule is specified once in `stages/CONTRACT.md` under "The second run", and the two preservation rules now match the lane shape `> <ACTOR>:` instead of the one id that was never on a page.

```
 BEFORE                              AFTER
 8 rules · 7 files · 5 shapes        1 field · 8 contracts · 1 spec
 0 contract fields for a re-run      on_rerun:, and the checker has
                                       something to read for the first time
 protection keyed to `> USER:`       keyed to `> <ACTOR>:`
   0 of 47 live comment lines          47 of 47
 1 construct named (the comment)     5 named, incl. the GATE row
```

⚠️ Declared is not enforced, and that distinction is the whole remaining risk. Nothing yet computes a diff before writing, and nothing asserts that a run left the five protected constructs alone. Until that lands, this ruling is a rule an agent is asked to obey rather than a step something performs, which is the same shape `QC5` names for its own missing generator. It is the open item above, and by this board's own close rule an unwritten checker does not hold the ruling open.

One re-run has already produced a real defect: a MISQ seed gate recorded as passed by an agent standing in for the human. The rule now forbids it, and nothing yet catches it. That half is `QB3d`'s, and the specific row is still an open item on `S-Seed-0-seed.md:157`.

## Files
- `haipipe-paper-stage/create-page.py`
  `existing_face()` at line 249, called at 290: get-or-create at the page level, silent on everything after. `template_divisions()` at 89 is what drops the template's guard comment.
- `stages/5-section-edit/stage.md`
  Line 267 preserves `> USER:` comments; line 272 forbids a second backward fill. The two closest things to the rule this face wants, four lines apart, in one stage's contract.
- `2-phase/REF/prose-quality.md`
  Line 34, "never compress, summarize, translate, or replace `> USER:`" lines. Required reading for every REVISE worker, and the only one of the eight that runs on every revise.
- `2-phase/USAGE.md`
  Line 53, the ruling that makes `> USER:` canonical and `> JL:` a tolerated alias when reading. The sentence the token split rests on.
- `stages/5-section-edit/template.md`
  Line 92 and again at 95, the hand-drawn protected region; the same line is in all 95 venue templates, and none of the 96 reaches a page.
- `1-lifecycle/ref/08-stage-gate.md`
  Line 21, restart semantics, scoped to `> REVIEWER:` comments; line 26, a human may reopen an agent-approved gate; line 205, the Gate Ledger's home on the page.
- `1-lifecycle/ref/09-stage-illuminate.md`
  Line 25, the RE-WALK step: surface what is there, ask keep or change, do not silently overwrite. Where the retired 2026-06-22 feedback note's rule graduated to.
- `0-lifecycle/0-seed/S-Seed-0-seed.md`
  Line 189, the gate row that names an agent as the approving actor, and line 157, the item asking JL to confirm or reject it.

## Law
A stage declares what its second run does, in one field, `on_rerun:`, whose only currently legal value is `diff-and-ask`. The absence of that field is what produced eight scattered patches in seven files, so the field is the ruling and the behaviour is the easy half.

A re-run does two things, and both are binding.

- 🔒 PROTECTED · a re-run may not rewrite these at all
  Any `> <ACTOR>:` comment lane, `state:`, `## Where we are`, a ticked box in `## Items to Finish`, and a GATE row in `## Log`. The GATE row is the one thing on the page that cannot be re-derived from disk if it is overwritten.
- 🔁 EVERYTHING ELSE · diff and ask
  Compute what would change, show it, then ask keep or change or reframe. Never overwrite silently.

Protection keys to the LANE SHAPE, `> <ACTOR>:`, and never to one actor id. This is the operative half, because both previous attempts failed on exactly that point: they guarded `> USER:`, and every human comment line on the paper says `> JL:`. Matching the shape closes the gap without editing a single human comment line, which is the one edit the board's own law forbids.

A local re-run rule that survives this ruling will contradict it later, so it is removed rather than left. The hand-drawn `<!-- Agents never overwrite below this line -->` is superseded rather than implemented: protection now names constructs that are already on the page, so no marker has to survive template compilation for the rule to hold.

## Discussion
> CC 260726: I would rule Ⓒ, with Ⓑ as its behaviour. Protected regions is the only option that scales to eleven display pages and forty section pages, because it puts the rule on the PAGE, where a human can see it, rather than in eight worker contracts where only the worker sees it. Ⓐ is safe and would stop the venue-change cascade from ever running unattended, which is most of the value of the lifecycle. Ⓓ doubles the page count.
> The reason to decide it soon rather than well: every one of the six local rules is currently correct, and each new stage adds a seventh.
> CC 260727: one judgment is open that the fork does not contain, and it blocks every option in the fork. The token fix has two shapes and they cost differently. Teaching both rules to match `> USER:` or `> JL:` is two string edits and leaves two names for one thing, which is how `output:` and `generated:` ended up naming one law on `QB2d`. Rewriting the 45 `> JL:` lines on the MISQ pages to `> USER:` makes one name true everywhere, and it does so by editing human comment lines, which is the single edit `board SKILL.md:475` exists to forbid. I recommend the first, and would spend the tidiness on the checker instead: one assertion that reports either token. The cost of the first is that the vocabulary stays double, so every future check has to remember both.

## Log
260726 · Created in the QB restructure. The question had no face because it is not about what a stage IS, and the old group was organised around what things are. Searching the paper skill for re-run handling turned up six rules in five shapes, which is the finding rather than the background.
260726 · Aligned against `QA6`, which had moved well past this group. `STATUS.md` is retired, so a stale stored frontier can no longer lie about a re-run; `DRIFT` went with it and was replaced by `STALE`, an S page whose own `state:` over-claims, which is exactly what a bad second run produces. The Gate Ledger also moved onto the page, adding the one thing on it that cannot be re-derived.

260726 · Opening reframed after the reader pass. The six scattered rules are not six bad decisions; they are the symptom of a behaviour with no contract field, and the ruling below is therefore a choice of what to DECLARE, not only of how to behave.

260727 · Re-measured every claim against disk, and the count was wrong in both directions. Two rules were missing: `stages/5-section-edit/stage.md:267` tells a backfill to preserve every `> USER:` comment exactly where it was, and `2-phase/REF/prose-quality.md:34` forbids compressing, translating or replacing one. Those two ARE the protection this face has been asking for, and the second is required reading for every REVISE worker, so "none of them is where the phase workers actually write" was false. What is actually broken is narrower and worse: both rules name `> USER:`, all 45 human comment lines across 7 of the 40 MISQ S pages read `> JL:`, `> USER:` appears on none of them, and `2-phase/USAGE.md:53` makes the mismatch legal by calling `> JL:` a tolerated alias. Second correction: the 2026-06-22 feedback note does not exist anywhere in the tree, and its rule WAS promoted, into `ref/09-stage-illuminate.md:25`, so "never promoted to a contract or a worker" was false too. Third: the hand-drawn guard is in all 95 venue templates as well as 1 of 8 stage templates, and `create-page.py :: template_divisions()` compiles all 96 copies out, which is why `## My Notes & Feedback` sits on 0 of the 40 live S pages and in 5 archived flat files. Four cited line numbers had drifted (template 89 to 92, gate 19 to 21, section-edit 270 to 272, and the missing note). Verified unchanged: no re-run field in `stages/CONTRACT.md`, the Gate Ledger's move onto each S page's `## Log`, and `STATUS.md`'s retirement with `DRIFT` replaced by `STALE`. Also verified that half the MISQ seed defect is now answered: `CONTRACT.md:170` dissolves the frontier half, and only the gate-actor half is still live.

260727 pm · RULED, on JL's "just do as what you want first" after asking for the explanation. Ⓒ protected regions with Ⓑ diff-and-ask for everything outside them, declared as `on_rerun:` in all eight `stage.md` contracts and specified once in `stages/CONTRACT.md`. The recommendation had stood in Discussion since 260726 and the two rejections still hold: Ⓐ would stop the venue-change cascade from running unattended, which is most of the value of the lifecycle, and Ⓓ doubles the page count. One thing changed from that recommendation: it wanted the declaration ON the page, and the page-marker version already exists in 96 files and reaches 0 pages, so the declaration went into the field instead and the PROTECTION was keyed to constructs the page already carries. That gets Ⓒ's benefit, a rule about what the page holds rather than about which worker is running, without depending on a marker that template compilation drops. The token split was closed by matching the lane shape rather than by rewriting 47 human comment lines, which would have fixed one law by breaking a stricter one.
260727 pm · JL asked for a fuller explanation of this face, so every load-bearing count was re-verified a second time the same day, and two had already moved. The `> JL:` lines went 45 to 47 and the pages carrying them 7 to 8, so the thing the rule cannot see is growing faster than the inventory describing it. And rule ⑦ moved from `stage.md:267` to `:301`, the fifth line-number drift recorded here. That second one is an argument about the ANSWER, not only the bookkeeping: an inventory keyed to file-and-line cannot stay true, so whatever is ruled must not be a sixth line-keyed rule in a seventh file. It supports Ⓒ, which puts the declaration on the page. Verified unchanged: `> USER:` on 0 of the 40 live S pages, `prose-quality.md:34` word for word, the guard in 96 template files and on 0 live pages, and `stages/CONTRACT.md` still carrying no re-run field (its one hit at :170 is prose about the frontier, not a field).
260727 · Items rebuilt as a queue. Deleted "Decide whether a re-run may change `state:`": it is folded into "Name what an S page protects beyond comments", which names `state:` outright, and `ref/08-stage-gate.md:26` already rules that a human may reopen an agent-approved gate and that reopening resets the ledger row, so what was left of it was the central ruling's option Ⓐ under another name. Two items added that name something already on disk: the token repair, and one assertion that every green page carries a human GATE row, which `haipipe-paper-enter/SKILL.md:259` already declares as the STALE condition and nothing checks.

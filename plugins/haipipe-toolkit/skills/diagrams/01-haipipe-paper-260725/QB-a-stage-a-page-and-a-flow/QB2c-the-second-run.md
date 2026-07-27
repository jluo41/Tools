# On the second run, what happens to a page a human has edited?
state: 🔴 OPEN
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

   ⑦ stages/5-section-edit/stage.md:267            ◀ FOUND 260727
        "preserve every existing > USER: comment EXACTLY where it was"

   ⑧ 2-phase/REF/prose-quality.md:34               ◀ FOUND 260727
        "Never compress, summarize, translate, or replace `> USER:`
         or `%% Comments: {USER}` lines. Keep them exactly as written"
        ✅ and ⑧ IS where a phase writes: every REVISE worker is
           required to read it (haipipe-paper-revise/SKILL.md:56).
        ⇒ ⑦ and ⑧ ARE the protection this face was asking for. They
          are also the two that cannot fire. See the token split.

   ── THE TOKEN SPLIT, which is why ⑦ and ⑧ protect nothing ─────────
      the two rules say      > USER:
      the live pages say     > JL:    45 lines, 7 of 40 MISQ S pages
      > USER: on any live S page                       0 occurrences
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
- [ ] 🧠 Rule the second run, and where it is DECLARED
      Ⓐ refuse and report · Ⓑ diff-and-ask · Ⓒ protected regions declared on the page · Ⓓ append a revision beside the old. This is two decisions, not one, because `stages/CONTRACT.md` has no re-run field: pick the behaviour, then pick whether it is declared as a page-level protected region (Ⓒ is the only option that puts it where a human is already looking) or as a stage-level `on_rerun:` in each `stage.md`. Ⓑ has been the written rule since it graduated into `ref/09-stage-illuminate.md:25` and has never been built.
- [ ] 🔧 Make the preservation rules name the token pages use
      `stages/5-section-edit/stage.md:267` and `2-phase/REF/prose-quality.md:34` both protect `> USER:`. All 45 human comment lines across 7 of the 40 MISQ S pages read `> JL:`, and `> USER:` appears on none of them. `2-phase/USAGE.md:53` makes `> JL:` a tolerated alias when reading, so the mismatch is legal and silent, and `prose-quality.md` is required reading for every REVISE worker (`haipipe-paper-revise/SKILL.md:56`), which means the rule that runs most often is the one keyed to the absent string.
- [ ] 📐 Name what an S page protects beyond comments
      The two rules above cover the comment line and nothing else. `state:`, `## Where we are`, ticked boxes in `## Items to Finish`, and the GATE rows in `## Log` are named by no rule in the stage path. The Ledger rows (`ref/08-stage-gate.md:205`) are the one item on the page that cannot be re-derived from disk if a run overwrites them.
- [ ] 🔧 Fix or delete the guard that reaches no page
      `stages/5-section-edit/template.md:92` and its 95 venue copies say "Agents never overwrite below this line", and `create-page.py :: template_divisions()` emits only division titles plus the first `<!-- RULE -->`, so all 96 copies are compiled out. `## My Notes & Feedback` sits on 0 of the 40 live MISQ S pages and in 5 archived flat files under `0-lifecycle/4-main/_archive/`. Either the creator carries the marker onto the page or the line is deleted from 96 files.
- [ ] 🔍 Assert every green S page carries a human GATE row
      `haipipe-paper-enter/SKILL.md:259` already rules that `✅` with no approval receipt is STALE, and nothing asserts it. The evidence is on disk: 40 S pages, each with a `state:` line and a `## Log`. `S-Seed-0-seed.md:189` is the row this catches, because its actor is an agent, and a bad second run is exactly how a green page acquires one.
- [ ] 🔧 Retire or generalise the local rules the ruling replaces
      Seven files hold the eight: `create-page.py`, `ref/09-stage-illuminate.md`, `stages/5-section-edit/template.md` (plus 95 venue copies), `ref/08-stage-gate.md`, `haipipe-paper-rebuttal/SKILL.md`, `stages/5-section-edit/stage.md` (two of them), `2-phase/REF/prose-quality.md`. A local rule that survives the ruling is a local rule that will contradict it later.
- [ ] 🧪 Re-run one stage on the page with 19 comments
      `0-lifecycle/4-main/S-Main-2-introduction.md` carries 19 `> JL:` lines, the most on the paper. Re-run section-edit on it and read what survived. Nobody knows today, which is the finding.

## Where we are
Nothing is ruled and the risk is live. Every stage can be re-run today, re-runs are routine rather than exceptional, and the protection a page receives depends on which stage is running rather than on what the page holds.

One re-run has already produced a real defect: a MISQ seed gate recorded as passed by an agent standing in for the human. That is `QB3d`'s failure to prevent, and this is the occasion that produced it.

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
_None yet. This face is 🔴, and its first item is the ruling that would produce one._

## Discussion
> CC 260726: I would rule Ⓒ, with Ⓑ as its behaviour. Protected regions is the only option that scales to eleven display pages and forty section pages, because it puts the rule on the PAGE, where a human can see it, rather than in eight worker contracts where only the worker sees it. Ⓐ is safe and would stop the venue-change cascade from ever running unattended, which is most of the value of the lifecycle. Ⓓ doubles the page count.
> The reason to decide it soon rather than well: every one of the six local rules is currently correct, and each new stage adds a seventh.
> CC 260727: one judgment is open that the fork does not contain, and it blocks every option in the fork. The token fix has two shapes and they cost differently. Teaching both rules to match `> USER:` or `> JL:` is two string edits and leaves two names for one thing, which is how `output:` and `generated:` ended up naming one law on `QB2d`. Rewriting the 45 `> JL:` lines on the MISQ pages to `> USER:` makes one name true everywhere, and it does so by editing human comment lines, which is the single edit `board SKILL.md:475` exists to forbid. I recommend the first, and would spend the tidiness on the checker instead: one assertion that reports either token. The cost of the first is that the vocabulary stays double, so every future check has to remember both.

## Log
260726 · Created in the QB restructure. The question had no face because it is not about what a stage IS, and the old group was organised around what things are. Searching the paper skill for re-run handling turned up six rules in five shapes, which is the finding rather than the background.
260726 · Aligned against `QA6`, which had moved well past this group. `STATUS.md` is retired, so a stale stored frontier can no longer lie about a re-run; `DRIFT` went with it and was replaced by `STALE`, an S page whose own `state:` over-claims, which is exactly what a bad second run produces. The Gate Ledger also moved onto the page, adding the one thing on it that cannot be re-derived.

260726 · Opening reframed after the reader pass. The six scattered rules are not six bad decisions; they are the symptom of a behaviour with no contract field, and the ruling below is therefore a choice of what to DECLARE, not only of how to behave.

260727 · Re-measured every claim against disk, and the count was wrong in both directions. Two rules were missing: `stages/5-section-edit/stage.md:267` tells a backfill to preserve every `> USER:` comment exactly where it was, and `2-phase/REF/prose-quality.md:34` forbids compressing, translating or replacing one. Those two ARE the protection this face has been asking for, and the second is required reading for every REVISE worker, so "none of them is where the phase workers actually write" was false. What is actually broken is narrower and worse: both rules name `> USER:`, all 45 human comment lines across 7 of the 40 MISQ S pages read `> JL:`, `> USER:` appears on none of them, and `2-phase/USAGE.md:53` makes the mismatch legal by calling `> JL:` a tolerated alias. Second correction: the 2026-06-22 feedback note does not exist anywhere in the tree, and its rule WAS promoted, into `ref/09-stage-illuminate.md:25`, so "never promoted to a contract or a worker" was false too. Third: the hand-drawn guard is in all 95 venue templates as well as 1 of 8 stage templates, and `create-page.py :: template_divisions()` compiles all 96 copies out, which is why `## My Notes & Feedback` sits on 0 of the 40 live S pages and in 5 archived flat files. Four cited line numbers had drifted (template 89 to 92, gate 19 to 21, section-edit 270 to 272, and the missing note). Verified unchanged: no re-run field in `stages/CONTRACT.md`, the Gate Ledger's move onto each S page's `## Log`, and `STATUS.md`'s retirement with `DRIFT` replaced by `STALE`. Also verified that half the MISQ seed defect is now answered: `CONTRACT.md:170` dissolves the frontier half, and only the gate-actor half is still live.

260727 · Items rebuilt as a queue. Deleted "Decide whether a re-run may change `state:`": it is folded into "Name what an S page protects beyond comments", which names `state:` outright, and `ref/08-stage-gate.md:26` already rules that a human may reopen an agent-approved gate and that reopening resets the ledger row, so what was left of it was the central ruling's option Ⓐ under another name. Two items added that name something already on disk: the token repair, and one assertion that every green page carries a human GATE row, which `haipipe-paper-enter/SKILL.md:259` already declares as the STALE condition and nothing checks.

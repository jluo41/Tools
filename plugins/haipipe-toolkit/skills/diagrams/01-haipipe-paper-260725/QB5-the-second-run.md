# On the second run, what happens to a page a human has edited?
state: 🔴 OPEN
owner: JL
method: find the one rule that already exists in six places, pick it, and put it where the writer is

## Question
Every stage will be run more than once. A venue change re-runs pitch, a returned probe answer re-runs revise, a reviewer round reopens whole families, and a re-walk after new evidence is the normal case rather than the exception. So the most consequential question about a stage is not what its first run produces. It is what its second run does to the page a human has already read, argued with, and commented on.

There is no general answer. There are six specific ones, scattered across six files, in five different shapes: page creation silently returns the existing page and writes nothing; a feedback note says re-walks should diff-and-ask; one template out of eight carries a hand-drawn line below which agents may not write; the gate reference says a restart re-runs a phase while READING the reviewer comments; the rebuttal skill says update checkboxes in place; and section-edit warns that a second backward fill would overwrite authored prose with a build product. Every one of them is sensible. None of them is general, and none is where the phase workers actually write.

What is at risk is specific and is the most expensive content on the board: a `> JL:` comment, a `state:` a human set, a `## Where we are` written after a gate, and prose somebody edited by hand. The board's standing rule is that a `> JL:` line is never deleted. Nothing in the stage path knows that rule exists.

## Boundary
- ✅ Covered here
  What a re-run does to an existing page, what is protected, and who decides.
- ↪ Covered elsewhere
  Who created the page is `QB4`; what the phases write is `QB8` to `QB11`; who may pass the gate a second time is `QB11`; ownership of regions on a shared page is `QA8`.

## Diagram
```
   🔁 THE SECOND RUN.   six rules exist. none of them is general.

   ① create-page.py :: existing_face()
        globs  S-<Family>-<unit>-*.md
        found  ──▶ print the path and RETURN.  ✅ safe, and silent:
                   it neither creates nor warns nor compares
        >1     ──▶ SystemExit "more than one face resolves"

   ② feedback/2026-06-22_…every-stage-must-illuminate….md:35
        "for re-walks, diff-and-ask rather than overwrite"
        ⚠️ a feedback note. Never promoted to a contract or a worker.

   ③ stages/5-section-edit/template.md:89
        "<!-- Yours. Agents never overwrite below this line. -->"
        ⚠️ ONE template out of eight, and it guards a Setext-era flat
           file, not an S page.

   ④ ref/08-stage-gate.md:19
        restart ──▶ the named phase re-runs READING the
                    `> REVIEWER:` comments
        ✅ the closest thing to a general rule, and it is about
           REVIEWER comments only.

   ⑤ haipipe-paper-rebuttal/SKILL.md:223
        "update checkbox state IN PLACE rather than regenerating"

   ⑥ stages/5-section-edit/stage.md:270
        "a second backward-fill would overwrite authored prose with
         a build product"

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
      ⚠️ not one of the six rules above names ANY of these, because
         five of them predate the S page and all six predate the
         Ledger's arrival.

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
                    ② already proposed this and it was never built.
      Ⓒ PROTECTED REGIONS  the page declares what an agent may
                    rewrite; everything else is frozen.  ③ is this
                    idea, drawn by hand, in one template.
      Ⓓ APPEND-ONLY  a re-run never edits; it writes a new revision
                    beside the old and the human merges.

   ── the case that already went wrong ──────────────────────────────
      MISQ seed: a re-run gate was recorded as PASSED by an agent
      standing in for the human. The re-run was the occasion; the
      missing rule was the cause.                           → QB11
```

## Content
### Why the silence in `create-page.py` is not the answer
Page creation is correctly idempotent: it finds the existing face and returns it. That is exactly right for creation and says nothing about the run. The phases execute afterwards and write into whatever `create-page.py` handed back, so the safe half of the path is the half that was never in danger, and the dangerous half has no rule at all.

### Six rules is worse than one rule or none
Each of the six is a local patch on the place where somebody was burned. That is how they should have started. The problem now is that a worker reading its own contract sees at most one of them, so the protection a page gets depends on which stage happens to be running rather than on what the page contains. Section-edit protects a hand-written region; seed protects nothing; and the one general-sounding rule, ④, is about reviewer comments during a restart, which is a narrower case than it sounds.

### The board already has the rule this needs
A `> JL:` line is never deleted. That is a standing law of the board, it applies to every page regardless of who is writing, and it is the exact shape the stage path is missing. Whatever is ruled here should extend that rule rather than invent a second one, because two protection schemes on one file is how the six got here.

## Items to Finish
- [ ] 🧠 Rule what a second run does
      Ⓐ refuse and report · Ⓑ diff-and-ask · Ⓒ protected regions declared on the page · Ⓓ append a revision beside the old. Ⓑ was proposed in a feedback note on 2026-06-22 and never built.
- [ ] 📐 Name what is protected on an S page
      At minimum `> JL:` lines, `state:`, `## Where we are`, and ticked Items. Say it once, for every stage, not per template.
- [ ] 🔧 Retire or generalise the five local rules
      Whichever way this is ruled, the six become one. A local rule that survives the ruling is a local rule that will contradict it later.
- [ ] 🔎 Decide whether a re-run may change `state:`
      A stage that re-runs after a gate has passed is proposing to reopen it. Whether it may set the value or only ask is unruled, and `QB11` is where that gate lives.
- [ ] 🧪 Re-run one stage on a page carrying a `> JL:` comment
      The acceptance test. Today nobody knows what happens, which is the finding.

## Where we are
Nothing is ruled and the risk is live. Every stage can be re-run today, re-runs are routine rather than exceptional, and the protection a page receives depends on which stage is running rather than on what the page holds.

One re-run has already produced a real defect: a MISQ seed gate recorded as passed by an agent standing in for the human. That is `QB11`'s failure to prevent, and this is the occasion that produced it.

## Files
- `haipipe-paper-stage/create-page.py`
  `existing_face()`: get-or-create at the page level, silent on everything after.
- `stages/5-section-edit/template.md`
  Line 89, the hand-drawn protected region; the only one of its kind.
- `1-lifecycle/ref/08-stage-gate.md`
  Line 19, restart semantics, scoped to `> REVIEWER:` comments.
- `haipipe-paper/feedback/2026-06-22_every-stage-must-illuminate-and-elicit-taste.md`
  Line 35, diff-and-ask, proposed and never promoted.

## Law
_None yet. This face is 🔴, and its first item is the ruling that would produce one._

## Discussion
> CC 260726: I would rule Ⓒ, with Ⓑ as its behaviour. Protected regions is the only option that scales to eleven display pages and forty section pages, because it puts the rule on the PAGE, where a human can see it, rather than in eight worker contracts where only the worker sees it. Ⓐ is safe and would stop the venue-change cascade from ever running unattended, which is most of the value of the lifecycle. Ⓓ doubles the page count.
> The reason to decide it soon rather than well: every one of the six local rules is currently correct, and each new stage adds a seventh.

## Log
260726 · Created in the QB restructure. The question had no face because it is not about what a stage IS, and the old group was organised around what things are. Searching the paper skill for re-run handling turned up six rules in five shapes, which is the finding rather than the background.
260726 · Aligned against `QA6`, which had moved well past this group. `STATUS.md` is retired, so a stale stored frontier can no longer lie about a re-run; `DRIFT` went with it and was replaced by `STALE`, an S page whose own `state:` over-claims, which is exactly what a bad second run produces. The Gate Ledger also moved onto the page, adding the one thing on it that cannot be re-derived.

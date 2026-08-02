# DRAFT · What it adds to the page, and what it refuses to write
state: 🟡 PARTIAL
owner: JL
method: write everything the stage can source, mark everything it cannot, and answer nothing

## Opening
DRAFT is the first phase of the flow, and it runs on a page it did not shape. The shell, the `## Content` divisions and the job line under each were already in place before it was called, and what a line inside a division may look like is the sentence layer's rule, not its own. `QC3` owns that object. This face owns the narrow, sharp thing DRAFT contributes on top of it.

That contribution is prose plus a marked hole. `\citep{key}` only when the key already greps in the `.bib`; `\cite{TOADD} [Q-Section-4]` when it does not; `{VAL:? what is owed} [Q-Section-4]` for a number; and one `- [ ] 🔎 Q-<Stage>-<n>` record in `## Items to Finish` for each. DRAFT is where a paper is most likely to acquire a lie, because a drafter that stops at every gap produces nothing while a drafter that fills them produces prose that reads finished and rests on a number nobody checked. The grammar exists to make the honest path the cheap one.

What is unresolved is the two cases the grammar cannot see. A `\cite{TOADD}` written with no bracket beside it is worse than an empty sentence: a hole no question will ever fill, and nothing executable detects one, though three separate files say in prose that it is a defect. And a gap the drafter cannot even phrase as an answerable question has no marker in the prose at all, which makes it the case most likely to become a quiet assertion. There is one sanctioned exit for it, and its location is the tell: the words "explicitly declined in the S page's `## Log`" appear only inside the text of a prompt the drafter hands to its review subagent, and in no rule the drafter itself is bound by.

Scope: This page covers What a draft must satisfy, which contract owns which region of the page, what DRAFT refuses to write, and the marked hole it writes instead. Neighbouring pages cover The board's shell and the ownership line inside a shared page are `QA8`; what a template IS is `QC3a`; the sentence formats are `QC5` to `QB12d` and their delivery is `QB11a`/`QB11b`; where the raised question goes next is `QC4b`; who discharges the placeholder is `QC4c`.

## Diagram
```
   ✍️ DRAFT DOES NOT CREATE A FILE. It fills regions of one that exists.

   ── THE PAGE THIS WRITES INTO ─────────────────────────────────────
      ↪ NOT HERE. One markdown file, four regions, four owners, and
        the reason they never collide, is `QC3`. DRAFT writes in two
        of those regions and must not touch the machine-managed one.
          ## Content            the divisions, already placed
          ## Items to Finish    one `- [ ] 🔎 Q-<Stage>-<n>` per hole
        Everything below is what DRAFT ITSELF adds.

   ── WHAT DRAFT ITSELF ADDS, AND WHAT IT REFUSES ──────────────────
      MAY WRITE   real prose, one sentence per source line
                  \citep{key}  ONLY if the key already greps in .bib
                  a Q-consumer record in ## Items to Finish

      MUST REFUSE a bibtex entry       the .bib is HUMAN-ONLY 🔒
                  a number it did not read from a landed answer
                  a citation key it has not verified
                  an answer to its own question
                  ▼ each becomes a MARKED HOLE instead
                    \cite{TOADD}          [Q-Section-4]
                    {VAL:? what is owed}  [Q-Section-4]
                    ╰─ the marker ─╯      ╰─ who owes it ─╯
                    side by side. NEVER fused.

      🔍 THREE finders report holes. TWO of them hold no pen:
         draft-citation  READ-ONLY · "It does NOT WRITE, anywhere"
         draft-values    READ-ONLY · same line, same words
         draft-display   ⚠️ NOT read-only. It declares Write + Edit
                         and FILES a DR row; the hub scopes that pen
                         to its own display inbox and nowhere else.
         finding a hole and filling one are different jobs on purpose.

   ── THE TWO STATES THE GRAMMAR CANNOT SEE ────────────────────────
      ⚠️ \cite{TOADD} with NO bracket beside it
         a hole no question will ever fill. THREE files call it a
         defect in prose; nothing EXECUTABLE detects it.
      ⚠️ a bare numeral typed straight into prose
         invisible by construction: nothing to hang a marker on. → QB12b

   ── WHO READS THESE FIELDS, AND HOW THEY FAIL ────────────────────
      fields   template · sections · formatting · q_anchor ·
               q_id_pattern, plus the page's `requires:`/`style_from:`
      reader   ③ THE EXECUTOR · a drafting agent               → QC2
      fails    🔇 SILENT, and this is the phase where silence costs
               most: an unbracketed `\cite{TOADD}` looks exactly like
               a hole that will be filled.
      to bind  ✅ the CHEAPEST bind in the group: `\cite{TOADD}` or
               `{VAL:?}` with no `[Q-…]` beside it is one regex. The
               grammar was designed to be greppable and nothing greps it.
      ⚠️ the one case no checker reaches is a gap that cannot be phrased
         as a question. It has no marker, so there is nothing to match.
         The one sanctioned exit for it is buried inside the review
         subagent's prompt (`SKILL.md:234-235`): the hole "is
         explicitly declined in the S page's `## Log`". No normative
         rule in the hub says that, so nothing makes a drafter do it.
```

## Content
### What DRAFT adds to a page it did not shape
The shell, the divisions and the sentence formats were all in place before DRAFT was called (`QC3`). What DRAFT contributes is prose at the sentence layer's formats and a marked hole wherever it cannot source a claim. It writes in `## Content` and `## Items to Finish` and nowhere else, and in particular never in the machine-managed `## Stage Contract`.

### A question is a product, not a failure
The phase is judged on whether every hole is marked and owned, not on how few holes there are. A section that raises nine questions and asserts nothing it cannot source has done its job; a section that raises none and quietly states a coefficient has not, and it looks better while being worse. That is why the rule has to be structural rather than cultural: writing a placeholder is faster than fabricating a citation.

DRAFT stops at the record. It writes `- [ ] 🔎 Q-<Stage>-<n>` in `## Items to Finish` and never opens a file under `1-probes/`. Authoring a `### q-executor`, choosing a route, judging the bank or setting a target is PROBE's work, and has been since 2026-07-20.

### Why unattended is safe here
DRAFT runs without a human because it cannot spend and cannot assert. Those two limits are what make it safe to leave alone, and the same two limits make its output incomplete by design.

## Aims
- [x] 📐 The refusal rule is stated
      `2-phase/0-draft/haipipe-paper-draft/SKILL.md:32-33`: grep the paper's `.bib` first, `\citep{key}` only for a key that greps, and "a key that does not grep is invented".
- [x] 📐 Typed placeholders exist, each naming its owing question
      `\cite{TOADD} [Q-<Stage>-<n>]` and `{VAL:? <what>} [Q-<Stage>-<n>]`, marker and bracket beside each other and never fused. `SKILL.md:32` calls an unbracketed one a defect.
- [x] 📐 DRAFT does not touch `1-probes/`
      `SKILL.md:37` (⛔) and `:162` (FORBIDDEN): it raises `- [ ] 🔎 Q-<Stage>-<n>` records in the S page's `## Items to Finish` and stops. Moved to PROBE 2026-07-20.
- [x] 📐 The self-review has a number and a fallout path
      `SKILL.md:241-242`: at most 2 rounds, and a third-round residual goes into `## Items to Finish` for CHECK rather than being hidden. The 📐 this face carried, asking for a number, was asking for something already written.
- [x] 🔧 Two finders are read-only, not three
      Corrected here 260727. `draft-citation` and `draft-values` each say "It does NOT WRITE, anywhere" at their line 27; `haipipe-paper-draft-display` declares `allowed-tools: Bash, Read, Write, Edit, Grep, Glob` and files a DR row, with `SKILL.md:189-190` scoping that pen to its display inbox.
- [~] ↪ MOVED to `QC3` · the four regions · the layering · the three seams where they disagree
- [ ] 🔍 Assert no placeholder without its `[Q-…]` bracket
      One regex over a grammar built to be greppable, and it has three prose homes and zero executable ones: `haipipe-paper-draft/SKILL.md:32` ("a placeholder with no bracket is a defect"), `:209-210` ("Verify mechanically that every `\cite{TOADD}` and `{VAL:?}` has a `[Q-<Stage>-<n>]` owner"), and `ref/08-stage-gate.md:199`, the section-edit exit criterion. Land it in `2-phase/3-check/haipipe-paper-check/checks.sh`, which already takes `--md <file>` for a stage doc or a section `.md` and today greps those files for bibtex leakage only.
- [ ] 🧠 Rule what DRAFT does with a gap it cannot phrase
      Two live options. (a) Promote the escape hatch that already exists in the text of the review-subagent prompt at `SKILL.md:234-235`, "explicitly declined in the S page's `## Log`", into a rule the hub itself is bound by; cheap and already half-written, but it hands the drafter a sanctioned way to write nothing, and a decline is invisible to any regex over the prose. (b) Require a coarse Q-consumer record even when the gap can only be phrased vaguely; nothing goes unowned and the existing bracket check covers it, at the price of a queue carrying questions PROBE cannot route.

## States
The grammar is implemented and in daily use on the MISQ paper. A stage calls DRAFT, DRAFT writes prose into `## Content` and one `- [ ] 🔎 Q-<Stage>-<n>` record per hole into `## Items to Finish`, and every claim it cannot source leaves a typed placeholder carrying the id of the question that will settle it. The refusals hold too: no bibtex, no unverified key, no number it did not read from a landed answer, and no answer to its own question. The self-review that runs before handoff has a real bound rather than a disposition, at most two rounds, with a third-round residual handed to CHECK instead of being quietly dropped.

Two things about the lanes are worth stating precisely, because this face got them wrong until 260727. Of the three finders, two hold no pen at all and one does: `draft-display` can write, and what it may write is a DR row in its own display inbox, never the manuscript, the S page or `1-probes/`. The hub remains the single writer of everything a reader will see.

One ruling is genuinely live, and it is the gap that cannot be phrased as an answerable question. Every check this face proposes works over markers in the prose, and that case has no marker to work over, which is why it is the last place a silent assertion can still get in.

## Files
- `2-phase/0-draft/haipipe-paper-draft/SKILL.md`
  The phase worker, and the single writer of everything this phase produces. Step 1 reads the stage's `stage.md` AND its `template.md`, and `:76` says plainly that the skill carries no templates of its own. The placeholder grammar and the refusal are stated at `:32-33`, the questions are raised at `:196`, and the self-review's two-round bound is at `:241-242`.
- `2-phase/0-draft/haipipe-paper-draft-citation/SKILL.md`
  The citation finder. READ-ONLY: `:27` is the line, "It does NOT WRITE, anywhere".
- `2-phase/0-draft/haipipe-paper-draft-values/SKILL.md`
  The value finder. READ-ONLY at its own `:27`, in the same words, and it never re-derives a number.
- `2-phase/0-draft/haipipe-paper-draft-display/SKILL.md`
  The one lane that holds a pen. Its `allowed-tools` carries `Write` and `Edit`, and it files a DR row; the hub scopes that pen to the display inbox at `haipipe-paper-draft/SKILL.md:189-190`.
- `1-lifecycle/ref/08-stage-gate.md`
  `:199`, where the bracket rule reappears as an exit criterion: every `\cite{TOADD}` / `{VAL:?}` carries its `[Q-<Stage>-<n>]`. One of the three prose homes the unwritten regex would replace.

## Law

- DRAFT does not create a file. It fills named regions of a page whose shell came from the Board, whose Content divisions were compiled from the stage's template at creation time, and whose sentences must satisfy the sentence layer's formats.
- DRAFT writes prose and QUESTIONS. It never writes a fact it cannot source: not a bibtex entry, not a number, not a citation key it has not verified, and never an answer to its own question. The `.bib` is human-only; an agent greps it and never writes it.
- Every unsourceable assertion becomes a marked hole with a named question beside it, and one `- [ ] 🔎 Q-<Stage>-<n>` record in `## Items to Finish`. The marker and the bracket sit side by side and are never fused, because a placeholder with no question is a hole nothing will ever fill.
- DRAFT never touches `1-probes/`. Raising the question is this phase; planning and running it is PROBE's.

## Discussion
> CC 260727: on the unphraseable gap I would rule (b), require a record even when the question is vague, and I want to be clear about what it costs because the cost is the reason (a) is tempting. (b) puts unanswerable questions into a queue PROBE has to look at and cannot route, and at `probe_depth: 0` it can only mark them DEFERRED, so the queue grows with items nobody can close. That is a real tax on the phase this board most wants to keep cheap.
> I would still pay it, on one argument: option (a) is the only path in this whole grammar that lets a drafter discharge an obligation by writing prose in a `## Log` rather than a marker in the sentence, and every check on this face works over the prose. A decline is invisible to the regex the 🔍 item above describes, so (a) would create the one hole the cheapest check in the group cannot see, which is precisely the failure this face was written about.

## Log
260726 · Rewritten on JL's correction, and reopened from ✅ to 🟡 because the question it now asks had never been asked. The previous version asked only what DRAFT must REFUSE to write. That is true and it is the small half: it said nothing about the fact that a draft must satisfy the Board's page grammar, the stage's template, and the sentence layer's formats at the same time. Reading `create-page.py` and `board/haipipe-board/stage.py` for this rewrite showed WHY those three never collide, each being compiled in at a different moment, and turned up a fourth constraint nothing had named: `## Stage Contract` is a sha256-digested machine-managed region, and a drafter that writes there loses the edit silently at the next sync.

260727 · Every claim on this face re-checked against `2-phase/0-draft/`, and the placeholder grammar held exactly as written: marker and bracket side by side, never fused, one `- [ ] 🔎 Q-<Stage>-<n>` record per hole in the S page's `## Items to Finish`, and `1-probes/` untouched, all of it at `haipipe-paper-draft/SKILL.md:32-37`, `:162` and `:196`. Two claims did not hold. The finders are not three read-only lanes: `draft-citation` and `draft-values` both say "It does NOT WRITE, anywhere", while `haipipe-paper-draft-display` declares `Write` and `Edit` in its `allowed-tools` and files a DR row, with the hub scoping that pen to its display inbox at `:189-190`. Calling all three read-only obscured the one lane that can change a file, so the Diagram now reads two-plus-one and the queue records the correction. The other was the 📐 asking the self-review for a number: `:241-242` already gives one, at most 2 rounds, and already says what happens when it does not converge, the third-round residual going into `## Items to Finish` for CHECK. That item was asking for something written before it was raised, so it closed as [x] rather than being carried.

260727 · The 🔍 item now names its home and its evidence. The bracket rule is asserted in prose three times (`SKILL.md:32`, `:209-210`, and `ref/08-stage-gate.md:199` as the section-edit exit criterion) and zero times in anything that runs; `2-phase/3-check/haipipe-paper-check/checks.sh` already takes `--md <file>` for a stage doc or a section and greps it for bibtex leakage only, which makes it the place a second regex belongs. The 🧠 also gained the thing it was missing, which is a pair of named options rather than an open question: reading `SKILL.md:234-235` showed that an escape hatch for the unphraseable gap already exists, "explicitly declined in the S page's `## Log`", written inside the text of the prompt the drafter hands its review subagent and in no rule the drafter itself obeys. That is now option (a), against requiring a coarse record as (b), and the recommendation sits in `## Discussion` with its cost.

Same pass, on the coordinator's go: the three regions the 260726 split left behind were cut, because a face that reproduces its anchor's paragraphs reports its anchor's open items as its own. `## Where we are` had been QC3's two paragraphs with four words changed and now states DRAFT's own position: the grammar is implemented and in daily use, the refusals hold, the self-review has a bound rather than a disposition, two lanes hold no pen and one does, and the single live ruling is the unphraseable gap. `## Files` lost `create-page.py`, `board/haipipe-board/stage.py` and `stages/5-section-edit/stage.md`, all three of which support only QC3's layering argument and are listed there, and gained what a reader of DRAFT actually needs: the hub with the line numbers for the grammar, the raise and the two-round bound, the two read-only finders with the "does NOT WRITE, anywhere" line in each, the one lane whose `allowed-tools` carries `Write`, and `ref/08-stage-gate.md:199`, where the bracket rule reappears as an exit criterion. `## Law` lost its second paragraph, the four-region layering, which was QC3's Law restated; paragraph 1 already points there and carries it. The queue item that had tracked this work came out with it, since the record belongs in this entry rather than in a queue nobody has to act on.

# REVISE · When may it change a sentence a human has already read?
state: 🟡 PARTIAL
owner: JL
method: substitute only what has landed, run place first, revise directly by default, and expose author-requested candidates as sentence apparatus

## Opening
REVISE is the only phase that rewrites prose a person has already read, and it does it without asking. That makes it the phase most likely to be distrusted, and distrust here is expensive in a specific way: if a reader cannot see what an agent altered, the only safe response is to re-read everything, and at that point the phase has cost more than it saved.

It is also the phase that discharges placeholders, which is where it can do real damage. Substituting a value whose answer has not actually landed turns a visible hole into an invisible claim, and that single failure would defeat the entire placeholder grammar. It is the reason the chain has a fixed order: `place` runs first, before any prose worker touches the sentence, because a rewritten sentence may no longer contain the bracket the answer needs.

What is unresolved is the case where the answer arrives and disagrees with its own sentence. Today `place` substitutes the number and stops. If the answer came back different in kind rather than merely different in value, the sentence around it may now be false, and nothing says whether repairing that is REVISE's job or a reopened DRAFT.

Underneath both of those sits a structural fact worth naming before either is ruled. None of this phase's discipline is a contract field. `place`-runs-first and the `%%` why-comment rule live in three worker `SKILL.md` files, so a stage contract says only the word `revise` in a list and nothing about what that word obliges. `QC3c` is the only other face in this group shaped that way, and its rules are likewise scattered, across six files. A behaviour with no field has nowhere to be declared, which is why the enforcement questions below have stayed open: they are being asked of something that was never written down in the place a stage is defined.

Scope: This page covers The four revise workers, why `place` runs first, what may be discharged, and why the phase is unattended. Neighbouring pages cover The placeholder grammar it discharges is `QC4a`; where the answer came from is `QC4b`; the human who reads its comments is `QC4d`; whether a stage may omit this phase is `QC4`.

## Diagram
```
   ♻️ REVISE                                      runs UNATTENDED

    1  place        ◀── RUNS FIRST, and this is not a preference
       │
       │   for every placeholder whose answer HAS LANDED:
       │     \cite{TOADD} [Q-X-n]  ──▶  \citep{realkey}
       │     {VAL:? …}    [Q-X-n]  ──▶  the number
       │     a done DR row         ──▶  \input + \ref
       │
       │   for every one that has NOT:
       │     LEAVE IT, and FLAG it.
       │
       │   never verifies · never searches · never invents
       ▼
    2  content      section → paragraph → weave → sentence
       │            the ¶-to-¶ arc, hinges, rhythm
       ▼
    3  humanizer    removes AI tells; keeps evidence-tied claims
       ▼
    4  results      results prose specifically

    every worker leaves      %% {CC-place}:      why this changed
    on every NON-TRIVIAL     %% {CC-content}:    …
    change                   %% {CC-humanizer}:  …
                                  │
                                  ▼
                       CHECK reads the COMMENTS, not the diff   → QC4d

      ⚠️ NON-TRIVIAL is the shipped word, and this face used to say
         "every change". `place` says outright that a pure
         `TOADD → \citep{key}` swap needs NO comment
         (`-place/SKILL.md:94`); the chain, `content` and its own
         checklist all say "non-trivial". So the comment count is
         NOT the edit count, and any check built on N-for-N fails on
         correct runs. Corrected 260727.

   ── WHY `place` MUST BE FIRST ─────────────────────────────────────
      if a prose worker runs first it rewrites the sentence AROUND
      the placeholder, and the substitution then lands in a sentence
      nobody wrote deliberately. Worse, a rewritten sentence may no
      longer contain the bracket at all, and the answer has nowhere
      to go.

   ── THE ONE FAILURE THIS PHASE MUST NEVER HAVE ────────────────────
      discharging a bracket whose answer has NOT landed.
      that turns a visible hole into an invisible claim, which is the
      exact defect the whole placeholder grammar exists to prevent.

   ── THE WHY-COMMENT IS THE INTERFACE ──────────────────────────────
      %% {CC-place}:      substituted \citep{kim2019} for TOADD;
                          answer landed in PP03/QX2, verified 260726
      %% {CC-content}:    split the ¶; the second claim had no hinge
      %% {CC-humanizer}:  "it is important to note that" removed

      without these a human at CHECK must diff prose against prose
      and reconstruct intent. With them the phase's whole output
      reads as a LIST OF DECISIONS. A worker that makes a JUDGMENT
      and does not comment it is a defect. A worker that swaps a
      verified key into its own placeholder is not.

      📍 what is actually on disk, MISQ 260727: 17 comments in 2 of
         14 `sections/*.tex`, under SIX tag names.
           CC-content  10   │  CC-cite    1
           CC-display   2   │  CC-humanizer 1
           CC-results   2   │  CC-values  1
         `place` has left ZERO anywhere in the paper, and `display`,
         `cite` and `values` name DRAFT finders, not revise workers.
         `appendices/` adds a seventh, `CC-appB-discriminant-v0709`.
         The tag set was never declared, so it drifted.

   ── THE OPEN CASE ─────────────────────────────────────────────────
      the landed answer CONTRADICTS its own sentence.
        the value came back different in KIND, not just in value
        `place` substitutes it and stops
        the sentence around it may now be FALSE
      ❓ REVISE's problem, or a reopened DRAFT? Nothing says.

   ── one stage skips this phase entirely ───────────────────────────
      2a-venue declares [draft, probe, check].               → QC4
      it produces a recommendation, not prose. Probably right,
      and stated nowhere.

   ── WHO READS THIS, AND HOW IT FAILS ─────────────────────────────
      fields   ⛔ NONE. Like QC3c, this phase has no contract field.
               `place`-runs-first and the `%%` why-comment rule live in
               three worker `SKILL.md` files, not in `stage.md`.
      reader   ③ THE EXECUTOR, at one remove: the stage never sees
               these rules, only the worker it dispatches to.  → QC2
      fails    🔇 SILENT. If a worker stops commenting, the symptom
               surfaces at CHECK as a human who cannot tell what
               changed, which reads like the human's problem.
      to bind  ⚡ PARTLY BOUND ALREADY, and this face had said nothing
               checks it. `checks.sh --stage-page` asserts the newest
               `[REVISE]` entry in the owning S page's `## Log` carries
               a `workers:` line, at ❌ FAIL tier, and
               `5-section-edit/stage.md:158` declares it as a
               `done_criteria`. So REVISE's PROVENANCE is mechanical:
               proof the four workers were dispatched rather than the
               prose hand-edited inline. Its COMMENTS are not.
               ✅ and the cheap unwritten check is a TAG check, never a
               count: every `%% {CC-<tag>}` must name a declared revise
               worker. One grep, both sides already on disk, and it
               FAILS TODAY on 4 of the 17 comments in `sections/`.
```

## Content
### Unattended, and why that is the cheaper trade
REVISE changes prose without asking, which sounds like the least safe thing in the lifecycle and is not. It cannot spend, it cannot fetch and it cannot assert: everything it writes either came from a landed answer or is a rephrasing of what was already there. The one gate in the stage sits after it, where a human reads the accumulated why-comments in a single pass.

Gating REVISE would double the human's cost per stage and catch nothing CHECK does not catch, because nothing REVISE does is irreversible or unlogged. That is the whole argument, and it depends entirely on the comments actually being written.

### What it may never discharge
A bracket whose answer has not landed stays exactly as it is and gets flagged. `place` is explicitly forbidden from verifying, searching or inventing: it is a substitution worker, and everything it substitutes must already exist somewhere it can read. The forbidding matters more than it sounds, because a worker that is allowed to check would eventually be allowed to conclude.

### The rule everything rests on, half enforced
The why-comment convention is stated in four worker contracts, and what is checked is the dispatch rather than the comment: `checks.sh --stage-page` FAILs a newest `[REVISE]` entry with no `workers:` line, which proves the four workers ran and says nothing about whether they explained themselves. The shipped rule is also narrower than it sounds. It asks for a comment on every NON-TRIVIAL change, and `place` states outright that a pure `TOADD` to `\citep{key}` swap needs none, so the comments can never be counted against the edits. If a worker stops commenting on the changes that do need it, the failure is silent and the symptom appears at the gate as a human who cannot tell what changed, which reads like the human's problem rather than the worker's.

### Venue-grounded scientific prose, not generic de-AI rewriting
AI prose is not fixed by deleting adjectives alone. The recurring defects are defensive repetition, formulaic framing, inflated importance, and a sentence that jumps from observation to conclusion without the connecting warrant. `revise-content` owns the paragraph's argument and hinge; `revise-humanizer` owns the sentence's language. Neither may repair a missing warrant by inventing evidence.

The language pass begins with the writing contract, not a generic "sound human" prompt. The section's venue `template.md` supplies its paragraph move, `style.md` supplies section-specific constraints and anti-patterns, and the pack-wide `style-profile.md` supplies the paper's voice. The paper-local `S-Venue-0` then adapts that contract to its contribution and causal boundary. Exemplars teach the shape of a move, never wording to reuse.

Every proposed wording change must pass four gates: preserve meaning, scope, causal strength, numbers, citations, displays, and defined terms; retain the paragraph's venue job; improve clarity by removing clutter or repairing a buried predicate without replacing technical language; and remove AI tells without deleting legitimate hedging, passive voice, authorial `we`, or evidence-bound qualification. SciWrite supplies the clarity checks, while evidence and numeric integrity remain CHECK responsibilities.

The default remains direct REVISE with `%% {CC-*}` why-comments. When the author explicitly requests original-preserving review, REVISE switches to candidate-diff mode: it leaves source prose and TeX unchanged, and attaches one full `> Note:` candidate beneath the source sentence. The diff uses `~~removed~~` and `**inserted**`, followed by a verified model label and date. The Board renders the first as a deletion line and the second in bold. A candidate is not an applied revision and cannot close REVISE.

## Aims
- [x] 📐 The four workers exist, and the chain orders them
      `place · content · humanizer · results` under `2-phase/2-revise/`, dispatched by the `haipipe-paper-revise` chain (`SKILL.md:43-46`, `:90`).
- [x] 📐 `place` runs first, and the order is called binding
      `haipipe-paper-revise/SKILL.md:91`: substituting after the prose workers would re-open sentences they had already finished, so the shipped text would never have been reviewed in its final form.
- [x] 📐 A bracket without a landed answer is never discharged
      `place` leaves and flags every placeholder whose answer has not landed, and never verifies, searches or invents.
- [x] 🔍 REVISE's provenance is already mechanical
      `checks.sh --stage-page` FAILs a newest `[REVISE]` entry with no `workers:` line, and `5-section-edit/stage.md:158` declares it as a `done_criteria`. The check this face called nonexistent covers dispatch; it does not cover comments.
- [x] ✍️ Venue-grounded SciWrite and humanizer gates are declared
      The language worker now resolves venue style before editing and applies meaning, venue-fit, clarity, and human-voice gates. It preserves evidence-bound hedging, passive voice, authorial `we`, numbers, citations, and technical terms.
- [x] 📝 Author-selected candidate-diff mode is implemented
      Original prose stays intact; one adjacent `> Note:` carries a complete `~~removed~~` / `**inserted**` candidate plus model/date. The Board renders the diff, and candidate Notes never sync to TeX.
- [~] ↪ MOVED to `QC2` · whether this phase's discipline earns a contract field. `QC2` owns that ruling for both fieldless faces, `QC3c` and this one, and states it as one item rather than two.
- [ ] 🔧 Correct the comment rule from "every change" to "non-trivial"
      Four shipped contracts say non-trivial, and `-place/SKILL.md:94` says a pure `TOADD` to `\citep{key}` swap needs no comment. This face's Law said every change, which makes the phase look defective exactly when it is behaving correctly, and made the check below unwritable.
- [ ] 📐 Declare the closed set of `{CC-*}` tags
      No list of legal tags exists anywhere, which is why `sections/` carries `display`, `cite` and `values` alongside `content`, `results` and `humanizer`, and `appendices/` carries `appB-discriminant`. The four workers are already decided; the vocabulary just needs writing down beside them, and the check below cannot be written first.
- [ ] 🔍 Assert every `%% {CC-<tag>}` names a declared revise worker
      One grep, both sides on disk, and it fails today. `sections/*.tex` holds 17 comments under six tags: `content` 10, `display` 2, `results` 2, `cite` 1, `humanizer` 1, `values` 1. Three of the six name DRAFT finders rather than revise workers, so 4 of 17 comments claim a worker that does not exist, and `place` has left none anywhere in the paper.
- [ ] 🧠 Rule what REVISE does when an answer contradicts its sentence
      Today `place` substitutes and stops. Two options: REVISE repairs the surrounding sentence, which lets a substitution worker rewrite a claim; or the contradiction reopens DRAFT, which costs a phase and keeps the repair with whoever wrote the claim. Nothing says which.
- [ ] 🧪 Run the `workers:` check against a real REVISE entry
      It has never fired. `0-lifecycle/` on the MISQ paper holds zero `[REVISE]` entries, so `checks.sh --stage-page` reports "REVISE proof skipped" on every page it is pointed at. A check that has never seen its input is not yet evidence.
- [ ] 🧪 Read one revised section from its comments alone
      `sections/04_personality_extraction.tex` is the only real test on disk: 13 of the paper's 17 comments are in that one file. Can a human accept or reject each change without opening the previous version?

## States
The four workers exist, the chain order is implemented with `place` first, and the why-comment convention is used on the MISQ paper. The language worker now resolves venue style before clarity and anti-AI edits, rather than treating academic prose as a generic paraphrase problem.

Candidate-diff mode has been exercised on the MISQ Abstract and Introduction. Its deletion and addition markup renders in the Board, but does not enter TeX. Two gaps remain about trust rather than mechanism: nothing checks that an edit carried a comment, and nothing says what happens when a landed answer makes its own sentence wrong.

## Files
- `2-phase/2-revise/haipipe-paper-revise/`
  The chain that dispatches the four, in order.
- `2-phase/2-revise/haipipe-paper-revise-place/`
  The substitution worker that runs first and refuses to do anything else.
- `2-phase/2-revise/haipipe-paper-revise-content/`
  Section, paragraph, weave, sentence; its siblings are `-humanizer` and `-results`.
- `2-phase/2-revise/haipipe-paper-revise-humanizer/ref/venue-sciwrite.md`
  The four language gates and the candidate-diff grammar.
- `venue/playbook-utd-is/`
  The per-section `template.md` and `style.md`, plus the pack-wide `style-profile.md` and MISQ taste signals.

## Law
REVISE runs unattended because it cannot spend, cannot fetch and cannot assert. Everything it writes is either a landed answer or a rephrasing of what was already there.

`place` runs FIRST. It substitutes only placeholders whose answers have landed, leaves and flags every other, and never verifies, searches or invents. Discharging a bracket whose answer has not landed turns a visible hole into an invisible claim, and is the one defect this phase must never have.

Every worker leaves a `%%` why-comment for every NON-TRIVIAL change. The human at CHECK reads the comments, not the diff; a judgment made without a comment is a defect, and a self-evident substitution is not. `place` names the exemption outright: a pure `\cite{TOADD}` to `\citep{key}` swap needs no comment. So the comment count is never the edit count, and REVISE's mechanical handle is the `workers:` provenance line plus the tag on each comment, not an arithmetic identity.

Language quality is venue-first and meaning-preserving. A generic de-AI pass may remove clutter, inflated framing, formulaic transitions, empty intensifiers, and buried predicates. It may not change a claim, its scope or causal strength, a defined term, a number, a citation, a display reference, or evidence-tied hedging. The writer reads the section template and style before changing its sentences; SciWrite gives the clarity test and the humanizer protects scholarly voice.

Default REVISE applies accepted prose directly and leaves why-comments. An explicit author request for original-preserving review selects candidate-diff mode instead: leave the sentence and TeX untouched, then attach one complete `> Note:` line using `~~removed~~` and `**inserted**` with a verified model/date suffix. That Note is review evidence only, not an applied revision.

## Discussion
> CC 260727: the comment rule's threshold is a real fork, and this face had been asserting the wrong side of it without noticing. The shipped word is NON-TRIVIAL, which leaves what deserves a comment to the worker's judgment. The alternative is EVERY change, mechanically, including each `TOADD` to `\citep{key}` swap. Option A, keep "non-trivial": costs the family any arithmetic check forever, so the only mechanical handles are the `workers:` provenance line and the tag on each comment, and a worker that quietly decides its judgment calls were trivial is undetectable. Option B, "every change": buys the N-for-N assertion this face had already written down as though it were true, and costs the human at CHECK real reading, because a section discharging twenty placeholders would open with twenty comments that say nothing a reader could not see. My recommendation is A, keep "non-trivial", and bind the TAG instead of the count: the tag check is one grep, it already fails on 4 of 17 comments, and it catches the failure that actually happened on disk, which is not a missing comment but a comment attributed to a worker that does not exist. Option B would be the right answer only if CHECK's cost were free, and the whole reason three phases run unattended is that it is not.

## Log
260726 · Carried from `_archive/QB7-revise.md` and retitled to the fork rather than the phase name. The live question is the permission, not the procedure: this is the only phase that rewrites prose a person has already read.

260726 · Opening gained the same structural point as `QC3c`: none of this phase's discipline is a contract field, so the enforcement questions have been asked of something never written down where a stage is defined. The why-comment check was also promoted from "enforced nowhere" to a concrete assertion, since the diff and the comments are both already on disk.

260727 · Verified against the four shipped worker contracts and the live paper, and two of this face's load-bearing statements were wrong. First, the comment rule is NOT "every change": `haipipe-paper-revise/SKILL.md:21` and `:99`, `-content/SKILL.md:37` and its own checklist at `:74` all say NON-TRIVIAL, and `-place/SKILL.md:94` goes further, stating that a pure `TOADD` to `\citep{key}` swap needs no comment. The Law, the Diagram and the Content paragraph said otherwise, so the N-regions-to-N-comments assertion this face had promoted the day before was unwritable: it would fail on every correct `place` run. It is deleted and replaced by the check the contracts do support, that every `%% {CC-<tag>}` must name a declared revise worker. Reading the MISQ paper for that gave the check its teeth before anyone writes it: `sections/*.tex` holds 17 comments under SIX tag names, and `display`, `cite` and `values` name DRAFT-phase finders rather than revise workers, so 4 of 17 already point at a worker that does not exist, `place` has left none at all, and `appendices/` adds a seventh free-form tag. The tag set had never been declared, which is why it drifted, so declaring it is now the item that unblocks the check. Second, "enforced nowhere" was also wrong: `checks.sh --stage-page` already asserts at FAIL tier that the newest `[REVISE]` entry in the owning S page's `## Log` carries a `workers:` line, and `5-section-edit` declares that as a `done_criteria`. So REVISE's dispatch is bound and only its comments are loose. That check has nonetheless never fired, because the MISQ `0-lifecycle/` carries zero `[REVISE]` entries, which is now a `🧪` item. The contract-field ruling was handed to `QC2`, which already owns it for both fieldless faces and was tracking the same decision twice.

260727 · Added the venue-grounded scientific-prose ruling from the MISQ revision session. The diagnosis is not "AI words" alone: content owns logical warrants and paragraph hinges, while humanizer owns language. Venue `template.md` and `style.md`, the shared `style-profile.md`, SciWrite's clarity checks, and the humanizer's preservation rules are now one four-gate protocol. The author-selected candidate-diff exception was implemented and tested on Main 0 and Main 1: source prose stays unchanged; the Board displays `~~deleted~~` and `**added**`; TeX is not synced. A fresh-context agent followed the new grammar and refused a fragment-only candidate or TeX sync.

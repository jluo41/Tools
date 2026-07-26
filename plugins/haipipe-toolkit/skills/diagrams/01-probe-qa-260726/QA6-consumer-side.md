# ⑦ The consumer side, where the stake lives

state: 🟡 PARTIAL
owner: JL
method: name the one place a stake is allowed, state the law that keeps it there, and admit that the law is held by nothing

## Question
Where does a consumer's reason for asking live, and what stops it from travelling with the question?
In the stage doc's `Q-consumer` section, and nothing stops it except a phase boundary and a law with no enforcement.
The stake is legitimate here and forbidden everywhere else, which makes this folder the only one on the map defined by what it is allowed to hold.

A stake hides in ordinary words, which is why the rule cannot be a filter.
"Rescue", "we want", "the hoped-for", a claim id, or "our paper" all carry it, and a question can leak the wanted answer purely by what it declines to ask.
So the defence is structural: the stake stays in a section that is never dispatched, the stripped version is written somewhere else, and the two sit far enough apart that carrying one does not carry the other.

## Boundary
- ✅ Covered here
  What is in the consumer's own folder, how a question is raised there, LAW 1, and the phase boundary that keeps DRAFT out of the probe files.
- ↪ Covered elsewhere
  The stripped question and the audit of the strip live on the wall, which is `QA7`.
  The bank's half of the wall is `QA8`; the loop step that does the strip is `QB2`.
  Where the answer comes back to rest in this folder is `QB6`.

## Diagram
```
   <consumer>/0-lifecycle/<stage>/<stage>.md
   ────────────────────────────────────────
     the stage's prose
     …
     ## Q-consumer                    ← at the END of every stage doc
       ## Q-Claim-6 · does WellDoc have a cycle column?
       my claim C6 dies if it does              ← THE STAKE, legal here
       → 1-probes/PP03_welldoc/QX1_cycle.md     ← a pointer, not an id
       Answer: …                                ← lands later, at ⑤

   <consumer>/0-lifecycle/1b-claims/1b-claims.md
     a claim's STATUS lives here and NOWHERE else, written by the
     author. a probe file never records whether a claim survived.

   ── LAW 1 ────────────────────────────────────────────────────────
   A CONSUMER SESSION NEVER RUNS BANK WORK INLINE.
     ✅ the EYE   read-only grep of {tasks,discoveries}/**/QA/*.md
                  LEGAL and REQUIRED. that IS step ② MATCH.
     ⛔ the PEN   writing any bank file, including a QA digest you
                  think you are being helpful by authoring
     ⛔ the RUN   executing bank work in the consumer's own session
   enforcement: NONE. nothing on disk records what a session did.

   ── the phase boundary ───────────────────────────────────────────
   DRAFT RAISES.        writes prose + the Q-consumer questions. stops.
                        authors no entry, chooses no route, judges no
                        bank, never opens 1-probes/.
   PROBE PLANS AND RUNS. all five steps.
   a DRAFT that writes a `### q-executor` is doing PROBE's job.
```

## Content
### 1 · One place for the stake, and it is the readable one
#### The stake belongs where a human can still argue with it
(the stage doc, next to the prose the question serves)
A stake is not contamination in the consumer's own file, it is the reason the question is worth asking, and hiding it would make the stage doc unreadable.
So the rule is not "never write the stake", it is "the stake stays in the document whose author owns the claim".
Everything downstream then has a simple test: if a file is not this stage doc and it carries a reason, something has leaked.

#### The id is consumer-local and never crosses
(`Q-Seed-1`, `Q-Claim-6`, and each family owns its own scheme)
Three id layers exist and none of them crosses the wall: `Q-<Stage>-<n>` here, `QX<n>` in the probe file, `QA/<n>-<slug>.md` in the bank.
They bind by PATH, through the `target` field, never by a shared id, which is why two consumers can both carry a `PP04` without colliding.
The stage doc's pointer to its entry is a path for the same reason.

### 2 · LAW 1, and the distinction that makes it usable
#### The eye is required; the pen and the run are banned
(step ② MATCH is a read-only grep, and it is mandatory)
Without the distinction the law would forbid the layer's own cheapest step, since matching against the bank means reading the bank.
The line is drawn at writing and at executing: a consumer session that runs the analysis itself, or writes a QA file it thinks is helpful, has made the bank probe-aware and every later answer is shaped by who asked.
Reading it changes nothing, so reading is free.

#### Nothing enforces it, and the reason is structural
(a rule about what a session DID leaves no trace on disk)
An inline run and a dispatched run produce the same artifacts.
A consumer-authored QA file and an executor-authored one are the same file.
So the honest options are a proxy check, a trust model with a named consequence, or accepting it as unenforceable and saying so on the page, and until JL rules, this page says so.

### 3 · What else this folder holds, and one thing it must not
A claim's status lives in `1b-claims.md`, written by the author, and never in a probe file.
That separation is the same wall seen from the other direction: the probe carries, the consumer judges.
The consumer's own registries also sit here, and they are the T1 rung of the cost ladder, the answers a consumer can give itself without asking anyone.

## Items to Finish
- [x] 📍 The stake's home is named, and it is the stage doc
      One `## Q-<Stage>-<n>` per question, at the end of every stage doc, in the consumer's own words.
- [x] ⚖️ LAW 1 is stated with the eye, pen and run distinction explicit
      Reading the bank is required, writing and running are banned.
- [x] 🚧 The phase boundary is stated: DRAFT raises, PROBE runs
      DRAFT never opens `1-probes/`, and a DRAFT that writes a q-executor is doing PROBE's job.
- [x] 🔢 The three id layers are local, and binding is by path
      Nothing binds by a shared id, which is why consumer-local numbering never collides.
- [ ] 🧠 JL rules whether LAW 1 can be enforced at all
      A rule about what a session did leaves no trace, so the options are a proxy check, a trust model with a named consequence, or an explicit ruling that it is unenforceable.
      This closes with any of the three, and stays open while the page implies a guarantee nothing provides.
- [ ] 🧠 JL confirms the stake word list is the right test
      A list of forbidden words is a weak proxy, and 260726 produced a live false positive: a QA file reading "citing this paper does not upgrade it into construct evidence" trips the "this paper" pattern while referring to a cited paper in the literature.
      A fluent leak passes the same list.

## Where we are
The consumer side is the settled half of the wall.

The stake has one legal home, the ids are local, binding is by path, and the phase boundary between raising a question and working it is stated plainly enough that a violation is nameable.
The unsettled part is LAW 1, which forbids something that leaves no evidence, and the word list that stands in for judgment, which was measured producing a false positive on the same day it was measured producing no true ones.

## Files
- `SKILL.md`
  The four forms, the Q-consumer shape, LAW 1 verbatim, and the DRAFT/PROBE phase split.
- `haipipe-paper-probe/`
  The paper adapter, whose `ref/per-stage-dispatch.md` says which stage raises what.

# And nothing else: results/ is not a consumer surface
state: 🔴 OPEN
owner: JL
method: state the closure as a rule about readers rather than about files, and find the one place it can be checked

## Opening
May a consumer read `results/` directly? The rule says no: the digest is the readable answer and a consumer reads that, never the results themselves. This is the closure that makes `QD1` meaningful, because a door only matters if the wall around it holds.

The reason is that `results/` is not a communication surface and was never designed as one. A `metrics.json` has whatever keys that run needed, a `report.md` was written for whoever was standing there, and a filename means what it meant that afternoon. None of it carries the caveats, and the caveats are most of what makes a number safe to use. `## Caveats` and `## Not-done` exist in the digest precisely because the raw evidence cannot carry them.

What makes this hard to enforce is that it is a rule about READERS, and this layer cannot see its readers. Everything else in the family is a rule about files: what may be written, where, containing what. This one says a file that exists and is perfectly readable must not be read by a particular party, and nothing here knows who is reading.

**Covered elsewhere**: What DOES leave is `QD1`; the door a question arrives through is `QA5`; the consumer side of the same wall is `QA8@probe`, which is where a checker would most plausibly live.

## Diagram
```
   WHAT LEAVES THE BANK

   📖 QA/<n>-<slug>.md          THE ONLY READABLE ANSWER      → QD1
        prose · anchors · CAVEATS · NOT-DONE

   ────────────────────────────────────────────────────────
   🔒 everything else

      results/<run>/metrics.json      keys chosen for that run
      results/<run>/report.md         written for whoever was there
      workflow/report.yaml            evidence, in IPO shape
      notebooks/<run>.ipynb           the execution record
      _WorkSpace/**                   the heavy artifacts

      all real. all readable. NONE of it a communication surface.

   ── what the raw evidence cannot carry ─────────────────
      ## Caveats     what would make this wrong
      ## Not-done    what was NOT checked

      these do not exist in metrics.json and cannot. A consumer
      reading the number directly gets the number WITHOUT the two
      sections that decide whether it may be used, and the number
      looks exactly as authoritative either way.

   ── why this rule is unlike every other rule here ──────
      every other rule    about a FILE: what may be written, where
      this rule           about a READER: who may open it

      and this layer cannot see its readers. It is consumer-unaware
      BY DESIGN, so it structurally cannot detect the violation.
                                                        → Items

   ── so the check lives on the OTHER side ───────────────
      a consumer that cites results/<...> instead of a QA path is
      the observable event, and it is observable in the CONSUMER's
      repository. The probe layer's card checker already walks
      exactly those bindings.                     → QA8@probe
```

## Content
### The closure is what makes the digest worth writing
If a consumer may read `results/` directly, the digest becomes optional documentation, and
optional documentation is not written. The rule and `QD1` stand or fall together: it is one design,
stated from two sides.

### The cost is real, and pretending otherwise is how the rule gets ignored
A consumer that needs a number nobody has digested has to ask, and asking costs a round trip
through the `qa` door and possibly a run. Reading `metrics.json` takes seconds. So the rule asks
someone to take the slow path at exactly the moment they are in a hurry, and a rule like that
survives only if the fast path is visibly unsafe.

That is why the caveats argument matters more than the architecture argument. "It breaks the
layering" persuades nobody at 11pm; "the number you are about to copy has a caveat you cannot see"
does.

### This layer cannot enforce it, and should stop pretending it might
Consumer-unawareness is not an accident to be worked around, it is the property that makes the
bank reusable, and it means this layer will never detect a consumer reading its files. The check
has to live where the citation is written, and the probe layer already walks exactly those
bindings when it verifies that each entry points at a real QA file. An entry pointing at
`results/…` instead is the observable violation.

## Aims
- [ ] 🚫 State the closure as a rule with a reason attached
      `SKILL.md` says a consumer reads the digest and never `results/`. It does not say why, and the reason (the caveats cannot travel) is the only part that will survive contact with someone in a hurry.
- [ ] 🔎 Put the check on the consumer side
      A probe entry whose `target:` names `results/` rather than a `QA/` path is the observable violation, and it is observable where the probe checker already looks. Belongs to `QA8@probe`; this face should ask for it, not build it.
- [ ] 📄 Rule whether a HUMAN reading results/ is a violation
      The rule is about the consumer layer, not about people. A researcher opening their own `metrics.json` is obviously fine, and nothing says so, which makes the rule read as broader and less credible than it is.
- [ ] 📏 Rule what happens when no digest exists and one is needed
      Today the honest answer is "ask, and wait for a run". Whether a consumer may cite a result while its digest is pending, with the pointer recorded, is the case that decides if this rule is livable.

## States
Stated once, in `SKILL.md`, in a single sentence: a task ends at Report, produces `results/`, and
the readable answer is the digest a consumer reads instead.

Nothing enforces it, this layer structurally cannot, and the reason behind it is written nowhere.
Of the four items above, only the third and fourth are about the rule itself; the first two are
about making it survivable.

- 260726 CC · 🔒 Separated the rule from its enforcement
      The rule belongs here and the checker does not: it has to live on the consumer's side, because this layer cannot see who is reading. Written down so nobody spends effort building a detector on the side that structurally cannot detect it.

## Files
- `SKILL.md`
  The one sentence stating the closure.
- `fn/qa.md`
  The digest that is the sanctioned alternative.
- `QA8@probe`
  The bank as the consumer sees it, and the most plausible home for the check.

## Log
260726 · Created with the board.

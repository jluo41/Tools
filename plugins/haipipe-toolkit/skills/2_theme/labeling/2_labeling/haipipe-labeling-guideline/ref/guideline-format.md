The guideline format
====================

What a guideline version `G_t` holds, and in what shape (JL 261014: "another issue we haven't made sure is the
guideline format, what should be the guideline format"). It is the format every Run in this view writes and every
reader reads; the files are the engine's `POLICY_COMPONENTS` in `labeling/policy/versions/G_<t>/`. Design record:
`Tools/blueprints/b15_theme_labeling/studio/s42-task-building-procedure/` (the building procedure).


Two readers, one source
-----------------------

A guideline is read by the person who owns the label, who must trust it, and by the labelers (the labeling agent
and the panel of open models), who must follow it. One structured source is rendered twice, so the two never
disagree:

```text
rules.yaml + the classes + the borders      the source: changed only through the person's rulings
      ├──▶ guideline.md     for the person: full, every rule with its evidence and its history
      └──▶ cheatsheet.md    for the labelers: short and ordered; the prompt they label with
```

A hand edit to either rendering is lost on the next render; change the source through a ruling.


guideline.md, section by section
--------------------------------

```text
§1 Question and scope   the one question; what is judged (the main text) and what is only context
§2 Classes              per value: a one-sentence definition · includes · excludes · two anchor items from gold
§3 Rules                R1 … Rk in order of precedence, each a rule card (below)
§4 Borders              per border pool (below): what makes it hard, the rules that decide it, one item each side
§5 Procedure            read the context → check the rules in order → class → region → confidence
§6 Uncertainty          what to do when unsure; the none value never means "unsure"
§7 Changes              G_(t-1) → G_t: each rule added, narrowed or dropped, with its round and the person's words
```

G_00 (written by `corpus-contract`) holds §1, empty §2 meanings, the named borders of §4 and §5-6; §2 is written at
G0 (`definition-discussion`); §3 and §7 grow only in `guideline-learn`.


The rule card
-------------

Each rule is one short, testable sentence with its proof attached, in `rules.yaml`:

```yaml
- id: R<k>
  if:   "<a condition a reader can check on one item>"
  then: <class value>
  border: <HL | LN | HN | HLN | ...>     # the border pool it settles
  precedence: <n>                        # a lower number is checked first; the first rule that fires wins
  evidence: [<item id>, ...]             # gold items that made it; each also in casebook.jsonl
  since: G_<t>                           # the version that added it
  why: "<the person's reason, in their words>"
  status: active                         # active | narrowed | dropped (kept, never deleted)
```

1. **From rulings only**: a rule exists because the person accepted a patch in `guideline-learn`; a model may
   propose a rule card, never activate one.
2. **Evidence first**: a rule with no gold item behind it is not a rule; the casebook row names the rule it proves.
3. **Regression**: `regression.jsonl` lists, per rule, the gold items it must still get right, so a patch shows its
   backward impact ("this change flips <k> earlier gold labels") before the person rules it.
4. **Never deleted**: a dropped or narrowed rule keeps its card with its new status; §7 says when and why.


The components
--------------

```text
guideline.md       §1-§7, rendered from the source, for the person
cheatsheet.md      §2 definitions + §3 rules in precedence order + §5, for the labelers' prompt
rules.yaml         the rule cards (the source of §3)
boundaries.yaml    §4: each border pool, its name, its state in the register, the rules that decide it
procedure.yaml     §5
uncertainty.yaml   §6
casebook.jsonl     gold items: id, class, region, the rule(s) they prove, the person's line
regression.jsonl   per rule, the gold it must keep right
diff.yaml          §7 in machine form: from, to, each change
gallery.md         anchor items for the person, by class and border
manifest.yaml      version, parent, status, components
```

`rules.yaml` is not yet in the engine's `POLICY_COMPONENTS`; until it is, the rule cards live in `boundaries.yaml`
under `rules:` and `guideline-learn` writes them there.


The seven pools, named
----------------------

A pool says which labels the labelers gave an item; its name says why the item sits there and what the guideline
needs. The names are the building law's (`haipipe-labeling-building` § The register), shown in §4 and on every
screen:

```text
H     Settled high       every reader reads it high
L     Settled low        every reader reads it low
N     Settled none       every reader reads it none
HL    Degree border      the thing is there; how much is unclear       needs a severity rule
LN    Presence border    is it there at all?                           needs a threshold rule
HN    Clash              readers see opposite extremes: the concept     needs the meaning clarified (most valuable)
                         itself is read two ways
HLN   Unmapped           anything is plausible; no rule covers it yet   needs a new rule
```

The settled pools are audited by random draw (shared mistakes hide there); the four border pools are where rounds
pick and rules come from.

# The change record: `✎`

**This file does not own the sentence apparatus.** `board/haipipe-board-sentence`
does, and `QB4 §3.3.3` states the taxonomy. Read those first. What follows is
only the part that belongs to this skill: how a change record is COMPUTED and
WHERE it is placed.

## 1 · What the owning contract already says

A `>` line directly under a sentence belongs to THAT sentence, not to the
paragraph and not to the page. Three kinds can hang there, and the badge at the
end of the sentence says which:

```
⚑  a TYPED LANE, and there are eight
   📚 > Citation:    a source
   🔢 > Value:       a number and where it came from
   🖼 > Display:     a figure or table
   ⚠️ > Check:       something still to verify
   🔎 > Q-consumer:  a question this sentence needs answered
   🔗 > Link:   📄 > Source:   📝 > Note:   for what the five above miss

💬  a COMMENT · `> JL: …` · a person is waiting on an answer

✎  a CHANGE RECORD · `> ✎ ~old~ *new* · WHO · YYMMDD HHMM` · which words moved
```

`⚑ 2` is two typed lanes, `💬 2` is two people waiting, `✎ 2` is two edits.
A person waiting outranks a record, so a sentence carrying both shows `💬`.

Three rules from `haipipe-board-sentence` bind this skill directly:

- **A lane is APPENDED, never edited in place.** The record is the point.
- **A signed `> WHO:` or `> ✎` line is never erased** (`ref/writing-rules.md`).
  It is the durable review trail.
- **A lane without a signature is not a lane**, it is unclaimed prose.

## 2 · The two marks

```
~removed~     renders struck through
*added*       renders inserted
plain words   SURVIVED the edit          ← the whole reason this is word-level
```

`haipipe-board/src/body.py` renders it: `render_change()` turns `~…~` into
`<del class="chg-old">` and `*…*` into `<ins class="chg-new">`.

Because `~` and `*` are the marks, they cannot appear in the text.
`cli/wdiff.py` refuses rather than emitting a record that renders wrong.

## 3 · Placement, which is this skill's job

**A record binds to the prose line above it**, so where it goes is not a
preference.

```
✅ sentence                              ❌ sentence A
   > Citation: …    existing lanes          sentence B
   > JL: …          untouched               sentence C
   > ✎ …            JOINS THE END           > ✎ (about A)   ← lands on C
```

Two placement rules follow, and `cli/wdiff.py apply` enforces both:

- **A new record joins the END of the sentence's lane run**, after any existing
  `> Citation:` / `> Value:` / `> JL:` lane. Inserting it straight under the
  sentence splits the run, and everything below the record rebinds to the record.
- **A rewrite that splits one sentence into several anchors on the FIRST** of
  them, and its diff covers the whole rewritten run. Diffing against the first
  new line alone marks everything that moved to a later line as deleted, which is
  a lie: a split sentence loses nothing.

Both were got wrong by hand on `QB4` on 260801, by an author who knew the rule,
which is why neither is left to judgment.

## 4 · The bridge to `/haipipe-paper`

`QB4 §3.3.3` states it, and it is the reason this skill can serve both hosts:

```
📚 > Citation:  ←→  \cite{TOADD}
🔢 > Value:     ←→  {VAL:? …}
🖼 > Display:   ←→  a display id
```

The lane and the placeholder are the same fact in two notations: a board lane
holds what a paper placeholder is waiting for. `cli/holes.py` audits both, and
`ref/holes.md` carries the discipline.

The humanizer's candidate lane is a second notation for the same computation
(`~~removed~~` / `**inserted**` inside a `> Note:`), which is why it calls
`cli/wdiff.py` rather than keeping its own diff.

`cli/wdiff.py` EMITS both notations, and `--host` selects which:

```
--host board   (default)  > ✎ ~old~ *new* · WHO · YYMMDD HHMM
--host paper              > Note: ~~old~~ **new** · WHO · WHEN
```

Until 0.5.0 it emitted the board notation only, and `haipipe-paper-revise`
instructed its caller to double the tildes by hand. The computation was in one
place and the OUTPUT was not, which is the same defect in a smaller place: the
last step before the marks reached a manuscript was left to the reader this
skill exists to protect. A host is a flag, never an instruction.

## 5 · Lifecycle

Not this skill's to define. `QB5e` owns it: records are archived on resolution
and restorable, purge is a separate explicit act, and nothing is silently
deleted. `cli/wdiff.py apply` refuses to write when the result would contain
fewer `✎` lines than it started with.

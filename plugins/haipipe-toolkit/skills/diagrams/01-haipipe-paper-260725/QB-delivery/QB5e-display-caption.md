# A display with a caption and a label
state: 🔴 OPEN
owner: JL
method: say what the caption must accomplish and what the label promises, and put both where the ruling says they live

## Opening
The picture is finished. What does the paper still have to write on it? Two things, and neither is the renderer's: a caption, which is an argument in the author's voice, and a label, which is a promise every citing sentence depends on.

`QB5@display` has ruled who owns them and is `✅ SETTLED`: "For a paper, the matching `S-Display-N` page owns those semantic fields in `### Wrapper`. The renderer can serialize them mechanically but cannot invent or revise them." Its Law: "The renderer writes a wrapper only from consumer-approved meaning." So ownership is settled and the CONTENT rules are blank, which is why every caption on this paper was written straight into `float.tex` by hand.

Scope: This page covers What a caption must accomplish for this venue, what a label promises and therefore may never do, and where in the paper both are authored. Neighbouring pages cover That the fields are consumer-owned at all is `QB5@display`, ruled and not re-argued. WHERE the float then lands is `QB5f`. What a SENTENCE citing the label means, and what state that pointer is in, is `QB5a` and `QB5b`. Float NUMBERING is assigned by order of appearance across the whole document, which is `QB9a`.

## Content
### Two fields, two different jobs
- the caption
  Prose, in the paper's voice, doing work the picture cannot: naming what the reader should take away, not describing what is drawn. A caption that restates the axis labels has spent a float and said nothing. It is also the only part of a display most readers read.
- the label
  A stable promise. Every `\ref{}` in every section depends on it, so it survives a re-render, a promotion, a change of renderer and a change of file path. `QB5a`'s law states the consequence: a sentence points at the UNIT, never at a file.

### Where they are supposed to be authored
`QB5@display` names the home: a `### Wrapper` block on the matching `S-Display-N` page. On this paper that home does not exist. All twelve display pages carry `### What it shows` and a `Registry id` line; **none has a `### Wrapper` block**, so every caption and label was authored directly into `displays/*/float.tex`, which is the file the ruling says a renderer may only serialize into.

That is not a small drift. It means the caption has no decision record: nothing says who approved this wording, or what the earlier one was.

### What a label promises, stated so it can be broken
A label is the only part of a display that other files depend on. Two consequences follow: renaming one is a breaking change across the manuscript, and two units may never declare the same label.

This paper breaks the second today. `displays/Table/table1-agreeableness-distribution` declares `\label{tab:distribution}` while `display09-agreeableness-distribution` declares `\label{tab:agreeableness-distribution}`, and §4 inputs the first while citing the second. The section therefore cites a label that nothing it reaches declares.

## Items to Finish
- [ ] ✍️ State what a caption must do for this venue
      Not a template. The test a caption passes or fails, written so CHECK can apply it without judgement.
- [ ] 🏠 Create the `### Wrapper` block the ruling already requires
      `QB5@display` says it lives on the `S-Display-N` page. Twelve pages, zero blocks. Until it exists, a caption has no decision record and no history.
- [ ] 🔒 Rule that a label is a breaking change, and that two units may never share one
      The second half is violated on this paper by the legacy `Table/` folder against `display09`.

## Where we are
Ownership is settled upstream, the content rules are unwritten, and the ruled home for the fields is absent from every display page on this paper. Captions live only in `float.tex`, hand-written.

Reframed 2026-07-27. This face was briefly "the wrapper: caption, label and placement" and carried three fields. Placement moved out to `QB5f`, because where a float lands is decided by which section cites it first and has nothing to do with what the caption says.

## Files
- `displays/*/float.tex`
  Where caption and label actually live today, written by hand.
- `0-lifecycle/3-display/S-Display-*.md`
  The twelve pages that should carry `### Wrapper` and do not.

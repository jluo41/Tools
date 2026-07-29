# Wrapper and placement
state: ✅ SETTLED
owner: JL
method: let the consumer own visual meaning while a renderer may serialize only approved fields

## Question
Who owns `float.tex`, its caption, label, and placement?

For a paper, the matching `S-Display-N` page owns those semantic fields in `### Wrapper`.
The renderer can serialize them mechanically but cannot invent or revise them.

## Diagram
```text
S-Display-N ### Wrapper                 renderer
caption · label · placement  ───────►   float.tex
                                           │
                                           └── references assets/<selected visual>
```

## Content
### Meaning remains on the Paper side
Caption text, stable label, float placement, unit identity, and citing sentence express the paper's argument.
They are not rendering parameters that a visual generator should infer.

### Finalization has a gate
Candidates can exist without a wrapper.
Finalization requires approved wrapper fields and preserves a hand-edited existing wrapper.

## Items to Finish
- [x] 🏷️ Define a canonical Paper wrapper source
      The `### Wrapper` block records literal caption, label, and placement.
- [x] 🛑 Prevent renderer-authored semantics
      The generic contract allows only asset-reference maintenance from caller-supplied fields.

## Where we are
The illustration helper requires explicit wrapper flags for a display-unit finalization.

## Files
- `paper/1-lifecycle/4-display/ref/paper-adapter.md`
  Paper wrapper ownership.
- `paper/1-lifecycle/haipipe-paper-stage/stages/4-display/template.md`
  The `### Wrapper` record.

## Law
Law: The renderer writes a wrapper only from consumer-approved meaning.

## Log
260727 · Resolved the former ambiguity between generic rendering and Paper-owned caption semantics.

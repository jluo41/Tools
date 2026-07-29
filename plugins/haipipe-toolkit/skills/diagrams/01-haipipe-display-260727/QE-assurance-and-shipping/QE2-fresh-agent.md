# Fresh-agent acceptance
state: ✅ SETTLED
owner: JL
method: test the contracts with a new context that has not participated in their design

## Question
Can a fresh agent follow the Display route without inventing a source, wrapper, or task?

Yes for the validated paper case: an existing approved aggregate starts at Paper Display, materializes Intake, and then reaches a named renderer.

## Content
### What the test must show
The agent distinguishes a missing aggregate from an existing one.
It refuses raw or unverified inputs.
It creates or resolves the S page and unit before rendering.
It treats wrapper semantics as Paper-owned.

### What has been observed
Independent fresh-context agents traced the forest-plot route.
They correctly started at Paper Display when the summary CSV and provenance already existed.
They also surfaced the known `QB2b@paper` per-unit Display-stage migration seam instead of silently ignoring it.

## Items to Finish
- [x] 🧪 Validate the Intake and wrapper contract with a fresh context
      Two independent agents traced Task → Intake → renderer → wrapper → sentence.
- [x] 🚧 Record the remaining migration seam
      The temporary explicit per-unit `create-page.py` route is documented until `QB2b@paper` is resolved.

## Where we are
The current contract passes the realistic existing-aggregate scenario without giving a renderer access to raw task data.

## Files
- `paper/1-lifecycle/4-display/ref/paper-adapter.md`
  Executable Paper-side route.
- `display/ref/display-intake-contract.md`
  Renderer-side refusal boundary.

## Law
Law: A display design is not complete until a fresh agent can follow its boundaries without help.

## Log
260727 · Fresh-context validations passed during the Intake and wrapper design work.

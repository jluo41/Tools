# Blueprint · Constitution

## A01 · Blueprint has a work-kind entry and composes the shared levels

> “那就比如说它有 Workflow for Blueprint”
> “那它们各自是不是应该也有自己的 skill？”

Source: the user's design request, 2026-11-27; implementation approved with
“OK好，那你开始去执行吧。” after the file plan.

**Rule:** Blueprint coordinates reusable tool, skill and workbench development.
Its record formats and execution gates remain with the shared level owners.
A responsibility such as UI implementation does not itself declare a Job type.

**Check:** A request to change a tool's behavior identifies its Blueprint owner,
affected contract, implementation, example and acceptance case. An ordinary
execution request routes to its work kind without creating a Blueprint.

## A02 · The definition and its example use the same framework

**Rule:** Follow PRINCIPLE.md's Work Folder, Work UI, Define Folder and Define UI
relationship. Reuse the shared Block renderer and real file readers. A contract
change names the affected definition and example; a validation repeats its actual
case. A skill-only edit does not demand unrelated page changes.

**Check:** A page change works inside its owning Block and reads the same source
as its example. A skill correction passes a realistic fresh-context exercise.
The trace records the guard, outcome and any unresolved part before closure.

**Validation:** Follow the root README's skill-development validation and the
owning UI skill's live-page checks; keep results in the Blueprint Trace.

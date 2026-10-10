# Build or drop the placeholder views?
state: 🟡 DRAFT · written by g02 2026-10-09 from the rail change and the re-shot screens; CHECK pending
answers: Q05
answer-status: answered
results-read: 2026-10-09T10:35:00-04:00

## Opening

Hide what is not built. A view that is only a placeholder at a scope leaves the rail and the tab strip at that scope,
and the agent cannot open it there; it comes back the day it is built. Nothing new was built under this Question.

**Where this Page sits:** [Q05 · Seven views are a placeholder at Group scope (Raw, Source, Record, Internal, External, Model, Checklist), and Internal and External at Individual too. Which are built next, and which leave the rail at that scope? (Evidence: studio s11, s12.)](../../j02_console.md).

**Why it matters:** A rail of placeholders tells a reader the console does more than it does.

## Content

### Answer

One list says where each view is a placeholder: `PLACEHOLDER` in `web/src/views.ts`. Hidden at Group: Raw, Source,
Record, Internal, External, Model, Checklist. Hidden at Individual: Internal, External, and Annotate (at Individual it
is the "apply a guideline" placeholder; its forge is built at Group). The rail drops them, switching scope closes
their tabs, and `view/open` or `highlight/set` on one returns "not built at this scope", for a click and for the agent
alike. Building one means deleting its scope from the list.

### Evidence

- The drawing: [s11 · the Group scope](../../studio/s11-group-scope/s11-group-scope.excalidraw): the Group rail now
  lists Case, Tasks, Annotate and Health; s12 lists the Individual side.
- The list: [views.ts](../../../../../plugins/inlab-human/servers/haichat-inlab/web/src/views.ts); the generated
  [10-ui-elements.txt](../../../../../plugins/inlab-human/servers/haichat-inlab/diagram/10-ui-elements.txt) names where
  each view is hidden.

### Limits

- Internal and External are hidden at both scopes, so the Insight group shows only Model and Tasks.
- The placeholder text in `Console.tsx` stays, unreachable, so a view brought back before it is built still says what
  it will hold.

### Next

Build Internal first (the per-patient insight cards it promises), then bring it back to the Individual rail.

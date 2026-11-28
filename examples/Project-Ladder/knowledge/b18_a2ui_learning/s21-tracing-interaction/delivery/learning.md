# Tracing a User Interaction

## Follow one round trip

Use the flight-booking example in [Resource 1](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md). Follow the value rather than treating every screen change as a new agent response.

1. **Locate the surface.** Identify its component IDs and the passenger-count binding.
2. **Change the count.** In the documented example, tapping the increment control writes the new value locally; bound widgets update without sending that edit to the agent.
3. **Confirm the choice.** The explicit confirmation button resolves its action context using current data values and sends an action message.
4. **Separate response from assumption.** A subsequent server response is a separate observation. Do not infer that it happened merely because the local count changed.

See [Resource 4](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md) for event actions and local functions. The event payload identifies the action, originating surface and component, and resolved context. Not every interaction has to make a server round trip.

## An observation sheet

This is a worked reasoning exercise; the expected observations below are not execution receipts.

| Step | Expected observation | What it would establish |
|---|---|---|
| Increase passenger count | Bound count changes locally | Data binding responds to the edit |
| Confirm booking | Action contains the current count | Explicit trigger carries the resolved context |
| Receive a later update | The addressed surface changes | A response was applied to the intended interface |

## Compare two debugging routes

- **Start at the screen:** useful for noticing the wrong value, but insufficient to locate its cause.
- **Trace the boundaries:** compare model value, binding path, outgoing action, and incoming response. This separates a display problem from an action-context problem.

## Try explaining

The count changes on screen, but the agent receives no message. Give one case where that is correct and one case where it suggests a bug. Name the additional observation that distinguishes them.

For a later fixed-message practice, reuse this observation sheet in a Job. Record the inputs and actual outputs there; keep the explanation here.

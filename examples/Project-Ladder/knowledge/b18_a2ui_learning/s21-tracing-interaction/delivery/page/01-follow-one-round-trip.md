# Follow one round trip

Use the flight-booking example in [Resource 1](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md). Follow the value rather than treating every screen change as a new agent response.

1. **Locate the surface.** Identify its component IDs and the passenger-count binding.
2. **Change the count.** In the documented example, tapping the increment control writes the new value locally; bound widgets update without sending that edit to the agent.
3. **Confirm the choice.** The explicit confirmation button resolves its action context using current data values and sends an action message.
4. **Separate response from assumption.** A subsequent server response is a separate observation. Do not infer that it happened merely because the local count changed.

See [Resource 4](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md) for event actions and local functions. The event payload identifies the action, originating surface and component, and resolved context. Not every interaction has to make a server round trip.

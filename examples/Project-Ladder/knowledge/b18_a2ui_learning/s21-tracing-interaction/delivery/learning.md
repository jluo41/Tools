# Tracing a User Interaction

## Where you start

**Follow one value through the flight booking, not every change on screen.**

- ✈️ The example: two flight cards and a Confirm booking button ([Resource 1](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md)).
- 🔢 The value to follow: the outbound passenger count, `/outbound/pax`.
- ⚠️ A worked reasoning exercise: the observations below are expected, not recorded.

## 1. Locate the surface

**Find the card, then the path it is bound to.**

- 🆕 The surface: `"flight-booking-surface"`
- 🧱 The component: `FlightCard` with the ID `flight_outbound`
- 🔗 Its binding: `passengers ← /outbound/pax`

✅ **You know it when:** you can point at the path the count reads.

## 2. Change the count

**Tapping + writes the value on the device; nothing is sent.**

- 👆 The user taps + on the outbound card.
- 🏠 The renderer writes `/outbound/pax = 2` into its own data model.
- 🔄 Every widget bound to that path updates in place.
- 📵 The agent hears nothing.

✅ **You know it when:** you can say why the screen changed without a message.

## 3. Confirm the choice

**Only an explicit tap sends something to the agent.**

- 👆 The user taps Confirm booking.
- 🔢 The button resolves its context from the current data: `outboundPax: 2`.
- 📤 The renderer sends an `action` message: the event name, the surface, the component and that context.

🔍 **Look for:** event actions and local functions in [Resource 4](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md)

✅ **You know it when:** you can name the one message that leaves the device.

## 4. Separate response from assumption

**A reply from the server is a separate thing to see.**

- 📥 A later update from the server is its own observation.
- ⚠️ Do not assume it happened because the count changed on screen.

## 5. Record what you observe

**One row per step: what you expect, and what it would prove.**

| Step | 👀 Expected | ✅ It would show |
|---|---|---|
| 👆 Raise the count | the count changes on the device | the binding responds to the edit |
| 📤 Confirm booking | the action carries the current count | the tap sends the resolved context |
| 📥 A later update | the addressed surface changes | the response reached the right interface |

## 6. Trace the boundaries, not the screen

**Compare what crosses each boundary.**

- 👀 Starting at the screen shows that a value is wrong, not why.
- 🔍 Compare the data value, the binding path, the outgoing action and the incoming response.
- 🧩 That tells a display problem apart from an action-context problem.

## Try explaining

**The count changes on screen, but the agent gets no message.**

- ✅ Give one case where that is correct.
- 🐞 Give one case where it points to a bug.
- 🔍 Name the extra observation that tells them apart.

🧪 For a later fixed-message practice, reuse the table of step 5 in a Job; keep the explanation here.

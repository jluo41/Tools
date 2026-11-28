# 3. Confirm the choice

**Only an explicit tap sends something to the agent.**

- 👆 The user taps Confirm booking.
- 🔢 The button resolves its context from the current data: `outboundPax: 2`.
- 📤 The renderer sends an `action` message: the event name, the surface, the component and that context.

🔍 **Look for:** event actions and local functions in [Resource 4](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md)

✅ **You know it when:** you can name the one message that leaves the device.

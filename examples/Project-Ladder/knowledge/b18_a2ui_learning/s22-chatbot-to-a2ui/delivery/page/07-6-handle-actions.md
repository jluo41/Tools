# 6. Handle actions

**A tap on a button reaches your agent; a local edit does not.**

- 👆 **A button:** the renderer sends an `action` message (e.g. `confirm_booking` with the passenger counts).
- 📤 Your server hands it to the agent, which answers with new text and, if needed, new messages.
- 🏠 **A local edit** (the passenger count) needs nothing from the agent.
- 📂 **In Travel A2UI:** the agent in `apps/server/src/travel_a2ui/brain/` receives the event.

✅ **You know it when:** you can say which taps reach the agent and which stay on the phone.

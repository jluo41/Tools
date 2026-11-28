# 6. Handle actions

**Change:** a tap on a button reaches your agent.
**Tool:** the renderer sends an `action` message (for example `confirm_booking` with the passenger counts); your server
hands it to the agent, which answers with new text and, if needed, new messages. Local edits, such as changing the
passenger count, need nothing from the agent.
**In Travel A2UI:** the agent in `apps/server/src/travel_a2ui/brain/` receives the event.

# Q · the cost of reconnecting an Agent SDK client per request

Using the Python package `claude_agent_sdk` and its `ClaudeSDKClient`, measure
two arrangements answering the SAME short prompt, three turns each:

- A · a client opened and closed inside each request, one connect per turn
- B · one client held open across all three turns, in streaming input mode

For each arrangement and each turn, report:

- seconds from send to the first token
- the total cost in USD carried by the result message
- the number of skills loaded at connect time, if the SDK reports it

Also report the model, the machine, the date, and the script that produced the
numbers, and keep the script.

Deliverable: a QA digest plus the raw per-turn timings.
Accepted: six timings and six costs, with the script named.

---
status: fixed
created: 2026-06-22
context: haipipe-paper orchestrator + haipipe-paper-enter
fixed_in: "haipipe-paper-enter v2.1.0 + haipipe-paper v2.0.0"
---

The orchestrator spec says every specialist dispatch should end with a structured tail block:

```
status:    ok | blocked | failed
summary:   ...
artifacts: [...]
next:      ...
```

In practice, the `enter` dashboard rendered the full paper session panel but did NOT output this tail. The orchestrator step 5 says "Capture the specialist's structured tail (status / summary / artifacts / next), present it." Without the tail, the orchestrator cannot machine-read the result, and the user cannot see the routing state at a glance.

The fix should be in haipipe-paper-enter's output format: always append the tail after the dashboard panel. The orchestrator should also enforce that it presents the tail, not silently swallow it.

Fix:

# 2. Generate the skill and add it to the prompt

**Change:** your prompt gets one more part.
**Tool:** the Agent SDK's skill generator (`SkillGenerator`; inside the SDK, `PromptGenerator`). It reads the catalog
and writes a Markdown skill: the Express grammar and one signature per component, such as
`FlightOption(airline, departTime, arriveTime, origin, destination, price, action, ...)`.
**In Travel A2UI:** `scripts/build_skills.py` writes `skills/` (`a2ui-core` teaches the notation, `a2ui-travel` this
catalog). Rerun it when the catalog changes.
Your own instructions and tools, for example a flight search, stay as they are.

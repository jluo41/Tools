# 2. Generate the skill and add it to the prompt

**Your prompt gets one more part; you do not write it by hand.**

- ✏️ **Change:** add the generated skill beside your own instructions and tools.
- 🧰 **Tool:** the Agent SDK's `SkillGenerator` (inside it, `PromptGenerator`) writes a Markdown skill from the catalog.
- 📄 **What it teaches:** the Express grammar, and one signature per component, e.g. `FlightOption(airline, departTime, arriveTime, origin, destination, price, action, ...)`.
- 📂 **In Travel A2UI:** `scripts/build_skills.py` writes `skills/`; rerun it when the catalog changes.

✅ **You know it when:** you can point at where the skill joins your prompt.

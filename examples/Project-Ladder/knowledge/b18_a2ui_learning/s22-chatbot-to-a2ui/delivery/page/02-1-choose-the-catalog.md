# 1. Choose the catalog

**Decide which components the agent may draw.**

- ✏️ **Change:** pick the components and functions the app allows.
- 🧰 **Tool:** the Basic Catalog, built into every official renderer: `Text`, `Row`, `Column`, `List`, `Button`, `TextField` and more.
- 📂 **In Travel A2UI:** `catalogs/a2ui-travel/catalog.json` adds `FlightOption`, `HotelCard`, `DateRangePicker`, `PriceSummary`.
- 🛡️ The catalog is the guardrail: the agent can only ask for what the app can draw.

✅ **You know it when:** you can list the components your first screen needs, and which are already basic.

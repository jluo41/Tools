# 1. Choose the catalog

**Change:** decide which components the agent may draw.
**Tool:** the Basic Catalog, built into every official renderer: `Text`, `Row`, `Column`, `List`, `Button`,
`TextField` and more. Start with it; write your own `catalog.json` only when you need a component it lacks.
**In Travel A2UI:** `catalogs/a2ui-travel/catalog.json` adds `FlightOption`, `HotelCard`, `DateRangePicker` and
`PriceSummary` to the basic ones. The catalog is the guardrail: the agent can only ask for what the app can draw.

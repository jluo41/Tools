# What the compiler does

**Four jobs, as the tokens arrive.**

1. 🔀 Split the chat text from the `<a2ui>` block.
2. 🧩 Parse each statement once it is complete.
3. 🛡️ Check it against the catalog; reject a component or property the catalog does not allow.
4. 🏷️ Give every component an ID and split the result into messages: 🆕 `createSurface`, 🧱 `updateComponents`, 🔢 `updateDataModel`.

# 2. Change the count

**Tapping + writes the value on the device; nothing is sent.**

- 👆 The user taps + on the outbound card.
- 🏠 The renderer writes `/outbound/pax = 2` into its own data model.
- 🔄 Every widget bound to that path updates in place.
- 📵 The agent hears nothing.

✅ **You know it when:** you can say why the screen changed without a message.

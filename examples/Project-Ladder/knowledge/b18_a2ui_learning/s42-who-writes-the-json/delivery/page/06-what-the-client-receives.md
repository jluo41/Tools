# What the client receives

**Only the JSON messages.**

- 📥 The renderer gets `createSurface`, `updateComponents`, `updateDataModel`, and the chat text.
- 🙈 It never sees Express.
- 📱 It builds the surface from the messages and keeps the data model live.

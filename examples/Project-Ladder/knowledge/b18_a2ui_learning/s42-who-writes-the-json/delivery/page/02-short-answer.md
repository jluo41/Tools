# Short answer

**In between: the model writes text in a fixed format; your server turns it into JSON.**

- 💬 **The model:** writes text, plus a block between `<a2ui>` and `</a2ui>` in A2UI Express.
- ⚙️ **The Agent SDK's compiler, on your server:** parses the block, checks it against the catalog, emits the JSON messages.
- 🚫 **Not guessing:** it is not free prose turned into JSON afterwards.
- 🧩 **Also possible:** the model writes the JSON directly; Express is shorter.

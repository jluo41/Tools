# 2. Read the components and the catalog

**Components are the pieces; the catalog says which pieces exist.**

- 🧱 Each component has an ID and names its children by ID, starting from `root`.
- 📋 The app owns the catalog; the agent can only compose from it.
- 📱 The renderer turns each component into a native widget.

🔍 **Look for:** `"component": "FlightCard"` and its `children` list ([Resource 1](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md))

✅ **You know it when:** you can draw the tree `root` › Column › FlightCard from the message.

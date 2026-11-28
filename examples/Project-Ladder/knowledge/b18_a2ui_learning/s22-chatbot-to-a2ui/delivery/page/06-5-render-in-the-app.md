# 5. Render in the app

**The app hosts a renderer in one region of the screen.**

- ✏️ **Change:** add a surface; navigation and chat stay your own code.
- 🧰 **Tool:** a Renderer SDK: `@a2ui/react`, `@a2ui/lit`, `@a2ui/angular`, `a2ui_flutter`, SwiftUI, Jetpack Compose.
- 🔢 It applies `createSurface`, `updateComponents`, `updateDataModel` and keeps bound values live.
- 📂 **In Travel A2UI:** `renderers/react/` and `renderers/flutter/`, used by `apps/web/` and `apps/flutter/`.

✅ **You know it when:** you can show where on your screen the surface sits.

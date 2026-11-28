# 5. Render in the app

**Change:** the app hosts a renderer in one region of the screen, the surface. Navigation and chat stay your code.
**Tool:** a Renderer SDK: `@a2ui/react`, `@a2ui/lit`, `@a2ui/angular`, `a2ui_flutter`, SwiftUI or Jetpack Compose.
It applies `createSurface`, `updateComponents` and `updateDataModel` and keeps bound values live.
**In Travel A2UI:** `renderers/react/` and `renderers/flutter/`, used by `apps/web/` and `apps/flutter/`.

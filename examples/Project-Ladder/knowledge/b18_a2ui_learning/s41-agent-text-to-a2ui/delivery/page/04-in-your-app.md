# In your app

1. **A renderer** for your platform: Flutter, Web (React, Lit, Angular), SwiftUI or Compose.
2. **A surface**: one region of the screen the renderer draws. Navigation and chat stay your own code.
3. **Actions back**: a tap on a button sends an `action` message to the agent. Editing a bound value, such as the
   passenger count, changes only the local data model and sends nothing.

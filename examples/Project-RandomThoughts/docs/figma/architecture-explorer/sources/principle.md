# Principle: how a plugin is designed

A plugin is two systems and the map between them. Design every plugin in this order.

1. **File System**: decide what folders the work is stored in.
   - Skill folders: what an agent knows how to do.
   - Block folders: each Block holds three kinds of numbered folders, side by side.
     - `jNN` Job: the work, Job ▶ Task ▶ Run ▶ Result.
     - `sNN` Studio: a topic thought through and drawn.
     - `cNN` Chat: one chat session, numbered in time order, naming the folders it changed.
2. **UI System**: decide how a page shows those folders; it shows nothing that is not on disk.
3. **The map**: every folder kind has a page part, every page part draws a folder.
   - Folder, Element and Session views each reach the other two.
4. **The rule**: a change to one side changes the other in the same change.

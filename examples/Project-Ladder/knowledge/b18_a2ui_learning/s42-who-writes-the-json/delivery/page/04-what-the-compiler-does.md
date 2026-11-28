# What the compiler does

It parses the block, rejects a component or property the catalog does not allow, gives every component an ID and
splits the result into messages: `createSurface`, then `updateComponents` for the layout and `updateDataModel` for the
values.

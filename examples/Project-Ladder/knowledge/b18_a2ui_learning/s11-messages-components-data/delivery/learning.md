# Messages, Components and Data

## Three things to distinguish

**A message changes a surface.** `createSurface` establishes it, `updateComponents` supplies component definitions, `updateDataModel` changes values, and `deleteSurface` removes it. A surface identifies the interface being updated. [Resource 2](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md)

**A component describes a piece of the interface.** IDs connect components into a hierarchy. The client resolves permitted component types through its catalog and renders native widgets. The app supplies that catalog; the agent composes within it. [Resource 1](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md)

**The data model holds values.** A binding references a path instead of embedding a fixed value in a component. A value change can therefore update the bound presentation without replacing the whole component description. [Resource 3](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md)

![Resource 3 · Data binding: one value, bound to a heading and an editable field](../../s01-official-sources/assets/resource-3.png)

## A small thought experiment

Imagine a trip card with a passenger count. The card's component definition establishes where the count appears. The data model holds the count itself. Increasing it from one to two changes the value; it need not change the card's identity.

This is a conceptual example, not a captured Run or a complete protocol payload.

| Question | Look at |
|---|---|
| Which interface changes? | Surface ID |
| Which widget and position? | Component IDs and relationships |
| Which value is displayed? | Data path and current value |
| Which widgets are allowed? | The application's catalog |

## Compare two explanations

- **Layout-only explanation:** “The agent sends a card.” This misses where its changing values live.
- **Structure-and-data explanation:** “The renderer resolves the card structure and its bound values.” This predicts why an existing card can update.

## Try explaining

Sketch a label showing a selected destination. Change only the selected value. Point to the part of the sketch that changes and the part that stays the same. Then explain how removing the whole surface differs from changing a value.

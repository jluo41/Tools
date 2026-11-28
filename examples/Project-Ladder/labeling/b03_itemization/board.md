# b03 · Itemization

board-kind: labeling-board
spine: Turn a source snapshot into reusable items without choosing a downstream label.
close: The Block design and its embedded interactions are reviewed.

labeling-block-type: itemization
preview-only: true
preview-entry: delivery/ui/block.html

## Topic

Turn a source snapshot into reusable items without choosing a downstream label.

## UI ownership

This independent Block owns one workbench entry. Jobs and Tasks are embedded selections; their names never become separate page titles or links. The model and rendered page are synthetic design examples, not production execution records.

## Handoffs

Source snapshot and an accepted item recipe → Items package with stable IDs, context and source references.

## Files

- `delivery/ui/model.json`: this Block's synthetic records.
- `delivery/ui/block.html`: the Block-owned interactive preview, also used inline in the conversation.

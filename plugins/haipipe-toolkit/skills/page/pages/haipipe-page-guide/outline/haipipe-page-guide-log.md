# haipipe-page-guide · log
page: haipipe-page-guide
kind: log · authored · append-only change history; no inferred human approval

### 260912 1358 · Replace the custom HTML entry with the standard Page Face and prepare an unapproved outline for review
User correction: “我的意思是 apply 我们的这个 skill 来做这个page啊，不是你随便写一个呀。”

The existing Folder is retained. The earlier HTML remains at its original materials path but is no longer bound by page.toml.
The Page Face uses the Page template, shared renderer, and real Outline records instead of an independently designed HTML surface.
The initial Page draft is not an approved Content release. Outline v0.1 records its proposed reader path; no approved or accepted tick is supplied.
The independent server remains read-only. Source and Outline/Evidence are available in its existing runtime; full standalone Studio/Runs/Delivery/Folder integration remains unmet.

### 260912 1624 · Add the standalone category-plugin pane
User request: “Could you add the plugin as what we do in the board page plugin as well?”

The standalone host now presents Outline, Runs, Delivery, and Folder in the canonical Page-plugin order. Each row reaches a real read-only presenter over the same Page Folder; Evidence remains inside Outline. Studio is omitted because standalone does not yet own its chat/draw backend. Read-only hosting removes the Source editor-shaped surface instead of showing disabled editing controls.

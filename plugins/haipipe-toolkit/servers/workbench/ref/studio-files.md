# Studio: its files and routes

Part of the [Workbench base README](../README.md).

| File | Responsibility |
|---|---|
| [xcal.py](../studio/xcal.py) | `/_board/excalidraw` editor routes, scene minting (`mint_board_scene`) and `/_board/excalidraw-save`. |
| [excalidraw_proxy.py](../studio/excalidraw_proxy.py) | Proxy to the local Excalidraw service; injects [assets/xcal-boot.js](../assets/xcal-boot.js), which arms a save only after the first gesture. |
| [autodraw.py](../studio/autodraw.py) | `/_board/autodraw`: `claude -p` authors a scene from the Page's `.md`. |
| [chat.py](../studio/chat.py), [turnring.py](../studio/turnring.py) | The GUI chat: the SDK turn and the turn ring; `chat_permissions`, `chat_context`, `chat_rules`, `chat_transcript`, `chat_host` and `chat_sessions` beside it hold the tool tiers, context priming, rule texts, transcripts, held clients and sessions. |
| [term.py](../studio/term.py) | The TUI: PTYs, parking, and the vendored xterm under `assets/vendor/xterm/`. |
| [autodeck.py](../studio/autodeck.py) | `/_board/autodeck`: `claude -p` authors the Page's slide deck. |
| `assets/js/10-drawer/`, `assets/css/86-*.css` | Drawer parts, concatenated into `board.js` / `board.css` by `_host/host_assets.py`. |

Its routes form the `shared` row of `_host/host_registry.WORKBENCH_ROUTES`;
a `--only` host without `shared` serves no terminal, chat or drawing save.
The lane contracts are [ref/draw.md](../../../skills/1_base/project/haipipe-studio/ref/draw.md)
and [ref/chat.md](../../../skills/1_base/project/haipipe-studio/ref/chat.md).

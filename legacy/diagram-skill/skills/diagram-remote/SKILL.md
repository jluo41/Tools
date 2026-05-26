---
name: diagram-remote
description: Open a local .excalidraw file on the self-hosted Excalidraw server (draw.jjluo.com). Uploads the file content and opens the board URL. The board name is derived from the file path with / replaced by --.
---

# diagram-remote

Open a local `.excalidraw` file in the self-hosted Excalidraw server and return a shareable board URL.

## Usage

```
/diagram-remote Tools/plugins/research-toolkit/diagram/canvas-260425.excalidraw
```

The file path can be absolute or relative to the current working directory.

---

## Steps

**1. Resolve the file path**

Make it absolute. If a relative path is given, resolve against the current working directory.

**2. Derive the board name**

- Strip the `.excalidraw` extension
- Replace every `/` (and `\`) with `--`
- Lowercase optional — preserve original casing

Examples:
```
canvas.excalidraw
  → canvas

Tools/plugins/diagram/canvas-260425.excalidraw
  → Tools--plugins--diagram--canvas-260425

/Users/jluo41/work/research/arch.excalidraw
  → Users--jluo41--work--research--arch
```

**3. Upload the file to the server**

Run the upload helper (no extra dependencies required — uses Python stdlib only):

```bash
python3 ~/.claude/skills/diagram-remote/upload.py "<abs_file_path>" "<board_name>"
```

The script POSTs the raw `.excalidraw` JSON to the server's `/upload/<board_name>` endpoint, which handles encryption and board registration server-side. It prints the board URL on success.

**4. Open the board in the browser**

```bash
open "https://draw.jjluo.com/d/<board_name>"
```

**5. Report to the user**

Tell the user:
- Board name
- URL: `https://draw.jjluo.com/d/<board_name>`
- The board auto-saves on every Ctrl+S — the URL at `draw.jjluo.com/d/<board_name>` always opens the latest saved version
- Collaborators can join via Live Collaboration from within the app

---

## Server config (reference)

| Setting | Value |
|---|---|
| Local API | `http://localhost:3003` |
| Public URL | `https://draw.jjluo.com` |
| Upload endpoint | `POST /upload/<board_name>` |
| Board list | `https://boards.draw.jjluo.com` |

If the server is unreachable, tell the user to check `cd apps/excalidraw && docker compose up -d`.

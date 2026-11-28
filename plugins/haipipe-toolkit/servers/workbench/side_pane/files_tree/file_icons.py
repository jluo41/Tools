"""The one icon lookup every file tree shares (Files pane, Studio › Folder): a file's icon from its type.

A kind reads at a glance: words 📝, pictures 🖼️, drawings ✏️, tables of data 📊, code (Python's own mark, 💻), settings ⚙️, documents to
send 📕📘📙📗, anything else 📄. Folders keep the one folder drawing (ui_parts.FOLDER_ICON).
"""
from __future__ import annotations

from pathlib import Path

FILE_ICONS = {
    ".md": "📝", ".txt": "📄", ".log": "📄",
    ".excalidraw": "✏️",
    ".png": "🖼️", ".jpg": "🖼️", ".jpeg": "🖼️", ".gif": "🖼️", ".svg": "🖼️", ".webp": "🖼️",
    ".pdf": "📕", ".docx": "📘", ".pptx": "📙", ".xlsx": "📗", ".tex": "📜", ".bib": "📚",
    ".csv": "📊", ".tsv": "📊", ".parquet": "📊", ".sql": "🗄️",
    ".ipynb": "📓", ".r": "📈",                   # .py: FILE_MARKS (Python's own mark)
    ".js": "💻", ".ts": "💻", ".css": "💻", ".html": "🌐", ".htm": "🌐",
    ".sh": "▶️",
    ".yaml": "⚙️", ".yml": "⚙️", ".toml": "⚙️", ".ini": "⚙️", ".cfg": "⚙️", ".env": "⚙️",
    ".json": "🧾",
    ".eml": "✉️",
    ".zip": "🗜️", ".gz": "🗜️", ".tar": "🗜️",
    ".mp4": "🎬", ".mov": "🎬", ".mp3": "🔊", ".wav": "🔊",
}
DEFAULT_ICON = "📄"
# a type whose emoji is wrong or vague gets its real mark, drawn inline so it looks the same on every platform
PYTHON_ICON = ('<svg class="file-icon" width="14" height="14" viewBox="0 0 24 24" aria-hidden="true" focusable="false" '
               'style="vertical-align:-2px">'
               '<path fill="#3776AB" d="M11.9 2C7 2 7.3 4.1 7.3 4.1v2.2h4.7v.7H5.4S2 6.6 2 11.9s3 5.1 3 5.1h1.8v-2.5'
               's-.1-3 2.9-3h4.9s2.8 0 2.8-2.7V4.8S17.8 2 11.9 2zM9.2 3.6a.9.9 0 1 1 0 1.8.9.9 0 0 1 0-1.8z"/>'
               '<path fill="#FFD43B" d="M12.1 22c4.9 0 4.6-2.1 4.6-2.1v-2.2H12v-.7h6.6S22 17.4 22 12.1s-3-5.1-3-5.1h-1.8'
               'v2.5s.1 3-2.9 3H9.4s-2.8 0-2.8 2.7v4S6.2 22 12.1 22zm2.7-1.6a.9.9 0 1 1 0-1.8.9.9 0 0 1 0 1.8z"/></svg>')
FILE_MARKS = {".py": PYTHON_ICON}


def file_icon(path: Path) -> str:
    """The icon for one file, by its suffix: its real mark when it has one (HTML), else an emoji; a file of no known
    type gets 📄."""
    suffix = path.suffix.lower()
    return FILE_MARKS.get(suffix) or FILE_ICONS.get(suffix, DEFAULT_ICON)


# a trace's file states (one ring that fills as the work moves, an amber diamond for a file the plan left out) are the
# one table of state marks every page draws too (state_marks.py)
from live.state_marks import STATE_COLORS, STATE_MARKS, STATE_ORDER  # noqa: E402,F401

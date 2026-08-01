"""QC8 · the write path (QC7, QB5): a typed line under its anchor sentence.

Moved out of serve.py on 2026-07-31 under the gate_live.py response-identical gate.
QC3's Law: a refactor moves code, features never ride along.
"""

import base64
import datetime as dt
import difflib
import hashlib
import itertools
import json
import os
import re
import shutil
import signal
import socket
import sqlite3
import struct
import subprocess
import sys
import threading
import time
import urllib.parse
from pathlib import Path
from urllib.parse import unquote

from . import base
from .base import esc4re




class WriteMixin:
    # ---- the two writes ----------------------------------------------
    def add_sentence(self, f, p):
        """➕ on a sentence (QA8, JL 260725): insert `> Lane: text` directly under
        that sentence in the source md — the same line an author types by hand.
        Anchor rule = the comment layer's: exact sentence match, miss fails visibly."""
        lane = re.sub(r"[^A-Za-z0-9-]", "", p.get("lane") or "Note")[:12] or "Note"
        text = " ".join((p.get("text") or "").split())
        sent = " ".join((p.get("sentence") or "").split())
        if not sent or not text:
            return None, "sentence or text is empty"

        def plain(s):
            s = re.sub(r"`([^`]+)`", r"\1", s)
            s = re.sub(r"\*\*((?:(?!\*\*).)+)\*\*", r"\1", s)
            s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
            return " ".join(s.split())

        lines = f.read_text(encoding="utf-8").split("\n")
        fence, hit = False, None
        for i, ln in enumerate(lines):
            if ln.lstrip().startswith("```"):
                fence = not fence
                continue
            s = ln.strip()
            if fence or not s or s.startswith(("#", ">", "|")) or re.match(r"^[-*]\s", s):
                continue
            if plain(s) == sent:
                hit = i
                break
        if hit is None:
            return None, "这句话在源文件里没找到（可能已被改动）—— 没写入"
        j = hit + 1                      # append at the END of the existing apparatus run
        while j < len(lines):
            if lines[j].lstrip().startswith(">"):
                j += 1
                continue
            if (not lines[j].strip() and j + 1 < len(lines)
                    and lines[j + 1].lstrip().startswith(">")):
                j += 1
                continue
            break
        lbl = lane if re.fullmatch(r"[A-Z]{1,4}", lane) else lane[0].upper() + lane[1:].lower()
        lines.insert(j, f"> {lbl}: {text}")
        f.write_text("\n".join(lines), encoding="utf-8")
        return None, None

    @staticmethod
    def _plain_sentence(s):
        """The browser sends visible sentence text; source may have light md."""
        s = re.sub(r"`([^`]+)`", r"\1", s)
        s = re.sub(r"\*\*((?:(?!\*\*).)+)\*\*", r"\1", s)
        s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
        return " ".join(s.split())

    @classmethod
    def _sentence_line(cls, lines, sentence):
        """Find one editable source sentence, never guessing across duplicates."""
        wanted = cls._plain_sentence(sentence)
        hits, fence = [], False
        for i, ln in enumerate(lines):
            if ln.lstrip().startswith("```"):
                fence = not fence
                continue
            s = ln.strip()
            if fence or not s or s.startswith(("#", ">", "|")) or re.match(r"^[-*]\s", s):
                continue
            if cls._plain_sentence(s) == wanted:
                hits.append(i)
        if not hits:
            return None, "这句话在源文件里没找到（可能已被改动）—— 没写入"
        if len(hits) > 1:
            return None, "这句话在本页出现不止一次—— 为避免改错，没有写入"
        return hits[0], None

    @staticmethod
    def _apparatus_end(lines, sentence_line):
        """All adjacent `>` rows belong to the sentence immediately above."""
        j = sentence_line + 1
        while j < len(lines):
            if lines[j].lstrip().startswith(">"):
                j += 1
                continue
            if (not lines[j].strip() and j + 1 < len(lines)
                    and lines[j + 1].lstrip().startswith(">")):
                j += 1
                continue
            break
        return j

    @staticmethod
    def _change_diff(before, after):
        """Whole post-edit sentence, with only changed word runs marked."""
        old, new = before.split(), after.split()
        out = []
        for op, a0, a1, b0, b1 in difflib.SequenceMatcher(a=old, b=new).get_opcodes():
            if op == "equal":
                out.append(" ".join(new[b0:b1]))
            elif op == "delete":
                out.append("~" + " ".join(old[a0:a1]) + "~")
            elif op == "insert":
                out.append("*" + " ".join(new[b0:b1]) + "*")
            else:
                out.append("~" + " ".join(old[a0:a1]) + "~")
                out.append("*" + " ".join(new[b0:b1]) + "*")
        return " ".join(x for x in out if x)

    def save_image(self, board, p):
        """把浏览器里粘贴的图片存进这块板子的 fig/，返回相对路径（JL 260731）。
        只存文件，不碰任何 .md —— markdown 那一行随后走 /_board/discuss 或
        /_board/comment 落盘，所以这里也不用重建 html。"""
        m = re.match(r"^data:image/(png|jpeg|jpg|gif|webp);base64,(.+)$",
                     p.get("data") or "", re.S)
        if not m:
            return None, "不是可识别的图片（要 png/jpeg/gif/webp 的 data URL）"
        try:
            raw = base64.b64decode(m.group(2), validate=True)
        except Exception:
            return None, "图片数据解不开（base64 坏了）"
        if len(raw) > 8 * 1024 * 1024:
            return None, "图片超过 8MB —— 请压缩后再贴"
        stem = re.sub(r"[^a-z0-9-]+", "-",
                      (p.get("name") or "paste").rsplit(".", 1)[0].lower()
                      ).strip("-")[:40] or "paste"
        ext = {"jpeg": "jpg"}.get(m.group(1), m.group(1))
        fig = board / "fig"
        fig.mkdir(exist_ok=True)
        stamp = time.strftime("%y%m%d-%H%M%S")
        name, i = f"{stem}-{stamp}.{ext}", 2
        while (fig / name).exists():
            name = f"{stem}-{stamp}-{i}.{ext}"
            i += 1
        (fig / name).write_bytes(raw)
        return {"rel": f"fig/{name}"}, None

    def add_comment(self, f, p):
        who = re.sub(r"[^A-Za-z0-9]", "", p.get("who", "JL")).upper()[:4] or "JL"
        sentence = " ".join((p.get("sentence") or "").split())
        text = (p.get("text") or "").strip()
        when = p.get("when") or ""
        if not sentence or not text:
            return None, "句子或评论是空的"
        lines = f.read_text(encoding="utf-8").split("\n")
        hit, err = self._sentence_line(lines, sentence)
        if err:
            return None, err
        entry = f"> {who}: {text}" + (f" · {when}" if when else "")
        lines.insert(self._apparatus_end(lines, hit), entry)
        f.write_text("\n".join(lines), encoding="utf-8")
        return {"sentence": sentence}, None

    def edit_sentence(self, f, p):
        who = re.sub(r"[^A-Za-z0-9]", "", p.get("who", "JL")).upper()[:4] or "JL"
        before = " ".join((p.get("sentence") or "").split())
        after = " ".join((p.get("replacement") or "").split())
        when = p.get("when") or ""
        if not before or not after:
            return None, "原句或修改后的句子是空的"
        if before == after:
            return None, "句子没有变化—— 没写入"
        lines = f.read_text(encoding="utf-8").split("\n")
        hit, err = self._sentence_line(lines, before)
        if err:
            return None, err
        source_before = lines[hit].strip()
        # Replacing a markdown-decorated sentence from a browser's textContent
        # would silently erase its links/code/bold.  v1 is intentionally exact.
        if source_before != before:
            return None, "这句话带有 Markdown 格式；为避免丢格式，请先在源文件编辑"
        lines[hit] = after
        diff = self._change_diff(before, after)
        entry = f"> ✎ {diff} · {who}" + (f" · {when}" if when else "")
        lines.insert(self._apparatus_end(lines, hit), entry)
        f.write_text("\n".join(lines), encoding="utf-8")
        return {"before": before, "after": after, "diff": diff}, None

    def add_discuss(self, f, p):
        """往 ## Discussion 末尾追加一条自由想法（一整段 → 一条 > WHO: …）。
        跟 add_comment 一样跳 ``` 围栏找真的段；没有 ## Discussion 就在
        ## Log 前新建。不钉在某句话上 —— 就是自由讨论。"""
        who = re.sub(r"[^A-Za-z0-9]", "", p.get("who", "JL")).upper()[:4] or "JL"
        text = " ".join((p.get("text") or "").split())
        if not text:
            return None, "想法是空的"
        line = f"> {who}: {text}"
        t = f.read_text(encoding="utf-8")
        lines = t.split("\n")
        fence = False
        di = li = None
        for i, ln in enumerate(lines):
            if ln.lstrip().startswith("```"):
                fence = not fence
                continue
            if fence:
                continue
            if di is None and re.match(r"^## Discussion\b", ln):
                di = i
            if li is None and re.match(r"^## Log\b", ln):
                li = i
        if di is not None:                      # 追加到 ## Discussion 段末尾
            j = di + 1
            while j < len(lines) and not re.match(r"^## ", lines[j]):
                j += 1
            while j > di + 1 and not lines[j - 1].strip():   # 跳过段尾空行
                j -= 1
            lines.insert(j, line)
            t = "\n".join(lines)
        else:                                   # 没有就新建一段
            if li is not None:
                lines.insert(li, "## Discussion\n" + line + "\n")
                t = "\n".join(lines)
            else:
                t = t.rstrip("\n") + "\n\n## Discussion\n" + line + "\n"
        f.write_text(t, encoding="utf-8")
        return "ok", None

    def resolve(self, f, p):
        quote = " ".join((p.get("quote") or "").split())
        to = "x" if p.get("done") else " "
        t = f.read_text(encoding="utf-8")
        pat = re.compile(r"^(-\s*\[)[ xX](\]\s*[A-Z]{1,4}\d{0,4}\s*[「\"“]"
                         + esc4re(quote) + r")", re.M)
        if not pat.search(t):
            return None, "在这个文件里找不到那条评论（引文对不上）"
        f.write_text(pat.sub(r"\g<1>" + to + r"\g<2>", t, count=1), encoding="utf-8")
        return "ok", None

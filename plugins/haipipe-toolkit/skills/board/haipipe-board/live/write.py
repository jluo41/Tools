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
import pathlib
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

        # ONE matcher for every writer (QF5). This path used to carry its own
        # copy of the scan, which silently differed in the case that matters:
        # it took the FIRST of several identical lines instead of refusing, so
        # adding a lane to a repeated sentence could write it under the wrong
        # one. `_sentence_line` refuses, and now both paths refuse alike.
        lines = f.read_text(encoding="utf-8").split("\n")
        hit, err = self._sentence_line(lines, sent)
        if hit is None:
            return None, err
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
        rows = self._record_lines(f"> {lbl}: ", text)
        if not rows:
            return None, "内容是空的"
        if rows == lines[j - len(rows):j]:
            return None, "这条记录已经在这句话下面了—— 没重复写入"
        lines[j:j] = rows
        f.write_text("\n".join(lines), encoding="utf-8")
        return None, None

    def add_card(self, f, p):
        """🪪 a card on a SPAN of words (JL 260802, ruled on QB5 as option D).

        Writes `> Card <the words>: <text>` under the sentence, which is the
        same line an author types by hand. The record carries its own span, so
        the PROSE never gains a marker: a card is the only thing on a board
        that points INTO a sentence, and it still costs the sentence nothing.

        Two gates, both refusing rather than guessing. The sentence must be
        found exactly once, through the one shared matcher every writer here
        uses. And the span must actually occur in that source line: a card
        written against words that are not there would render as a loud miss,
        so it is cheaper to refuse at the keyboard than to ship a broken row.
        """
        span = " ".join((p.get("span") or "").split())
        text = " ".join((p.get("text") or "").split())
        sent = " ".join((p.get("sentence") or "").split())
        if not span or not text:
            return None, "span or text is empty"
        if ":" in span or "：" in span:
            # The grammar splits the record on its FIRST colon, so a span
            # holding one would be cut in half and silently point at a
            # different run of words.
            return None, "a card's words may not contain a colon"

        lines = f.read_text(encoding="utf-8").split("\n")
        hit, err = self._sentence_line(lines, sent)
        if hit is None:
            return None, err
        if span not in lines[hit] and span not in self._plain_sentence(lines[hit]):
            return None, f"“{span}” is not in that source line — nothing written"

        j = self._apparatus_end(lines, hit)
        rows = self._record_lines(f"> Card {span}: ", text)
        if not rows:
            return None, "内容是空的"
        if rows == lines[j - len(rows):j]:
            return None, "这张卡片已经在这句话下面了—— 没重复写入"
        lines[j:j] = rows
        f.write_text("\n".join(lines), encoding="utf-8")
        return None, None

    # Everything the RENDERER consumes has to be undone here, or the posted
    # string and the source line describe the same sentence and still differ.
    # Two rules, and which one applies depends on what the browser ends up with:
    #   KEEP the text  ->  the mark is decoration the reader still sees
    #   DELETE it      ->  the renderer replaced it with a control whose label
    #                      is not the source text, so the client posts nothing
    #                      for it and the source must lose it too
    _DIALECT = [
        re.compile(r"\\cite[tp]?\*?\{[^}]*\}"),            # \citep{smith2024}
        re.compile(r"\\(?:auto|C|c)?ref\{[^}]*\}"),         # \ref{tab:main}
        re.compile(r"\{VAL:[^}]*\}"),                       # {VAL:? the number}
        re.compile(r"\[Q-[A-Za-z0-9]+-\d+\]"),              # [Q-Sec6Results-4]
        re.compile(r"\bS-Display-\d+[a-z]?(?:[a-z]\d+)?\b"),
    ]

    @staticmethod
    def _record_lines(head, text, when=""):
        """One record, however many lines the person typed.

        A record is a `>` RUN, not a string: `> WHO: first` followed by bare
        `>` continuation lines, which `render_apparatus` already folds into the
        same lane (`body.py`'s `.lane-cont`). Writing the raw textarea value
        instead put a string containing newlines into one list slot, and the
        join then split it, so the second line of every multi-line comment
        escaped the record and landed in the page as PROSE: it rendered as a
        sentence, it became a new writable anchor, and it carried the timestamp
        away from the comment it belonged to (JL 260801).

        Collapsing the newlines instead, which the lane and discussion writers
        did, is not corruption but it silently destroys the paragraphing of
        anything anyone pastes. Continuations keep it.

        A leading `>` in the typed text is removed: `>>` means a REPLY BY
        SOMEONE ELSE in this grammar, and a paste must not be able to forge one.
        """
        raw = [ln.rstrip() for ln in (text or "").replace("\r\n", "\n").split("\n")]
        out, blank = [], False
        for ln in raw:
            ln = re.sub(r"^\s*>+\s*", "", ln).strip()
            if not ln:
                blank = bool(out)          # one break, never a run of them
                continue
            if not out:
                out.append(f"{head}{ln}" + (f" · {when}" if when else ""))
            else:
                if blank:
                    out.append(">")
                out.append(f"> {ln}")
            blank = False
        return out

    @staticmethod
    def _plain_sentence(s):
        """The browser sends visible sentence text; source may have light md."""
        s = re.sub(r"`([^`]+)`", r"\1", s)
        s = re.sub(r"\*\*((?:(?!\*\*).)+)\*\*", r"\1", s)
        s = re.sub(r"~~((?:(?!~~).)+)~~", r"\1", s)          # <del>: text kept
        s = re.sub(r"!\[([^\]]*)\]\([^)]*\)", "", s)        # <img>: no text at all
        s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
        for pat in WriteMixin._DIALECT:                     # chips: <button>, deleted
            s = pat.sub("", s)
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
        if hits and lines[hits[0]][:1].isspace():
            # An indented line belongs to the `- [ ]` item above it. Every
            # writer here works in whole lines, so a write would either strip
            # the indent (severing the explanation from its item, the one
            # SOURCE-CORRUPTING case in this file) or insert a `>` run at
            # column 0 that the item cannot render. Refuse, and say why.
            return None, "这行是某个 item 的说明行，改它会把它从 item 上扯下来—— 没写入"
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
    def _wdiff():
        """-> haipipe-writing's `wdiff` function, or None if it is not here.

        ONE COMPUTATION, NOT TWO THAT AGREE (JL 260802: "we also need to have a
        very good writing diff to track the changes along the way"). This file
        and `haipipe-writing/cli/wdiff.py` both computed the word-level diff
        with difflib, and on 260802 they produced byte-identical output on
        every case tried, which is agreement by luck rather than by
        construction: the next edit to either one splits them silently, and the
        `> ✎` record is a durable review trail.

        It is looked up rather than imported, because every unit in this family
        must stay deletable from every other. If `haipipe-writing` is not
        installed the local computation below still answers, and
        `tests/test_change_diff.py` fails the moment the two stop matching.
        """
        import importlib.util
        f = (pathlib.Path(__file__).resolve().parent.parent.parent
             / "haipipe-writing" / "cli" / "wdiff.py")
        if not f.exists():
            f = f.parent.parent.parent.parent / "writing" / "haipipe-writing" / "cli" / "wdiff.py"
        if not f.exists():
            return None
        try:
            spec = importlib.util.spec_from_file_location("_hw_wdiff", f)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            return getattr(m, "wdiff", None)
        except Exception:
            return None

    @classmethod
    def _change_diff(cls, before, after):
        """Whole post-edit sentence, with only changed word runs marked."""
        shared = cls._wdiff()
        if shared:
            try:
                return shared(before, after, host="board")
            except Exception:
                pass                      # fall through to the local copy
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
        rows = self._record_lines(f"> Comment {who} ", text, when)
        if not rows:
            return None, "评论是空的"
        at = self._apparatus_end(lines, hit)
        if lines[hit + 1:at] and rows == lines[at - len(rows):at]:
            # The identical record is already the last one on this sentence, so
            # this is a double-click or a replayed POST, not a second thought.
            return None, "这条记录已经在这句话下面了—— 没重复写入"
        lines[at:at] = rows
        f.write_text("\n".join(lines), encoding="utf-8")
        return {"sentence": sentence, "lines": len(rows)}, None

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
        # A SENTENCE comment is written `> Comment WHO …` since 260802. The
        # bare-initial form still parses, but it is not what to write, and
        # `check.py` warns on it inside Content: the engine must not produce
        # what the checker flags. `## Discussion` is untouched below, because
        # its `> JL:` / `>> CC0726:` thread grammar is a different thing.
        who = re.sub(r"[^A-Za-z0-9]", "", p.get("who", "JL")).upper()[:4] or "JL"
        # Same record grammar as a comment: a typed paragraph break survives as
        # a continuation instead of being flattened into one long line.
        rows = self._record_lines(f"> {who}: ", p.get("text") or "")
        if not rows:
            return None, "想法是空的"
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
            if rows == lines[j - len(rows):j]:
                return None, "这条想法已经在 ## Discussion 末尾了—— 没重复写入"
            lines[j:j] = rows
            t = "\n".join(lines)
        else:                                   # 没有就新建一段
            block = "## Discussion\n" + "\n".join(rows) + "\n"
            if li is not None:
                lines.insert(li, block)
                t = "\n".join(lines)
            else:
                t = t.rstrip("\n") + "\n\n" + block
        f.write_text(t, encoding="utf-8")
        return "ok", None

    def resolve(self, f, p):
        quote = " ".join((p.get("quote") or "").split())
        to = "x" if p.get("done") else " "
        t = f.read_text(encoding="utf-8")
        pat = re.compile(r"^(-\s*\[)[ xX](\]\s*[A-Z]{1,4}\d{0,4}\s*[「\"“]"
                         + esc4re(quote) + r")", re.M)
        hits = pat.findall(t)
        if not hits:
            return None, "在这个文件里找不到那条评论（引文对不上）"
        if len(hits) > 1:
            # Every other writer refuses an ambiguous match rather than take
            # the first (`_sentence_line`); this one kept a `count=1` and
            # silently flipped whichever row came first, answering ok.
            return None, "这条引文在本页出现不止一次—— 为避免改错，没有写入"
        f.write_text(pat.sub(r"\g<1>" + to + r"\g<2>", t, count=1), encoding="utf-8")
        return "ok", None

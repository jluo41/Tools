"""5 · Revise of the draft Task: which sentence a review line, a card, a check or a Flow line names (must-check M-D05).

A Draft numbered per paragraph repeats its bare ids (s1 in C1.P1, C2.P1 and C2.P2), so a bare id can name two
sentences. Every key here is then the full address (C2.P1.s1); a Draft whose bare ids are unique keeps the bare id
(s12) as before. The test for "repeats" is hai-draft's `src/page_renumber.py` `repeated()`, done here on the
Draft Lab's own parse of §3 (no skill import). draft_step_revise.py, draft_step_revise_notes.py and
draft_step_revise_history.py read sentences through `Keys`.
"""
from __future__ import annotations

import re
from pathlib import Path

from live.sentence_id import sid as _sid

ADDR = r"(?:C\d+\.P\d+\.)?[Ss]\d+[a-z]*"          # a sentence id, bare (s3) or by its full address (C2.P1.s3)
_HEAD = re.compile(r"^#{1,6}\s*(C\d+\.P\d+)\b")
_ROW = re.compile(r"^- B\d+[a-z]* · ([Ss]\d+[a-z]*) · (.*)$")


def section3(text: str) -> str:
    """A Draft file's `## 3 · …` text (its sentences), or the whole text when it has no such heading."""
    m = re.search(r"(?m)^## 3 ·", text)
    if not m:
        return text
    rest = text[m.end():]
    nxt = re.search(r"(?m)^## ", rest)
    return rest[:nxt.start()] if nxt else rest


def rows(text: str) -> list:
    """[(paragraph id, sentence id, words)] in reading order; a sentence above any `### C<n>.P<n>` heading has pid ""."""
    out, pid = [], ""
    for line in text.splitlines():
        h = _HEAD.match(line)
        if h:
            pid = h.group(1)
            continue
        m = _ROW.match(line)
        if m:
            out.append((pid, _sid(m.group(1)), m.group(2).strip()))
    return out


def same(a: str, b: str) -> bool:
    return " ".join((a or "").split()) == " ".join((b or "").split())


class Keys:
    """The sentences of one Draft and the key each is known by: its full address when the Draft repeats a bare id,
    else its bare id."""

    def __init__(self, d_or_rows):
        if isinstance(d_or_rows, dict):
            d_or_rows = rows("\n".join(b for _, b in d_or_rows.get("text", [])))
        self.rows = list(d_or_rows)
        bare = [s for _, s, _ in self.rows]
        self.rep = len(set(bare)) != len(bare)
        self.paras = list(dict.fromkeys(p for p, _, _ in self.rows if p))
        self.full = {}
        for p, s, w in self.rows:
            self.full.setdefault(f"{p}.{s}" if p else s, (p, s, w))
        self.first = {}
        for p, s, _ in self.rows:
            self.first.setdefault(s, f"{p}.{s}" if p else s)

    def key(self, pid: str, sid: str) -> str:
        return f"{pid}.{_sid(sid)}" if self.rep and pid else _sid(sid)

    def words(self) -> dict:
        """{key: the sentence's words now}, in reading order."""
        out = {}
        for p, s, w in self.rows:
            out.setdefault(self.key(p, s), w)
        return out

    def order(self) -> dict:
        """{key: its place in reading order}, with each bare id and full address of the sentence as well."""
        out = {}
        for i, (p, s, _) in enumerate(self.rows):
            for k in (self.key(p, s), f"{p}.{s}" if p else s, s):
                out.setdefault(k, i)
        return out

    def resolve(self, raw: str, words: str | None = None) -> str:
        """The key of the sentence `raw` names (s3, S3, C2.P1.s3), or "" when the Draft has none. A bare id on a Draft
        that repeats it names the one whose words are `words`, else the first."""
        raw = _sid((raw or "").strip())
        if "." in raw:
            if raw in self.full:
                p, s, _ = self.full[raw]
                return self.key(p, s)
            bare = raw.rsplit(".", 1)[1]
            return bare if not self.rep and bare in self.first else ""
        if raw not in self.first:
            return ""
        if not self.rep:
            return raw
        hits = [self.key(p, s) for p, s, w in self.rows if s == raw]
        if words is not None:
            hit = next((self.key(p, s) for p, s, w in self.rows if s == raw and same(w, words)), "")
            if hit:
                return hit
        return hits[0]

    def resolve_seq(self, raws: list, flows: list | None = None) -> list:
        """The keys of a review report's lines, read in their order: on a Draft that repeats bare ids, a bare id is the
        sentence of the paragraph its block's `Flow <k>:` line names, when the report gives each paragraph its own
        block; else the next sentence with that id at or after the paragraph of the line before it (the report reads
        the text in order), so `s1 … s10, s1 … s6` lands on C1.P1 and then C2.P1."""
        if not self.rep:
            return [self.resolve(r) for r in raws]
        flows = list(flows or [""] * len(raws))
        blocks = len(set(f for f in flows if f)) > 1
        out, at, used = [], 0, set()
        for raw, flow in zip(raws, flows):
            raw = _sid(raw)
            pid = self.flow_pid(flow) if blocks and flow and "." not in raw else ""
            if pid and f"{pid}.{raw}" in self.full:
                k = f"{pid}.{raw}"
                used.add(k)
                at = self.paras.index(pid)
                out.append(k)
                continue
            if "." in raw:
                k = self.resolve(raw)
                pp = k.rsplit(".", 1)[0] if k else ""
                if k:
                    used.add(k)
                if pp in self.paras:
                    at = self.paras.index(pp)
                out.append(k)
                continue
            order = list(range(at, len(self.paras))) + list(range(0, at))
            hit = next((i for i in order if f"{self.paras[i]}.{raw}" in self.full
                        and f"{self.paras[i]}.{raw}" not in used), None)
            if hit is None:
                out.append(self.resolve(raw))
                continue
            k = f"{self.paras[hit]}.{raw}"
            used.add(k)
            at = hit
            out.append(k)
        return out

    def flow_pid(self, k: str) -> str:
        """The paragraph a `Flow <k>:` line names: a full address (C2.P1) as it is; `P<n>` by its number when the
        Draft's paragraph numbers are unique (C1.P1, C1.P2, C2.P3), else the n-th paragraph in reading order, a title
        paragraph (C<n>.P0) not counted."""
        if k in self.paras:
            return k
        m = re.fullmatch(r"P(\d+)", k or "")
        if not m:
            return ""
        nums = [p.split(".")[1] for p in self.paras]
        if len(set(nums)) == len(nums):
            hit = next((p for p in self.paras if p.endswith("." + k)), "")
            if hit:
                return hit
        counted = [p for p in self.paras if not p.endswith(".P0")]
        n = int(m.group(1))
        return counted[n - 1] if 0 < n <= len(counted) else ""

    def sentences_of(self, pid: str) -> list:
        return [self.key(p, s) for p, s, _ in self.rows if p == pid]


# ── the words a review scored (M-D13: a ★ on other words, or on an older numbering, is stale) ──────────────────

def scored_version(title: str, body: str = "") -> str:
    """The Draft version a pass's review read: `## Pass 2 · 261115 · on draft v6.0 …` → v6.0."""
    m = re.search(r"\bon draft (v\d+(?:\.\d+)*)", title or "") or re.search(r"\bon draft (v\d+(?:\.\d+)*)", body or "")
    return m.group(1) if m else ""


def version_rows(d: dict, version: str):
    """The rows of Draft `version` (the current one, or its file in draft/previous/), or None when it is not on disk."""
    if not version:
        return None
    if d.get("version") == version:
        return rows("\n".join(b for _, b in d.get("text", [])))
    draft = Path(d.get("file") or "")
    stem = draft.name.split("-draft-")[0] if "-draft-" in draft.name else ""
    prev = draft.parent / "previous"
    files = sorted(prev.glob(f"*-draft-{version}.md")) if prev.is_dir() else []
    files = [f for f in files if f.name.startswith(stem + "-draft-")] or files
    if not files:
        return None
    return rows(section3(files[0].read_text(encoding="utf-8", errors="replace")))


def scored_words(old, raw: str, key: str):
    """The words line `raw` scored in the old Draft's rows (by its full address, else its bare id, else the key's
    paragraph); None when that Draft did not have the id."""
    o = Keys(old)
    raw = _sid(raw)
    if raw in o.full:
        return o.full[raw][2]
    bare = raw.rsplit(".", 1)[-1]
    if "." in key:
        alt = f"{key.rsplit('.', 1)[0]}.{bare}"
        if alt in o.full:
            return o.full[alt][2]
    if bare in o.first and not o.rep:
        return o.full[o.first[bare]][2]
    return None

"""The Excalidraw+ link on a page: mint a hosted scene and keep its URL in `## Outline`.

Split out of xcal.py (2026-11-13) by responsibility; behaviour unchanged.
XcalMixin in xcal.py inherits XcalOutlineMixin, so serve.py still composes `XcalMixin`.
"""

import json
import os
import re


class XcalOutlineMixin:
    def excalidraw_key(self):
        """The Excalidraw+ key, from the environment or from env.sh at the root.

        env.sh is gitignored and per-machine (QE6), and serve.py is often started
        from a shell that never sourced it, so falling back to reading the file is
        the difference between "works" and "works only if you remembered".
        """
        k = os.environ.get("EXCALIDRAW_API_KEY", "").strip()
        if k:
            return k, "environment"
        env = self.root / "env.sh"
        if env.exists():
            m = re.search(r'^\s*export\s+EXCALIDRAW_API_KEY\s*=\s*["\']?([^"\'\s#]+)',
                          env.read_text(encoding="utf-8", errors="ignore"), re.M)
            if m:
                return m.group(1), "env.sh"
        return "", ""

    def new_excalidraw(self, f, p):
        """✨ Mint an Excalidraw+ scene for this page and write its link into ## Outline.

        The point is that nobody should have to leave the board, create a drawing
        by hand, and paste a URL back: the page asks for one and gets one.

        The response shape is DISCOVERED rather than assumed. Excalidraw+'s API is
        public beta and its docs list the endpoints without showing the bodies, so
        this asks, then REPORTS what came back, including the raw keys when no link
        is found. A wrong guess that fails loudly beats a wrong guess that writes
        a plausible dead URL into twenty-eight pages.
        """
        import urllib.error
        import urllib.request

        key, src = self.excalidraw_key()
        if not key:
            return None, ("no EXCALIDRAW_API_KEY. Add `export EXCALIDRAW_API_KEY=…` to "
                          "env.sh at the repo root (it is gitignored), or export it in the "
                          "shell that runs serve.py. The key comes from your Excalidraw+ "
                          "workspace settings.")
        base = os.environ.get("EXCALIDRAW_API_BASE", "https://api.excalidraw.com/api/v1")

        def call(method, path, body=None):
            req = urllib.request.Request(
                base + path, method=method,
                data=json.dumps(body).encode() if body is not None else None,
                headers={"Authorization": f"Bearer {key}",
                         "Content-Type": "application/json",
                         "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as r:
                raw = r.read().decode("utf-8", "replace")
            return json.loads(raw) if raw.strip() else {}

        try:
            coll = os.environ.get("EXCALIDRAW_COLLECTION_ID", "").strip()
            if not coll:
                got = call("GET", "/collections")
                items = got if isinstance(got, list) else (got.get("data") or got.get("collections") or [])
                if not items:
                    return None, f"no collections came back from {base}/collections: {str(got)[:200]}"
                coll = str(items[0].get("id") or items[0].get("collectionId") or "")
                if not coll:
                    return None, f"a collection came back with no id: {str(items[0])[:200]}"
            title = f.stem
            scene = call("POST", f"/collections/{coll}/scenes", {"name": title})
        except urllib.error.HTTPError as e:
            return None, f"excalidraw API {e.code} on {e.url}: {e.read()[:200].decode('utf-8','replace')}"
        except Exception as e:
            return None, f"{type(e).__name__} talking to {base}: {e}"

        # Find a link in whatever came back, without inventing one.
        def find_url(o):
            if isinstance(o, str) and o.startswith("http"):
                return o
            if isinstance(o, dict):
                for k2 in ("url", "link", "shareLink", "publicLink", "editLink", "href"):
                    u = find_url(o.get(k2))
                    if u:
                        return u
                for v in o.values():
                    u = find_url(v)
                    if u:
                        return u
            if isinstance(o, list):
                for v in o:
                    u = find_url(v)
                    if u:
                        return u
            return None

        url = find_url(scene)
        if not url:
            keys = ", ".join(sorted(scene)) if isinstance(scene, dict) else type(scene).__name__
            return None, ("the scene was created but no link field was found in the response. "
                          f"Keys: {keys}. Open it in the Excalidraw+ workspace, copy the URL, and "
                          "paste it here; then tell CC which field holds it so this can stop guessing.")
        res, err = self.add_diagram(f, {"url": url})
        if err:
            return None, f"created {url} but could not write it: {err}"
        return {"url": url, "key_from": src, **(res or {})}, None

    def add_diagram(self, f, p):
        """➕ Excalidraw in 📃 Page: paste a share URL on the page and it
        lands on its own line inside `## Outline` — the same line an author types by hand,
        so the md stays the single source and the canvas comes back through build.py.
        One canvas per page: pasting again replaces the old URL instead of stacking a
        second iframe onto the section."""
        url = (p.get("url") or "").strip()
        drop = bool(p.get("remove"))
        # The hosted app, OR this board's own Excalidraw. A self-hosted URL is not
        # guessable, so board.md declares the host once (`excalidraw:`) and this
        # accepts anything under it; without that the ➕ control could not take the
        # very URL the board tells every page to use.
        host = ""
        bmd = f.parent / "board.md"
        if bmd.exists():
            m = re.search(r"^excalidraw:\s*(\S+)", bmd.read_text(encoding="utf-8"), re.M)
            if m:
                host = m.group(1).rstrip("/")
        okay = re.fullmatch(r"https?://(?:app\.)?excalidraw\.com/\S+", url) or (
            host and url.startswith(host + "/"))
        if not drop and not okay:
            hint = f" or this board's own {host}/…" if host else ""
            return None, f"not an excalidraw link (https://app.excalidraw.com/s/…{hint})"
        lines = f.read_text(encoding="utf-8").split("\n")
        def is_xcal(s):
            """A line that is ALREADY an excalidraw embed, hosted or ours.

            It must know about the board's own host too, or a second paste on a
            self-hosted page appends a second iframe instead of replacing the
            first, which is the stacking this endpoint exists to prevent.
            """
            s = s.strip()
            if re.fullmatch(r"https?://(?:app\.)?excalidraw\.com/\S+", s):
                return True
            return bool(host) and s.startswith(host + "/")

        # ## Outline 的范围。找的时候要跳 ``` 围栏：QA4 正文里就摆着 md 段落的示例，
        # 不跳的话会写进示例里（评论层 260723 真踩过这个坑）。
        fence, start, end = False, None, None
        for i, ln in enumerate(lines):
            if ln.lstrip().startswith("```"):
                fence = not fence
                continue
            if fence:
                continue
            if start is None:
                if re.match(r"^## (?:Outline|Diagram|图)\s*$", ln):
                    start = i
                continue
            if re.match(r"^## ", ln):
                end = i
                break

        if start is None and drop:
            return None, "this page has no ## Outline section"
        if start is None:
            # 没有 Outline 这一节就现开一节，位置按固定层次：Outline 在 Content 之前。
            fence, anchor = False, None
            for i, ln in enumerate(lines):
                if ln.lstrip().startswith("```"):
                    fence = not fence
                    continue
                if fence:
                    continue
                if re.match(r"^## (?:Content|Aims|Items to Finish|Done when|完成条件|清单)\b", ln):
                    anchor = i
                    break
            block = ["## Outline", url, ""]
            if anchor is None:
                lines += [""] + block
            else:
                lines[anchor:anchor] = block
            f.write_text("\n".join(lines), encoding="utf-8")
            return {"warn": "created ## Outline holding only a canvas; the ascii map is "
                            "the part that survives being copied, so add one"}, None

        end = end if end is not None else len(lines)
        if drop:
            # 🗑 QD7 (JL 260726): attaching used to be reversible only by hand, so
            # a wrong paste sent the reader to the editor the button exists to
            # avoid. Removal takes out the URL LINE and one blank line above it,
            # and touches nothing else: the ascii figure, the heading, and the
            # section all stay, because deleting a section is a different act
            # with a different blast radius.
            gone = [j for j in range(start + 1, end) if is_xcal(lines[j])]
            if not gone:
                return None, "this Outline has no excalidraw to remove"
            for j in reversed(gone):
                if j - 1 > start and not lines[j - 1].strip():
                    del lines[j - 1:j + 1]
                else:
                    del lines[j]
            f.write_text("\n".join(lines), encoding="utf-8")
            return {"removed": len(gone)}, None
        for j in range(start + 1, end):
            if is_xcal(lines[j]):
                lines[j] = url
                f.write_text("\n".join(lines), encoding="utf-8")
                return {"replaced": True}, None
        k = end
        while k - 1 > start and not lines[k - 1].strip():
            k -= 1
        lines[k:k] = ["", url]
        f.write_text("\n".join(lines), encoding="utf-8")
        has_ascii = any(lines[j].lstrip().startswith("```") for j in range(start + 1, end))
        return ({} if has_ascii else
                {"warn": "this Outline has no ascii map; the canvas is the half that "
                         "disappears when it cannot load"}), None

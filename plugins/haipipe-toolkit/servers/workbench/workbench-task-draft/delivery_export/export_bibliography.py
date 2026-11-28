"""📚 Export · the Page's Bib and evidence receipt: selected CITE Results frozen into a derived Bib.

Part of `ExportMixin` (export.py), which composes it; see export.py for the
writer/door division and where each export lands."""
import json
import os
import re
from pathlib import Path

from src.common import (evidence_lane_dir)
from src.page_evidence import (_result_document)
from src.evidence_selection import (selected_results, legacy_profile, EvidenceSelectionError,
                                    draft_delivery, page_head, pending_items)

from live.export_common import _CITE


class ExportBibliographyMixin:

    def _selected_bibliography(self, page_src, out_dir):
        """Freeze a derived Bib from the selected, verified CITE Results only."""
        if legacy_profile(page_src):
            own = evidence_lane_dir(page_src.parent, "bibex") / (page_src.stem + ".bib")
            if not own.is_file():
                return None
            # the paper build reads a Page's Bib only from delivery/latex/selected-bibliography/ (LLMRec, 261022:
            # a legacy-profile Introduction compiled its own PDF from bibex but left the paper build no Bib)
            target = out_dir / "selected-bibliography" / own.name
            target.parent.mkdir(exist_ok=True)
            text = own.read_text(encoding="utf-8")
            if not target.is_file() or target.read_text(encoding="utf-8") != text:
                target.write_text(text, encoding="utf-8")
            return own
        entries = {}
        # A draft export (`delivery: draft` with a `draft-bibliography:`) lets a CITE Result that cannot give its own
        # keys fall back to that declared .bib, which _draft_bibliography then checks key by key (MISQ, 261022:
        # luo2026mapping, mccrae2003personality and dowell2016cdc had no source Run yet). Final delivery stays strict.
        draft_fallback = draft_delivery(page_src) and bool(page_head(page_src, "draft-bibliography"))
        for manifest in selected_results(page_src):
            document = _result_document(manifest)
            if str(document.get("type", "")).upper() != "CITE":
                continue
            payload = document.get("payload") or {}
            ref = payload.get("bibliography") if isinstance(payload, dict) else None
            if (not isinstance(ref, str) or not ref) and isinstance(payload, dict) and payload.get("sources"):
                # the older paper-local CITE shape (pj…): no payload .bib of its own, but each
                # source names its key and the Supporting Result it comes from
                try:
                    own = self._supporting_bibliography(manifest, document)
                except EvidenceSelectionError:
                    if draft_fallback:
                        continue
                    raise
                for key, entry in own.items():
                    if key in entries and entries[key].strip() != entry.strip():
                        raise EvidenceSelectionError(f"Selected CITE Results conflict on bibliography key {key}")
                    entries[key] = entry
                continue
            if not isinstance(ref, str) or not ref:
                raise EvidenceSelectionError(f"{manifest}: CITE payload.bibliography is missing")
            if ref.startswith("<resolved-result>/"):
                ref = ref[len("<resolved-result>/"):]
            bib = (manifest.parent / ref).resolve()
            try:
                bib.relative_to((manifest.parent / "payload").resolve())
                bib.relative_to(manifest.parent.resolve())
            except ValueError as exc:
                raise EvidenceSelectionError(f"{manifest}: bibliography leaves its selected Result payload") from exc
            if not bib.is_file() or bib.suffix != ".bib":
                if draft_fallback:
                    continue
                raise EvidenceSelectionError(f"{manifest}: selected bibliography is missing")
            raw = bib.read_text(encoding="utf-8")
            keys = re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", raw)
            if len(keys) != len(set(keys)):
                raise EvidenceSelectionError(f"{manifest}: duplicate keys within selected bibliography")
            source = self._bib_entries(raw)
            if not source:
                raise EvidenceSelectionError(f"{manifest}: selected bibliography contains no entries")
            for key, entry in source.items():
                if key in entries and entries[key].strip() != entry.strip():
                    raise EvidenceSelectionError(f"Selected CITE Results conflict on bibliography key {key}")
                entries[key] = entry
        verified = None
        if entries:
            target = out_dir / "selected-bibliography"
            target.mkdir(exist_ok=True)
            verified = target / (page_src.stem + ".bib")
            text = "\n\n".join(entries.values()) + "\n"
            if not verified.is_file() or verified.read_text(encoding="utf-8") != text:
                verified.write_text(text, encoding="utf-8")
        return self._draft_bibliography(page_src, out_dir, entries) or verified

    def _draft_bibliography(self, page_src, out_dir, verified):
        """`delivery: draft` + `draft-bibliography: <bib>`: a Page at SHAPE cites before
        its CITE Results are verified. The keys its Content cites that no verified CITE
        Result supplies are copied, by exact key, from that person-written Bib into
        `draft-bibliography/<page>.bib` beside the verified entries. It is never
        `selected-bibliography/`, which stays verified-only; the receipt names it."""
        target = out_dir / "draft-bibliography" / (page_src.stem + ".bib")
        declared = page_head(page_src, "draft-bibliography")
        if not (draft_delivery(page_src) and declared):
            target.unlink(missing_ok=True)
            return None
        source = (page_src.parent / declared).resolve()
        if not source.is_file():
            raise EvidenceSelectionError(f"draft-bibliography not found: {declared}")
        text = page_src.read_text(encoding="utf-8", errors="replace")
        # a `\cite{…}` quoted inside a code span is a note about a citation, not one (MISQ t01, 261022: a note
        # quoting another Section's `\cite{TOADD}` stopped the Introduction's draft export)
        text = re.sub(r"`[^`\n]*`", "", text)
        # a table or figure the page prints may cite too (MISQ t23, 261022: the variable table's body cites three
        # keys the text does not, and they printed as [?]); its .tex files sit in the selected DISPLAY Results
        for manifest in selected_results(page_src, strict=False):
            if str(_result_document(manifest).get("type", "")).upper() in {"DISPLAY", "TABLE"}:
                for tex in sorted((manifest.parent / "payload").rglob("*.tex")):
                    text += "\n" + tex.read_text(encoding="utf-8", errors="replace")
        keys = []
        for m in _CITE.finditer(text):
            keys += [k.strip() for k in m.group(1).split(",") if k.strip() and k.strip() not in keys]
        missing = [k for k in dict.fromkeys(keys) if k not in verified]
        if not missing:
            target.unlink(missing_ok=True)
            return None
        pool = self._bib_entries(source.read_text(encoding="utf-8", errors="replace"))
        absent = [k for k in missing if k not in pool]
        if absent:
            raise EvidenceSelectionError(f"cited key(s) {', '.join(absent)} are not in {declared}")
        target.parent.mkdir(exist_ok=True)
        body = "\n\n".join(list(verified.values()) + [pool[k] for k in missing]) + "\n"
        if not target.is_file() or target.read_text(encoding="utf-8") != body:
            target.write_text(body, encoding="utf-8")
        return target

    def _supporting_bibliography(self, manifest, document):
        """The entries an older CITE Result cites, each taken by its exact key from the
        one-entry `.bib` of a Supporting Result the Result itself names. A key found in
        none of them is refused by name: no paper-wide seed Bib, no key renaming."""
        from src.item_table import moved_path, repo_root
        keys = [str(s.get("cite", "")).strip().lstrip("@").strip()
                for s in (document.get("payload") or {}).get("sources", []) if isinstance(s, dict)]
        keys = [k for k in dict.fromkeys(keys) if k]
        if not keys:
            raise EvidenceSelectionError(f"{manifest}: CITE payload.bibliography is missing")
        root = repo_root(manifest.parent).resolve()
        found = {}
        for support in document.get("supporting_results") or []:
            rel = support.get("result") if isinstance(support, dict) else None
            folder = (root / rel).resolve() if isinstance(rel, str) and rel else None
            if folder is not None and not folder.is_dir():
                folder = moved_path(root, rel)            # a receipt keeps its Run's old path (AGENTS.md)
                folder = folder.resolve() if folder is not None else None
            if folder is None or not folder.is_dir():
                continue
            try:
                folder.relative_to(root)
            except ValueError:
                raise EvidenceSelectionError(f"{manifest}: a Supporting Result leaves the repository") from None
            for bib in sorted(folder.glob("*.bib")):
                for key, entry in self._bib_entries(bib.read_text(encoding="utf-8", errors="replace")).items():
                    found.setdefault(key, entry)
        # A source whose `identity:` is a DOI is the same paper as a Supporting entry with that DOI, whatever key
        # each names it by (MISQ t01, 261022: the text cites barnett2017opioid, the discovery Run's own Bib names
        # it Barnett_2017; both doi:10.1056/NEJMsa1610524). The entry prints under the key the text cites.
        doi_of = lambda text: (re.search(r"(?i)\bdoi\s*=\s*[{\"]\s*([^}\"]+)", text) or [None, ""])[1].strip().lower()
        by_doi = {doi_of(entry): entry for entry in found.values() if doi_of(entry)}
        for s in (document.get("payload") or {}).get("sources", []):
            if not isinstance(s, dict):
                continue
            key = str(s.get("cite", "")).strip().lstrip("@").strip()
            ident = str(s.get("identity", "")).strip().lower()
            if key and key not in found and ident.startswith("doi:") and ident[4:].strip() in by_doi:
                found[key] = re.sub(r"^(\s*@\w+\s*\{)\s*[^,]+,", lambda m: m.group(1) + key + ",",
                                    by_doi[ident[4:].strip()], count=1)
        missing = [k for k in keys if k not in found]
        if missing:
            raise EvidenceSelectionError(
                f"{manifest}: cited key(s) {', '.join(missing)} are in none of its Supporting Results' "
                "Bib; give the Result a payload.bibliography, or cite the Supporting Result's own key")
        return {k: found[k] for k in keys}

    def _evidence_receipt(self, page_src, out_dir):
        """Record selection provenance separately from conversion success.

        Paths only, no content hashes (JL 260928): staleness is file time or `git diff`."""
        manifests = selected_results(page_src)
        record = {
            "schema_version": 2,
            "profile": "legacy-migration" if legacy_profile(page_src) else "current-ledger",
            "source": page_src.name,
            "results": [{"path": path.relative_to(page_src.parent).as_posix()}
                        for path in manifests],
        }
        if draft_delivery(page_src):
            # a DRAFT delivery says what it left out and where its unverified cites came from
            record["delivery"] = "draft"
            record["pending"] = pending_items(page_src)
            draft_bib = out_dir / "draft-bibliography" / (page_src.stem + ".bib")
            if draft_bib.is_file():
                record["draft_bibliography"] = {
                    "path": Path(os.path.relpath(draft_bib, page_src.parent)).as_posix(),
                    "from": page_head(page_src, "draft-bibliography"),
                    "verified": False}
        (out_dir / "evidence-selection.json").write_text(
            json.dumps(record, indent=2) + "\n", encoding="utf-8")

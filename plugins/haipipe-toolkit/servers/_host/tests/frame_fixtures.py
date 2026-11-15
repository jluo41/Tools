"""Shared fixtures of the frame tests: a tiny Project on disk and a one-slide deck."""
from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import unittest
import zipfile
from html import unescape
from urllib.parse import parse_qs, unquote, urlparse
from pathlib import Path

from host_paths import bootstrap
bootstrap()

from live import frame  # noqa: E402
from live import task_draft  # noqa: E402
from live.frame_view import FrameMixin  # noqa: E402


def project(tmp: str) -> Path:
    """A Project with one work Block: a Question, a drawing, one Job, one Task with a hard and a
    soft Run, code, a notebook and a delivery."""
    root = Path(tmp)
    block = root / "Project" / "tasks" / "b01_topic"
    task = block / "j01_job" / "t01_task"
    for d in (block / "studio" / "s01-flow", block / "reports" / "q01_ask", block / "delivery" / "d01-report",
              task / "scripts", task / "notebooks", task / "runs" / "r01_fit", task / "runs" / "run-build-t01"):
        d.mkdir(parents=True)
    (block / "b01_topic.md").write_text("# b01 · Topic\n\nboard-kind: task-block\nspine: a topic\n")
    (block / "studio" / "s01-flow" / "flow.excalidraw").write_text("{}")
    (block / "reports" / "q01_ask" / "q01_ask.md").write_text(
        "# What is asked?\n\nanswer-status: open\n\n## Opening\n\nOne line that answers it.\n")
    (block / "studio" / "s01-flow" / "s01-flow.md").write_text(
        "s01 · Flow\n=====\n\n**Topic:** how it flows.\n\n**Feeds:** `reports/q01_ask/`.\n\ns01-D01 · Proposed: one.\n")
    (block / "j01_job" / "j01_job.md").write_text("# j01 · Job\n\nanswers: Q01\n")
    (block / "delivery" / "d01-report" / "index.html").write_text("<p>x</p>")
    (task / "t01_task.md").write_text("# t01 · Task\n\ngoal: one thing\n\n## Plan\n\ninputs → worker → Runs\n")
    (task / "scripts" / "worker.py").write_text("print(1)\n")
    (task / "notebooks" / "r01_fit.ipynb").write_text("{}")
    (task / "runs" / "r01_fit" / "run.yaml").write_text("run: r01_fit\nkind: hard\ntype: [fit, evaluate]\nstatus: done\n")
    (task / "runs" / "run-build-t01" / "run.yaml").write_text("run: run-build-t01\nkind: soft\ntype: build\nstatus: open\n")
    return root


def tiny_deck(path: Path) -> Path:
    """A one-slide .pptx written by hand: a rounded box with text, an arrow and a picture."""
    A = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
    P = 'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
    R = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    rel = lambda rid, kind, target: (f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/'
                                     f'2006/relationships/{kind}" Target="{target}"/>')
    rels = lambda *r: ('<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                       + "".join(r) + "</Relationships>")
    box = ('<p:sp><p:nvSpPr><p:cNvPr id="2" name="box"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm>'
           '<a:off x="127000" y="127000"/><a:ext cx="2540000" cy="1270000"/></a:xfrm><a:prstGeom prst="roundRect">'
           '<a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="1F3A68"/></a:solidFill></p:spPr><p:txBody>'
           '<a:bodyPr anchor="ctr"/><a:p><a:pPr algn="ctr"/><a:r><a:rPr sz="2400" b="1"><a:solidFill>'
           '<a:srgbClr val="FFFFFF"/></a:solidFill></a:rPr><a:t>Prep AI &amp; you</a:t></a:r></a:p></p:txBody></p:sp>')
    arrow = ('<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="3" name=""/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr><p:spPr><a:xfrm>'
             '<a:off x="2794000" y="762000"/><a:ext cx="1270000" cy="0"/></a:xfrm><a:prstGeom prst="straightConnector1">'
             '<a:avLst/></a:prstGeom><a:ln w="25400"><a:solidFill><a:srgbClr val="C92A2A"/></a:solidFill>'
             '<a:tailEnd type="triangle"/></a:ln></p:spPr></p:cxnSp>')
    pic = ('<p:pic><p:nvPicPr><p:cNvPr id="4" name=""/><p:cNvPicPr/><p:nvPr/></p:nvPicPr><p:blipFill>'
           '<a:blip r:embed="rImg"/><a:stretch/></p:blipFill><p:spPr><a:xfrm><a:off x="4318000" y="127000"/>'
           '<a:ext cx="1270000" cy="1270000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("ppt/presentation.xml", f'<p:presentation {P} {R}><p:sldIdLst><p:sldId id="256" r:id="rS1"/>'
                   '</p:sldIdLst><p:sldSz cx="9144000" cy="5143500"/></p:presentation>')
        z.writestr("ppt/_rels/presentation.xml.rels", rels(rel("rS1", "slide", "slides/slide1.xml")))
        z.writestr("ppt/slides/slide1.xml", f'<p:sld {P} {A} {R}><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" '
                   f'name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>{box}{arrow}{pic}</p:spTree>'
                   '</p:cSld></p:sld>')
        z.writestr("ppt/slides/_rels/slide1.xml.rels", rels(rel("rImg", "image", "/ppt/media/image1.png")))
        z.writestr("ppt/media/image1.png", b"\x89PNG\r\n\x1a\nfake")
    return path

"""The frame's Delivery and Related: deliverables, versions, decks, Word files, emails and notes."""
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
from frame_fixtures import project, tiny_deck  # noqa: E402,F401


class FrameDeliveryTest(unittest.TestCase):
    def test_delivery_is_the_blocks_with_a_part_per_source_and_links_down(self):
        # b10 s03-D06 (JL 261011: "for the section, we will do not have the related studio and delivery";
        # "also for the Jobs"): one Delivery, the Block's; a Job or Task picks its part and links back down
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            task = block / "j01_job/t01_task"
            (block / "delivery/j01_job/t01_task/latex").mkdir(parents=True)
            (block / "delivery/j01_job/t01_task/latex/t01_task.tex").write_text("x", encoding="utf-8")
            (block / "delivery/j01_job/report.pdf").write_bytes(b"x")
            page = frame.render(frame.VANILLA, root, block, "Delivery")
            table = page.split("<h3>By source</h3>", 1)[1]
            self.assertIn(frame._e(frame.href(task, root, frame.VANILLA, "Delivery")), table)   # to the part
            self.assertIn(frame._e("/_board/workbench?path=Project%2Ftasks%2Fb01_topic%2Fj01_job%2Ft01_task"), table)
            self.assertIn("└ ", table)                                                       # a Task under its Job
            self.assertEqual(re.findall(r"<td>(\d+)</td>", table), ["1", "1"])              # a Job's own file only
            for folder, picked in ((block / "j01_job", "j01_job"), (task, "j01 › t01_task")):     # folder names (s32-D15)
                with self.subTest(folder=folder.name):
                    page = frame.render(frame.VANILLA, root, folder, "Delivery")
                    parts = re.search(r'<nav class="row subs delivery-parts">(.*?)</nav>', page).group(1)
                    self.assertEqual(re.findall(r'aria-current="true">([^<]+)</a>', parts), [picked])
                    self.assertIn("Its part of the Block's Delivery", page)
                    self.assertIn("· Delivery · <span class=lv>b01</span>", page)

    def test_a_deliverable_is_one_item_with_its_lanes_and_versions(self):
        # JL 261014: "for the delivery, I think we just make the item to be the same ... all of them should one
        # Delivery Item, and within it, we can see different versions"
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            shutil.rmtree(block / "delivery")
            slide, render = block / "delivery/slide", block / "delivery/render"
            slide.mkdir(parents=True), render.mkdir(parents=True)
            for n, name in enumerate(("Deck-v1", "Deck-v2", "Deck-Visual-v3")):
                f = tiny_deck(slide / f"{name}.pptx")
                os.utime(f, (1_700_000_000 + n * 100,) * 2)
            (render / "Deck-Visual-v3.png").write_bytes(b"png")                       # its render: same version
            os.utime(render / "Deck-Visual-v3.png", (1_700_000_300,) * 2)
            sec = block / "delivery/j01_job/t01_task"
            for lane, files in (("web", ("index.html",)), ("word", ("t01_task.docx", "t01_task.pdf")),
                                ("latex", ("t01_task.pdf",))):
                (sec / lane).mkdir(parents=True)
                for name in files:
                    (sec / lane / name).write_bytes(b"x")
            (block / "delivery/word").mkdir()
            (block / "delivery/word/Paper.docx").write_bytes(b"x")
            (block / "delivery/word/Paper-SI.docx").write_bytes(b"x")              # no number: its own item
            items = {i["title"]: i for i in frame.delivery_items(block)}
            self.assertEqual(sorted(items), ["Deck", "Paper", "Paper-SI", "t01_task"])
            deck = items["Deck"]
            self.assertEqual([v["label"] for v in deck["versions"]], ["Visual-v3", "v2", "v1"])
            self.assertEqual([f.name for f in deck["versions"][0]["files"]], ["Deck-Visual-v3.pptx", "Deck-Visual-v3.png"])
            self.assertEqual(items["t01_task"]["fixed"], ["PDF", "Word", "Web page"])     # three lanes, one item
            self.assertEqual(items["t01_task"]["source"], "j01_job › t01_task")
            page = frame.render(frame.VANILLA, root, block, "Delivery")
            card = page.split('data-studio-key="Deck"', 1)[1].split("</details>", 1)[0]
            self.assertNotIn("topic-meta", card)          # no line under the name (JL 261014: "so many unnecessary
            self.assertNotIn("versions, newest", card)    # information")
            self.assertNotIn("Add to Current", card)      # JL 261014: "remove the add to current"
            self.assertEqual(re.findall(r'data-dv="(\d)" aria-pressed="(\w+)"', card),
                             [("0", "true"), ("1", "false"), ("2", "false")])
            self.assertIn('<img class=related-img loading=lazy alt="Deck-Visual-v3.png"', card)   # the render first
            self.assertIn(frame._e(frame.ROUTE + "?view=pptx&path=Project%2Ftasks%2Fb01_topic%2Fdelivery%2Fslide%2F"
                                   "Deck-v2.pptx"), card)                                    # else the deck, drawn
            self.assertIn('<div class=dv-pane data-dv="1" hidden>', card)
            self.assertIn("PDF · latex ↗", page)                                            # two PDFs: by lane

    def test_related_versions_fold_into_the_item_that_has_a_row(self):
        # JL 261014: "一个东西，我们会有一个 version 又一个 version ... 怎么去比较好地去 handle that?" The same rule as Delivery
        with tempfile.TemporaryDirectory() as tmp:
            block = Path(tmp) / "Project/work/b01_topic"
            (block / "related/files").mkdir(parents=True)
            for n, name in enumerate(("Proposal-v1.docx", "Proposal-v2.docx", "Proposal-v3.pptx")):
                (block / "related/files" / name).write_bytes(b"x")
                os.utime(block / "related/files" / name, (1_700_000_000 + n * 100,) * 2)
            (block / "related/files/Budget.xlsx").write_bytes(b"x")
            (block / "related/files/Budget.pdf").write_bytes(b"x")                 # one name, two formats: apart
            (block / "related/related.md").write_text(
                "| kind | date | item | link | feeds | group |\n|---|---|---|---|---|---|\n"
                "| file | 2026-10-01 | The proposal | `files/Proposal-v1.docx` | s01 | IRB |\n", encoding="utf-8")
            items = frame.related_items(block)
            self.assertEqual([i["title"] for i in items], ["The proposal", "Budget.pdf", "Budget.xlsx"])
            item = items[0]
            self.assertEqual([v["label"] for v in item["versions"]], ["v3", "v2", "v1"])    # newest first
            self.assertEqual(item["groups"], ["files", "IRB"])                             # the row's, kept
            self.assertIn("3 versions", item["meta"])
            html_ = frame.related_view(block, Path(tmp)).html
            self.assertIn('class="row dv-vers"', html_)
            self.assertIn(frame._e("view=pptx&path=Project%2Fwork%2Fb01_topic%2Frelated%2Ffiles%2FProposal-v3.pptx"),
                          html_)                                                            # a deck previews here too

    def test_a_deck_is_drawn_slide_by_slide_from_its_package(self):
        # JL 261014: "could we do the preview of the slide as well?"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            deck = tiny_deck(root / "deck.pptx")
            page = frame.pptx_preview(deck, root)
            self.assertIn("deck.pptx · read from the deck package: 1 slide · 1 pictures", page)
            self.assertIn('viewBox="0 0 720.00 405.00"', page)                       # 9,144,000 EMU = 720 pt
            self.assertIn('fill="#1f3a68"', page)                                    # the box, its colour
            self.assertIn('translate(10.00 10.00)', page)
            self.assertIn("Prep AI &amp; you</span>", page)                           # its text, escaped
            self.assertIn("font-size:24.00px;font-weight:700;color:#ffffff", page)
            self.assertIn('stroke="#c92a2a" stroke-width="2.00"', page)               # the arrow
            self.assertIn('marker-end="url(#pm0)"', page)
            self.assertIn(frame._e("?view=pptx&path=deck.pptx&media=ppt%2Fmedia%2Fimage1.png"), page)
            self.assertNotIn("base64", page)                                         # pictures by link, not inlined
            self.assertEqual(frame.pptx_media(deck, "ppt/media/image1.png"), (b"\x89PNG\r\n\x1a\nfake", "image/png"))
            self.assertIsNone(frame.pptx_media(deck, "ppt/slides/slide1.xml"))      # only pictures leave the package

    def test_a_related_item_is_grouped_by_its_kind(self):
        # JL 261013 (the groups are "things like meeting, email, paper"): a kept file sits under its subfolder,
        # a row kept as a web link under its kind; the group cell still adds more (b10 s04-D08)
        with tempfile.TemporaryDirectory() as tmp:
            block = Path(tmp) / "Project/paper/Paper-X"
            (block / "related/paper").mkdir(parents=True)
            (block / "related/paper/smith2024.pdf").write_bytes(b"%PDF-1.4")
            (block / "related/meetings").mkdir()
            (block / "related/meetings/2026-10-10-1800 kickoff.md").write_text("# kickoff\n", encoding="utf-8")
            (block / "related/related.md").write_text(
                "| kind | date | item | link | feeds | group |\n|---|---|---|---|---|---|\n"
                "| paper | 2024 | Smith 2024 | `paper/smith2024.pdf` | s01 |  |\n"
                "| paper | 2025 | Jones 2025 | https://doi.org/10.1/x | s01 |  |\n"
                "| meeting | 2026-10-10 | Kickoff | `meetings/2026-10-10-1800 kickoff.md` | s01 | IRB |\n",
                encoding="utf-8")
            groups = {i["title"]: i["groups"] for i in frame.related_items(block)}
            self.assertEqual(groups["Smith 2024"], ["paper"])
            self.assertEqual(groups["Jones 2025"], ["paper"])
            self.assertEqual(groups["Kickoff"], ["meetings", "IRB"])

    def test_related_folds_inside_the_studio_at_every_level(self):
        # b10 s04, JL 261011: Related is the Studio's second folding part, under the topic cards
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            (block / "related/meetings").mkdir(parents=True)
            (block / "related/meetings/2026-10-10-1800 kickoff.md").write_text("# kickoff\n", encoding="utf-8")
            (block / "related/files").mkdir()
            (block / "related/files/draft.docx").write_bytes(b"x")
            (block / "related/related.md").write_text(
                "| kind | date | item | link | feeds |\n|---|---|---|---|---|\n"
                "| meeting | 2026-10-10 | Kickoff | `meetings/2026-10-10-1800 kickoff.md` | s01 |\n"
                "| paper | 2024 | A paper | https://example.org/paper | q01 |\n", encoding="utf-8")
            for folder in (block, block / "j01_job/t01_task"):
                with self.subTest(level=frame.level_of(folder)):
                    page = frame.render(frame.VANILLA, root, folder, "Related")
                    self.assertIn("<details class=studio-related id=studio-related open>", page)  # a Related link unfolds it
                    self.assertIn("related/ · 2 items · meeting 1 · paper 1", page)
                    self.assertNotIn('<nav class="row subs">', page)
                    self.assertIn("Kickoff", page)
                    self.assertIn("A paper", page)
                    self.assertIn("/_board/page?path=%2FProject%2Ftasks%2Fb01_topic%2Frelated%2Fmeetings", page)
                    self.assertIn("example.org/paper ↗", page)
                    # the Studio's group bar; a subfolder is a group of its files (s04-D08, JL 261011)
                    self.assertNotIn("related-group", page)
                    bar = re.search(r'data-group-kind=related data-group-noun=item>(.*?)</nav>', page).group(1)
                    self.assertEqual(re.findall(r'data-studio-tag="([^"]*)"', bar),
                                     ["__current__", "files", "meetings", "paper"])
                    self.assertIn('meetings <span class=tag-count>1</span>', bar)
                    self.assertIn('paper <span class=tag-count>1</span>', bar)            # the web link, by its kind
                    self.assertNotIn("Untagged", bar)
                    self.assertIn('<span class=chip data-tag="meetings">meetings</span>', page)  # no ×: the folder
                    self.assertIn("class=grp-new", bar)
                    self.assertIn("related/files/draft.docx · no row yet", page)   # the sent file has no row
                    self.assertIn("files/draft.docx", page)
                    # a Word file opens on its preview, read from its package (frame.docx_preview)
                    self.assertIn(frame._e("/_board/workbench?view=docx&path=Project%2Ftasks%2Fb01_topic%2Frelated"
                                           "%2Ffiles%2Fdraft.docx"), page)
                    self.assertIn("run-add-related-", page)
                    studio = frame.render(frame.VANILLA, root, folder, "Idea Studio")
                    self.assertIn("<details class=studio-related id=studio-related>", studio)  # folded by default
                    self.assertIn("Kickoff", studio)
                    old = frame.render(frame.VANILLA, root, folder, "Description", "Related")
                    self.assertIn("<details class=studio-related id=studio-related open>", old)

    def test_a_word_file_previews_from_its_package(self):
        import zipfile
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            doc = root / "Project/tasks/b01_topic/related/materials/form.docx"
            doc.parent.mkdir(parents=True)
            w = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
            with zipfile.ZipFile(doc, "w") as z:
                z.writestr("word/document.xml", f'<w:document {w}><w:body>'
                           '<w:p><w:commentRangeStart w:id="0"/><w:r><w:t>Your text here</w:t></w:r></w:p>'
                           '<w:tbl><w:tr><w:tc><w:p><w:r><w:t>in a cell</w:t></w:r><w:commentRangeEnd w:id="0"/>'
                           '</w:p></w:tc></w:tr></w:tbl></w:body></w:document>')
                z.writestr("word/comments.xml", f'<w:comments {w}><w:comment w:id="0" w:author="GG">'
                           '<w:p><w:r><w:t>one comment</w:t></w:r></w:p></w:comment></w:comments>')
            page = frame.docx_preview(doc, root)
            self.assertIn("Your text here", page)
            self.assertIn("in a cell", page)                  # a table's text is kept
            self.assertIn("1 comments", page)                 # a comment over two blocks keeps its card
            self.assertIn("one comment", page)

    def test_an_email_previews_as_it_came(self):
        # JL 261011: "the related can have /emails as well"; an .eml opens on its headers and its text
        from email.message import EmailMessage
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            mail = block / "related/emails/2026-10-09-0900 IRB question.eml"
            mail.parent.mkdir(parents=True)
            msg = EmailMessage()
            msg["From"], msg["To"], msg["Subject"] = "a@x.org", "b@y.org", "IRB question"
            msg.set_content("Can we share <the> data?")
            msg.add_attachment(b"pdf", maintype="application", subtype="pdf", filename="form.pdf")
            mail.write_bytes(bytes(msg))
            page = frame.eml_preview(mail, root)
            self.assertIn("<th>Subject</th><td>IRB question</td>", page)
            self.assertIn("Can we share &lt;the&gt; data?", page)                          # escaped
            self.assertIn("form.pdf (1 KB)", page)
            listing = frame.render(frame.VANILLA, root, block, "Related")
            self.assertIn('<span class=chip data-tag="emails">emails</span>', listing)   # its subfolder's group
            self.assertIn(frame._e("/_board/workbench?view=eml&path=Project%2Ftasks%2Fb01_topic%2Frelated%2F"
                                   "emails%2F2026-10-09-0900+IRB+question.eml"), listing)

    def test_a_meeting_note_reads_as_plain_markdown(self):
        # JL 261011: a related meeting opened on "Not a Page"; any .md that is no Page reads as Markdown
        from live.page_reader import markdown_document, markdown_html
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            note = root / "Project/tasks/b01_topic/related/meetings/2026-10-10-1800 kickoff.md"
            note.parent.mkdir(parents=True)
            note.write_text("---\ntitle: kickoff\n---\n\n# Kickoff\n\n## Recording\n![[rec.webm]]\n\n"
                            "> [!quote]- Live transcript (2 lines)\n> [0:09] S1 hello\n> [0:11] S2 <b>hi</b>\n\n"
                            "| kind | link |\n|---|---|\n| paper | [it](papers/a.pdf) |\n\n- [ ] S1 push\n",
                            encoding="utf-8")
            page = markdown_document(note, root)
            self.assertIn("<pre class=front>title: kickoff</pre>", page)
            self.assertIn("<h1>Kickoff</h1>", page)
            self.assertIn("⤷ rec.webm", page)                                     # an Obsidian embed names its file
            self.assertIn('<details class="callout quote"><summary>Live transcript (2 lines)</summary>', page)
            self.assertIn("[0:09] S1 hello<br>[0:11] S2 &lt;b&gt;hi&lt;/b&gt;", page)  # one line per turn, escaped
            self.assertIn('href="/Project/tasks/b01_topic/related/meetings/papers/a.pdf"', page)
            self.assertIn("<li>☐ S1 push</li>", page)
            self.assertIn("<h1>related</h1>", markdown_html("related\n=======\n\nrows\n"))   # an underlined heading
            self.assertNotIn("javascript", markdown_html("[x](javascript:alert(1))"))


if __name__ == "__main__":
    unittest.main()

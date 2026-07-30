#!/usr/bin/env python3
"""Contract checks for render-local sentence addressing and focused Q chat."""
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


class SentenceChatContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.js = (HERE / "assets" / "board.js").read_text(encoding="utf-8")
        cls.css = (HERE / "assets" / "board.css").read_text(encoding="utf-8")

    def test_reuses_existing_question_chat(self):
        self.assertIn("window.__boardSentenceChat", self.js)
        self.assertIn("await chatOpen(sec)", self.js)
        self.assertIn(
            "setSentenceFocus(ref, sentence, attached, contentPath)", self.js
        )
        self.assertNotIn("await chatSend(prompt)", self.js)

    def test_visible_focus_card_is_clearable_without_closing_chat(self):
        self.assertIn('class="sfocus"', self.js)
        self.assertIn('class="sfclear"', self.js)
        self.assertIn("chat.querySelector('.sfclear').onclick = clearSentenceFocus", self.js)
        self.assertIn("#chat .sfocus[hidden]{display:none}", self.css)

    def test_next_message_contains_address_sentence_and_apparatus(self):
        self.assertIn("function focusedMessage(message)", self.js)
        self.assertIn("'Focus this turn on sentence ' + sentenceFocus.ref", self.js)
        self.assertIn("'Sentence:\\n' + sentenceFocus.sentence", self.js)
        self.assertIn("sentenceFocus.attached", self.js)
        self.assertIn("'Content location:\\n' + sentenceFocus.contentPath", self.js)
        self.assertIn("message: focusedMessage(msg)", self.js)
        self.assertIn(
            "chat.querySelector('.send').onclick = function () { chatSend(); }",
            self.js,
        )
        self.assertNotIn("chat.querySelector('.send').onclick = chatSend;", self.js)

    def test_content_sentence_addresses_are_generated_and_rewired(self):
        self.assertIn("sec.querySelector('details.sect.content')", self.js)
        self.assertIn("var contentId = 'C' + (ci + 1)", self.js)
        self.assertIn(
            "var shortId = contentId + '.P' + nextP + '.S1'", self.js
        )
        self.assertIn("var fullId = sec.id + '.' + shortId", self.js)
        self.assertIn("window.__boardWireSentenceChats = wireSentenceChats", self.js)
        self.assertIn("if (window.__boardWireSentenceChats)", self.js)

    def test_heading_is_a_terminal_sibling_not_a_sentence_parent(self):
        self.assertIn("var headingId = 'H' + nextH", self.js)
        self.assertIn("var headingRef = contentRef + '.' + headingId", self.js)
        self.assertIn("node.dataset.headingRef = headingRef", self.js)
        self.assertNotIn("headingRef + '.P'", self.js)
        self.assertIn(".caddr,.haddr", self.css)

    def test_hover_and_keyboard_entry_are_both_styled(self):
        self.assertIn("p.sentence-target:hover+.schatbar", self.css)
        self.assertIn(".schatbar:focus-within", self.css)
        self.assertIn(".schat:focus-visible", self.css)

    def test_desktop_rail_has_comment_and_chat_actions(self):
        self.assertIn("comment.className = 'scomment'", self.js)
        self.assertIn("openSentenceComment(p, bar)", self.js)
        self.assertIn("chatButton.className = 'schat'", self.js)

    def test_touch_collapses_actions_into_overflow_menu(self):
        self.assertIn("more.className = 'smore'", self.js)
        self.assertIn("menuAction('＋ Comment'", self.js)
        self.assertIn("menuAction('💬 Chat'", self.js)
        self.assertIn("menuAction('✎ Edit'", self.js)
        self.assertIn("@media (hover:none),(pointer:coarse)", self.css)
        self.assertIn(".schatbar.menu-open>.smenu", self.css)


if __name__ == "__main__":
    unittest.main()

"""QD5 · the operating shell: pane recognition, injection, and link carry-over.

The browser half is checks/splitshell.mjs (three real frames, a real rebuild).
What is unit-testable is everything that decides WHAT a pane is served, and the
one invariant QB2 cares about: strip the query and the file is untouched.
"""
import unittest

from live.shell import PANE_CSS, ShellMixin, _LINK, _shell_doc


class PaneRecognitionTest(unittest.TestCase):
    def test_a_board_page_with_a_pane_query_is_a_pane(self):
        for kind in ("index", "page", "chat"):
            self.assertEqual(
                ShellMixin.pane_of(f"/x/board/QD/QD5-y.html?pane={kind}"), kind)

    def test_everything_else_is_not(self):
        # no query, unknown kind, and not a page: all fall through to the
        # static handler, which is what serves the board today.
        self.assertIsNone(ShellMixin.pane_of("/x/board/QD/QD5-y.html"))
        self.assertIsNone(ShellMixin.pane_of("/x/board/QD/QD5-y.html?pane=zzz"))
        self.assertIsNone(ShellMixin.pane_of("/_board/health?pane=page"))
        self.assertIsNone(ShellMixin.pane_of("/x/scene.excalidraw?pane=page"))

    def test_every_pane_kind_has_a_stylesheet(self):
        self.assertEqual(set(PANE_CSS), {"index", "page", "chat"})


class SplitDoorTest(unittest.TestCase):
    """ONE URL PER PAGE, and the split is what a browser tab gets.

    `split_of` reads request headers, so it is an instance method now; these
    stand a bare object up with just the headers it looks at.
    """

    @staticmethod
    def ask(path, **headers):
        obj = ShellMixin.__new__(ShellMixin)
        obj.headers = headers
        return ShellMixin.split_of(obj, path)

    def test_a_browser_tab_gets_the_shell(self):
        self.assertEqual(self.ask("/x/board/QD/QD5-y.html", Accept="text/html"),
                         "/x/board/QD/QD5-y.html")

    def test_asking_by_name_still_works(self):
        self.assertEqual(self.ask("/x/board/QD/QD5-y.html?split"),
                         "/x/board/QD/QD5-y.html")

    def test_plain_is_the_opt_out(self):
        self.assertIsNone(self.ask("/x/board/QD/QD5-y.html?plain", Accept="text/html"))

    def test_a_pane_is_not_a_split_and_a_split_is_not_a_pane(self):
        self.assertIsNone(self.ask("/x/board/QD/QD5-y.html?pane=page", Accept="text/html"))
        self.assertIsNone(ShellMixin.pane_of("/x/board/QD/QD5-y.html?split"))

    def test_curl_and_every_fetch_still_get_the_file(self):
        """`70-router.js`, `20-live-refresh.js` and curl all send */*."""
        self.assertIsNone(self.ask("/x/board/QD/QD5-y.html", Accept="*/*"))
        self.assertIsNone(self.ask("/x/board/QD/QD5-y.html"))

    def test_an_iframe_that_DOES_send_the_header_is_believed(self):
        self.assertIsNone(self.ask("/x/board/QD/QD5-y.html",
                                   Accept="text/html", **{"Sec-Fetch-Dest": "iframe"}))

    def test_nothing_but_a_page_is_a_split(self):
        self.assertIsNone(self.ask("/_board/health", Accept="text/html"))


class IndexOfTest(unittest.TestCase):
    def test_any_page_in_the_tree_names_the_same_index(self):
        self.assertEqual(
            ShellMixin._index_of("/a/b/board/QD/QD5-x.html"), "/a/b/board/index.html")
        self.assertEqual(
            ShellMixin._index_of("/a/b/board/QD.html"), "/a/b/board/index.html")

    def test_a_board_whose_own_folder_is_named_board_cuts_at_the_last_one(self):
        # `.../board/board/QD/x.html` must not resolve to the outer folder
        self.assertEqual(ShellMixin._index_of("/a/board/board/QD/x.html"),
                         "/a/board/board/index.html")


class LinkCarryOverTest(unittest.TestCase):
    """A link out of a pane has to land in a pane, or the frame stops being one."""

    def test_relative_page_links_gain_the_query(self):
        self.assertEqual(_LINK.sub(r'href="\1?pane=page\2"', '<a href="QD/QD5-x.html">'),
                         '<a href="QD/QD5-x.html?pane=page">')

    def test_a_fragment_survives_on_the_far_side_of_the_query(self):
        self.assertEqual(_LINK.sub(r'href="\1?pane=page\2"', '<a href="QA.html#top">'),
                         '<a href="QA.html?pane=page#top">')

    def test_external_and_bare_fragments_are_left_alone(self):
        for href in ('href="https://x.dev/a.html"', 'href="#top"',
                     'href="QD5.md"', 'href="x.html?pane=chat"'):
            self.assertEqual(_LINK.sub(r'href="\1?pane=page\2"', href), href)


class ShellDocTest(unittest.TestCase):
    def setUp(self):
        self.doc = _shell_doc("/b/board/QD/QD5-x.html", "/b/board/index.html")

    def test_three_frames_each_pointing_at_its_own_pane(self):
        """The page frame has a `src`; the other two carry `data-src` and are
        given one the first time they are shown (260802), so opening a page
        loads ONE document."""
        self.assertIn('name="page"  id="fp" src="/b/board/QD/QD5-x.html?pane=page"', self.doc)
        self.assertIn('name="index" id="fi" data-src="/b/board/index.html?pane=index"', self.doc)
        self.assertIn('name="chat"  id="fc" data-src="/b/board/QD/QD5-x.html?pane=chat"', self.doc)

    def test_the_side_panes_are_hidden_until_asked_for(self):
        self.assertIn("var off = true;", self.doc)      # the rail
        self.assertIn("var hidden = true;", self.doc)   # the chat

    def test_no_placeholder_survives_into_the_served_document(self):
        self.assertNotIn("__", self.doc.replace("__", "", 0) and
                         "".join(t for t in self.doc.split() if t.startswith("__")))

    def test_the_shell_holds_no_long_lived_connection(self):
        """C4 P6: a held connection is one of the browser's six per origin, and
        opening the split twice inside a few seconds then wanted seven. The
        refresh belongs to each pane, which asks about its own URL."""
        self.assertNotIn("EventSource", self.doc)
        self.assertNotIn("_events", self.doc)

    def test_the_strip_names_the_board_and_offers_the_way_out(self):
        for hook in ('id="where"', 'id="what"', 'id="plain"', 'href="/boards"',
                     'id="ti"', 'id="mtui"', 'id="mgui"'):
            self.assertIn(hook, self.doc)

    def test_the_chat_is_two_toggles_and_not_a_menu(self):
        """JL 260802: which chat you want and whether you want one are the same
        question, so they are the same control — and no popup to dismiss."""
        self.assertNotIn('id="cmenu"', self.doc)
        self.assertIn('data-mode="tui"', self.doc)
        self.assertIn('data-mode="gui"', self.doc)

    def test_the_way_out_asks_for_plain(self):
        """A bare url is the split now, so `↗ plain` has to say `?plain`."""
        self.assertIn("?plain", self.doc)

    def test_the_page_it_was_opened_on_is_baked_in(self):
        self.assertIn("OPENED = '/b/board/QD/QD5-x.html'", self.doc)
        self.assertIn("INDEX = '/b/board/index.html'", self.doc)


if __name__ == "__main__":
    unittest.main()

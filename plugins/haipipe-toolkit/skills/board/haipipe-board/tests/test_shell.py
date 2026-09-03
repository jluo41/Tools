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

    def test_only_wrap_fragment_is_recognized(self):
        self.assertEqual(
            ShellMixin.fragment_of("/x/board/QD/QD5-y.html?fragment=wrap"), "wrap")
        self.assertIsNone(
            ShellMixin.fragment_of("/x/board/QD/QD5-y.html?fragment=sidebar"))
        self.assertIsNone(ShellMixin.fragment_of("/x/board/QD/QD5-y.html"))


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

    def test_embed_is_an_internal_file_route(self):
        self.assertIsNone(self.ask("/x/board/QD/QD5-y.html?embed", Accept="text/html"))

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

    def test_the_plugin_pane_is_visible_on_a_first_visit(self):
        self.assertIn("var off = true;", self.doc)      # the rail
        self.assertIn("var hidden = false;", self.doc)  # the direct plugin strip
        self.assertIn("if (savedPane !== null) hidden = savedPane !== '1';", self.doc)

    def test_no_placeholder_survives_into_the_served_document(self):
        self.assertNotIn("__", self.doc.replace("__", "", 0) and
                         "".join(t for t in self.doc.split() if t.startswith("__")))

    def test_the_shell_holds_no_long_lived_connection(self):
        """C4 P6: a held connection is one of the browser's six per origin, and
        opening the split twice inside a few seconds then wanted seven. The
        refresh belongs to each pane, which asks about its own URL."""
        self.assertNotIn("EventSource", self.doc)
        self.assertNotIn("_events", self.doc)

    def test_the_strip_names_the_board_without_an_old_view_exit(self):
        for hook in ('id="where"', 'id="what"', 'href="/boards"',
                     'id="ti"', 'id="mtui"', 'id="mgui"'):
            self.assertIn(hook, self.doc)
        self.assertNotIn('id="plain"', self.doc)

    def test_the_chat_is_two_toggles_and_not_a_menu(self):
        """JL 260802: which chat you want and whether you want one are the same
        question, so they are the same control — and no popup to dismiss."""
        self.assertNotIn('id="cmenu"', self.doc)
        self.assertIn('data-mode="tui"', self.doc)
        self.assertIn('data-mode="gui"', self.doc)

    def test_internal_frames_use_embed_not_a_second_reader_view(self):
        self.assertIn("?embed", self.doc)

    def test_plugin_frame_detects_html_from_the_url_path_only(self):
        """A plugin query may end in an encoded Page URL whose value is .html.

        That does not make the plugin endpoint itself an HTML Page. The old
        raw-string suffix test appended ``?embed`` to Labeling's ``page=``
        value and the right pane landed on a 400 response.
        """
        self.assertIn("new URL(u, location.href).pathname", self.doc)
        self.assertNotIn("u + (/\\.html$/.test(u) ? '?embed' : '')", self.doc)

    def test_registry_tabs_are_filtered_by_the_live_pages_applies_gate(self):
        """A type-specific tab must not remain in another Page's menus."""
        self.assertIn(
            "w.boardPlugins.applicable(w.boardPlugins.livePage()).forEach",
            self.doc,
        )
        self.assertNotIn("w.boardPlugins.all().forEach(function (e)", self.doc)

    def test_direct_plugin_tabs_can_close_and_stay_closed(self):
        """The first page visit opens its palette; later visits honor a close."""
        self.assertIn("xdefs().forEach(function (entry) { openSet.push(entry.id); });",
                      self.doc)
        self.assertIn("if (!storedSet) {", self.doc)
        self.assertIn("if (i > 0) openSet.unshift(id);", self.doc)
        self.assertNotIn("if (i !== 0) openSet.unshift(id);", self.doc)
        self.assertIn("openSet.indexOf(def) >= 0", self.doc)
        self.assertIn('class="rptx" data-close="', self.doc)
        self.assertIn("closeTab(b.dataset.close);", self.doc)
        self.assertIn("if (offerable(openSet[j]))", self.doc)
        self.assertIn("if (plus) plus.hidden = true;", self.doc)
        self.assertIn("overflow-x:auto", self.doc)

    def test_active_plugin_close_is_a_touch_target_not_a_tiny_glyph(self):
        """The active tab must be reliably closable on a phone."""
        self.assertIn("width:36px;min-width:36px", self.doc)
        self.assertIn("touch-action:manipulation", self.doc)
        self.assertIn("b.addEventListener('pointerdown'", self.doc)
        self.assertIn("ev.stopPropagation();", self.doc)
        start = self.doc.index("b.addEventListener('pointerdown'", self.doc.index(".rptx"))
        end = self.doc.index("});", start)
        self.assertNotIn("preventDefault", self.doc[start:end])

    def test_the_page_it_was_opened_on_is_baked_in(self):
        self.assertIn("OPENED = '/b/board/QD/QD5-x.html'", self.doc)
        self.assertIn("INDEX = '/b/board/index.html'", self.doc)


if __name__ == "__main__":
    unittest.main()

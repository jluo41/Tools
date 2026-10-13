"""serve.py --share (live/share.py, b10 s52): the emailed-code sign-in Debate-AI uses, then only what the access
table grants; everything else is 404, and a shared link is read-only for all but owners."""
import http.client
import sys
import tempfile
import threading
import unittest
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlencode

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import serve  # noqa: E402
from live import share as S  # noqa: E402

TABLE = """owners: [owner@jhu.edu]
groups:
  team: [Member@JH.edu]
grants:
  - {who: viewer@jh.edu, what: proj/work/b01_alpha, level: view}
  - {who: "group:team", what: proj, level: view}
"""


def write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


class EmailAndTableTest(unittest.TestCase):
    def test_jhu_addresses_fold_and_match_exactly(self):
        self.assertEqual(S.canonical_email(" Rgao28@JH.edu "), "rgao28@jhu.edu")       # one inbox, two names
        self.assertEqual(S.canonical_email("rgao28@jhmi.edu"), "rgao28@jhmi.edu")      # its own mailbox
        self.assertIsNone(S.canonical_email("not an email"))
        for ok in ("a@jhu.edu", "a@jhmi.edu", "a@cs.jhu.edu"):
            self.assertTrue(S.accepted(ok), ok)
        for bad in ("a@evil-jhu.edu", "a@jhu.edu.evil.com", "a@gmail.com"):
            self.assertFalse(S.accepted(bad), bad)
        self.assertTrue(S.accepted("a@kennedykrieger.org", ("kennedykrieger.org",)))

    def test_the_table_gives_levels_by_email_group_and_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / ".server_config" / "access.yaml", TABLE)
            cfg = S.ShareConfig.load(root)
            self.assertEqual(cfg.level("viewer@jhu.edu", "proj/work/b01_alpha/j01_x/t01_y"), 1)
            self.assertEqual(cfg.level("viewer@jhu.edu", "proj/work/b02_beta"), 0)
            self.assertEqual(cfg.level("viewer@jhu.edu", "proj/work/b01_alphabet"), 0)   # a prefix is not a folder
            self.assertEqual(cfg.level("member@jhu.edu", "proj/work/b02_beta"), 1)       # the group, the Project
            self.assertEqual(cfg.level("owner@jhu.edu", "anything/at/all"), 4)
            self.assertFalse(cfg.named("stranger@jhu.edu"))
            self.assertTrue((root / ".server_config" / "share-secret").is_file())
            self.assertEqual(cfg.port, 0)                                                # no door port named

    def test_mail_goes_as_typed_signed_with_the_standard_library(self):
        """261012: zdi1@jh.edu got nothing; the code went to the folded zdi1@jhu.edu, and five doors' Python had no
        azure package. The address is the one typed; the call is ACS's HMAC scheme, checked here by recomputing it."""
        import base64
        import hashlib
        import hmac
        import json
        import urllib.request
        self.assertEqual(S.mail_to("  ZDI1@JH.edu "), "zdi1@jh.edu")
        self.assertEqual(S.canonical_email("zdi1@jh.edu"), "zdi1@jhu.edu")             # still one person to match
        self.assertIsNone(S.mail_to("not an address"))
        key = base64.b64encode(b"k" * 32).decode()
        seen = {}

        class Reply:
            status = 202
            def read(self): return b""
            def __enter__(self): return self
            def __exit__(self, *a): return False

        real = urllib.request.urlopen
        urllib.request.urlopen = lambda req, timeout=0: seen.setdefault("req", req) and Reply()
        try:
            S.acs_send(f"endpoint=https://acs.example.com/;accesskey={key}", "noreply@cdhai.com", "zdi1@jh.edu",
                       "Your sign-in code", "Your sign-in code is 123456.")
        finally:
            urllib.request.urlopen = real
        req = seen["req"]
        self.assertEqual(req.full_url, "https://acs.example.com/emails:send?api-version=" + S.ACS_API)
        self.assertEqual(json.loads(req.data)["recipients"]["to"], [{"address": "zdi1@jh.edu"}])
        h = {k.lower(): v for k, v in req.header_items()}
        digest = base64.b64encode(hashlib.sha256(req.data).digest()).decode()
        self.assertEqual(h["x-ms-content-sha256"], digest)
        signed = f"POST\n/emails:send?api-version={S.ACS_API}\n{h['x-ms-date']};acs.example.com;{digest}"
        sig = base64.b64encode(hmac.new(b"k" * 32, signed.encode(), hashlib.sha256).digest()).decode()
        self.assertTrue(h["authorization"].endswith("&Signature=" + sig))

    def test_a_space_door_uses_the_mail_key_above_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            write(Path(tmp) / ".server_config" / "share.env", "ACS_CONNECTION_STRING=endpoint=above\n")
            space = Path(tmp) / "A-SPACE"
            write(space / ".server_config" / "access.yaml", "owners: [owner@jhu.edu]\n")
            saved = S.os.environ.pop("SHARE_ACS_CONNECTION_STRING", None)
            try:
                self.assertEqual(S.ShareConfig.load(space).acs, "endpoint=above")          # one key, every door
                write(space / ".server_config" / "share.env", "ACS_CONNECTION_STRING=endpoint=own\n")
                self.assertEqual(S.ShareConfig.load(space).acs, "endpoint=own")            # its own wins
            finally:
                if saved is not None:
                    S.os.environ["SHARE_ACS_CONNECTION_STRING"] = saved

    def test_a_grant_keeps_the_door_note_and_a_list_names_the_door(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / ".server_config" / "access.yaml",
                  "# physician's door\npublic_url: https://door.example\nport: 5691\nowners: [owner@jhu.edu]\n")
            S.add_grant(root, "a@jh.edu", "proj")
            listed = S.people_group(root, "team")
            text = (root / ".server_config" / "access.yaml").read_text()
            self.assertTrue(text.startswith("# physician's door\n"))                     # its own note, kept
            self.assertIn("port: 5691", text)
            self.assertIn("(door.example)", listed.read_text())                         # the list names its door
            self.assertEqual(oct((root / ".server_config" / "access.yaml").stat().st_mode & 0o777), "0o600")

    def test_a_code_works_once_expires_and_is_rate_limited(self):
        with tempfile.TemporaryDirectory() as tmp:
            now = [1000.0]
            store = S.CodeStore(Path(tmp) / "codes.json", b"k", clock=lambda: now[0])
            code = store.issue("a@jhu.edu")
            self.assertTrue(store.verify("a@jhu.edu", code))
            self.assertFalse(store.verify("a@jhu.edu", code))                          # one use
            code = store.issue("a@jhu.edu")
            now[0] += S.CODE_TTL + 1
            self.assertFalse(store.verify("a@jhu.edu", code))                          # expired
            first, second = store.issue("a@jhu.edu"), store.issue("a@jhu.edu")
            self.assertTrue(store.verify("a@jhu.edu", first))                         # an older code still works
            self.assertFalse(store.verify("a@jhu.edu", second))                        # and ends the round
            code = store.issue("a@jhu.edu")
            for _ in range(S.CODE_TRIES):
                store.verify("a@jhu.edu", "000000" if code != "000000" else "111111")
            self.assertFalse(store.verify("a@jhu.edu", code))                          # five wrong tries end it
            for _ in range(S.SENDS_PER_HOUR):
                store.issue("b@jhu.edu")
            self.assertIsNone(store.issue("b@jhu.edu"))                                # five an hour


class ShareHostTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = self.root = Path(self.tmp.name).resolve()
        write(root / "env.sh", "")
        write(root / "proj" / "work" / "b01_alpha" / "board.md", "# alpha\n")
        write(root / "proj" / "work" / "b01_alpha" / "note.txt", "alpha note\n")
        write(root / "proj" / "work" / "b02_beta" / "board.md", "# beta\n")
        write(root / "other" / "secret.txt", "not shared\n")
        write(root / ".server_config" / "access.yaml",
              "owners: [owner@jhu.edu]\ngrants:\n  - {who: viewer@jh.edu, what: proj/work/b01_alpha, level: view}\n")

        class TestHandler(serve.Handler):
            pass
        TestHandler.root = root
        TestHandler.terminal_enabled = False
        TestHandler.auth_users = None
        TestHandler.configure_share(root)
        self.sent = {}
        self.real_send = S.send_code
        S.send_code = lambda cfg, email, code: self.sent.__setitem__(email, code) or "mail"
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), partial(TestHandler, directory=str(root)))
        self.handler = TestHandler
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.port = self.httpd.server_port

    def tearDown(self):
        S.send_code = self.real_send
        self.httpd.shutdown()
        self.httpd.server_close()
        self.tmp.cleanup()

    def ask(self, method, path, form=None, cookie=None):
        c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=30)
        headers = {"Cookie": cookie} if cookie else {}
        body = urlencode(form) if form is not None else None
        if body is not None:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        c.request(method, path, body=body, headers=headers)
        r = c.getresponse()
        data = r.read().decode("utf-8", "ignore")
        c.close()
        return r.status, r.getheader("Location") or "", r.getheader("Set-Cookie") or "", data

    def sign_in(self, email):
        self.ask("POST", "/_share/signin", {"email": email, "next": "/"})
        code = self.sent[email.strip().lower()]
        status, where, cookie, _ = self.ask("POST", "/_share/verify", {"email": email, "code": code, "next": "/"})
        self.assertEqual(status, 303)
        return cookie.split(";", 1)[0]

    def test_a_stranger_is_sent_to_sign_in_and_gets_no_code(self):
        status, where, _, _ = self.ask("GET", "/proj/work/b01_alpha/note.txt")
        self.assertEqual(status, 303)
        self.assertTrue(where.startswith("/_share/signin?next="))
        same = []
        for email in ("stranger@jhu.edu", "someone@gmail.com", "viewer@jh.edu"):
            status, _, _, page = self.ask("POST", "/_share/signin", {"email": email})
            self.assertEqual(status, 200)
            same.append(S.SAME_ANSWER in page)
            self.assertIn(f"Sent to {email}", page)                     # the address typed, never folded
        self.assertEqual(same, [True, True, True])                       # nobody learns who has access
        self.assertEqual(list(self.sent), ["viewer@jh.edu"])             # only a named email, as typed
        wrong = "000000" if self.sent["viewer@jh.edu"] != "000000" else "111111"
        status, _, _, _ = self.ask("POST", "/_share/verify", {"email": "viewer@jh.edu", "code": wrong})
        self.assertEqual(status, 401)

    def test_a_viewer_reaches_only_the_shared_block_and_reads_only(self):
        cookie = self.sign_in("Viewer@JH.edu")
        self.assertEqual(self.ask("GET", "/proj/work/b01_alpha/note.txt", cookie=cookie)[0], 200)
        status, _, _, page = self.ask("GET", "/_board/workbench?path=proj/work/b01_alpha&studio=1", cookie=cookie)
        self.assertEqual(status, 200)                                     # the Block's own workbench page
        self.assertIn("b01_alpha", page)
        self.assertEqual(self.ask("GET", "/_board/workbench?path=proj/work/b02_beta", cookie=cookie)[0], 404)
        self.assertEqual(self.ask("GET", "/proj/work/b02_beta/board.md", cookie=cookie)[0], 404)
        self.assertEqual(self.ask("GET", "/other/secret.txt", cookie=cookie)[0], 404)
        self.assertEqual(self.ask("GET", "/_board/page?path=%2Fproj%2Fwork%2Fb02_beta%2Fboard.md", cookie=cookie)[0], 404)
        self.assertEqual(self.ask("GET", "/_board/workbench?path=../../etc", cookie=cookie)[0], 404)
        self.assertEqual(self.ask("GET", "/_board/guide", cookie=cookie)[0], 404)          # names no path
        self.assertEqual(self.ask("POST", "/_board/studio-group", {"x": "1"}, cookie=cookie)[0], 403)
        status, _, _, home = self.ask("GET", "/", cookie=cookie)
        self.assertEqual(status, 200)
        self.assertIn("b01_alpha", home)
        self.assertNotIn("b02_beta", home)
        log = (self.root / ".server_config" / "share-log.tsv").read_text()
        self.assertIn("viewer@jhu.edu\tGET\t/proj/work/b01_alpha/note.txt", log)
        status, _, cleared, _ = self.ask("GET", "/_share/signout", cookie=cookie)
        self.assertIn("Max-Age=0", cleared)

    def test_a_forged_or_revoked_cookie_opens_nothing(self):
        cookie = self.sign_in("viewer@jhu.edu")
        forged = cookie[:-4] + ("0000" if not cookie.endswith("0000") else "1111")
        self.assertEqual(self.ask("GET", "/proj/work/b01_alpha/note.txt", cookie=forged)[0], 303)
        (self.root / ".server_config" / "access.yaml").write_text("owners: [owner@jhu.edu]\ngrants: []\n")
        self.handler.configure_share(self.root)       # the table is read at start
        self.assertEqual(self.ask("GET", "/proj/work/b01_alpha/note.txt", cookie=cookie)[0], 303)

    def test_anyone_at_jhu_opens_a_block_shared_that_way(self):
        S.add_grant(self.root, S.ANYONE_JHU, "proj/work/b02_beta")
        cookie = self.sign_in("Someone.New@jhmi.edu")                 # named nowhere, but a JHU email
        self.assertEqual(self.ask("GET", "/proj/work/b02_beta/board.md", cookie=cookie)[0], 200)
        self.assertEqual(self.ask("GET", "/proj/work/b01_alpha/note.txt", cookie=cookie)[0], 404)
        self.ask("POST", "/_share/signin", {"email": "someone@gmail.com"})
        self.assertNotIn("someone@gmail.com", self.sent)               # still JHU only

    def test_a_list_file_names_who_may_open_and_edits_apply_at_once(self):
        listed = S.people_group(self.root, "beta")
        S.add_grant(self.root, "group:beta", "proj/work/b02_beta")
        listed.write_text(listed.read_text() + "member.one@jh.edu   # a note\nnot-an-email\n")
        cookie = self.sign_in("member.one@jhu.edu")
        self.assertEqual(self.ask("GET", "/proj/work/b02_beta/board.md", cookie=cookie)[0], 200)
        self.assertEqual(self.ask("GET", "/proj/work/b01_alpha/note.txt", cookie=cookie)[0], 404)
        import os, time
        listed.write_text("# emptied\n")
        os.utime(listed, (time.time() + 5, time.time() + 5))             # a later save
        self.assertEqual(self.ask("GET", "/proj/work/b02_beta/board.md", cookie=cookie)[0], 303)   # out at once

    def test_a_link_from_the_desktop_door_still_lands(self):
        """261012: block.jjluo.com served the Desktop, so its links name the SPACE first; the SPACE's own door
        drops that name and sends the reader on."""
        name = self.root.name
        status, where, _, _ = self.ask("GET", f"/_board/workbench?path={name}/proj/work/b01_alpha&studio=1")
        self.assertEqual(status, 303)
        self.assertEqual(where, "/_board/workbench?path=proj/work/b01_alpha&studio=1")
        cookie = self.sign_in("viewer@jh.edu")
        self.assertEqual(self.ask("GET", where, cookie=cookie)[0], 200)
        status, where, _, _ = self.ask("GET", "/_board/workbench?path=proj/work/b01_alpha")    # nothing to move
        self.assertTrue(where.startswith("/_share/signin"))

    def test_an_owner_reaches_everything(self):
        cookie = self.sign_in("owner@jhu.edu")
        self.assertEqual(self.ask("GET", "/other/secret.txt", cookie=cookie)[0], 200)
        status, _, _, home = self.ask("GET", "/", cookie=cookie)                  # the share list, not a scan
        self.assertEqual(status, 200)
        self.assertIn("b01_alpha", home)
        self.assertEqual(self.ask("GET", "/proj/work/b02_beta/board.md", cookie=cookie)[0], 200)


if __name__ == "__main__":
    unittest.main()

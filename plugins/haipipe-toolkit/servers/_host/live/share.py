"""Share mode: named people open the Blocks they were given, after an emailed code (b10 s52, JL 261012).

`serve.py --share` turns it on. A person signs in the way Debate-AI signs people in (JHU-CDHAI/Debate-AI,
`apps/web/lib/email.ts`, `accounts.ts`, `auth.ts`): a JHU email, a six-digit code sent to it, then a signed
cookie. What they may open is the SPACE's access table, `.server_config/access.yaml`:

    owners: [jluo41@jhu.edu]                      # see and do everything, as without --share
    groups:
      shift: [a@jhu.edu, b@jhmi.edu]
    grants:                                       # what: a Block, Job or Task folder, or a whole Project
      - {who: group:shift, what: examples-0-cowork/Project-SHIFT-Study, level: view}
      - {who: c@jhu.edu, what: examples-0-cowork/Project-SHIFT-Study/cowork/b21_event_cgm, level: view}
      - {who: anyone@jhu, what: Tools-SPACE/blueprints/b10_project_workbench, level: view}   # any JHU email
    extra_domains: []                             # beyond jhu.edu, jh.edu, jhmi.edu and their subdomains
    mail_from: noreply@cdhai.com

Rules, each as Debate-AI keeps them unless said:

1. **Email**: jhu.edu, jh.edu, jhmi.edu and their subdomains (and `extra_domains`); jh.edu and jhu.edu are one
   person when matching a grant, jhmi.edu stays its own; a domain matches exactly or as a subdomain, never by its
   ending alone. The code goes to the address as typed (JL 261012: zdi1@jh.edu got nothing while it went to
   zdi1@jhu.edu, which is not always a mailbox).
2. **Code**: six digits, 10 minutes, one use, five wrong tries; ten codes an hour per email, and any code
   still within its 10 minutes works (JL 261012: a newer code had made the one in the inbox fail); kept hashed.
3. **Only named people get one** (not Debate-AI's rule): a code goes only to an owner or an email the table names,
   and everyone sees the same answer, so nobody learns who has access.
4. **Mail**: Azure Communication Services, as Debate-AI (`ACS_CONNECTION_STRING` in `.server_config/share.env`,
   the root's or the nearest above it, so one key serves every SPACE's door; from `mail_from`), through its REST
   API with the standard library (`acs_send`), so a door sends on any SPACE's Python (261012: five doors ran on a
   .venv without the azure package and sent nothing). With no mail, an owner's code goes to the server log, and nobody else gets one.
5. **Session**: a signed cookie (HMAC with `.server_config/share-secret`), HTTP-only, seven days.
6. **What a request may reach**: every path it names (`path=`, `board=`, ... or the file it asks for) must sit
   inside a grant; an owner reaches everything; anything else is 404, as if it were not there. The Excalidraw
   app's own files are open to anyone signed in with a grant.
7. **Levels**: view < comment < edit < owner. This first version is read-only for all but owners: a POST, the
   terminal and chat are an owner's (s52 Open 5).
8. **Who opened what**: one line per granted request in `.server_config/share-log.tsv` (s52 Open 4).
"""
from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import html
import json
import os
import re
import secrets
import sys
import threading
import time
from dataclasses import dataclass, field
from http.cookies import SimpleCookie
from pathlib import Path
from urllib.parse import parse_qs, parse_qsl, quote, unquote, urlencode, urlsplit, urlunsplit

LEVELS = {"view": 1, "comment": 2, "edit": 3, "owner": 4}
INSTITUTION = ("jhu.edu", "jh.edu", "jhmi.edu")
FOLD = {"jh.edu": "jhu.edu"}                     # one person, two names, when matching; mail goes as typed
CODE_TTL, CODE_TRIES, SENDS_PER_HOUR, SESSION_DAYS = 600, 5, 10, 7
COOKIE = "hai_share"
PATH_KEYS = ("path", "board", "file", "folder", "page", "md")
OPEN_PREFIXES = ("/_excalidraw", "/assets/", "/favicon", "/manifest.webmanifest", "/apple-touch-icon.png",
                 "/_assets/")
EMAIL = re.compile(r"^[a-z0-9._%+\-]+@([a-z0-9\-]+(?:\.[a-z0-9\-]+)+)$")
SAME_ANSWER = "If this email has access, a code is on its way. It works for 10 minutes."
CODE_NOTE = ("Any code from the last 10 minutes works. At most 10 codes an hour go to one email; "
             "if none arrives, use one you already have, or wait.")
ANYONE_JHU = "anyone@jhu"                              # who: any JHU email may open it (a link to share widely)


# ── who ────────────────────────────────────────────────────────────────────────────────────────

def canonical_email(raw: str) -> str | None:
    """The one form of an address for matching, or None when it is not one: lower case; jh.edu becomes jhu.edu.
    Never the address to mail: that is the one typed (`mail_to`)."""
    email = (raw or "").strip().lower()
    m = EMAIL.match(email)
    if not m:
        return None
    local, domain = email.split("@", 1)
    return f"{local}@{FOLD.get(domain, domain)}"


def mail_to(raw: str) -> str | None:
    """The address a code goes to: as typed, lower case, or None when it is not an address."""
    email = (raw or "").strip().lower()
    return email if EMAIL.match(email) else None


def accepted(email: str, extra: tuple = ()) -> bool:
    """A JHU address (or an extra domain): the domain itself or a subdomain of it, never by its ending alone
    (`evil-jhu.edu`, `jhu.edu.evil.com` fail)."""
    domain = email.rsplit("@", 1)[-1]
    return any(domain == base or domain.endswith("." + base) for base in (*INSTITUTION, *extra))


# ── the access table ───────────────────────────────────────────────────────────────────────────

def people(path: Path) -> list:
    """The emails in a list file, one per line; blank lines and # comments skipped (JL 261012: "could I only
    prepare a list of jh emails, only these people can access it")."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    return [ln.split("#", 1)[0].strip() for ln in lines if ln.split("#", 1)[0].strip()]


def stamp(paths) -> tuple:
    out = []
    for p in paths:
        try:
            out.append(p.stat().st_mtime if p.is_file() else 0.0)
        except OSError:
            out.append(-1.0)
    return tuple(out)


def _rel(value: str) -> str:
    return unquote(value).strip().strip("/").replace("\\", "/")


@dataclass
class ShareConfig:
    root: Path
    owners: set = field(default_factory=set)
    groups: dict = field(default_factory=dict)
    grants: list = field(default_factory=list)          # (who, what, level)
    extra_domains: tuple = ()
    mail_from: str = "noreply@cdhai.com"
    acs: str = ""
    secret: bytes = b""
    mtime: tuple = ()                                    # access.yaml's and its list files', to re-read on change
    public_url: str = ""
    watched: tuple = ()                                  # the list files its groups read
    port: int = 0                                        # this door's local port (`wb.py share --serve`)

    @classmethod
    def load(cls, root) -> "ShareConfig":
        import yaml
        root = Path(root).resolve()
        cfg_dir = root / ".server_config"
        table = cfg_dir / "access.yaml"
        data = yaml.safe_load(table.read_text(encoding="utf-8")) if table.is_file() else {}
        data = data or {}
        owners = {e for e in (canonical_email(x) for x in data.get("owners") or []) if e}
        groups, watched = {}, []
        for g, members in (data.get("groups") or {}).items():
            if isinstance(members, str) and members.startswith("@"):     # "@people/b10.txt": a list file
                listed = Path(members[1:]).expanduser()
                listed = listed if listed.is_absolute() else cfg_dir / listed
                watched.append(listed)
                members = people(listed)
            groups[str(g)] = {e for e in (canonical_email(x) for x in members or []) if e}
        grants = []
        for g in data.get("grants") or []:
            level = str(g.get("level", "view")).lower()
            if level not in LEVELS:
                raise ValueError(f"access.yaml: level {level!r} is not one of {', '.join(LEVELS)}")
            who = str(g.get("who", "")).strip().lower()
            who = who if who.startswith("group:") or who == ANYONE_JHU else (canonical_email(who) or "")
            what = _rel(str(g.get("what", "")))
            if who and what:
                grants.append((who, what, LEVELS[level]))
        secret_file = cfg_dir / "share-secret"
        if not secret_file.is_file():
            cfg_dir.mkdir(exist_ok=True)
            secret_file.write_bytes(secrets.token_bytes(32))
            os.chmod(secret_file, 0o600)
        acs = os.environ.get("SHARE_ACS_CONNECTION_STRING", "")
        env = next((d / ".server_config" / "share.env" for d in (root, *root.parents)
                    if (d / ".server_config" / "share.env").is_file()), None)   # the nearest: one key, every door
        if not acs and env:
            for line in env.read_text(encoding="utf-8").splitlines():
                key, _, value = line.partition("=")
                if key.strip() == "ACS_CONNECTION_STRING":
                    acs = value.strip().strip("\"'")
        return cls(root, owners, groups, grants,
                   tuple(str(d).lower().lstrip("@") for d in data.get("extra_domains") or []),
                   str(data.get("mail_from") or "noreply@cdhai.com"), acs, secret_file.read_bytes(),
                   stamp([table, *watched]), str(data.get("public_url") or ""), tuple(watched),
                   int(data.get("port") or 0))

    def _is(self, email: str, who: str) -> bool:
        if who == ANYONE_JHU:                            # one link for everyone at JHU (JL 261012)
            return accepted(email, self.extra_domains)
        return email in self.groups.get(who[6:], set()) if who.startswith("group:") else email == who

    def named(self, email: str) -> bool:
        """An owner, or someone the table gives something: the only addresses a code is sent to."""
        return email in self.owners or any(self._is(email, who) for who, _, _ in self.grants)

    def level(self, email: str, rel: str) -> int:
        """This email's level on one SPACE-relative path: the highest grant that holds it, 0 for none."""
        if email in self.owners:
            return LEVELS["owner"]
        rel = rel.strip("/")
        return max([lvl for who, what, lvl in self.grants if self._is(email, who)
                    and (rel == what or rel.startswith(what + "/"))] or [0])

    def given(self, email: str) -> list:
        """(what, level) for each grant this email holds, highest level per path."""
        best: dict = {}
        for who, what, lvl in self.grants:
            if self._is(email, who):
                best[what] = max(best.get(what, 0), lvl)
        return sorted(best.items())


# ── codes ──────────────────────────────────────────────────────────────────────────────────────

class CodeStore:
    """Codes, hashed, in .server_config/share-codes.json; one lock for the threaded server."""

    def __init__(self, path: Path, secret: bytes, clock=time.time):
        self.path, self.secret, self.clock, self.lock = path, secret, clock, threading.Lock()

    def _hash(self, email: str, code: str) -> str:
        return hmac.new(self.secret, f"{email}\n{code}".encode(), hashlib.sha256).hexdigest()

    def _load(self) -> dict:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}

    def _save(self, data: dict) -> None:
        self.path.parent.mkdir(exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data), encoding="utf-8")
        os.chmod(tmp, 0o600)
        tmp.replace(self.path)

    def issue(self, email: str) -> str | None:
        """A new code for this email, or None when it has had SENDS_PER_HOUR codes in the last hour. Codes sent
        before it stay good until they expire, so whichever email arrives first works."""
        now = self.clock()
        with self.lock:
            data = self._load()
            row = data.get(email) or {}
            sent = [t for t in row.get("sent", []) if now - t < 3600]
            if len(sent) >= SENDS_PER_HOUR:
                return None
            code = f"{secrets.randbelow(10 ** 6):06d}"
            live = [c for c in row.get("codes", []) if c.get("expires", 0) >= now]
            data[email] = {"codes": live + [{"hash": self._hash(email, code), "expires": now + CODE_TTL}],
                           "tries": row.get("tries", 0) if live else 0, "sent": sent + [now]}
            self._save(data)
            return code

    def verify(self, email: str, code: str) -> bool:
        """True once for any of this email's unexpired codes; one success ends them all; five wrong tries too."""
        now = self.clock()
        with self.lock:
            data = self._load()
            row = data.get(email)
            live = [c for c in (row or {}).get("codes", []) if c.get("expires", 0) >= now]
            if not live:
                return False
            given = self._hash(email, (code or "").strip())
            if any(hmac.compare_digest(c["hash"], given) for c in live):
                row["codes"], row["tries"] = [], 0          # one use: every code of this round ends
                self._save(data)
                return True
            row["tries"] = row.get("tries", 0) + 1
            row["codes"] = [] if row["tries"] >= CODE_TRIES else live
            self._save(data)
            return False


ACS_API = "2023-03-31"


def acs_request(conn: str, method: str, path: str, body: bytes = b"") -> tuple:
    """One signed call to Azure Communication Services (its HMAC-SHA256 scheme, the standard library only):
    (HTTP status, response text). `conn` is the connection string, `endpoint=https://...;accesskey=...`."""
    import base64 as b64
    import urllib.error
    import urllib.request
    from email.utils import formatdate
    parts = dict(kv.split("=", 1) for kv in conn.strip().strip(";").split(";") if "=" in kv)
    endpoint, key = parts["endpoint"].rstrip("/"), b64.b64decode(parts["accesskey"])
    host = urlsplit(endpoint).netloc
    path = f"{path}{'&' if '?' in path else '?'}api-version={ACS_API}"
    date = formatdate(usegmt=True)
    digest = b64.b64encode(hashlib.sha256(body).digest()).decode()
    signed = f"{method}\n{path}\n{date};{host};{digest}"
    sig = b64.b64encode(hmac.new(key, signed.encode(), hashlib.sha256).digest()).decode()
    req = urllib.request.Request(endpoint + path, data=body or None, method=method, headers={
        "Content-Type": "application/json", "x-ms-date": date, "x-ms-content-sha256": digest,
        "Authorization": f"HMAC-SHA256 SignedHeaders=x-ms-date;host;x-ms-content-sha256&Signature={sig}"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "ignore")


def acs_send(conn: str, sender: str, to: str, subject: str, text: str) -> None:
    """Hand one plain email to Azure Communication Services; it answers 202 when it takes it."""
    body = json.dumps({"senderAddress": sender, "recipients": {"to": [{"address": to}]},
                       "content": {"subject": subject, "plainText": text}}).encode()
    status, reply = acs_request(conn, "POST", "/emails:send", body)
    if status != 202:
        raise RuntimeError(f"HTTP {status}: {reply[:200]}")


def send_code(cfg: ShareConfig, email: str, code: str) -> str:
    """Email the code to `email` as typed ("mail"); with no mail set up, an owner's code goes to the server log
    ("log"); else "none"."""
    if cfg.acs:
        try:
            acs_send(cfg.acs, cfg.mail_from, email, "Your sign-in code",
                     f"Your sign-in code is {code}. It works for 10 minutes.\n\n"
                     "If you did not ask for it, you can ignore this email.")
            print(f"[share] code mailed to {email}", file=sys.stderr, flush=True)
            return "mail"
        except Exception as exc:                             # noqa: BLE001: report, never crash a request
            print(f"[share] mail to {email} failed: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
    if canonical_email(email) in cfg.owners:
        print(f"[share] no mail set up: sign-in code for owner {email}: {code}", file=sys.stderr, flush=True)
        return "log"
    return "none"


TABLE_HEAD = ("# Who may open what on this SPACE's share door (serve.py --share; b10 s52). Git-ignored.\n"
              "# Edit by hand or with `wb.py share <folder> <email>`; the door reads it again when it changes.\n")


def _save_table(table: Path, data: dict) -> None:
    """Write access.yaml (mode 600: it holds emails), keeping the comment lines it starts with, the door's own
    note, else TABLE_HEAD."""
    import yaml
    head = ""
    for ln in (table.read_text(encoding="utf-8").splitlines() if table.is_file() else []):
        if not ln.startswith("#"):
            break
        head += ln + "\n"
    table.parent.mkdir(exist_ok=True)
    table.write_text((head or TABLE_HEAD) + yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    os.chmod(table, 0o600)


def add_grant(root, who: str, what: str, level: str = "view") -> dict:
    """Write one grant into access.yaml (/wb share); an existing line for the same who and what takes the level."""
    import yaml
    level = level.lower()
    if level not in LEVELS or level == "owner":
        raise ValueError(f"level {level!r}: view, comment or edit (owners are listed under owners:)")
    who = who.strip().lower()
    if not who.startswith("group:") and who != ANYONE_JHU:
        email = canonical_email(who)
        if not email or not accepted(email):
            raise ValueError(f"{who!r} is not a JHU email (jhu.edu, jh.edu, jhmi.edu) or group:<name>")
        who = email
    root = Path(root).resolve()
    table = root / ".server_config" / "access.yaml"
    data = (yaml.safe_load(table.read_text(encoding="utf-8")) if table.is_file() else None) or {}
    data.setdefault("owners", [])
    grants = [g for g in data.get("grants") or [] if not (str(g.get("who", "")).lower() == who
                                                         and _rel(str(g.get("what", ""))) == _rel(what))]
    grants.append({"who": who, "what": _rel(what), "level": level})
    data["grants"] = grants
    _save_table(table, data)
    return {"who": who, "what": _rel(what), "level": level}


def people_group(root, name: str) -> Path:
    """Make group <name> read `.server_config/people/<name>.txt` (created with a short header when missing), and
    return that file: the list JL keeps, one JHU email per line."""
    import yaml
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", name or ""):
        raise ValueError(f"group name {name!r}: lower-case letters, digits, - and _")
    root = Path(root).resolve()
    cfg_dir = root / ".server_config"
    listed = cfg_dir / "people" / f"{name}.txt"
    table = cfg_dir / "access.yaml"
    data = (yaml.safe_load(table.read_text(encoding="utf-8")) if table.is_file() else None) or {}
    door = urlsplit(str(data.get("public_url") or "")).netloc or "this SPACE's share door"
    if not listed.is_file():
        listed.parent.mkdir(parents=True, exist_ok=True)
        listed.write_text(f"# Who may open what group:{name} is given ({door}). One JHU email per line\n"
                          "# (jhu.edu, jh.edu, jhmi.edu); a line starting with # is a note. Saved changes apply\n"
                          "# at the next click: add a line to let someone in, delete it to take them out.\n",
                          encoding="utf-8")
        os.chmod(listed, 0o600)
    groups = data.get("groups") or {}
    groups[name] = f"@people/{name}.txt"
    data["groups"] = groups
    _save_table(table, data)
    return listed


# ── the handler ────────────────────────────────────────────────────────────────────────────────

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<style>body{{font:16px/1.5 -apple-system,Segoe UI,sans-serif;background:#f6f7f9;color:#1e1e1e;margin:0}}
main{{max-width:420px;margin:12vh auto;background:#fff;border:1px solid #d6d9de;border-radius:10px;padding:28px}}
h1{{font-size:22px;margin:0 0 12px}}p{{color:#495057}}input{{width:100%;box-sizing:border-box;font-size:18px;padding:10px;
margin:6px 0 14px;border:1px solid #ced4da;border-radius:6px}}button{{font-size:16px;padding:10px 16px;border:0;
border-radius:6px;background:#1c7ed6;color:#fff;cursor:pointer}}ul{{padding-left:18px}}a{{color:#1c7ed6}}
.small{{font-size:13px;color:#868e96}}</style></head><body><main>{body}</main></body></html>"""


class ShareMixin:
    """Ahead of AuthMixin: with `share` set, every request passes share_gate first; without it, nothing changes."""

    share: ShareConfig | None = None
    share_codes: CodeStore | None = None
    share_user: str | None = None

    @classmethod
    def configure_share(cls, root) -> ShareConfig:
        cls.share = ShareConfig.load(root)
        cls.share_codes = CodeStore(cls.share.root / ".server_config" / "share-codes.json", cls.share.secret)
        return cls.share

    def require_request_auth(self) -> bool:
        if self.share is None:
            return super().require_request_auth()
        self.share_fresh()
        return self.share_gate()

    def share_fresh(self) -> None:
        """Read access.yaml again when it, or a group's list file, has changed (`/wb share` edits it; JL edits a
        list): a grant takes effect at once, and a removed one ends at the next request."""
        table = self.share.root / ".server_config" / "access.yaml"
        if stamp([table, *self.share.watched]) != self.share.mtime:
            try:
                type(self).share = ShareConfig.load(self.share.root)
            except (OSError, ValueError) as exc:
                print(f"[share] access.yaml not read again, the old table stays: {exc}", file=sys.stderr, flush=True)

    # the gate --------------------------------------------------------------------------------------
    def share_gate(self) -> bool:
        path = urlsplit(self.path).path
        if path.startswith("/_share/"):
            self.share_route(path)
            return False
        moved = self.share_old_link() if self.command in ("GET", "HEAD") else None
        if moved:
            return self.share_redirect(moved)
        email = self.share_cookie_email()
        if not email:
            if self.command in ("GET", "HEAD"):
                return self.share_redirect("/_share/signin?" + urlencode({"next": self.path}))
            self.close_connection = True
            return self.share_send(401, "Sign in first.", plain=True)
        self.share_user = email
        if path == "/":                                  # everyone, owners too: the root may hold every SPACE
            return self.share_home(email)
        if email in self.share.owners:
            self.share_note(email)
            return True
        if self.command not in ("GET", "HEAD") or path.startswith("/_term") or path.startswith("/_board/chat"):
            self.close_connection = self.command == "POST"
            return self.share_send(403, "This shared link is read-only.", plain=True)
        if self.share_reach(email, path) <= 0:
            self.send_error(404, "not found")
            return False
        self.share_note(email)
        return True

    def share_old_link(self) -> str | None:
        """A link from when one door served the whole Desktop names its SPACE first (`path=Tools-SPACE/blueprints/
        b10_...`); on that SPACE's own door the page is `path=blueprints/b10_...` (261012: one door per SPACE).
        The same address without the SPACE's name, or None when nothing names it."""
        parts = urlsplit(self.path)
        lead, root, moved, query = self.share.root.name + "/", self.share.root, False, []
        for k, v in parse_qsl(parts.query, keep_blank_values=True):
            if k in PATH_KEYS and _rel(v).startswith(lead) and not (root / _rel(v)).exists():
                v, moved = _rel(v)[len(lead):], True
            query.append((k, v))
        return urlunsplit(("", "", parts.path, urlencode(query, safe="/"), parts.fragment)) if moved else None

    def share_reach(self, email: str, path: str) -> int:
        """The lowest level among every path this request names; open app files for anyone with a grant."""
        query = parse_qs(urlsplit(self.path).query)
        named = [v for k in PATH_KEYS for v in query.get(k, []) if v.strip()]
        if not named and not path.startswith("/_"):
            named = [path]                                   # a file asked for directly
        if not named:
            return 1 if path.startswith(OPEN_PREFIXES) and self.share.given(email) else 0
        root = self.share.root
        levels = []
        for value in named:
            try:
                target = (root / _rel(value)).resolve()
                rel = target.relative_to(root).as_posix()
            except (OSError, ValueError):
                return 0                                     # outside the SPACE
            levels.append(self.share.level(email, rel))
        return min(levels)

    def share_note(self, email: str) -> None:
        log = self.share.root / ".server_config" / "share-log.tsv"
        try:
            fd = os.open(log, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)     # emails: this account only
            with os.fdopen(fd, "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{email}\t{self.command}\t{self.path[:300]}\n")
        except OSError:
            pass

    # the cookie ------------------------------------------------------------------------------------
    def _share_sign(self, payload: str) -> str:
        return hmac.new(self.share.secret, payload.encode(), hashlib.sha256).hexdigest()

    def share_cookie_email(self) -> str | None:
        try:
            morsel = SimpleCookie(self.headers.get("Cookie", "")).get(COOKIE)
            if morsel is None:
                return None
            encoded, signature = morsel.value.rsplit(".", 1)
            if not hmac.compare_digest(self._share_sign(encoded), signature):
                return None
            email, expires = base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)).decode().split("\n", 1)
            if int(expires) <= time.time() or not self.share.named(email):
                return None                                  # expired, or taken off the table since
            return email
        except (ValueError, UnicodeDecodeError, binascii.Error):
            return None

    def share_cookie(self, email: str | None) -> str:
        secure = (self.headers.get("X-Forwarded-Proto", "").lower() == "https"
                  or getattr(self, "public_url", "").startswith("https://"))
        if email is None:
            value, age = "", 0
        else:
            expires = int(time.time()) + SESSION_DAYS * 86400
            encoded = base64.urlsafe_b64encode(f"{email}\n{expires}".encode()).decode().rstrip("=")
            value, age = f"{encoded}.{self._share_sign(encoded)}", SESSION_DAYS * 86400
        return f"{COOKIE}={value}; Path=/; Max-Age={age}; HttpOnly; SameSite=Lax" + ("; Secure" if secure else "")

    # pages -----------------------------------------------------------------------------------------
    def share_send(self, status: int, body: str, *, title: str = "Sign in", cookie: str | None = None,
                   plain: bool = False) -> bool:
        data = (body + "\n" if plain else PAGE.format(title=html.escape(title), body=body)).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8" if plain else "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)
        return False

    def share_redirect(self, to: str, cookie: str | None = None) -> bool:
        self.send_response(303)
        self.send_header("Location", to)
        self.send_header("Content-Length", "0")
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        return False

    def share_form(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(min(n, 4096)).decode("utf-8", "ignore") if n else ""
        return {k: v[0] for k, v in parse_qs(raw).items()}

    @staticmethod
    def share_next(value: str) -> str:
        return value if value.startswith("/") and not value.startswith("//") else "/"

    def share_route(self, path: str) -> None:
        if path == "/_share/signout":
            self.share_redirect("/_share/signin", cookie=self.share_cookie(None))
            return
        if path == "/_share/signin" and self.command in ("GET", "HEAD"):
            nxt = self.share_next(parse_qs(urlsplit(self.path).query).get("next", ["/"])[0])
            self.share_send(200, '<h1>Sign in</h1><p>Your JHU email. A six-digit code will be sent to it.</p>'
                            '<form method="post" action="/_share/signin">'
                            f'<input type="hidden" name="next" value="{html.escape(nxt)}">'
                            '<input name="email" type="email" autocomplete="email" required autofocus '
                            'placeholder="name@jhu.edu"><button>Send me a code</button></form>')
            return
        if path == "/_share/signin" and self.command == "POST":
            form = self.share_form()
            nxt = self.share_next(form.get("next", "/"))
            typed, email = mail_to(form.get("email", "")), canonical_email(form.get("email", ""))
            if email and accepted(email, self.share.extra_domains) and self.share.named(email):
                code = self.share_codes.issue(email)
                if code:
                    send_code(self.share, typed, code)       # as typed: zdi1@jh.edu, never folded (261012)
            shown = html.escape(typed or form.get("email", ""))
            self.share_send(200, f'<h1>Check your inbox</h1><p>{SAME_ANSWER}</p>'
                            '<form method="post" action="/_share/verify">'
                            f'<input type="hidden" name="next" value="{html.escape(nxt)}">'
                            f'<input type="hidden" name="email" value="{shown}">'
                            '<input name="code" inputmode="numeric" autocomplete="one-time-code" maxlength="6" '
                            'required autofocus placeholder="six digits"><button>Sign in</button></form>'
                            f'<p class="small">{CODE_NOTE}</p>'
                            f'<p class="small">Sent to {shown}. <a href="/_share/signin">Use another email</a></p>')
            return
        if path == "/_share/verify" and self.command == "POST":
            form = self.share_form()
            email = canonical_email(form.get("email", ""))
            if email and self.share.named(email) and self.share_codes.verify(email, form.get("code", "")):
                self.share_redirect(self.share_next(form.get("next", "/")), cookie=self.share_cookie(email))
                return
            self.share_send(401, '<h1>That code did not work</h1><p>It may be wrong or expired. '
                            '<a href="/_share/signin">Ask for a new code</a>.</p>')
            return
        self.send_error(404, "not found")

    def share_home(self, email: str) -> bool:
        rows = []
        owner = email in self.share.owners
        given = sorted({what: lvl for _, what, lvl in self.share.grants}.items()) if owner else self.share.given(email)
        for what, lvl in given:
            name = {v: k for k, v in LEVELS.items()}[lvl]
            for block in self.share_blocks(what):
                link = "/_board/workbench?" + urlencode({"path": block, "studio": "1"}, safe="/")
                rows.append(f'<li><a href="{html.escape(link)}">{html.escape(block.rsplit("/", 1)[-1])}</a> '
                            f'<span class="small">{name} · {html.escape(block)}</span></li>')
        body = (f"<h1>{'Shared from here' if owner else 'Shared with you'}</h1><p class='small'>Signed in as "
                f"{html.escape(email)}{' (owner: every folder opens for you)' if owner else ''} · "
                "<a href='/_share/signout'>sign out</a></p>"
                + (f"<ul>{''.join(rows)}</ul>" if rows else "<p>Nothing is shared with this email yet.</p>"))
        return self.share_send(200, body, title="Shared with you")

    def share_blocks(self, what: str) -> list:
        """The Blocks a grant opens: itself when it is a Block, Job or Task folder; else the Blocks under it."""
        base = self.share.root / what
        if (base / "board.md").is_file() or re.match(r"^[bjt]\d{2,3}_", base.name):
            return [what]
        found = sorted(p.parent.relative_to(self.share.root).as_posix() for p in base.glob("*/*/board.md"))
        found += sorted(p.parent.relative_to(self.share.root).as_posix() for p in base.glob("*/board.md"))
        return [b for b in dict.fromkeys(found) if "/_" not in "/" + b] or [what]

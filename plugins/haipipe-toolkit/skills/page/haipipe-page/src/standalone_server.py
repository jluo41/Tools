"""Bounded, stdlib HTTP transport for one Page, independent of any Board.

Public entry points: create_server(context, host='127.0.0.1', port=0,
token=None, read_only=False, public_url=None) and serve(same arguments).
The returned ThreadingHTTPServer exposes startup_url and supports shutdown().
Tokens can be supplied as Authorization: Bearer or exchanged for a cookie at
startup_url. Reverse proxies must preserve Host and use the public_url origin.
"""
from __future__ import annotations

import hmac
import ipaddress
import json
import mimetypes
import os
import re
import secrets
import socket
import stat
import threading
from dataclasses import replace
from http.cookies import SimpleCookie
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlsplit

from live.delivery import DeliveryTabMixin
from live.evidence import EvidenceTabMixin
from live.folderstat import FolderStatMixin
from live.outline import OutlineMixin
from live.runs import RunsTabMixin
from live.value import ValueMixin
from src import page_workspace

ASSETS = Path(__file__).resolve().parent.parent / 'assets'
MAX_BODY = 4 * 1024 * 1024
PUBLIC_SUFFIXES = {
    '.html', '.htm', '.css', '.js', '.svg', '.png', '.jpg', '.jpeg', '.gif',
    '.webp', '.ico', '.pdf', '.woff', '.woff2', '.ttf', '.avif', '.mp4', '.mp3',
}
PRIVATE_PARTS = page_workspace.PRIVATE_LANES | page_workspace.PRIVATE_FILES


def _origin(value):
    """Normalize an origin without trusting DNS or forwarding headers."""
    parsed = urlsplit(value)
    if (parsed.scheme not in {'http', 'https'} or not parsed.hostname
            or parsed.username or parsed.password or parsed.query
            or parsed.fragment or parsed.path not in {'', '/'}):
        raise ValueError('Expected an http(s) origin without a path')
    host = parsed.hostname.lower()
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    return parsed.scheme, host, port


def _local(host):
    if host.lower() == 'localhost':
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def _relative(value):
    if not isinstance(value, str) or not value or '\\' in value or '\x00' in value:
        raise ValueError('Invalid Page path')
    if value.startswith('/') or any(p in {'', '.', '..'} for p in value.split('/')):
        raise ValueError('Path must stay inside this Page folder')
    if (any(p.startswith('.') or p.lower() in page_workspace.PRIVATE_FILES for p in value.split('/'))
            or value.split('/')[0].lower() in page_workspace.PRIVATE_LANES):
        raise ValueError('Private Page path')
    return Path(value)


class PageHandler(OutlineMixin, EvidenceTabMixin, ValueMixin, FolderStatMixin,
                  RunsTabMixin, DeliveryTabMixin,
                  SimpleHTTPRequestHandler):
    """No directory listings, Board discovery, subprocesses or terminal APIs."""

    # Standalone Delivery presents artifacts already on disk. Its Board-only
    # build/author routes are deliberately not advertised or called.
    delivery_interactive = False
    delivery_asset_base = ""

    def __init__(self, *args, **kwargs):
        self.root = self.server_context.folder.resolve()  # set on bound subclass
        super().__init__(*args, directory=str(self.root), **kwargs)

    def setup(self):
        super().setup()
        self.connection.settimeout(15)

    def log_message(self, fmt, *args):
        # A login URL carries a token; never log request targets or headers.
        pass

    def end_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def _send(self, status, body, content_type='text/html; charset=utf-8', **headers):
        if isinstance(body, str):
            body = body.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        for key, value in headers.items():
            self.send_header(key.replace('_', '-'), value)
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(body)

    def reply(self, code, obj):
        self._send(code, json.dumps(obj, ensure_ascii=False),
                   'application/json; charset=utf-8')

    def _error(self, code, message):
        self.reply(code, {'ok': False, 'err': message})

    def _host_origin(self):
        hosts = self.headers.get_all('Host', [])
        if len(hosts) != 1:
            raise ValueError('Exactly one Host header is required')
        if any(char.isspace() or char in '/?#@\\' for char in hosts[0]):
            raise ValueError('Invalid Host header')
        # public_url determines the external scheme; forwarded headers cannot.
        origin = _origin(self.server.external_scheme + '://' + hosts[0])
        if origin not in self.server.allowed_origins:
            raise ValueError('Host is not an allowed Page origin')
        return origin

    def _authenticated(self):
        if self.server.token is None:
            return True
        auth = self.headers.get('Authorization', '')
        if auth.startswith('Bearer ') and hmac.compare_digest(
                auth[7:].encode(), self.server.token.encode()):
            return True
        cookie = SimpleCookie()
        try:
            cookie.load(self.headers.get('Cookie', ''))
            value = cookie.get(self.server.cookie_name)
            return bool(value and hmac.compare_digest(
                value.value.encode(), self.server.session_cookie.encode()))
        except Exception:
            return False

    def _guard(self, writing=False, login=False):
        try:
            host_origin = self._host_origin()
            if writing:
                origins = self.headers.get_all('Origin', [])
                bearer = self.headers.get('Authorization', '').startswith('Bearer ')
                if len(origins) > 1 or (not origins and not bearer):
                    raise ValueError('A same-origin Origin header is required')
                if origins and _origin(origins[0]) != host_origin:
                    raise ValueError('Origin does not match Host')
                if self.headers.get('Sec-Fetch-Site') == 'cross-site':
                    raise ValueError('Cross-site writes are forbidden')
        except ValueError as exc:
            self._error(403, str(exc))
            return False
        if not login and not self._authenticated():
            self._error(401, 'Authentication required; open the Page login URL')
            return False
        if writing and not login and self.server.read_only:
            self._error(403, 'This Page server is read-only')
            return False
        return True

    def _bounded(self, relative):
        path = self.root / _relative(relative)
        if not path.resolve().is_relative_to(self.root):
            raise ValueError('Path escapes the Page folder')
        # Disallow even internal links: the resolved target could change later.
        for part in (path, *path.parents):
            if part == self.root:
                break
            if part.is_symlink():
                raise ValueError('Symlinks are not served or edited')
        return path

    def _safe_page_tree(self):
        # Shared viewers read nested evidence and plan files directly. Refuse
        # linked trees before handing them to a viewer or its write handler.
        for parent, dirs, files in os.walk(self.root, followlinks=False):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in PRIVATE_PARTS]
            for name in dirs + files:
                if (Path(parent) / name).is_symlink():
                    raise ValueError('Page viewers require a folder without symlinks')

    def target(self, payload):
        try:
            source = self.server.context.source
            relative = source.relative_to(self.root).as_posix()
            requested = payload.get('file') or relative
            if requested != relative:
                raise ValueError('Only this Page source may be targeted')
            # path is presentation context, never an alternate filesystem root.
            path = payload.get('path') or ''
            if not isinstance(path, str) or '..' in unquote(path).split('/') or '\\' in path:
                raise ValueError('Invalid Page location')
            self._bounded(relative)
            self._safe_page_tree()
            return source, self.root
        except (ValueError, OSError) as exc:
            return None, str(exc)

    def translate_path(self, path):
        return str(self._bounded(unquote(urlsplit(path).path).lstrip('/')))

    def _source_path(self, relative):
        path = self._bounded(relative)
        if path not in page_workspace.source_files(self.server.context):
            raise ValueError('File is not an editable Page source')
        return path

    def _login(self, supplied=None):
        if self.server.token is None:
            return self._send(303, '', Location='/')
        if supplied is None:
            return self._send(200, '<!doctype html><title>Page login</title>'
                              '<form method="post" action="/_page/login">'
                              '<label>Page token <input name="token" type="password" '
                              'required autocomplete="off"></label>'
                              '<button>Open Page</button></form>')
        if not hmac.compare_digest(supplied.encode(), self.server.token.encode()):
            return self._error(401, 'Invalid Page token')
        cookie = (f'{self.server.cookie_name}={self.server.session_cookie}; '
                  'Path=/; HttpOnly; SameSite=Strict')
        if self.server.external_scheme == 'https':
            cookie += '; Secure'
        return self._send(303, '', Location='/', Set_Cookie=cookie)

    def _registered_download(self, target):
        """A declared import or an asset reachable from its material references.

        Editable files are not a static-download allowlist: a Page may contain
        unrelated implementation sources. Binary/text attachments are limited
        to the registered content and its confined imported-material closure.
        """
        content = self.server.context.content
        if content is None:
            return False
        content = self._bounded(content.relative_to(self.root).as_posix())
        if target == content:
            return True
        materials = self.root / 'outline/evidence/materials'
        if not content.is_relative_to(materials) or not target.is_relative_to(materials):
            return False
        return target in page_workspace.dependency_files(content, materials)

    def _static(self, path):
        if path in {'/_page/assets/workspace.js', '/_page/assets/workspace.css'}:
            target = ASSETS / path.rsplit('/', 1)[-1]
            return self._send(200, target.read_bytes(),
                              mimetypes.guess_type(str(target))[0] or 'application/octet-stream')
        target = Path(self.translate_path(self.path))
        attachment = target.suffix.lower() not in PUBLIC_SUFFIXES
        if attachment and not self._registered_download(target):
            raise ValueError('File is not a registered imported download')
        # Open each component without following links, including races between
        # validation and open. Never hand a directory to SimpleHTTP's listing.
        fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            parts = target.relative_to(self.root).parts
            for index, part in enumerate(parts):
                flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
                if index < len(parts) - 1:
                    flags |= os.O_DIRECTORY
                child = os.open(part, flags, dir_fd=fd)
                os.close(fd)
                fd = child
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                raise ValueError('Directory listings are disabled')
            with os.fdopen(fd, 'rb', closefd=False) as stream:
                self.send_response(200)
                self.send_header('Content-Type', mimetypes.guess_type(str(target))[0]
                                 or 'application/octet-stream')
                self.send_header('Content-Length', str(os.fstat(fd).st_size))
                if attachment:
                    fallback = re.sub(r'[^A-Za-z0-9._-]', '_', target.name) or 'download'
                    self.send_header('Content-Disposition',
                                     f'attachment; filename="{fallback}"; '
                                     f"filename*=UTF-8''{quote(target.name, safe='')}")
                if target.suffix.lower() in {'.html', '.htm', '.svg'}:
                    # Direct navigation must preserve the same opaque origin
                    # as the imported-content iframe. Scripts may run, but
                    # cannot read authenticated Page APIs, storage, or cookies.
                    self.send_header('Content-Security-Policy',
                                     "sandbox allow-scripts; base-uri 'none'; form-action 'none'")
                self.end_headers()
                if self.command != 'HEAD':
                    self.copyfile(stream, self.wfile)
        finally:
            os.close(fd)

    def _get(self):
        parsed = urlsplit(self.path)
        login = parsed.path == '/_page/login'
        if not self._guard(login=login):
            return
        try:
            if login:
                return self._login(parse_qs(parsed.query).get('token', [None])[0])
            if parsed.path == '/':
                self._bounded(self.server.context.source.relative_to(self.root).as_posix())
                self._safe_page_tree()
                document = page_workspace.render_page(self.server.context)
                def live_body(match):
                    attrs = re.sub(r'\sdata-(?:live|read-only)\s*=\s*(?:"[^"]*"|\x27[^\x27]*\x27|[^\s>]+)',
                                   '', match.group(1), flags=re.I)
                    return f'<body{attrs} data-live="true" data-read-only="{str(self.server.read_only).lower()}">'
                document = re.sub(r'<body\b([^>]*)>', live_body, document, count=1, flags=re.I)
                if self.server.read_only:
                    # A reading host has no Source workspace: hiding only the
                    # Save button still presented a large editor-shaped field.
                    document = document.replace(
                        '<a class="live-only" href="#source-editor">Source</a>', '')
                    document = re.sub(
                        r'<section id="source-editor"[^>]*>.*?</section>', '', document,
                        count=1, flags=re.I | re.S,
                    )
                return self._send(200, document)
            if parsed.path == '/_page/source':
                relative = parse_qs(parsed.query).get('file', [''])[0]
                self._source_path(relative)
                return self.reply(200, {'ok': True, **page_workspace.read_source(self.server.context, relative)})
            route = parsed.path.replace('/_page/', '/_board/', 1)
            views = {'/_board/outline': self.outline_view,
                     '/_board/evidence': self.evidence_tab_view,
                     '/_board/value': self.value_view,
                     '/_board/runs': self.runs_view,
                     '/_board/delivery': self.delivery_tab_view,
                     '/_board/folderstat': self.folderstat_view}
            if route in views:
                return views[route](head_only=self.command == 'HEAD')
            return self._static(parsed.path)
        except (ValueError, OSError):
            return self._error(404, 'Page file unavailable or outside the permitted folder')
        except Exception:
            return self._error(500, 'Unable to render this Page')

    def do_GET(self):
        self._get()

    def do_HEAD(self):
        self._get()

    def _body(self):
        lengths = self.headers.get_all('Content-Length', [])
        if len(lengths) != 1 or self.headers.get('Transfer-Encoding'):
            raise ValueError('One Content-Length is required')
        length = int(lengths[0])
        if not 0 <= length <= MAX_BODY:
            raise ValueError('Request body exceeds the Page size limit')
        return self.rfile.read(length).decode('utf-8')

    def do_POST(self):
        path = urlsplit(self.path).path
        login = path == '/_page/login'
        if not self._guard(writing=True, login=login):
            return
        try:
            raw = self._body()
            if login:
                return self._login(parse_qs(raw).get('token', [''])[0])
            if self.headers.get_content_type() != 'application/json':
                return self._error(415, 'Expected application/json')
            payload = json.loads(raw)
            if not isinstance(payload, dict):
                raise ValueError('Expected a JSON object')
            with self.server.write_lock:
                if path == '/_page/source':
                    relative = payload.get('file')
                    self._source_path(relative)
                    if not all(isinstance(payload.get(k), str) for k in ('text', 'sha256')):
                        raise ValueError('text and sha256 must be strings')
                    try:
                        result = page_workspace.save_source(self.server.context, relative,
                                                            payload['text'], payload['sha256'])
                    except page_workspace.SourceConflictError as exc:
                        return self._error(409, str(exc))
                    return self.reply(200, {'ok': True, **result})
                route = path.replace('/_page/', '/_board/', 1)
                plugins = {'/_board/outline': self.plug_outline,
                           '/_board/evidence': self.plug_evidence,
                           '/_board/value': self.plug_value,
                           '/_board/runs': self.plug_runs,
                           '/_board/delivery': self.plug_delivery,
                           '/_board/folderstat': self.plug_folderstat}
                if route not in plugins:
                    return self._error(404, 'Unsupported Page endpoint')
                result, err = plugins[route](payload)
                return self.reply(400 if err else 200,
                                  {**(result or {}), 'ok': not bool(err),
                                   'err': err, 'tab': result})
        except (ValueError, UnicodeError, OSError) as exc:
            self._error(400, str(exc) if isinstance(exc, ValueError) else 'Invalid Page request')
        except Exception:
            self._error(500, 'Unable to process this Page request')


def create_server(context, host='127.0.0.1', port=0, token=None,
                  read_only=False, public_url=None):
    """Create an unstarted server; non-loopback writes require an explicit token."""
    if token is not None and (not isinstance(token, str) or not token.strip()):
        raise ValueError('token must be a nonempty string')
    if not _local(host) and token is None and not read_only:
        raise ValueError('Non-local binding requires --token or --read-only')
    external = _origin(public_url) if public_url else None
    if external and not _local(external[1]) and token is None and not read_only:
        raise ValueError('A non-local public URL requires --token or --read-only')
    root = context.folder.resolve()
    if not context.source.resolve().is_relative_to(root):
        raise ValueError('Page source must be inside its folder')
    if context.content is not None and not context.content.resolve().is_relative_to(root):
        raise ValueError('Page content must be inside its folder')
    context = replace(context, folder=root, source=context.source.resolve(),
                      content=context.content.resolve() if context.content else None)
    handler = type('BoundPageHandler', (PageHandler,), {'server_context': context})
    server_type = ThreadingHTTPServer
    if ':' in host:
        server_type = type('IPv6PageServer', (ThreadingHTTPServer,),
                           {'address_family': socket.AF_INET6})
    server = server_type((host, port), handler)
    server.context = context
    server.token = token
    server.read_only = read_only
    server.write_lock = threading.RLock()
    server.session_cookie = secrets.token_urlsafe(32)
    server.cookie_name = 'page_session_' + secrets.token_hex(6)
    actual_port = server.server_address[1]
    display_host = '127.0.0.1' if host == '0.0.0.0' else '::1' if host == '::' else host
    authority = f'[{display_host}]' if ':' in display_host else display_host
    base = public_url.rstrip('/') if public_url else f'http://{authority}:{actual_port}'
    server.external_scheme = external[0] if external else 'http'
    server.allowed_origins = {external} if external else {_origin(base)}
    if not external and _local(host):
        server.allowed_origins.update({('http', 'localhost', actual_port),
                                       ('http', '127.0.0.1', actual_port),
                                       ('http', '::1', actual_port)})
    server.startup_url = base + ('/_page/login?token=' + quote(token, safe='') if token else '/')
    return server


def serve(context, host='127.0.0.1', port=0, token=None,
          read_only=False, public_url=None):
    """Print a token-free login URL, serve until interrupted, and close cleanly."""
    server = create_server(context, host, port, token, read_only, public_url)
    safe_url = urlsplit(server.startup_url)._replace(query='', fragment='').geturl()
    print(f'Page server: {safe_url}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

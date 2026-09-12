"""Run from any directory: python -m unittest discover -s <Page>/tests.

Uses the real shared Page loader/renderers and HTTP sockets; no Board root or
board.md is present. A fresh Python process also verifies independent imports.
"""
from __future__ import annotations

import concurrent.futures
from contextlib import redirect_stdout, redirect_stderr
import http.client
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import Mock, patch
from urllib.parse import urlsplit

PAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PAGE_ROOT))

from src.page_workspace import load_page, read_source
from src.standalone_server import create_server, serve


class StandaloneServerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='standalone-page-')
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name) / 'page'
        self.folder.mkdir()
        self.source = self.folder / 'Q1-example.md'
        self.source.write_text('# Example Page\n\n## Opening\nA standalone page.\n\n'
                               '## Content\n### 1 · Findings\nExample content.\n\n'
                               '## Aims\n- ⬜ A1.1 · Review findings.\n', encoding='utf-8')
        self.context = load_page(self.source)
        self.server = None
        self.start()

    def start(self, **kwargs):
        if self.server:
            self.stop()
        self.server = create_server(self.context, **kwargs)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.origin = f'http://127.0.0.1:{self.server.server_port}'
        self.addCleanup(self.stop)

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.thread.join(timeout=3)
            self.server = None

    def request(self, method='GET', path='/', payload=None, headers=None):
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=5)
        body = json.dumps(payload) if payload is not None else None
        merged = {'Origin': self.origin, 'Content-Type': 'application/json'}
        merged.update(headers or {})
        try:
            connection.request(method, path, body=body, headers=merged)
            response = connection.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            connection.close()

    def source_payload(self, text=None):
        result = read_source(self.context, self.source.name)
        if text is None:
            text = result['text'] + '\nChanged source.\n'
        return {'file': self.source.name, 'text': text, 'sha256': result['sha256']}

    def test_root_get_head_and_assets_without_board(self):
        self.assertFalse((self.folder / 'board.md').exists())
        code, headers, body = self.request()
        self.assertEqual(code, 200)
        self.assertIn(b'data-live="true"', body)
        self.assertIn(b'id="page-plugin-button"', body)
        self.assertIn(b'id="page-plugin-pane"', body)
        self.assertIn('🧭 Outline'.encode(), body)
        self.assertIn('⚙️ Runs'.encode(), body)
        self.assertIn('📤 Delivery'.encode(), body)
        self.assertIn('📂 Folder'.encode(), body)
        self.assertEqual(int(headers['Content-Length']), len(body))
        code, headers, body = self.request('HEAD')
        self.assertEqual((code, body), (200, b''))
        self.assertGreater(int(headers['Content-Length']), 0)
        for suffix in ('js', 'css'):
            path = '/_page/assets/workspace.' + suffix
            code, _, body = self.request(path=path)
            self.assertEqual(code, 200)
            self.assertGreater(len(body), 100)
            self.assertEqual(self.request('HEAD', path)[2], b'')

    def test_source_read_save_and_stale_conflict(self):
        code, _, body = self.request(path='/_page/source?file=' + self.source.name)
        self.assertEqual(code, 200)
        initial = json.loads(body)
        self.assertEqual(initial['text'], self.source.read_text())
        payload = self.source_payload()
        code, _, body = self.request('POST', '/_page/source', payload)
        self.assertEqual(code, 200, body)
        self.assertNotEqual(initial['sha256'], json.loads(body)['sha256'])
        self.assertEqual(self.source.read_text(), payload['text'])
        payload['text'] = 'stale replacement'
        self.assertEqual(self.request('POST', '/_page/source', payload)[0], 409)
        self.assertNotEqual(self.source.read_text(), payload['text'])

    def test_concurrent_saves_have_one_winner(self):
        payload = self.source_payload()
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(self.request, 'POST', '/_page/source',
                                   {**payload, 'text': payload['text'] + str(index)}) for index in range(2)]
            self.assertEqual(sorted(f.result()[0] for f in futures), [200, 409])

    def test_invalid_face_save_is_rejected_without_losing_editor(self):
        before = self.source.read_text()
        code, _, _ = self.request('POST', '/_page/source', self.source_payload('not a Page Face'))
        self.assertEqual(code, 400)
        self.assertEqual(self.source.read_text(), before)
        self.assertEqual(self.request()[0], 200)

    def test_shared_views_and_head(self):
        for prefix in ('/_board/', '/_page/'):
            for name in ('outline', 'evidence', 'value', 'runs', 'delivery', 'folderstat'):
                path = prefix + name + '?file=' + self.source.name
                code, _, body = self.request(path=path)
                self.assertEqual(code, 200, (path, body))
                self.assertGreater(len(body), 20)
                code, headers, body = self.request('HEAD', path)
                self.assertEqual((code, body), (200, b''))
                self.assertGreater(int(headers['Content-Length']), 0)

    def test_outline_registration_and_response_contract(self):
        code, _, body = self.request('POST', '/_board/outline', {'file': self.source.name})
        self.assertEqual(code, 200, body)
        result = json.loads(body)
        self.assertTrue(result['ok'])
        self.assertEqual(result['url'], result['tab']['url'])
        self.assertIn('/_board/outline?', result['url'])
        # The shared writer's result remains available in both UI shapes.
        with patch('src.standalone_server.OutlineMixin.plug_outline',
                   return_value=({'version': 'v1', 'saved': True}, None)):
            result = json.loads(self.request('POST', '/_board/outline',
                                            {'file': self.source.name})[2])
            self.assertEqual(result['version'], result['tab']['version'])

    def test_target_never_selects_another_page(self):
        (self.folder / 'Q2-other.md').write_text('Other page')
        for file in ('Q2-other.md', '../Q1-example.md', '/etc/passwd'):
            code, _, _ = self.request('POST', '/_board/outline', {'file': file})
            self.assertEqual(code, 400)
        code, _, _ = self.request('POST', '/_board/outline',
                                  {'file': self.source.name, 'path': '/../elsewhere/'})
        self.assertEqual(code, 400)

    def test_traversal_hidden_files_and_server_state_are_denied(self):
        (self.folder / '.env').write_text('secret')
        (self.folder / 'env.sh').write_text('secret')
        (self.folder / 'server.json').write_text('secret')
        (self.folder / 'studio').mkdir()
        (self.folder / 'studio' / 'chat.html').write_text('secret')
        for path in ('/../outside.html', '/%2e%2e/outside.html', '/.env', '/env.sh',
                     '/server.json', '/studio/chat.html', '/%5c..%5coutside.html',
                     '/_page/source?file=../outside.html'):
            code, _, body = self.request(path=path)
            self.assertEqual(code, 404, (path, body))
            self.assertNotIn(b'secret', body)

    def test_static_files_and_directory_listings(self):
        assets = self.folder / 'assets'
        assets.mkdir()
        (assets / 'figure.svg').write_text('<svg/>')
        self.assertEqual(self.request(path='/assets/figure.svg')[2], b'<svg/>')
        self.assertEqual(self.request('HEAD', '/assets/figure.svg')[2], b'')
        self.assertEqual(self.request(path='/assets/')[0], 404)

    def test_serve_prints_token_free_login_url(self):
        self.start(token='private token/+')
        original_url = self.server.startup_url
        fake = Mock(startup_url=original_url)
        fake.serve_forever.side_effect = KeyboardInterrupt
        output, errors = io.StringIO(), io.StringIO()
        with patch('src.standalone_server.create_server', return_value=fake), \
                redirect_stdout(output), redirect_stderr(errors):
            serve(self.context, token='private token/+')
        self.assertEqual(output.getvalue(), f'Page server: {self.origin}/_page/login\n')
        self.assertEqual(errors.getvalue(), '')
        self.assertEqual(fake.startup_url, original_url)
        self.assertIn('?token=', original_url)
        fake.server_close.assert_called_once()
        code, _, body = self.request(path='/_page/login')
        self.assertEqual(code, 200)
        self.assertIn(b'type="password"', body)
        self.assertNotIn(b'private token', body)

    def test_declared_text_and_binary_downloads(self):
        from src.page_workspace import create_page
        for suffix, data in (('.md', b'# Imported notes\n'), ('.txt', b'plain text\n'),
                             ('.csv', b'x,y\n1,2\n'), ('.bin', b'\x00\xff\x80binary')):
            original = Path(self.temp.name) / ('input' + suffix)
            original.write_bytes(data)
            self.context = create_page(original, Path(self.temp.name) / ('page-' + suffix[1:]))
            self.start()
            path = '/' + self.context.content.relative_to(self.context.folder).as_posix()
            for method in ('GET', 'HEAD'):
                code, headers, body = self.request(method, path)
                self.assertEqual(code, 200, (path, body))
                self.assertTrue(headers['Content-Disposition'].startswith('attachment;'))
                self.assertIn("filename*=UTF-8''input" + suffix, headers['Content-Disposition'])
                self.assertEqual(int(headers['Content-Length']), len(data))
                self.assertEqual(body, data if method == 'GET' else b'')

    def test_registered_material_downloads_exclude_unrelated_sources(self):
        from src.page_workspace import create_page
        original = Path(self.temp.name) / 'index.md'
        original.write_text('[Table](table.csv)\n[Bytes](payload.bin)\n[Code](example.py)\n')
        for name, data in (('table.csv', b'x\n1\n'), ('payload.bin', b'\xff\x00'),
                           ('example.py', b'print("imported")\n')):
            (original.parent / name).write_bytes(data)
        self.context = create_page(original, Path(self.temp.name) / 'materials-page')
        self.start()
        materials = self.context.content.parent
        for name in ('table.csv', 'payload.bin', 'example.py'):
            path = '/' + (materials / name).relative_to(self.context.folder).as_posix()
            code, headers, body = self.request(path=path)
            self.assertEqual(code, 200, body)
            self.assertEqual(body, (materials / name).read_bytes())
            self.assertIn('attachment;', headers['Content-Disposition'])
        (materials / 'unregistered.py').write_text('unregistered source')
        (self.context.folder / 'private-code.py').write_text('unrelated source')
        for path in ('/private-code.py', '/outline/evidence/materials/unregistered.py',
                     '/page.toml', '/' + self.context.source.name):
            self.assertEqual(self.request(path=path)[0], 404, path)
        # Even a reference cannot authorize hidden/private files or escapes.
        for name in ('.hidden.bin', 'credentials.json', 'escape.bin'):
            candidate = materials / name
            if name == 'escape.bin':
                candidate.symlink_to(original.parent / 'payload.bin')
            else:
                candidate.write_text('private bytes')
            self.context.content.write_text('[Download](' + name + ')\n')
            code, _, body = self.request(path='/outline/evidence/materials/' + name)
            self.assertEqual(code, 404, name)
            self.assertNotIn(b'private bytes', body)

    def test_active_static_documents_have_opaque_origins(self):
        for name in ('imported.html', 'imported.htm', 'imported.svg'):
            (self.folder / name).write_text('<script>fetch("/_page/source")</script>')
            for method in ('GET', 'HEAD'):
                code, headers, _ = self.request(method, '/' + name)
                self.assertEqual(code, 200)
                self.assertIn('sandbox allow-scripts', headers['Content-Security-Policy'])
                self.assertNotIn('allow-same-origin', headers['Content-Security-Policy'])
        self.assertEqual(self.request('POST', '/_page/source', self.source_payload(),
                                      {'Origin': 'null'})[0], 403)
        self.assertNotIn('Access-Control-Allow-Origin', self.request()[1])

    def test_imported_context_content_and_source_editor(self):
        from src.page_workspace import create_page
        original = Path(self.temp.name) / 'import.html'
        original.write_text('<!doctype html><h1>Imported reading</h1><script>fetch("/_page/source")</script>')
        destination = Path(self.temp.name) / 'imported-page'
        create_page(original, destination)
        self.stop()
        self.context = load_page(destination)
        self.start()
        code, _, body = self.request()
        self.assertEqual(code, 200)
        self.assertIn(b'id="source-file"', body)
        self.assertIn(b'sandbox="allow-scripts"', body)
        relative = self.context.content.relative_to(self.context.folder).as_posix()
        code, _, body = self.request(path='/_page/source?file=' + relative)
        self.assertEqual(code, 200)
        old = json.loads(body)
        updated = '<h1>Edited imported reading</h1>'
        code, _, body = self.request('POST', '/_page/source',
                                     {'file': relative, 'text': updated, 'sha256': old['sha256']})
        self.assertEqual(code, 200, body)
        self.assertEqual(self.context.content.read_text(), updated)
        self.assertIn('sandbox allow-scripts', self.request(path='/' + relative)[1]['Content-Security-Policy'])

    def test_symlink_escapes_static_source_and_shared_view(self):
        outside = Path(self.temp.name) / 'outside.html'
        outside.write_text('outside secret')
        (self.folder / 'escape.html').symlink_to(outside)
        for path in ('/escape.html', '/_page/source?file=escape.html',
                     '/_board/outline?file=' + self.source.name, '/'):
            code, _, body = self.request(path=path)
            self.assertIn(code, (400, 404))
            self.assertNotIn(b'outside secret', body)
        payload = {**self.source_payload(), 'file': 'escape.html'}
        self.assertEqual(self.request('POST', '/_page/source', payload)[0], 400)
        self.assertEqual(outside.read_text(), 'outside secret')

    def test_wrong_origin_host_and_fetch_site(self):
        payload = self.source_payload()
        for headers in ({'Origin': 'https://evil.example'}, {'Host': 'evil.example'},
                        {'Origin': 'null'}, {'Sec-Fetch-Site': 'cross-site'}):
            self.assertEqual(self.request('POST', '/_page/source', payload, headers)[0], 403)
        self.assertEqual(self.request(headers={'Host': 'evil.example'})[0], 403)
        self.assertNotEqual(self.source.read_text(), payload['text'])

    def test_token_cookie_login_and_bearer(self):
        self.start(token='test-token')
        self.assertEqual(self.request()[0], 401)
        self.assertEqual(self.request(headers={'Authorization': 'Bearer wrong'})[0], 401)
        self.assertEqual(self.request(path='/_page/login?token=wrong')[0], 401)
        login_path = urlsplit(self.server.startup_url).path + '?' + urlsplit(self.server.startup_url).query
        code, headers, body = self.request(path=login_path)
        self.assertEqual(code, 303)
        self.assertEqual(headers['Location'], '/')
        self.assertNotIn(b'test-token', body)
        self.assertIn('HttpOnly', headers['Set-Cookie'])
        self.assertIn('SameSite=Strict', headers['Set-Cookie'])
        cookie = headers['Set-Cookie'].split(';', 1)[0]
        self.assertEqual(self.request(headers={'Cookie': cookie})[0], 200)
        self.assertEqual(self.request('POST', '/_page/source', self.source_payload(),
                                      {'Cookie': cookie})[0], 200)
        self.assertEqual(self.request('POST', '/_page/source', self.source_payload(),
                                      {'Authorization': 'Bearer wrong'})[0], 401)
        self.assertEqual(self.request(headers={'Authorization': 'Bearer test-token'})[0], 200)

    def test_read_only_and_nonlocal_policy(self):
        with self.assertRaises(ValueError):
            create_server(self.context, host='0.0.0.0')
        with self.assertRaises(ValueError):
            create_server(self.context, public_url='https://page.example')
        self.start(read_only=True)
        self.assertEqual(self.request()[0], 200)
        page = self.request()[2]
        self.assertIn(b'data-read-only="true"', page)
        self.assertNotIn(b'id="source-editor"', page)
        self.assertNotIn(b'href="#source-editor"', page)
        for name in ('outline', 'runs', 'delivery', 'folderstat'):
            self.assertEqual(self.request(path=f'/_board/{name}?file={self.source.name}')[0], 200)
        self.assertEqual(self.request('POST', '/_page/source', self.source_payload())[0], 403)
        self.assertEqual(self.request('POST', '/_board/outline', {'file': self.source.name})[0], 403)

    def test_public_origin_and_cookie_security(self):
        self.start(token='test-token', public_url='https://page.example')
        self.assertEqual(self.request()[0], 403)
        headers = {'Host': 'page.example', 'Origin': 'https://page.example'}
        code, response_headers, _ = self.request(path='/_page/login?token=test-token', headers=headers)
        self.assertEqual(code, 303)
        self.assertIn('; Secure', response_headers['Set-Cookie'])
        self.assertEqual(self.request(headers={**headers, 'Authorization': 'Bearer test-token'})[0], 200)

    def test_read_only_outline_keeps_prose_without_editors(self):
        outline = self.folder / 'outline'
        outline.mkdir()
        (outline / 'Q1-example-outline-v0.1.md').write_text(
            '# Example outline\napproved: ⬜\n\n## C1 · Findings\n'
            '### C1.P1 · Explain ownership\n'
            '- B1 · The Page keeps one source document\n'
            '  Note: One source is shared by both hosts.\n'
            '  Evidence: none · internal definition\n')
        self.source.write_text(self.source.read_text().replace(
            'Example content.', 'Example content. <!-- realizes: C1.P1.B1 -->'))
        route = '/_board/outline?path=%2F&file=Q1-example.md&lens=div'
        writable = self.request(path=route)[2].decode()
        self.assertIn('<form class=preview-form', writable)
        self.start(read_only=True)
        code, _, body = self.request(path=route)
        self.assertEqual(code, 200)
        markup = body.decode().split('<body', 1)[1].split('<script', 1)[0]
        self.assertNotIn('function readParagraph(group)', body.decode())
        self.assertIn('Example content.', markup)
        self.assertIn('Read paragraph', markup)
        self.assertIn('class=preview-copy', markup)
        for control in ('<textarea', '<form', 'Save draft', 'Save comment', 'Edit draft for'):
            self.assertNotIn(control, markup)
        self.assertEqual(self.request('POST', '/_board/outline',
                                     {'action': 'edit-preview'})[0], 403)

    def test_malformed_posts_and_unsupported_features(self):
        for payload in ([], {'file': self.source.name}, {'file': '../outside'}):
            self.assertEqual(self.request('POST', '/_page/source', payload)[0], 400)
        self.assertEqual(self.request('POST', '/_page/source', self.source_payload(),
                                      {'Content-Type': 'text/plain'})[0], 415)
        for path in ('/_board/terminal', '/_board/ask', '/_page/agent'):
            self.assertEqual(self.request('POST', path, {})[0], 404)

    def test_imports_are_independent_in_fresh_process(self):
        script = ('import sys; from pathlib import Path; '
                  'sys.path.insert(0, sys.argv[1]); '
                  'from src.standalone_server import create_server; '
                  'from src.page_workspace import load_page; '
                  'c=load_page(Path(sys.argv[2])); s=create_server(c); s.server_close(); '
                  'assert not any("haipipe-board" in str(getattr(m,"__file__","")) '
                  'for m in list(sys.modules.values()))')
        result = subprocess.run([sys.executable, '-c', script, str(PAGE_ROOT), str(self.source)],
                                cwd=self.temp.name, capture_output=True, text=True,
                                env={**os.environ, 'PYTHONPATH': ''}, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()

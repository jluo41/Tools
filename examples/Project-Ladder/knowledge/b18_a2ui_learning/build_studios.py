"""Build A2UI learning drawings and decks with the shared Studio tools."""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path
import random
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'plugins/haipipe-toolkit').is_dir())
KIT = ROOT / 'plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts'
sys.path.insert(0, str(KIT))
import quick_draw as Q
import icons
import topic_slides

TOPICS = {
    's01-official-sources': ('Resources', 'Official Sources and Versions'),
    's11-messages-components-data': ('Concepts', 'Messages, Components and Data'),
    's21-tracing-interaction': ('Methods', 'Tracing a User Interaction'),
    's22-chatbot-to-a2ui': ('Methods', 'From a Text Chatbot to A2UI, Step by Step'),
    's31-use-cases-boundaries': ('Connections and Applications', 'Use Cases and Boundaries'),
    's41-agent-text-to-a2ui': ('Questions', 'If My Agent Only Returns Text, What Changes?'),
    's42-who-writes-the-json': ('Questions', 'Who Writes the JSON?'),
}
TOPIC_IMAGES = {'s01-official-sources': (1, 2, 3, 4, 5, 6), 's11-messages-components-data': (1, 3), 's41-agent-text-to-a2ui': (1,), 's22-chatbot-to-a2ui': (5,)}


# the six source records of s01-official-sources/delivery/learning.md, drawn as cards (name, page, what to read, used by)
RESOURCES = [
    ('Resource 1 · Architecture', 'Overview: How A2UI Works', 'Step-by-step generation,\nrender on the client,\nhandle user actions', 's11, s21',
     'Berlin to San Francisco: the agent sends cards,\n+ changes passengers locally, Confirm sends action'),
    ('Resource 2 · Messages', 'Messages', 'createSurface, updateComponents,\nupdateDataModel, deleteSurface', 's11',
     'The same flight screen as three JSON messages:\ncreate the surface, lay out, fill the values'),
    ('Resource 3 · Data binding', 'Data Model and Data Binding', 'Path references,\nreactive binding', 's11, s21',
     'Kyoto, Japan sits once in the data model;\na heading reads it, the email field writes it'),
    ('Resource 4 · Actions', 'Actions, Events and Functions', 'Event actions, local functions,\nthe renderer-to-agent action', 's21',
     'An Event asks the agent and starts its turn;\na Function runs without one (openUrl)'),
    ('Resource 5 · Quickstart', 'Quickstart (Travel A2UI)', 'How A2UI fits into this app;\na reference, not run here', 's31',
     'Travel A2UI: one Python server,\na React web client and a Flutter phone client'),
    ('Resource 6 · Repository', 'Official A2UI repository', 'README: Architecture, When to use;\npin a release before running', 's31, j01',
     'Cards, forms, lists: what A2UI draws\nwith native widgets on every platform'),
]
ASSETS = HERE / 's01-official-sources/assets'


def image_size(i, box_w, box_h):
    """The image's size inside a box_w x box_h frame, its shape kept."""
    import struct
    head = (ASSETS / f'resource-{i + 1}.png').read_bytes()[16:24]
    w, h = struct.unpack('>II', head)
    s = min(box_w / w, box_h / h)
    return round(w * s), round(h * s)


def image_files():
    """The six images as Excalidraw files, keyed by their fileId."""
    import base64
    return {f'resource-{i}': {'mimeType': 'image/png', 'id': f'resource-{i}', 'created': 0,
                              'dataURL': 'data:image/png;base64,' + base64.b64encode((ASSETS / f'resource-{i}.png').read_bytes()).decode()}
            for i in range(1, 7)}

def drawing(slug):
    random.seed(slug)
    els = []

    def words(key, x, y, value, size=25, color=Q.ON):
        rows = Q.text(key, x, y, value, size, color)
        for e in rows:
            e['fontFamily'] = 6
        els.extend(rows)

    def arrow(key, points, dashed=False):
        els.extend(Q.arrow(key, points, dashed=dashed))

    words('title', 35, 25, TOPICS[slug][1], 35, Q.TITLE)
    if slug.startswith('s01'):
        def card(i, x, y):
            name, page, read, supports, vivid = RESOURCES[i]
            key = f'r{i + 1}'
            els.extend(Q.box(key, x, y, 440, 520, '', 'plain'))
            words(key + '-name', x + 18, y + 12, name, 23, Q.TITLE)
            words(key + '-page', x + 18, y + 46, page, 18, Q.BODY)
            w, h = image_size(i, 404, 330)
            els.append(Q._el('image', key + '-img', x + 18 + (404 - w) / 2, y + 80, w, h, 'transparent',
                             fileId=f'resource-{i + 1}', status='saved', scale=[1, 1], roundness=None))
            words(key + '-vivid', x + 18, y + 422, vivid, 18, Q.ON)
            words(key + '-use', x + 18, y + 488, 'Supports ' + supports, 18, '#047857')
        els += icons.document('docs', 35, 85, 'off', w=55, h=70)
        words('docs-label', 105, 105, 'Official docs · Resources 1–4', 28)
        for i in range(4):
            card(i, 35 + i * 465, 175)
        els += icons.laptop('code', 15, 730, 'off')
        words('code-label', 205, 755, 'Sample + code · Resources 5–6', 28)
        for i in (4, 5):
            card(i, 35 + (i - 4) * 465, 850)
        arrow('docs-route', [(1625, 700), (1625, 900), (1440, 960)])
        arrow('code-route', [(940, 1100), (1060, 1040)])
        els += Q.diamond('version', 1060, 900, 360, 180, '', 'decision')
        words('version-label', 1140, 960, 'Same version?\nv1.0 throughout', 25)
        arrow('reading', [(1240, 1085), (1240, 1160)])
        els += icons.person('learner', 1130, 1170, 'off', s=.8)
        words('explanation', 1255, 1180, 'Explain one claim\nName its Resource', 26)
        words('question', 1060, 1330, 'Which section of which\nResource supports the claim?', 26, '#b45309')
        words('foot', 35, 1400, 'Images: official A2UI docs and README, Apache-2.0 (assets/SOURCES.md) · v1.0 examples · '
                                'Pin code before execution', 20)
    elif slug.startswith('s11'):
        def image(i, x, y, box_w, box_h):
            w, h = image_size(i - 1, box_w, box_h)
            els.append(Q._el('image', f'img-{i}', x, y, w, h, 'transparent', fileId=f'resource-{i}', status='saved',
                             scale=[1, 1], roundness=None))
            return h
        # 1. the pipeline in three parts, as the official overview draws it (Resource 1)
        lanes = [('server', 35, 'Server · your agent', 'agent'), ('wire', 470, 'Transport', 'plain'),
                 ('client', 905, 'Client · your app', 'plain')]
        for key, x, label, sem in lanes:
            els.extend(Q.box('lane-' + key, x, 95, 400, 330, '', sem))
            words('lane-' + key + '-name', x + 18, 108, label, 24, Q.TITLE)
        els += icons.server('agent', 60, 160, 'off', w=90, h=105)
        words('agent-label', 170, 165, 'Agent + LLM\nA2UI Agent SDK', 21)
        els += icons.document('catalog', 70, 290, 'off', w=60, h=78)
        words('catalog-label', 150, 300, 'catalog.json\nallowed components', 20)
        for n, (name, what) in enumerate((('createSurface', 'open surface "flight-booking"'),
                                          ('updateComponents', 'Card > Column > FlightCard, Button'),
                                          ('updateDataModel', '/outbound/pax = 1, price = 455'))):
            els.extend(Q.box('msg-' + str(n), 490, 160 + n * 85, 360, 70, '', 'decision'))
            words('msg-name-' + str(n), 505, 168 + n * 85, '↓ ' + name, 20, Q.ON)
            words('msg-what-' + str(n), 505, 198 + n * 85, what, 16, Q.BODY)
        arrow('to-wire', [(435, 260), (470, 260)])
        arrow('to-client', [(870, 260), (905, 260)])
        els += icons.laptop('renderer', 920, 160, 'off')
        words('renderer-label', 1110, 175, 'Renderer\nFlutter · Web\nSwiftUI · Compose', 19)
        els += icons.phone('surface', 1170, 280, 'off')
        words('surface-label', 940, 300, 'Surface:\nnative widgets', 20)
        arrow('action', [(1205, 425), (1205, 460), (245, 460), (245, 372)], True)
        words('action-label', 520, 468, '↑ action, when the user taps Confirm', 18, '#b45309')
        # 2. one surface, two halves: structure and values (Resource 3)
        words('halves', 35, 520, 'One surface, two halves', 26, Q.TITLE)
        els.extend(Q.box('components', 35, 565, 400, 250, '', 'plain'))
        words('components-head', 55, 575, 'Components: structure', 22, Q.TITLE)
        words('components-tree', 55, 615, 'Card "root"\n└ Column\n  ├ FlightCard  passengers ← /outbound/pax\n  └ Button "Confirm booking"', 17, Q.ON)
        words('components-note', 55, 750, 'IDs and places; the catalog\nsays which types exist', 17, Q.BODY)
        els += icons.cylinder('values', 480, 615, 'off', w=110, h=120)
        words('values-head', 470, 575, 'Data model: values', 22, Q.TITLE)
        words('values-body', 605, 640, '/outbound/pax = 1\n/outbound/price = 455', 18, Q.ON)
        arrow('binding', [(478, 690), (440, 690)])
        words('binding-label', 445, 705, 'binding', 17, '#047857')
        words('plus', 470, 760, 'Tap + : pax becomes 2.\nThe value changes, the FlightCard stays.', 19, '#047857')
        # the official pictures this drawing follows
        h1 = image(1, 905, 520, 190, 330)
        image(3, 1110, 520, 300, 330)
        words('img-caption', 905, 865, 'Resource 1 (left): the pipeline · Resource 3 (right): a value bound\nto a heading and an editable field', 17, Q.BODY)
        words('question', 35, 930, 'Change the value. Does the component identity change?', 27, '#b45309')
    elif slug.startswith('s21'):
        NEW, RED = '#047857', '#b91c1c'

        def shrink(parts, x0, y0, s):
            """Scale an icon's elements about (x0, y0), so a full-size icon fits a lane."""
            for el in parts:
                el['x'] = x0 + (el['x'] - x0) * s
                el['y'] = y0 + (el['y'] - y0) * s
                el['width'] *= s
                el['height'] *= s
                if 'points' in el:
                    el['points'] = [[px * s, py * s] for px, py in el['points']]
            return parts

        def lane_icon(eid, lane, x, y):
            """A picture above each column: a person, a phone, a server rack, a cloud for the LLM API."""
            if lane == 'user':
                return shrink(icons.person(eid, x - 39, y, 'off'), x - 39, y, 0.55)
            if lane == 'app':
                return shrink(icons.phone(eid, x - 38, y, 'off'), x - 38, y, 0.65)
            if lane == 'server':
                return icons.server(eid, x - 40, y, 'off', w=80, h=88)
            return shrink(icons.cloud(eid, x - 65, y + 15, 'off'), x - 65, y + 15, 0.5) + [
                e for e in Q.text(eid + '-api', x - 18, y + 40, 'LLM', 18, Q.ON)]

        def timeline(key, x0, title, lanes, events, color):
            """A sequence drawing: one column per actor, time running down, one arrow per message."""
            words(key + '-title', x0, 95, title, 26, color)
            xs = {}
            for n, (lane, label) in enumerate(lanes):
                x = x0 + 40 + n * 190
                xs[lane] = x
                els.extend(lane_icon(f'{key}-{lane}-icon', lane, x, 140))
                els.extend(Q.box(f'{key}-{lane}', x - 80, 240, 160, 58, label, 'agent' if lane == 'model' else 'plain', 17))
                els.extend(Q.line(f'{key}-{lane}-life', [(x, 303), (x, 1235)], dashed=True))
            y = 335
            for n, ev in enumerate(events):
                a, b, label, kind = ev
                tint = {'new': NEW, 'local': NEW, 'old': Q.ON, 'warn': RED}[kind]
                words(f'{key}-t{n}', x0 - 30, y - 12, str(n + 1), 17, Q.BODY)
                lines = label.count('\n') + 1
                if a == b:                                   # something that happens inside one actor: a note on its line
                    w = max(len(s) for s in label.split('\n')) * 8.6 + 24
                    els.extend(Q.box(f'{key}-e{n}', xs[a] - w / 2, y - 12 - 10 * lines, w, 24 + 20 * lines, label,
                                     'end' if kind in ('new', 'local') else 'plain', 16))
                else:
                    els.extend(Q.arrow(f'{key}-e{n}', [(xs[a], y), (xs[b], y)], color=tint, dashed=kind == 'local'))
                    words(f'{key}-l{n}', min(xs[a], xs[b]) + 10, y - 10 - 20 * lines, label, 16, tint)
                y += 75
            return y

        lanes = [('user', 'User'), ('app', 'App\n(renderer)'), ('server', 'Your server\n(endpoint)'), ('model', 'Model\n(LLM API)')]
        timeline('old', 60, 'Without A2UI: every change is another chat turn', lanes, [
            ('user', 'app', 'types "BER to SFO today, 2 back Oct 19"', 'old'),
            ('app', 'server', 'the message', 'old'),
            ('server', 'model', 'prompt + tools (search flights)', 'old'),
            ('model', 'server', 'text: "LH 454 at 455, UA 901 at 970"', 'old'),
            ('server', 'app', 'the text', 'old'),
            ('app', 'app', 'a chat bubble', 'old'),
            ('user', 'app', 'types "make the outbound 2 people"', 'warn'),
            ('app', 'server', 'the message', 'old'),
            ('server', 'model', 'a new turn, just for a number', 'warn'),
            ('model', 'server', 'new text with the new price', 'old'),
            ('server', 'app', 'another bubble', 'old'),
            ('user', 'app', 'types "ok, book it"', 'old'),
        ], Q.ON)
        timeline('new', 920, 'With A2UI: the screen holds the state', lanes, [
            ('user', 'app', 'types "BER to SFO today, 2 back Oct 19"', 'old'),
            ('app', 'server', 'the message', 'old'),
            ('server', 'model', 'prompt + tools + A2UI skill', 'new'),
            ('model', 'server', 'text + <a2ui> … </a2ui>', 'new'),
            ('server', 'server', 'SDK: check, compile to JSON', 'new'),
            ('server', 'app', 'text + createSurface, updateComponents,\nupdateDataModel (/outbound/pax = 1)', 'new'),
            ('app', 'app', 'renderer draws two flight cards', 'new'),
            ('user', 'app', 'taps + on the outbound card', 'local'),
            ('app', 'app', 'data model /outbound/pax = 2:\nthe card updates, nothing is sent', 'local'),
            ('user', 'app', 'taps Confirm booking', 'old'),
            ('app', 'server', 'action confirm_booking\n{outboundPax: 2, returnPax: 2}', 'new'),
            ('server', 'model', 'the next turn, with the action', 'old'),
        ], NEW)
        words('who', 60, 1255, 'Your server is your endpoint: it holds your agent code and the A2UI SDK, and calls the Model through an LLM API.', 19, Q.ON)
        words('key', 60, 1290, 'Green: new with A2UI · dashed green: stays on the device · red: an extra round trip without A2UI', 19, Q.BODY)
        words('question', 60, 1335, 'Count the trips to the model before booking, in each timeline.', 26, '#b45309')
    elif slug.startswith('s22'):
        NEW = '#047857'
        w, h = image_size(4, 330, 640)
        els.append(Q._el('image', 'img-5', 1500, 95, w, h, 'transparent', fileId='resource-5', status='saved',
                         scale=[1, 1], roundness=None))
        words('img-caption', 1500, 105 + h, 'Resource 5: Travel A2UI,\neach part with its real path', 17, Q.BODY)
        # today
        words('today-head', 35, 95, 'Your chatbot today', 24, Q.TITLE)
        els.extend(Q.box('today-prompt', 35, 135, 230, 70, 'instructions + tools', 'plain', 18))
        arrow('today-1', [(270, 170), (320, 170)])
        els.extend(Q.box('today-model', 325, 135, 120, 70, 'Model', 'agent', 20))
        arrow('today-2', [(450, 170), (500, 170)])
        els.extend(Q.box('today-text', 505, 135, 230, 70, 'chat text', 'plain', 18))
        arrow('today-3', [(740, 170), (790, 170)])
        words('today-app', 800, 152, 'app: a chat bubble', 19, Q.BODY)
        # the six steps
        words('steps-head', 35, 250, 'Add six steps (green); the rest stays', 24, Q.TITLE)
        els.extend(Q.box('server', 35, 290, 1010, 330, '', 'plain', dashed=True))
        words('server-name', 50, 297, 'On your server', 18, Q.BODY)
        els.extend(Q.box('client', 1075, 290, 400, 330, '', 'plain', dashed=True))
        words('client-name', 1090, 297, 'In your app', 18, Q.BODY)
        steps = [('s1', 50, '1 Catalog', 'Basic Catalog\n(Text, Column, Button…)\nor your catalog.json'),
                 ('s2', 250, '2 Skill', 'SkillGenerator\nwrites skills/*.md,\nadded to the prompt'),
                 ('model', 450, 'Model', 'your model,\nunchanged; writes\ntext + <a2ui>'),
                 ('s3', 650, '3 Compile', 'A2uiGenerator,\nopen_stream:\ncheck, then JSON'),
                 ('s4', 850, '4 Send', 'your channel, or\na2ui-a2a, a2ui-adk,\nAG-UI, MCP'),
                 ('s5', 1090, '5 Render', '@a2ui/react, @a2ui/lit,\na2ui_flutter,\nSwiftUI, Compose')]
        for key, x, name, tools in steps:
            els.extend(Q.box(key, x, 335, 180, 70, name, 'agent' if key == 'model' else 'end', 21))
            words(key + '-tools', x + 5, 420, tools, 16, Q.ON if key == 'model' else NEW)
        for a, b in (('s1', 's2'), ('s2', 'model'), ('model', 's3'), ('s3', 's4')):
            xa = dict((k, x) for k, x, *_ in steps)[a] + 180
            arrow(a + '-' + b, [(xa + 2, 370), (xa + 18, 370)])
        arrow('s4-s5', [(1032, 370), (1088, 370)])
        els += icons.phone('app', 1300, 410, 'off')
        arrow('action', [(1335, 545), (1335, 590), (610, 590), (610, 410)], True)
        words('action-label', 700, 596, '6 Actions: a tap sends action to the agent', 18, NEW)
        # the packages
        words('pkg-head', 35, 660, 'The A2UI packages', 24, Q.TITLE)
        words('pkg', 35, 700, 'Agent SDK (steps 2, 3): Python a2ui-agent-sdk · TypeScript @a2ui/agent · Dart a2ui_agent\n'
              'Renderer SDK (step 5): @a2ui/react · @a2ui/lit · @a2ui/angular · a2ui_flutter · SwiftUI · Compose\n'
              'Core SDK: a2ui-core · @a2ui/web_core · a2ui_core, used inside both; you rarely call it', 18, Q.ON)
        words('question', 35, 820, 'Which steps does your chatbot already have, and which three packages would you add?', 24, '#b45309')
    elif slug.startswith('s41'):
        def image(i, x, y, box_w, box_h):
            w, h = image_size(i - 1, box_w, box_h)
            els.append(Q._el('image', f'img-{i}', x, y, w, h, 'transparent', fileId=f'resource-{i}', status='saved',
                             scale=[1, 1], roundness=None))
        NEW = '#047857'
        # before: a prompt, the model, one text answer
        words('before-head', 35, 95, 'Before: the model returns text', 28, Q.TITLE)
        els.extend(Q.box('before-prompt', 35, 145, 250, 110, 'Your prompt\n+ your tools', 'plain', 20))
        arrow('before-1', [(290, 200), (340, 200)])
        els.extend(Q.box('before-model', 345, 160, 130, 80, 'Model', 'agent', 22))
        arrow('before-2', [(480, 200), (530, 200)])
        els.extend(Q.box('before-text', 535, 150, 330, 100, '"Here are two direct\nflights, LH 454 and UA 901"', 'plain', 19))
        words('before-note', 535, 265, 'The app shows a chat bubble. Nothing to tap.', 19, Q.BODY)
        # after: two things are added (green); the rest stays
        words('after-head', 35, 340, 'After: green is new; everything else stays', 28, Q.TITLE)
        els.extend(Q.box('after-prompt', 35, 395, 250, 250, '', 'plain'))
        words('prompt-head', 50, 405, 'Your prompt', 21, Q.TITLE)
        words('prompt-old', 50, 440, '• your instructions\n• your tools\n  (searchFlights)', 18, Q.ON)
        els.extend(Q.box('skill', 50, 535, 220, 95, '', 'end'))
        words('skill-text', 62, 543, '+ A2UI skill\nmade by the SDK\nfrom catalog.json', 18, NEW)
        arrow('after-1', [(290, 520), (340, 520)])
        els.extend(Q.box('after-model', 345, 480, 130, 80, 'Model', 'agent', 22))
        arrow('after-2', [(480, 520), (530, 520)])
        els.extend(Q.box('output', 535, 395, 330, 250, '', 'plain'))
        words('output-head', 550, 405, 'What the model writes', 21, Q.TITLE)
        words('output-text', 550, 440, 'Text, as before:\n"Here are two direct flights"', 18, Q.ON)
        els.extend(Q.box('express', 550, 505, 300, 125, '', 'end'))
        words('express-text', 562, 512, '+ <a2ui>\n  root = Card(Column([\n    FlightCard(...), Button(...)]))\n  </a2ui>', 16, NEW)
        # the two parts go two ways
        arrow('text-way', [(700, 650), (700, 690), (415, 690), (415, 738)])
        words('text-way-label', 430, 700, 'text: sent as before', 18, Q.BODY)
        arrow('a2ui-way', [(860, 570), (905, 570), (905, 745)])
        els.extend(Q.box('compiler', 735, 750, 330, 110, '', 'end'))
        words('compiler-text', 750, 758, '+ SDK compiler, on your server\nchecks it against catalog.json,\nturns it into JSON messages', 17, NEW)
        arrow('json-way', [(730, 805), (520, 805)])
        words('json-label', 540, 772, 'JSON', 18, NEW)
        els += icons.phone('app', 380, 745, 'off')
        words('app-text', 35, 755, 'The app shows\nthe chat text\nand, under it,\nflight cards\nto tap', 19, Q.ON)
        image(1, 1110, 95, 330, 640)
        words('img-caption', 1110, 750, 'Resource 1: the official pipeline.\nPurple is your code; the teal\ndashed boxes are the A2UI SDK.', 18, Q.BODY)
        words('question', 35, 930, 'The model still writes text. Who turns the <a2ui> part into JSON?', 26, '#b45309')
    elif slug.startswith('s42'):
        NEW, RED = '#047857', '#b91c1c'
        # 1. what the model streams: chat text, then the <a2ui> block (official flight example, Resource 1)
        words('model-head', 35, 95, '1. The model streams text + an <a2ui> block', 24, Q.TITLE)
        els.extend(Q.box('answer', 35, 135, 540, 400, '', 'plain'))
        words('answer-text', 52, 147, '"Here are direct flights. Adjust the passengers below:"', 16, Q.ON)
        els.extend(Q.box('express', 50, 180, 510, 340, '', 'end'))
        words('express-code', 62, 190, '<a2ui>\n$/outbound/pax = 1\n$/outbound/price = 455\n$/return/pax = 2\n$/return/price = 970\n'
              'root = Card(Column([\n  FlightCard(flightNumber="LH 454", origin="BER",\n    destination="SFO", price=$/outbound/price,\n'
              '    passengers=$/outbound/pax),\n  FlightCard(flightNumber="UA 901", ...),\n  Button(Text("Confirm booking"),\n'
              '    action=Event("confirm_booking", {...}))\n]))\n</a2ui>', 15, NEW)
        arrow('to-sdk', [(580, 330), (625, 330)])
        # 2. the Agent SDK on your server
        words('sdk-head', 630, 95, '2. The Agent SDK, on your server', 24, Q.TITLE)
        els.extend(Q.box('sdk', 630, 135, 330, 400, '', 'end'))
        words('sdk-steps', 648, 150, 'As the tokens arrive:\n\n① split chat text from\n    the <a2ui> block\n② parse each statement\n'
              '    when it is complete\n③ check it against\n    catalog.json and the surface\n④ give components IDs,\n'
              '    split into messages', 18, NEW)
        arrow('bad', [(795, 540), (795, 590), (300, 590), (300, 540)], True)
        words('bad-label', 330, 597, '❗ invalid: not sent; returned to the model to fix', 18, RED)
        arrow('to-json', [(965, 330), (1005, 330)])
        # 3. the JSON messages that leave the server (Resource 2, "Messages on the wire")
        words('json-head', 1010, 95, '3. JSON messages to the app', 24, Q.TITLE)
        msgs = [('createSurface', '"surfaceId": "flight-booking-surface",\n"catalogId": ".../travel/v1/catalog.json"'),
                ('updateComponents', '{"id": "flight_return",\n "component": "FlightCard", "flightNumber": "UA 901",\n'
                                     ' "passengers": {"@path": "/return/pax"}}  ...'),
                ('updateDataModel', '"value": {"outbound": {"pax": 1, "price": 455},\n          "return":   {"pax": 2, "price": 970}}')]
        y = 135
        for n, (name, body) in enumerate(msgs):
            hgt = 95 if n != 1 else 120
            els.extend(Q.box(f'msg-{n}', 1010, y, 470, hgt, '', 'decision'))
            words(f'msg-{n}-name', 1025, y + 8, name, 19, Q.ON)
            words(f'msg-{n}-body', 1025, y + 36, body, 14, Q.BODY)
            y += hgt + 15
        # 4. the app: chat text and the cards
        arrow('to-app', [(1245, 485), (1245, 640), (1110, 640)])
        arrow('text-to-app', [(90, 545), (90, 720), (945, 720)])
        words('text-label', 110, 690, 'chat text, sent as before', 17, Q.BODY)
        els += icons.phone('app', 960, 640, 'off')
        words('app-text', 1100, 660, '4. The renderer draws:\nthe chat text, two flight cards\n(LH 454: 1 passenger,\n UA 901: 2 passengers)\nand Confirm booking', 18, Q.ON)
        # the answer to the topic's question, traced in green
        els.extend(Q.box('trace', 35, 790, 860, 70, '', 'end'))
        words('trace-text', 50, 800, '$/return/pax = 2  →  updateDataModel "return": {"pax": 2}  →\n'
              'FlightCard UA 901, bound to /return/pax, shows 2 passengers', 18, NEW)
        words('source', 35, 880, 'Example and messages from the official overview (Resources 1 and 2)', 17, Q.BODY)
        words('question', 35, 925, 'Which step would reject FlightCard(seat="12A") if the catalog has no seat?', 24, '#b45309')
    else:
        els += icons.person('choice', 490, 135, 'off', s=.8)
        words('choice-label', 330, 80, 'Does the task change the controls?', 30)
        arrow('dynamic', [(490, 295), (270, 415)])
        arrow('fixed', [(590, 295), (820, 415)])
        els += icons.phone('dynamic-ui', 180, 430, 'off')
        words('dynamic-label', 65, 660, 'Dynamic surface\nCatalog-constrained', 29)
        els += icons.document('fixed-ui', 795, 440, 'off', w=95, h=130)
        words('fixed-label', 700, 660, 'Fixed form\nStable sequence', 29)
        words('yes', 255, 340, 'Often', 26)
        words('no', 755, 340, 'Rarely', 26)
        words('question', 35, 820, 'A fixed-message test checks behavior, not general model reliability.', 25, '#b45309')
    for e in els:
        if e['type'] == 'text':
            e['fontFamily'] = 6
    return els


def page_tabs(topic):
    """Split the topic's learning.md into one file per section under delivery/page/, a left tab each on Page
    (top-view-left-tab-right-content); s01's Source records give one tab per Resource. learning.md stays the one
    authored file: these are rebuilt from it."""
    text = (topic / 'delivery/learning.md').read_text()
    out = topic / 'delivery/page'
    out.mkdir(exist_ok=True)
    for old in out.glob('*.md'):
        old.unlink()
    parts = []
    for block in re.split(r'(?m)^## ', text)[1:]:
        head, _, body = block.partition('\n')
        subs = re.split(r'(?m)^### ', body)
        if len(subs) > 1 and all(s.startswith('Resource ') for s in subs[1:]):
            parts += [(s.partition('\n')[0].strip(), s.partition('\n')[2]) for s in subs[1:]]
        else:
            parts.append((head.strip(), body))
    items = []
    for n, (head, body) in enumerate(parts, 1):
        name = f'{n:02d}-' + re.sub(r'[^a-z0-9]+', '-', head.lower()).strip('-') + '.md'
        body = re.sub(r'\]\((?!https?:|/|#)([^)]+)\)', r'](../\1)', body)   # relative links, one folder deeper
        (out / name).write_text(f'# {head}\n{body.rstrip()}\n')
        items.append({'name': head, 'path': (out / name).relative_to(ROOT).as_posix()})
    views_path = topic / 'studio-views.json'
    views = json.loads(views_path.read_text())
    for view in views['views']:
        if view['name'] == 'Page':
            view['items'] = items
    views_path.write_text(json.dumps(views, indent=2, ensure_ascii=False) + '\n')


def merger(slug):
    path = ROOT / 'examples/Project-Ladder/blueprint/b17_theme_work/s05-knowledge-structure/build_structure.py'
    spec = importlib.util.spec_from_file_location('knowledge_drawing_owner', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.NAME = slug
    return mod.merge_drawing


def build():
    for slug in TOPICS:
        topic = HERE / slug
        page_tabs(topic)
        target = topic / (slug + '.excalidraw')
        old = json.loads(target.read_text()) if target.exists() else {}
        els, seed = merger(slug)(old, drawing(slug))
        Q.write(target, els)
        data = json.loads(target.read_text())
        data['knowledgeSeed'] = seed
        for key in ('files', 'appState'):
            if key in old:
                data[key] = old[key]
        if slug in TOPIC_IMAGES:
            files = image_files()
            data['files'] = {**data.get('files', {}), **{f'resource-{i}': files[f'resource-{i}'] for i in TOPIC_IMAGES[slug]}}
        target.write_text(json.dumps(data) + '\n')
        subprocess.run(['python3', str(KIT / 'render_png.py'), str(target), str(topic / (slug + '.png')), '1'], check=True)
        slides = topic_slides.record(topic)
        delivered = copy.deepcopy(slides)
        for slide in delivered:
            slide['image'] = '../../' + slide['image']
        deck = topic / 'delivery/deck'
        (deck / (slug + '.slides.html')).write_text(topic_slides.deck(topic, delivered))
        code = ('import sys; from pathlib import Path; sys.path.insert(0,sys.argv[1]); '
                'import topic_slides; topic_slides.write_pptx(Path(sys.argv[2]),Path(sys.argv[3]))')
        subprocess.run(['python3', '-c', code, str(KIT), str(topic), str(deck / (slug + '.slides.pptx'))], check=True)


def check():
    assert (HERE / '_studio_groups.txt').read_text().splitlines() == list(dict.fromkeys(v[0] for v in TOPICS.values()))
    assert {p.name for p in HERE.glob('s[0-9][0-9]-*')} == set(TOPICS)
    assert [p.name for p in HERE.glob('j[0-9][0-9]_*')] == ['j01_interactive_card'], 'Only the one optional practice Job'
    for slug, (band, title) in TOPICS.items():
        topic = HERE / slug
        face = (topic / (slug + '.md')).read_text()
        assert face.startswith(f'{slug[:3]} · {band}: {title}') and f'**Tags:** {band}' in face
        notes = (topic / 'delivery/learning.md').read_text()
        assert len(notes.split()) > 150 and '## Try explaining' in notes
        assert not re.search('[\u4e00-\u9fff]', face + notes)
        views = json.loads((topic / 'studio-views.json').read_text())['views']
        assert [v['name'] for v in views] == ['Page', 'Draw', 'Map', 'Slides']
        for view in views:
            for row in view['items']:
                assert (ROOT / row['path']).is_file(), row
        data = json.loads((topic / (slug + '.excalidraw')).read_text())
        assert not re.search('[\u4e00-\u9fff]', ''.join(e.get('text', '') for e in data['elements']))
        assert any(e['type'] == 'arrow' for e in data['elements'])
        assert (topic / (slug + '.png')).stat().st_size > 1000
        for suffix in ('html', 'pptx'):
            assert (topic / 'delivery/deck' / (slug + '.slides.' + suffix)).stat().st_size > 1000
        for link in re.findall(r'\]\(([^)]+)\)', notes):
            if link.startswith('/_board/page?path='):
                from urllib.parse import parse_qs, urlparse, unquote
                assert not urlparse(link).fragment, 'Shared Markdown reader does not create heading anchors'
                path = parse_qs(urlparse(link).query)['path'][0].lstrip('/')
                assert (ROOT / path).is_file(), link
            elif not link.startswith(('https://', 'http://', '#')):
                assert (topic / 'delivery' / link.split('#')[0]).resolve().is_file(), link
    print('A2UI: four real English Studio topics, ordered Bands, bound content and drawing/deck files checked')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        check()
    else:
        build()
        check()

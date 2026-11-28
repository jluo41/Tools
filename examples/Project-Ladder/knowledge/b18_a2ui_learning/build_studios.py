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
    's01-official-sources': ('Resource', 'Official Sources and Versions'),
    's11-messages-components-data': ('Method', 'Messages, Components and Data'),
    's21-tracing-interaction': ('Method', 'Tracing a User Interaction'),
    's22-chatbot-to-a2ui': ('Method', 'From a Text Chatbot to A2UI, Step by Step'),
    's31-use-cases-boundaries': ('Method', 'Use Cases and Boundaries'),
    's41-agent-text-to-a2ui': ('Question', 'If My Agent Only Returns Text, What Changes?'),
    's42-who-writes-the-json': ('Question', 'Who Writes the JSON?'),
}
# each Band is one Studio Type (hai-knowledge A07), kept in the Work Blueprint b17 beside s05 Block Structure: Knowledge
TYPES_HOME = ROOT / 'examples/Project-Ladder/blueprint/b17_theme_work'
TYPES = {'Resource': 's77-studio-type-resources', 'Method': 's78-studio-type-methods',
         'Question': 's80-studio-type-questions'}
TYPE_NAMES = {'Resource': 'resources', 'Method': 'methods', 'Question': 'questions'}
TOPIC_IMAGES = {'s01-official-sources': (1, 2, 3, 4, 5, 6), 's11-messages-components-data': (1, 3), 's41-agent-text-to-a2ui': (1,), 's22-chatbot-to-a2ui': (5,)}


# the six source records of s01-official-sources/delivery/learning.md, drawn as cards (name, page, what to read, used by)
RESOURCES = [
    ('Resource 1 · Architecture', 'Overview: How A2UI Works', 'Step-by-step generation,\nrender on the client,\nhandle user actions', 's11, s21',
     'Berlin to San Francisco: the agent sends cards;\ntapping + changes passengers locally'),
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
# the passenger count as each of Resources 1 to 4 shows it
TRACE = ['on the phone: 1, then + makes 2', 'in the JSON: "@path": "/outbound/pax"',
         'one value, bound to the card', 'in the action: outboundPax: 2']
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


def shrink(parts, x0, y0, s):
    """Scale an icon's elements about (x0, y0), so a full-size icon fits beside a label."""
    for el in parts:
        el['x'] = x0 + (el['x'] - x0) * s
        el['y'] = y0 + (el['y'] - y0) * s
        el['width'] *= s
        el['height'] *= s
        if 'points' in el:
            el['points'] = [[px * s, py * s] for px, py in el['points']]
    return parts


def actor(eid, kind, x, y):
    """One actor's picture, about 90 high, its top-left at (x, y): person, phone, server, cloud (an LLM API), doc."""
    if kind == 'person':
        return shrink(icons.person(eid, x, y, 'off'), x, y, 0.55)
    if kind == 'phone':
        return shrink(icons.phone(eid, x, y, 'off'), x, y, 0.65)
    if kind == 'server':
        return icons.server(eid, x, y, 'off', w=80, h=88)
    if kind == 'cloud':
        return shrink(icons.cloud(eid, x, y + 10, 'off'), x, y + 10, 0.5) + Q.text(eid + '-llm', x + 47, y + 35, 'LLM', 18, Q.ON)
    return icons.document(eid, x, y, 'off', w=62, h=80)

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
        NEW = '#047857'
        # a reading trail, not a grid: six stops along one path, each with its official picture
        stops = [  # (index, picture's top-left x, y, fit width, fit height, tilt)
            (0, 150, 250, 330, 470, -0.03), (1, 600, 150, 250, 330, 0.035), (2, 950, 210, 430, 300, -0.02),
            (3, 1500, 150, 380, 250, 0.03), (4, 1330, 650, 260, 360, -0.035), (5, 720, 720, 430, 280, 0.025)]
        centres = [(x + image_size(i, bw, bh)[0] / 2, y + image_size(i, bw, bh)[1] / 2) for i, x, y, bw, bh, _ in stops]
        # the trail first, so every picture sits on top of it: start, the six stops in reading order, the sign
        trail = [(110, 330), centres[0], centres[1], centres[2], centres[3], (1930, 330), (1930, 600), centres[4], centres[5],
                 (420, 1020)]
        els.extend(Q.arrow('trail', trail, color='#94a3b8', width=3, dashed=True))
        for i, x, y, bw, bh, tilt in stops:
            name, page, read, supports, vivid = RESOURCES[i]
            w, h = image_size(i, bw, bh)
            els.append(Q._el('image', f'r{i + 1}-img', x, y, w, h, 'transparent', fileId=f'resource-{i + 1}',
                             status='saved', scale=[1, 1], roundness=None, angle=tilt))
            els.extend(Q.dot(f'r{i + 1}-pin', x + w / 2, y - 8, 9, 'warn'))
            words(f'r{i + 1}-name', x, y - 52, name, 22, Q.TITLE)
            words(f'r{i + 1}-vivid', x, y + h + 18, vivid, 16, Q.ON)
            if i < 4:
                words(f'r{i + 1}-trace', x, y + h + 62, '✈️ ' + TRACE[i], 16, NEW)
        els += actor('learner', 'person', 40, 200)
        words('ask', 20, 120, '"What is A2UI,\nand which version?"', 19, Q.ON)
        words('docs-band', 1000, 80, 'Read the docs: Resources 1 to 4', 20, Q.BODY)
        words('code-band', 1060, 1085, 'Then run it: Resources 5 and 6', 20, Q.BODY)
        # the version sign at the end of the trail
        els.extend(Q.box('sign', 200, 930, 300, 90, 'v1.0 here\n(docs also show v0.9.1)', 'decision', 19))
        words('pin', 200, 1035, '📌 pin the code and the packages together;\nnever mix a v0.9 path with a v1.0 message', 18, NEW)
        words('question', 700, 1160, 'Which version do the six Resources follow,\nand what must you pin before running code?', 24, '#b45309')
        words('foot', 35, 1260, 'Images: official A2UI docs and README, Apache-2.0 (assets/SOURCES.md)', 17, Q.BODY)
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
        els += actor('today-prompt', 'doc', 45, 135)
        words('today-prompt-l', 120, 150, 'instructions\n+ tools', 17, Q.BODY)
        arrow('today-1', [(230, 175), (275, 175)])
        els += actor('today-model', 'cloud', 285, 135)
        words('today-model-l', 290, 225, 'Model (LLM API)', 17, Q.BODY)
        arrow('today-2', [(430, 175), (475, 175)])
        els.extend(Q.box('today-text', 485, 145, 190, 60, 'chat text', 'plain', 18))
        arrow('today-3', [(680, 175), (725, 175)])
        els += actor('today-app', 'phone', 735, 130)
        words('today-app-l', 805, 160, 'a chat bubble', 17, Q.BODY)
        # the six steps: a picture each, the tool under it, green when new
        words('steps-head', 35, 285, 'Add six steps (green); the rest stays', 24, Q.TITLE)
        els.extend(Q.box('server', 35, 325, 1040, 400, '', 'plain', dashed=True))
        words('server-name', 50, 332, 'Your server (endpoint)', 18, Q.BODY)
        els.extend(Q.box('client', 1100, 325, 375, 400, '', 'plain', dashed=True))
        words('client-name', 1115, 332, 'Your app', 18, Q.BODY)
        steps = [('s1', 70, 'doc', '1 Catalog', 'Basic Catalog, or\nyour catalog.json', NEW),
                 ('s2', 275, 'doc', '2 Skill', 'SkillGenerator\nwrites skills/*.md\ninto the prompt', NEW),
                 ('model', 470, 'cloud', 'Model (LLM API)', 'the same model,\nnow also writes\n<a2ui>', Q.ON),
                 ('s3', 690, 'server', '3 Compile', 'A2uiGenerator,\nopen_stream:\ncheck, then JSON', NEW),
                 ('s4', 890, None, '4 Send', 'your channel, or\na2ui-a2a, a2ui-adk,\nAG-UI, MCP', NEW),
                 ('s5', 1130, 'phone', '5 Render', '@a2ui/react, @a2ui/lit,\na2ui_flutter,\nSwiftUI, Compose', NEW)]
        trace = {'s1': 'FlightCard is\nin the catalog', 's2': 'FlightCard(..., \npassengers)', 'model': 'FlightCard("UA 901",\npassengers=2)',
                 's3': '"return":\n{"pax": 2}', 's4': 'sent over\nSSE', 's5': 'UA 901 ·\n2 passengers'}
        where = {'s1': 'catalogs/…/catalog.json', 's2': 'scripts/build_skills.py', 'model': 'brain/',
                 's3': 'brain/catalog.py', 's4': 'server-sent events', 's5': 'renderers/react/'}
        for key, x, kind, name, tools, color in steps:
            words(key + '-trace', x - 10, 570, '✈️ ' + trace[key], 15, NEW)
            words(key + '-where', x - 10, 620, where[key], 14, Q.BODY)
            if kind:
                els.extend(actor(key, kind, x, 370))
            else:
                els.extend(Q.arrow(key, [(x, 415), (x + 140, 415)], color=NEW, width=4))
            words(key + '-name', x - 10, 470, name, 20, color)
            words(key + '-tools', x - 10, 505, tools, 16, color)
        for a, b in ((150, 260), (360, 460), (630, 680), (790, 880), (1040, 1120)):
            arrow(f'step-{a}', [(a, 415), (b, 415)])
        els += actor('tapper', 'person', 1330, 360)
        words('tapper-l', 1385, 470, 'User', 18, Q.BODY)
        arrow('action', [(1350, 515), (1350, 700), (645, 700), (645, 445), (605, 430)])
        els[-1]['strokeColor'] = NEW
        words('action-l', 700, 675, '6 Actions: Confirm sends action {returnPax: 2} back', 17, NEW)
        # the packages, one line each
        words('pkg-head', 35, 760, 'The A2UI packages', 24, Q.TITLE)
        words('pkg-1', 35, 800, 'Agent SDK (steps 2, 3): a2ui-agent-sdk · @a2ui/agent · a2ui_agent', 18, Q.ON)
        words('pkg-2', 35, 830, 'Renderer SDK (step 5): @a2ui/react · @a2ui/lit · @a2ui/angular · a2ui_flutter', 18, Q.ON)
        words('pkg-3', 35, 860, 'Core SDK, used inside both: a2ui-core · @a2ui/web_core · a2ui_core', 18, Q.ON)
        words('trace', 35, 905, '✈️ "Book BER to SFO" → skill-taught model → <a2ui> → JSON → two flight cards on the phone', 19, NEW)
        words('question', 35, 955, 'Which steps does your chatbot already have, and which packages would you add (one server, two React)?', 24, '#b45309')
    elif slug.startswith('s41'):
        NEW = '#047857'
        w, h = image_size(0, 330, 640)
        els.append(Q._el('image', 'img-1', 1130, 95, w, h, 'transparent', fileId='resource-1', status='saved',
                         scale=[1, 1], roundness=None))
        words('img-caption', 1130, 105 + h, 'Resource 1: purple is your code;\nthe teal dashed boxes are the A2UI SDK', 17, Q.BODY)
        # before: prompt, model, one sentence, a chat bubble
        words('before-head', 35, 95, 'Before: the model answers in text', 26, Q.TITLE)
        els += actor('before-prompt', 'doc', 50, 140)
        words('before-prompt-l', 30, 230, 'your prompt\n+ tools', 17, Q.BODY)
        arrow('before-1', [(125, 180), (175, 180)])
        els += actor('before-model', 'cloud', 185, 140)
        words('before-model-l', 190, 230, 'Model (LLM API)', 17, Q.BODY)
        arrow('before-2', [(330, 180), (380, 180)])
        els.extend(Q.box('before-text', 390, 140, 360, 80, '"Here are two direct flights,\nLH 454 and UA 901"', 'plain', 19))
        arrow('before-3', [(755, 180), (820, 180)])
        els += actor('before-app', 'phone', 830, 135)
        words('before-app-l', 900, 165, 'Your app: a chat bubble,\nnothing to tap', 17, Q.BODY)
        # after: the same chain, with three green additions
        words('after-head', 35, 320, 'After: green is new; everything else stays', 26, Q.TITLE)
        els += actor('after-prompt', 'doc', 50, 370)
        words('after-prompt-l', 30, 460, 'your prompt\n+ tools', 17, Q.BODY)
        words('skill', 30, 505, '+ A2UI skill,\nmade by the SDK\nfrom catalog.json', 17, NEW)
        arrow('after-1', [(125, 410), (175, 410)])
        els += actor('after-model', 'cloud', 185, 370)
        words('after-model-l', 190, 460, 'Model (LLM API)', 17, Q.BODY)
        arrow('after-2', [(330, 410), (380, 410)])
        words('out-text', 395, 365, '"Here are two direct flights"', 19, Q.ON)
        els.extend(Q.box('express', 390, 400, 360, 110, '', 'end'))
        words('express-text', 405, 410, '+ <a2ui>\n  FlightCard(flightNumber="LH 454", ...)\n  Button(Text("Confirm booking"))\n</a2ui>', 16, NEW)
        arrow('to-sdk', [(755, 455), (830, 455)])
        els += actor('sdk', 'server', 840, 410)
        words('sdk-l', 935, 415, '+ SDK compiler\non your server\n(endpoint):\nchecks, writes JSON', 17, NEW)
        arrow('json', [(880, 505), (880, 600), (525, 600), (525, 640)])
        words('json-l', 600, 572, 'JSON messages', 17, NEW)
        arrow('text-way', [(395, 392), (330, 392), (330, 690), (470, 690)])
        words('text-way-l', 260, 700, 'text, as before', 17, Q.BODY)
        els += actor('after-app', 'phone', 485, 645)
        words('after-app-l', 560, 650, 'Your app: the chat text, and', 18, Q.ON)
        words('after-app-new', 560, 675, '+ a renderer draws a surface:\n  a card "LH 454" to tap', 18, NEW)
        words('trace', 35, 790, '✈️ LH 454 moves: in the sentence before, in a card you can tap after', 20, NEW)
        words('question', 35, 850, 'Name the green parts your chatbot needs: which are on the server, which in the app?', 25, '#b45309')
    elif slug.startswith('s42'):
        NEW, RED = '#047857', '#b91c1c'
        # 1. the model writes the <a2ui> block (the official flight example)
        els += actor('model', 'cloud', 35, 90)
        words('model-head', 185, 100, '1. The model (LLM API) streams\ntext + an <a2ui> block', 22, Q.TITLE)
        els.extend(Q.box('express', 35, 185, 560, 350, '', 'plain'))
        lines = ['"Here are direct flights. Adjust the passengers below:"', '<a2ui>', '$/outbound/pax = 1',
                 '$/outbound/price = 455', '$/return/pax = 2', '$/return/price = 970', 'root = Card(Column([',
                 '  FlightCard(flightNumber="LH 454", passengers=$/outbound/pax, ...),',
                 '  FlightCard(flightNumber="UA 901", passengers=$/return/pax, ...),',
                 '  Button(Text("Confirm booking"), action=Event("confirm_booking"))', ']))', '</a2ui>']
        for n, line in enumerate(lines):
            traced = 'return/pax' in line
            words(f'line-{n}', 52, 197 + n * 27, line, 16, NEW if traced else Q.ON)
        arrow('to-sdk', [(600, 360), (650, 360)])
        # 2. the Agent SDK on your server
        els += actor('sdk', 'server', 665, 185)
        words('sdk-head', 760, 190, '2. The Agent SDK,\non your server (endpoint)', 22, Q.TITLE)
        for n, step in enumerate(['① split the chat text from <a2ui>', '② parse each statement as it ends',
                                  '③ check it against catalog.json', '④ give IDs, split into messages']):
            words(f'sdk-{n}', 665, 300 + n * 34, step, 18, NEW)
        arrow('bad', [(760, 450), (760, 575), (300, 575), (300, 540)])
        els[-1]['strokeColor'] = RED
        words('bad-l', 330, 583, '❗ invalid: not sent; back to the model to fix', 17, RED)
        arrow('to-json', [(965, 360), (1010, 360)])
        # 3. the JSON messages that leave the server
        words('json-head', 1015, 100, '3. JSON messages to the app', 22, Q.TITLE)
        msgs = [('createSurface', '"surfaceId": "flight-booking-surface"', Q.BODY),
                ('updateComponents', '"flight_return": FlightCard,\n"passengers": {"@path": "/return/pax"}', NEW),
                ('updateDataModel', '"return": {"pax": 2, "price": 970}', NEW)]
        for n, (name, body, color) in enumerate(msgs):
            y = 145 + n * 130
            els.extend(Q.box(f'msg-{n}', 1015, y, 430, 110, '', 'decision'))
            words(f'msg-{n}-name', 1030, y + 10, name, 19, Q.ON)
            words(f'msg-{n}-body', 1030, y + 45, body, 15, color)
        arrow('to-app', [(1230, 540), (1230, 660), (1130, 660)])
        # 4. the app
        els += actor('app', 'phone', 1050, 620)
        words('app-l', 1240, 680, '4. The renderer draws\nUA 901 · 2 passengers', 19, NEW)
        words('trace', 35, 660, '✈️ $/return/pax = 2  →  "return": {"pax": 2}  →  the UA 901 card shows 2', 20, NEW)
        words('source', 35, 705, 'Example and messages from the official overview (Resources 1 and 2)', 17, Q.BODY)
        words('question', 35, 760, 'Which step would reject FlightCard(seat="12A") if the catalog has no seat?', 24, '#b45309')
    else:
        NEW, RED = '#047857', '#b91c1c'
        els.extend(Q.diamond('decide', 470, 85, 460, 150, '', 'decision'))
        words('decide-l', 545, 135, 'Does the request change\nwhat the screen should show?', 21, Q.ON)
        # yes: a travel assistant
        arrow('yes', [(560, 235), (300, 300)])
        words('yes-l', 330, 245, 'yes, often', 19, NEW)
        els += actor('traveller', 'person', 60, 300)
        words('ask', 120, 300, '"BER to SFO today,\n2 back on Oct 19"', 18, Q.ON)
        words('user-l', 60, 400, 'User', 17, Q.BODY)
        arrow('ask-agent', [(215, 375), (240, 375), (240, 440)])
        els += actor('agent', 'cloud', 175, 440)
        words('agent-l', 160, 530, 'Agent (LLM API):\nwrites FlightCard(..., passengers=2)', 16, NEW)
        arrow('agent-app', [(310, 470), (340, 470), (340, 420)])
        els += actor('travel-app', 'phone', 310, 320)
        words('travel-l', 375, 320, 'Travel assistant: A2UI\nbuilds two flight cards\nfor this request', 18, NEW)
        words('travel-v', 375, 400, '✈️ UA 901 · passengers 2', 18, NEW)
        # no: a sign-up form
        arrow('no', [(840, 235), (1060, 300)])
        words('no-l', 970, 245, 'no, rarely', 19, Q.BODY)
        els += actor('form', 'doc', 980, 320)
        words('form-l', 1060, 320, 'Sign-up form: the same\nfields every time;\nordinary app UI is simpler', 18, Q.BODY)
        # the boundaries either way
        words('bound-head', 60, 600, 'Boundaries, whichever you choose', 22, Q.TITLE)
        els += icons.shield('catalog', 60, 645, 'off', s=0.6)
        words('bound-1', 130, 650, '⚠️ the agent asks for a component the app lacks\n→ the catalog rejects it', 18, RED)
        els += icons.lock('auth', 700, 655)
        words('bound-2', 770, 650, '⚠️ a card that looks right triggers a payment\n→ your app checks the action', 18, RED)
        words('source', 60, 750, 'When to use A2UI: Resource 6 · a design judgement, not an A2UI rule', 17, Q.BODY)
        words('question', 60, 800, 'Sign-up form or travel assistant: which one gets A2UI, and why?', 25, '#b45309')
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
    views['check_type'] = TYPE_NAMES[TOPICS[topic.name][0]]       # by name, so a renumbered type topic still resolves
    from check_views import build as check_build
    for path, text in check_build(topic, views, ROOT).items():
        path.write_text(text)


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
    assert {p.name for p in HERE.glob('s[0-9][0-9]-*')} == set(TOPICS), 'Studio Types live in the Blueprint, not here'
    import type_follow
    for band, slug in TYPES.items():
        assert (TYPES_HOME / slug / 'elements.md').is_file(), slug
    assert [p.name for p in HERE.glob('j[0-9][0-9]_*')] == ['j01_interactive_card'], 'Only the one optional practice Job'
    for slug, (band, title) in TOPICS.items():
        topic = HERE / slug
        face = (topic / (slug + '.md')).read_text()
        assert face.startswith(f'{slug[:3]} · {band}: {title}') and f'**Tags:** {band}' in face
        notes = (topic / 'delivery/learning.md').read_text()
        assert len(notes.split()) > 150 and '## Try explaining' in notes
        assert not re.search('[\u4e00-\u9fff]', face + notes)
        data = json.loads((topic / 'studio-views.json').read_text())
        assert data['check_type'] == TYPE_NAMES[band], slug
        bad, _ = type_follow.problems(topic, ROOT)
        assert not bad, (slug, bad)
        views = data['views']
        assert [v['name'] for v in views] == ['Page', 'Draw', 'Map', 'Slides', 'Check']
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
    print('A2UI: English Studio topics, one Studio Type per Band, each topic follows its type, drawing/deck files checked')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        check()
    else:
        build()
        check()

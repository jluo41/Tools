"""Shared fixture for the focus page tests (test_focus_*.py): a temporary root with one Block face,
and the helpers that write a Findings Block or a Task."""
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()


class FocusPageCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.block = self.root / "b01_study"
        self.block.mkdir()
        self.face = self.block / "board.md"
        self.face.write_text("# Study\nspine: Compare the methods.\nclose: Each result names its source.\n")

    def findings_block(self):
        report = self.block / 'reports/q01_a/q01_a.md'
        report.parent.mkdir(parents=True)
        report.write_text('# A\nstate: OPEN\n\n## Opening\n\nNo answer has been recorded yet.\n')
        done = self.block / 'reports/q02_b/q02_b.md'
        done.parent.mkdir(parents=True)
        done.write_text('# B\nstate: OPEN\n\n## Opening\n\nAgreed (261104): Every table is stored.\n')
        task = self.block / 'j01_work/t01_read'
        task.mkdir(parents=True)
        (self.block / 'j01_work/j01_work.md').write_text('# j01\nstate: PARTIAL\n')
        (task / 't01_read.md').write_text('# t01\nstate: PARTIAL\n\n## Content\n\n<!-- note -->\nReading of run `r01`.\n\n- 106 tables checked: 84 pass.\n')
        self.face.write_text('# Study\ngoal: Compare.\n\n## Questions\n\n```yaml\nquestions:\n'
                             '- id: Q01\n  title: Stored tables\n  group: Coverage\n  report: reports/q01_a/q01_a.md\n  work:\n  - j01_work/t01_read\n'
                             '- id: Q02\n  title: Whole tables\n  group: Cards\n  report: reports/q02_b/q02_b.md\n```\n')

    def write_task(self, job, name, state, figure=False):
        task = self.block / job / name
        task.mkdir(parents=True, exist_ok=True)
        (task / (name + '.md')).write_text(f'# {name}\ngoal: Goal of {name}.\nstate: {state}\n')
        if figure:
            result = task / 'runs' / 'r01_first' / 'result'
            result.mkdir(parents=True)
            (result / 'figure.png').write_bytes(b'png')
            (result / 'display.yaml').write_text('question: Does it differ by region?\n')
            (result / 'headline.txt').write_text('It differs little.\n')
        return task


# A work page draws its views as bands on one page (view_bands.py, JL 261124): read one band, or the bands' names.
_BAND_AT = '<section class="work-section-group view-band" id="band-'


def band(page: str, key: str) -> str:
    """The band of view `key` (overview, standing, findings, delivery, ...), up to the next band or the card's end."""
    start = page.find(_BAND_AT + key + '"')
    if start == -1:
        return ''
    ends = [i for i in (page.find(_BAND_AT, start + 1), page.find('</section><footer>', start)) if i != -1]
    return page[start:min(ends)] if ends else page[start:]


def band_names(page: str) -> list:
    """The bands' names in order, as the view buttons named them before."""
    import re
    return [n.split(' ', 1)[-1] for n in re.findall(r'view-band" id="band-[^"]+" data-view="[^"]+"><h2>([^<]+)</h2>', page)]


def view_names(page: str) -> list:
    """The view buttons' names in order (Main, then the views that are not bands)."""
    import re
    bar = re.search(r'<nav class="section-views".*?</nav>', page, re.S)
    return re.findall(r'<a [^>]*>([^<]+)</a>', bar.group(0)) if bar else []

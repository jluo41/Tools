"""Build the local decision report from authored data and template. No model calls."""
import argparse
import json
from pathlib import Path


def build(report_path, template_path, output_path):
    report = json.loads(report_path.read_text())
    assert report['schema_version'] == 1
    assert report['report_id'] and report['guideline_version']
    ids = [d['id'] for d in report['decisions']]
    assert len(ids) == len(set(ids)), 'Duplicate decision ids'
    sources = {s['id'] for s in report['sources']}
    assert len(sources) == len(report['sources'])
    for d in report['decisions']:
        assert len(d['options']) >= 2
        option_ids = [o['id'] for o in d['options']]
        assert len(set(option_ids)) == len(option_ids)
        assert not {'none', 'defer'} & set(option_ids)
        assert set(d['source_ids']) <= sources
        for example in d['examples']:
            assert example['split'] == 'learning', 'Evaluation examples cannot enter development reports'
    data = json.dumps(report, ensure_ascii=False).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    template = template_path.read_text()
    assert template.count('__REPORT_DATA__') == 1
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(template.replace('__REPORT_DATA__', data))
    print(f'Built {output_path}: {len(ids)} decisions; learning-only evidence')


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    p = argparse.ArgumentParser()
    p.add_argument('--report', type=Path, default=root / 'source/report-v1.json')
    p.add_argument('--out', type=Path, default=root / 'build/index.html')
    args = p.parse_args()
    build(args.report, root / 'source/template.html', args.out)

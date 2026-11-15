"""Build an offline HTML review, with hashed source excerpts for traceability."""
from datetime import datetime, timezone
from hashlib import sha256
from html import escape as e
import json
from pathlib import Path

from findings import FINDINGS, REFERENCES

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def luminance(color):
    values = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
    return sum(a * b for a, b in zip(linear, (.2126, .7152, .0722)))


def contrast(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + .05) / (lo + .05)


def examples(key):
    """Synthetic examples, not captured production HTML or active work controls."""
    examples_by_key = {
        'contrast': (
            '<div class="goal dark-old"><b>比较两种设计方法</b><small>目标与评价条件</small></div>',
            '<div class="goal dark-new"><b>比较两种设计方法</b><small>目标与评价条件</small></div>'),
        'targets': (
            '<div class="rail small-hit"><span>目标</span><span>方法</span><span>结果</span></div><small>单行推算约 30px</small>',
            '<div class="rail large-hit"><span>目标</span><span>方法</span><span>结果</span></div><small>展开后仍至少 44px</small>'),
        'dialog': (
            '<div class="mock-window"><b>方法比较</b><div class="sheet"></div></div><small>弹窗名称：未关联标题</small>',
            '<div class="mock-window"><b>方法比较</b><div class="sheet"></div></div><small>弹窗名称：方法比较</small>'),
        'focus': (
            '<div class="journey"><span class="focus-ring">托盘入口</span><span>↓ 画面滚动</span><span class="destination">审阅目标</span></div>',
            '<div class="journey"><span>托盘入口</span><span>↓ 画面与焦点一起到达</span><span class="destination focus-ring">审阅目标</span></div>'),
        'state': (
            '<div class="goal"><b>比较两种设计方法</b><small>signed</small></div>',
            '<div class="goal"><b>比较两种设计方法</b><span aria-label="已签署">✓</span></div>'),
        'empty': (
            '<div class="mock-section"><b>结果</b><p>Nothing here yet.</p></div><div class="mock-section"><b>下一步</b><p>补充评价条件</p></div>',
            '<div class="mock-section"><b>下一步</b><p>补充评价条件</p></div>'),
        'borders': (
            '<div class="job-list strong"><div>基线方法</div><div class="latest">修订方法 <small>最新</small></div><div class="held">备选方法</div></div>',
            '<div class="job-list quiet"><div>基线方法</div><div class="latest">修订方法 <small>最新</small></div><div class="held">备选方法</div></div>'),
        'rules': (
            '<div class="rule-flow"><span>根规则 → 标记</span><span>旧指南 → 状态词与进度数</span><span>生成结果 → 表达不一致</span></div>',
            '<div class="rule-flow"><span>根规则</span><span>↓ 同步到活动指南</span><span>共享组件 → 一致的表达</span></div>'),
    }
    before, after = examples_by_key[key]
    return ('<div class="comparison"><figure><figcaption>现状示意</figcaption><div class="sample">'
            + before + '</div></figure><figure><figcaption>建议示意</figcaption><div class="sample">'
            + after + '</div></figure></div>')


def main():
    cards, receipt = [], {'generated_utc': datetime.now(timezone.utc).isoformat(), 'sources': {}}
    for f in FINDINGS:
        excerpts = []
        for path, start, end in f['evidence']:
            raw = (ROOT / path).read_bytes()
            lines = raw.decode().splitlines()
            assert 1 <= start <= end <= len(lines), (path, start, end)
            receipt['sources'][path] = sha256(raw).hexdigest()
            snippet = '\n'.join(f'{n}: {lines[n - 1]}' for n in range(start, end + 1))
            excerpts.append(f'<p class="source-path">{e(path)}:{start}–{end}</p><pre><code>{e(snippet)}</code></pre>')
        refs = ' · '.join(f'<a href="{REFERENCES[r][1]}" rel="noreferrer">{e(REFERENCES[r][0])}</a>' for r in f['refs'])
        calculation = ''
        if f['id'] == 'contrast':
            old = contrast('#e8e8e6', '#eef3fb')
            muted = contrast('#a0a09c', '#eef3fb')
            new = contrast('#e8e8e6', '#253749')
            new_muted = contrast('#a0a09c', '#253749')
            receipt['contrast'] = dict(old_title=old, old_muted=muted, proposed_title=new, proposed_muted=new_muted)
            calculation = f'<p class="measurement">指定颜色计算：原标题 {old:.2f}:1，原说明 {muted:.2f}:1；建议配色 {new:.2f}:1 / {new_muted:.2f}:1。非浏览器实测。</p>'
        rows = ''.join(f'<div><dt>{label}</dt><dd>{e(f[key])}</dd></div>' for label, key in [
            ('实际影响', 'impact'), ('建议怎么改', 'change'), ('为什么这样改', 'principle'), ('如何验收', 'test')])
        cards.append(f'''<article id="{f['id']}" data-group="{f['group']}" data-kind="{f['kind']}">
<div class="eyebrow">{f['group']} <span>／ {f['kind']}</span></div>
<h2><a href="#{f['id']}">{f['title']}</a></h2><p class="lead">{f['summary']}</p>
{examples(f['id'])}{calculation}
<details><summary>依据、改法与理由</summary><div class="details-body">
<p class="fact">{e(f['fact'])}</p><dl>{rows}</dl><p class="boundary">{e(f['limit'])}</p>
<details class="evidence"><summary>查看代码证据</summary>{''.join(excerpts)}</details>
<p class="reference">{refs}</p></div></details></article>''')
    nav = ''.join(f'<a href="#{f["id"]}">{f["title"]}</a>' for f in FINDINGS)
    page = (HERE / 'template.html').read_text().replace('<!-- FINDINGS -->', '\n'.join(cards)).replace('<!-- NAV -->', nav)
    (HERE / 'index.html').write_text(page)
    (HERE / 'source-receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    print(f'Built {HERE / "index.html"}')


if __name__ == '__main__':
    main()

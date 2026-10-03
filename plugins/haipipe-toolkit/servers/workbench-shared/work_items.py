"""Paper's Work disclosure grammar, reused by family-owned presenters.

Only presentation is shared. Callers supply escaped tags/tree markup; this
module does not read files, bind Questions, count Runs or allocate execution.
"""
from html import escape


def work_item(label, name, explanation, tags_html, folders_html, *, key="", for_keys="", element_id=""):
    """A labeled short name, one explanation, context tags, then a folder fold."""
    attrs = (' id="' + escape(element_id, quote=True) + '"') if element_id else ''
    return ('<details class="lw-w" data-key="%s" data-for="%s"%s>'
            '<summary><span class="bjt-chev">›</span><div class="lw-sum">'
            '<div class="lw-wline"><span class="item-kind">%s</span><span class="lw-wq">%s</span></div>%s'
            '<div class="lw-tags">%s</div></div></summary><div class="lw-folders">%s</div></details>'
            % (escape(key, quote=True), escape(for_keys, quote=True), attrs,
               escape(label), escape(name),
               ('<div class="lw-wtext">%s</div>' % escape(explanation)) if explanation else '',
               tags_html, folders_html))


# Extracted from Paper's existing stylesheet; keep both families on this grammar.
WORK_ITEM_CSS = """
.lw-w{padding:6px 8px;margin:0 -8px 6px;border-radius:8px} .lw-w>summary:hover .lw-wq{color:var(--acc)}
.lw-w>summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:1em minmax(0,1fr);gap:4px;align-items:baseline}
.lw-w>summary::-webkit-details-marker{display:none} .lw-w[open]>summary .bjt-chev{transform:rotate(90deg)}
.lw-sum{min-width:0} .lw-folders{margin:4px 0 2px 1.3em}
.lw-wline{display:grid;grid-template-columns:auto minmax(0,1fr);gap:8px;align-items:baseline} .lw-wq{font-weight:600;font-size:14.5px}
.lw-wtext{font-size:14px;margin-top:2px}
.lw-tags{display:flex;gap:4px 12px;flex-wrap:wrap;margin:3px 0 0} .lw-for{color:var(--acc);font-size:12.5px;font-weight:600}
.lw-also,.lw-size{color:var(--mut);font-size:12.5px}

.bj-home,.bj-none{font-size:12.5px}
.bj-b,.bj-j,.bj-t{font-size:14px;line-height:1.55;display:flex;gap:6px;flex-wrap:wrap;align-items:baseline}
.bj-j{margin-left:16px} .bj-t{margin-left:32px}
.bj-tr>summary{list-style:none;cursor:pointer} .bj-tr>summary::-webkit-details-marker{display:none}
.bj-rs{color:var(--mut);font-size:12.5px} .bj-rs::before{content:"▸ "} .bj-tr[open]>summary .bj-rs::before{content:"▾ "}
.bj-rn{font-size:12.5px} .bj-runs{margin-left:48px}
.bj-run{display:block;font-size:12.5px;line-height:1.7;color:inherit;text-decoration:none}
a.bj-run:hover .idtag{color:var(--acc);text-decoration:underline}

.item-kind{color:var(--acc);font:650 12px ui-monospace,Menlo,monospace;border:1px solid var(--acc);border-radius:999px;
 padding:1px 8px;white-space:nowrap}
"""

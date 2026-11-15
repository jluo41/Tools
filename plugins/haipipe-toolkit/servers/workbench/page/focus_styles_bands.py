"""The focus page's shared CSS and small scripts (bands, Findings, fitted maps, folds, data cards), and the helpers
that build its band sections (band_sec, numbered) and fitted maps (map_html)."""
from __future__ import annotations

from pathlib import Path

from live import frame
from live.ui_parts import PB_CSS, word_span


DC_CSS = ('<style>.dc-table{margin:0 0 14px}.dc-name{margin:0 0 2px;overflow-wrap:anywhere}.dc-name code,.dc-cols code{font-size:12px}'
          '.dc-meta{margin:0 0 6px;color:var(--muted);font-size:13px}.dc-cols{margin:0;line-height:1.9}'
          '.dc-cols code{background:var(--wash,#f6f6f7);border-radius:4px;padding:1px 5px}'
          '.dc-tag{display:inline-block;font-size:11px;padding:0 6px;margin-right:4px;border-radius:9px;border:1px solid var(--line);color:var(--muted)}'
          '.dc-tag.out{border-color:var(--accent);color:var(--accent)}.wk-runs details.dc-fold{margin:2px 0 6px 22px;font-size:13px}'
          '.wk-runs details.dc-fold>summary{color:var(--muted);cursor:pointer}</style>')


                                                                      # and Work (round 2: "not run" beside "waiting")
# every mark has its word (page rules); a receipt says complete, completed or ok for a finished Run (261105: a
# finished Run read "⬜" when its receipt said completed)
FOLD_CSS = """<style>
.fold-tree,.fold-tree ul{list-style:none;margin:0;padding:0}.fold-tree ul{margin-left:9px;padding-left:16px;border-left:1px solid var(--line,#ddd)}
.fold-tree li{position:relative;padding:2px 0}.fold-tree ul>li::before{content:"";position:absolute;left:-16px;top:13px;width:12px;border-top:1px solid var(--line,#ddd)}
.fold-tree summary{list-style:none;cursor:pointer}.fold-tree summary::-webkit-details-marker{display:none}
.fold-tree summary::before{content:"▸";flex:none;width:10px;color:var(--muted,#888);font-size:10px}.fold-tree details[open]>summary::before{content:"▾"}
.fold-row{display:flex;gap:10px;align-items:baseline;min-width:0}.fold-row.leaf{padding-left:10px}
.fold-row a{flex:none;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px;text-decoration:none}.fold-row a:hover{text-decoration:underline}
.fold-row b.fam{flex:none;font-size:13px}.fold-tree .fold-out{padding:4px 0 6px 10px}.fold-tree .fold-out::before{display:none}.fold-row .st{flex:none;font-size:12px;color:var(--muted,#888)}
.fold-row small{flex:1;min-width:0;color:var(--muted,#888);font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
@media (max-width:640px){.fold-row{flex-wrap:wrap;gap:2px 8px}.fold-row small{flex-basis:100%;white-space:normal}}
</style>"""


# A Block's, Job's or Task's map, and a map framed in a side tab, fit their box (round 3): the root's column and a card's
# column shrink to what is left, a leaf wraps in its column, and at phone width a card's leaves hang under it (the
# tree stays: the root on the left, each card wired to it; JL 261031 "the mindmap tree for all the time")
FIT_MAP = ('.focus-map.fit-map{overflow-x:hidden;cursor:auto}'
           '.focus-map.fit-map .pm.pm-folds,.focus-map.fit-map .pm{width:auto;min-width:0;'
           'grid-template-columns:minmax(110px,190px) minmax(0,1fr)!important;gap:0 34px!important}'
           '.focus-map.fit-map .pm .pm-para{grid-template-columns:minmax(150px,230px) minmax(0,1fr)!important;gap:0 30px!important;margin:2px 0}'
           '.focus-map.fit-map .pm .pm-leaves,.focus-map.fit-map .pm .pm-leaves li{white-space:normal!important;max-width:none!important;'
           'overflow-wrap:break-word}'
           '.focus-map.fit-map .pm .pm-root b{font-size:15px;overflow-wrap:normal;word-break:normal}'
           '.focus-map.fit-map .pm .pm-q{width:auto}'
           '@media(max-width:600px){.focus-map.fit-map .pm.pm-folds,.focus-map.fit-map .pm{grid-template-columns:92px minmax(0,1fr)!important;'
           'gap:0 12px!important}.focus-map.fit-map .pm .pm-para{display:block!important;margin:4px 0}'
           '.focus-map.fit-map .pm .pm-leaves{padding:4px 0 6px 18px}.focus-map.fit-map .pm-root{padding:9px 10px}'
           '.focus-map.fit-map .pm .pm-root b{font-size:13.5px}.focus-map.fit-map .pm-pnode{font-size:13px;padding:7px 9px}}')


# a map framed in a side tab scrolls sideways instead of wrapping its names (JL 261109)
FRAMED_SCROLL = ('.focus-map.fit-map.framed{overflow-x:auto}'
                 '.focus-map.fit-map.framed .pm,.focus-map.fit-map.framed .pm.pm-folds{width:max-content!important;'
                 'grid-template-columns:190px max-content!important}'
                 '.focus-map.fit-map.framed .pm .pm-para{grid-template-columns:230px max-content!important}'
                 '.focus-map.fit-map.framed .pm .pm-leaves,.focus-map.fit-map.framed .pm .pm-leaves li{white-space:nowrap!important;'
                 'overflow-wrap:normal!important}')


# at phone width the tree keeps to the screen: a narrow root, a narrow first column, leaves that wrap; an opened branch
# still slides sideways (261031: "I want to have the mindmap tree for all the time"; round 2: clipped at 390 px)
MAP_PHONE = ('@media(max-width:600px){.focus-map .pm,.focus-map .pm-folds{grid-template-columns:104px auto!important;gap:0 14px!important}'
             '.focus-map .pm-root{padding:9px 10px}.focus-map .pm-root b{font-size:13.5px!important}'
             '.focus-map .pm-para,.focus-map .pm-folds .pm-para{grid-template-columns:150px auto!important;gap:0 14px!important}'
             '.focus-map .pm-q{width:150px}.focus-map .pm-pnode{font-size:13px;padding:7px 9px}'
             '.focus-map .pm-leaves li{white-space:normal!important;max-width:220px!important}}')


def map_html(html: str, folder: Path, root: Path) -> str:
    """A drawn map as a page shows it: its node ids from the served root, never the machine's own folders (round 2:
    the map's HTML carried an absolute path); the root's name breaks only at its underscores."""
    top = str(Path(root).resolve())
    html = html.replace(frame.esc("@" + top + "/"), "@").replace("@" + top + "/", "@")
    name = frame.esc(folder.name)
    return html.replace(f'<div class="pm-node pm-root"><b>{name}</b>',
                        f'<div class="pm-node pm-root"><b>{name.replace("_", "_<wbr>")}</b>', 1)


STAGE_MARK = {"explore": "⬜", "shaping": "⏳", "agreed": "✅", "closed": "✅"}


BAND_CSS = """<style>
.band-sec{margin:0 0 8px}
.band-sec>summary{display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;list-style:none;cursor:pointer;font-size:15px;font-weight:600;
 border:1px solid var(--line);border-radius:8px;background:var(--paper);padding:8px 14px}
.band-sec>summary::-webkit-details-marker{display:none}
.band-sec>summary::before{content:"▸";flex:none;width:12px;color:var(--muted);font-size:12px}.band-sec[open]>summary::before{content:"▾"}
.band-sec>summary:hover{color:var(--accent)}
.band-sec .bar{flex:0 0 120px;height:5px;border-radius:3px;background:var(--wash);overflow:hidden}
.band-sec .bar i{display:block;height:100%;background:#2b8a3e}.band-sec .bar i.part{background:#e8590c}
.band-sec .word,.job-row small{flex:none;margin-left:auto;font-size:12px;font-weight:400;color:var(--muted);text-align:right}
.band-sec .word.you{color:light-dark(#b35c00,#ffc078);font-weight:600}
.band-wait{margin:-4px 0 10px 30px;font-size:13px;line-height:1.4;color:light-dark(#b35c00,#ffc078)}.band-sec[open]+.band-wait{display:none}
.band-jobs{padding:6px 0 4px 14px}
.job-row{border-bottom:1px solid var(--line)}.job-row:last-child{border-bottom:0}
.job-row>summary{display:flex;align-items:center;gap:8px;list-style:none;cursor:pointer;padding:7px 15px 7px 2px;font-size:14px}
.job-row>summary::-webkit-details-marker{display:none}
.job-row>summary::before{content:"▸";flex:none;width:12px;color:var(--muted);font-size:11px}.job-row[open]>summary::before{content:"▾"}
.job-row .jn{flex:none;font-size:12px;color:var(--muted)}.job-row b{font-weight:600;overflow-wrap:anywhere}
.job-row .bar{flex:0 0 120px;height:5px;border-radius:3px;background:var(--wash);overflow:hidden}
.job-row .bar i{display:block;height:100%;background:#2b8a3e}.job-row .bar i.part{background:#e8590c}
.job-tree{padding:0 0 8px 20px}
@media (max-width:600px){.band-sec .bar{flex-basis:56px}.job-row>summary{flex-wrap:wrap;padding-right:6px}.topic-row{padding-right:6px!important}.job-row .bar{display:none}.job-row>summary>a,.job-row>summary>b,.topic-row>a{flex:1 1 0;min-width:0}.job-row small{white-space:nowrap}.band-sec>summary{flex-wrap:nowrap}.band-sec .word{white-space:nowrap}.band-sec .bar{display:none}.band-jobs{padding-left:4px}.topic-row{padding-left:8px!important}}
.band-sec .bt{flex:0 1 auto;min-width:0;overflow-wrap:anywhere}
</style>"""


def band_sec(n: int, title: str, word: str, body: str, waits: str = "", cls: str = "", share: int | None = None,
             opened: bool = False, sid: str = "", src: str = "") -> str:
    """One closed numbered section of a work page: its bar (`N · title`, its state word on the right), its content; the
    one thing that waits on the person under the closed bar, outside the fold, hidden once it is opened (JL 261106:
    "a section that waits on you also shows that one item under its closed bar"). `src="ix"` tags a 🙋 N that only
    rolls up collection Runs, so the page's tray counts those rows once."""
    bar = (f'<span class=bar><i class="{"part" if share < 100 else ""}" style="width:{share}%"></i></span>'
           if share is not None else "")
    return (f'<details class={chr(34) + "band-sec " + cls + chr(34) if cls else "band-sec"}{f" id={sid}" if sid else ""}{" open" if opened else ""}><summary><span class=bt>{n} · {title}</span>{word_span(word, src)}{bar}</summary>'
            f'<div class=band-jobs>{body}</div></details>' + (f'<p class=band-wait>{frame.esc(waits)}</p>' if waits else ""))


FINDINGS_CSS = """<style>
.find-q{padding:10px 2px;border-bottom:1px solid var(--line)}.find-q:last-child{border-bottom:0}
.find-h{display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;font-size:14px}.find-h b{font-weight:600;overflow-wrap:anywhere}
.find-h .find-open{margin-left:auto;font-size:12px}
.find-pill{flex:none;font-size:12px;border:1px solid var(--line);border-radius:6px;padding:1px 8px;background:var(--wash);color:var(--muted);white-space:nowrap}
.find-pill.agreed{border-color:#2b8a3e;color:#2b8a3e}.find-pill.proposed{border-color:#e8590c;color:#c2410c}
.find-ask{margin:6px 0 0;font-size:13px;color:var(--muted)}.find-sub{margin:12px 0 0;font-size:13px;font-weight:600}.find-verbs{margin:0 0 10px}
.find-map{display:block;width:100%;height:220px;border:1px solid var(--line);border-radius:8px}
.find-a{margin:6px 0 0;font-size:14px;line-height:1.5}
.find-r{margin:6px 0 0;padding:0 0 0 18px;font-size:13px;line-height:1.5}.find-r li{margin:3px 0}.find-r small{color:var(--muted)}
.find-more{margin-top:4px;font-size:13px}.find-more>summary{cursor:pointer;color:var(--muted)}
.wk-rows{list-style:none;margin:0;padding:0;font-size:14px}.wk-rows li{display:flex;flex-wrap:wrap;gap:4px 10px;padding:6px 2px;border-bottom:1px solid var(--line)}
.wk-rows li:last-child{border-bottom:0}.wk-rows small{margin-left:auto;font-size:12px;color:var(--muted)}
.wk-band{display:flex;align-items:center;gap:12px;margin:22px 0 10px;font-size:17px;font-weight:600}.wk-band:first-child{margin-top:6px}
.wk-band::after{content:"";flex:1;border-top:1px solid var(--line)}
.fd-row{display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid var(--line);font-size:14px}
.fd-row .n{min-width:150px;font-weight:500;overflow-wrap:anywhere}.fd-row .d{flex:1;min-width:0;color:var(--muted);font-size:13px;overflow-wrap:anywhere}
.wk-scroll{overflow-x:auto;margin:4px 0 6px}.wk-table{border-collapse:collapse;font-size:13px}
.wk-table th,.wk-table td{padding:4px 14px 4px 0;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}
.wk-table th{font-weight:600;color:var(--muted);font-size:12px}
.pb-panel table.wk-table{display:table;width:auto}.pb-panel .wk-table thead{display:table-header-group}
.pb-panel .wk-table tbody{display:table-row-group}.pb-panel .wk-table tr{display:table-row}
.pb-panel .wk-table td,.pb-panel .wk-table th{display:table-cell;width:auto}
.wk-rows .st{flex:none;min-width:84px;font-size:12px;color:var(--muted)}.wk-rows .hl{flex:1 1 220px;min-width:0;font-size:13px}
.wk-runs a{font-size:13.5px}.wk-runs .st{min-width:124px}.wk-rows .mk{flex:none}
.wk-rows .row-verb,.wk-rows .pb-copy1{flex:none;margin-left:8px;font-size:12.5px;padding:1px 10px}.wk-rows small+.row-verb{margin-left:10px}
.job-row .hl{flex:1 1 auto;min-width:0;font-size:13px;color:var(--ink);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.job-row .ix-answer,.wk-rows .ix-answer{flex:none;font-size:12px;padding:1px 9px;border-color:light-dark(#ffa94d,#b35c00);color:light-dark(#b35c00,#ffc078)}
.job-row b,.job-row .hl{overflow-wrap:break-word;word-break:normal}
.st-lead{margin:0 0 12px;font-size:16px;line-height:1.5}.st-lead b{font-weight:600}
.vt-now-runs a{color:var(--accent);text-decoration:underline}
@media(max-width:600px){.job-row .hl{white-space:normal;flex-basis:100%;order:5}
 /* a table keeps its columns and their names at phone width, in its own box that scrolls sideways (round 3: stacked
    rows lost the column labels and the page slid to 565 px) */
 .pb-panel table.vt-t,.pb-panel table.wk-table{display:table!important;width:auto}
 .pb-panel .vt-t thead,.pb-panel .wk-table thead{display:table-header-group!important}
 .pb-panel .vt-t tbody,.pb-panel .wk-table tbody{display:table-row-group!important}
 .pb-panel .vt-t tr,.pb-panel .wk-table tr{display:table-row!important;padding:0}
 .pb-panel .vt-t td,.pb-panel .vt-t th,.pb-panel .wk-table td,.pb-panel .wk-table th{display:table-cell!important;width:auto;min-width:0}
 .pb-panel .vt-t td,.pb-panel .vt-t th{border:1px solid var(--line)!important;padding:4px 6px!important}
 .pb-panel .wk-table td,.pb-panel .wk-table th{padding:4px 12px 4px 0!important;border-bottom:1px solid var(--line)!important}
 .wk-scroll,.vt-scroll{max-width:100%;overflow-x:auto}}
</style>"""


# A design section's website loads when its tab first shows; its drawing fits the panel's width.
DESIGN_JS = ("<style>.find-drawing{display:block;max-width:100%;height:auto;border:1px solid var(--line,#ddd);border-radius:6px}</style>"
             "<script>(function(){document.querySelectorAll('.find-design').forEach(function(w){var s=w.closest('details');"
             "function load(){if(s&&!s.open)return;w.querySelectorAll('.pb-panel:not([hidden]) iframe[data-src]:not([src])')"
             ".forEach(function(f){f.src=f.dataset.src})}"
             "if(s)s.addEventListener('toggle',load);w.addEventListener('click',function(){setTimeout(load)});load()})})()</script>")


# A framed map as tall as its map: measured from the map itself (never the frame's own height, which would grow it
# without end), again whenever a card in it opens or closes.
FIT_FRAME_JS = ("<script>window.fitMap=window.fitMap||function(f){try{var d=f.contentDocument,m=d&&d.querySelector('.focus-map');"
                "if(!m)return;var fit=function(){var h=Math.ceil(m.getBoundingClientRect().bottom+(d.defaultView.scrollY||0))+12;"
                "if(Math.abs(h-f.offsetHeight)>3)f.style.height=Math.max(140,h)+'px';};fit();setTimeout(fit,120);"
                "if(window.ResizeObserver)new ResizeObserver(fit).observe(m);}catch(e){}};"
                "document.querySelectorAll('iframe.find-map').forEach(function(f){if(f.contentDocument&&f.contentDocument.readyState==='complete')fitMap(f);});</script>")


def numbered(secs: list, first: int = 1) -> str:
    """Numbered closed bars from [(title, word, body, waits[, share])]; a title is HTML already."""
    return "".join(band_sec(n, s[0], s[1], s[2], s[3] if len(s) > 3 else "", share=s[4] if len(s) > 4 else None,
                            sid=s[5] if len(s) > 5 else "")
                   for n, s in enumerate(secs, first))


# a link to a page's #find-<part> opens that closed section and brings it into view (the Project's Findings rows)
OPEN_HASH_JS = ("<script>(function(){var d=location.hash&&document.getElementById(location.hash.slice(1));"
                "if(d&&d.tagName==='DETAILS'){d.open=true;d.scrollIntoView()}})()</script>")


def side_css() -> str:
    try:
        from live.board_views import SIDE_CSS
    except Exception:
        SIDE_CSS = ""
    return BAND_CSS + FINDINGS_CSS + PB_CSS + SIDE_CSS


RAIL_IX_CSS = ('<style>.ix-rail>.fd-h{display:flex;align-items:center;gap:8px;font-size:16px;margin:0 0 8px}'
               '.ix-rail>.fd-wait{margin:0 0 12px}.ix-addr{font-size:11px;color:var(--muted)}</style>')

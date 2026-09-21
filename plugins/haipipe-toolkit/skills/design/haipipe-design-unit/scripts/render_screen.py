#!/usr/bin/env python3
"""Render one UI Design Unit inside its current Result and measure it. Never judges.

    python3 render_screen.py --result-dir <result> --html <result>/content/screen.html --png <result>/render/screen-v2.png
    python3 render_screen.py --result-dir <result> --html … --png … --manifest <result>/render/manifest.json \
                             --item ITEM03 --candidate rd26_generate_item03 --version 2

A `visual` criterion is an observation method, so this script reports what a
headless browser sees. It writes only render evidence in the specified Result;
the worker reads the numbers and picture, then writes its own checks. Reported:
its height against the viewport, how far the last block reaches, the number of
buttons and links, the smallest tap target, and the weakest text contrast.

With --manifest it appends one entry naming the picture, the draft it belongs
to (`candidate`), source/picture hashes and version. Pin the manifest as
`render_manifest` in result.yaml before completing the Result. The presenter
reads it directly; this script never writes a Delivery projection or runtime.
Each picture/version is written once; a changed screen needs a new version.
Requires PyYAML, Playwright's Python package and a local Chrome/Chromium binary;
it uses that binary directly and does not download a browser.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

import yaml

CHROMES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
)

MEASURE = """() => {
  function lum(c){var m=c.match(/[\\d.]+/g).map(Number);
    var s=m.slice(0,3).map(function(v){v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)});
    return 0.2126*s[0]+0.7152*s[1]+0.0722*s[2]}
  function ratio(a,b){var x=lum(a),y=lum(b);return Math.round(((Math.max(x,y)+0.05)/(Math.min(x,y)+0.05))*100)/100}
  function bg(el){while(el){var c=getComputedStyle(el).backgroundColor;
    if(c&&c!=='rgba(0, 0, 0, 0)'&&c!=='transparent')return c;el=el.parentElement}return 'rgb(255, 255, 255)'}
  var taps=[].slice.call(document.querySelectorAll('button,a,input,select,textarea'));
  var last=document.body.lastElementChild, seen=null;
  [].slice.call(document.body.children).forEach(function(e){if(e.tagName!=='SCRIPT')seen=e});
  var out={
    page_height: document.documentElement.scrollHeight,
    page_width: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth),
    viewport_width: window.innerWidth,
    viewport_height: window.innerHeight,
    pixel_ratio: window.devicePixelRatio,
    leftmost_edge: Math.min(0, ...Array.from(document.body.querySelectorAll('*'), e => e.getBoundingClientRect().left)),
    body_box: Math.round(document.body.getBoundingClientRect().height),
    last_block_bottom: seen ? Math.round(seen.getBoundingClientRect().bottom) : 0,
    buttons: document.querySelectorAll('button').length,
    links: document.querySelectorAll('a').length,
    scripts: document.querySelectorAll('script').length,
    smallest_tap: taps.length ? Math.min.apply(null, taps.map(function(e){
      return Math.round(e.getBoundingClientRect().height)})) : null,
    taps: taps.map(function(e){return e.tagName.toLowerCase()+':'+Math.round(e.getBoundingClientRect().height)}).join(' '),
    button_label_contrast: (function(){var b=document.querySelector('button');
      return b ? ratio(getComputedStyle(b).color, bg(b)) : null})(),
    weakest_text_contrast: (function(){var worst=99;
      [].slice.call(document.querySelectorAll('p,h1,h2,h3,h4,li,span,div,b,strong,s,em,i,small,td,th,a,button,label,header,footer,main,section')).forEach(function(e){
        var own=Array.prototype.some.call(e.childNodes,function(n){return n.nodeType===3&&n.textContent.trim()});
        if(!own)return;
        var r=ratio(getComputedStyle(e).color,bg(e)); if(r<worst)worst=r});
      // A form control shows text through its value, its chosen option, or its
      // placeholder, never through a child text node, so the sweep above walks
      // straight past it (found on ITEM10, 260920: three <select> date controls).
      [].slice.call(document.querySelectorAll('input,select,textarea')).forEach(function(e){
        var shown=e.value||'';
        if(e.tagName==='SELECT'&&e.selectedIndex>=0)shown=e.options[e.selectedIndex].text;
        if(!shown.trim())shown=e.getAttribute('placeholder')||'';
        if(!shown.trim())return;
        var r=ratio(getComputedStyle(e).color,bg(e)); if(r<worst)worst=r});
      return worst===99?null:worst})(),
    // Every field's own edge against what it sits on: the Brief asks 3:1, and a
    // border too faint to see is a field a patient does not know to fill in.
    weakest_control_border: (function(){var worst=99;
      [].slice.call(document.querySelectorAll('input,select,textarea')).forEach(function(e){
        var s=getComputedStyle(e);
        if(s.borderTopStyle==='none'||parseFloat(s.borderTopWidth)===0)return;
        var r=ratio(s.borderTopColor,bg(e.parentElement)); if(r<worst)worst=r});
      return worst===99?null:worst})(),
    controls: document.querySelectorAll('input,select,textarea').length
  };
  return out;
}
"""


def chrome() -> str:
    found = os.environ.get("CHROME") or next((c for c in CHROMES if Path(c).is_file() or shutil.which(c)), "")
    if not found:
        sys.exit("no Chrome or Chromium found; set CHROME=<path to the browser>")
    return str(Path(found).resolve()) if Path(found).is_file() else shutil.which(found) or found


def render(html: Path, png: Path, width: int, height: int, scale: int) -> dict:
    """Measure and capture the same emulated viewport, including horizontal overflow."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("render_screen.py requires the playwright Python package and a local Chrome")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=chrome(), headless=True)
        try:
            context = browser.new_context(viewport={"width": width, "height": height},
                                          device_scale_factor=scale, java_script_enabled=False,
                                          offline=True)
            page = context.new_page()
            page.goto(html.resolve().as_uri(), wait_until="load", timeout=30000)
            page.evaluate("() => document.fonts.ready.then(() => true)")
            measured = page.evaluate(MEASURE)
            if (measured["viewport_width"], measured["viewport_height"], measured["pixel_ratio"]) != (width, height, scale):
                sys.exit("browser viewport differs from the requested viewport; no picture accepted")
            png.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(png), full_page=False, animations="disabled", timeout=30000)
            context.close()
        finally:
            browser.close()
    measured["viewport"] = f"{measured['viewport_width']}x{measured['viewport_height']}"
    measured["scale"] = measured["pixel_ratio"]
    measured["fits_one_screen"] = (measured["page_height"] <= height
                                   and measured["last_block_bottom"] <= height
                                   and measured["page_width"] <= width
                                   and measured["leftmost_edge"] >= 0)
    return measured


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output_paths(args):
    """Check every persistent write before starting Chrome or creating files."""
    result = args.result_dir.resolve()
    runtime = result / "runtime.yaml"
    state = yaml.safe_load(runtime.read_text(encoding="utf-8")) if runtime.is_file() else {}
    if isinstance(state, dict) and state.get("status") in {"complete", "failed", "blocked", "superseded"}:
        sys.exit("cannot render into a closed Result; use the current Run's Result")
    for path in (args.png, args.manifest, args.json):
        if path is None:
            continue
        resolved = path.resolve()
        if result / "render" not in resolved.parents or resolved == args.html.resolve():
            sys.exit("render outputs must stay inside the current Result's render/ directory")
    outputs = [p.resolve() for p in (args.png, args.manifest, args.json) if p is not None]
    if len(outputs) != len(set(outputs)):
        sys.exit("picture, manifest and measurements need distinct paths")
    if args.manifest and args.manifest.parent.resolve() not in args.png.resolve().parents:
        sys.exit("picture must be inside the render manifest's directory")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--result-dir", type=Path, required=True, help="the current writable Run Result")
    ap.add_argument("--html", type=Path, required=True, help="the screen to render (a Design Unit artifact)")
    ap.add_argument("--png", type=Path, required=True, help="where to write the picture; never overwritten")
    ap.add_argument("--width", type=int, default=390)
    ap.add_argument("--height", type=int, default=844)
    ap.add_argument("--scale", type=int, default=2, help="device pixel ratio of the picture")
    ap.add_argument("--json", type=Path, help="also write the measurements here")
    ap.add_argument("--manifest", type=Path, help="Result-local render/manifest.json; pin it in result.yaml")
    ap.add_argument("--item", help="Design Item id, required with --manifest")
    ap.add_argument("--candidate", help="the Generate run this picture belongs to, required with --manifest")
    ap.add_argument("--version", type=int, help="picture version, required with --manifest")
    args = ap.parse_args()

    if min(args.width, args.height, args.scale) <= 0:
        sys.exit("width, height and scale must be positive")
    output_paths(args)
    if not args.html.is_file():
        sys.exit(f"no screen at {args.html}")
    if args.png.exists():
        sys.exit(f"{args.png} exists; a changed screen needs a new picture version")
    if args.json and args.json.exists():
        sys.exit(f"{args.json} exists; use a new measurements file for each picture version")
    if args.manifest and not (args.item and args.candidate and args.version and args.version > 0):
        sys.exit("--manifest needs --item, --candidate and a positive --version")
    entries = []
    if args.manifest:
        entries = json.loads(args.manifest.read_text()) if args.manifest.is_file() else []
        if not isinstance(entries, list) or any(not isinstance(e, dict) for e in entries):
            sys.exit("render manifest must be a list of entries")
        source = os.path.relpath(args.html.resolve(), args.manifest.parent.resolve())
        if any(e.get("candidate") == args.candidate and e.get("source") == source
               and e.get("version") == args.version for e in entries):
            sys.exit("render source/version already exists; use a new version")

    measured = render(args.html, args.png, args.width, args.height, args.scale)
    report = {"screen": str(args.html), "sha256": sha(args.html), "picture": str(args.png),
              "render_sha256": sha(args.png), **measured}

    if args.manifest:
        entries.append({"item": args.item, "render": os.path.relpath(args.png.resolve(), args.manifest.parent.resolve()),
                        "candidate": args.candidate, "source": source,
                        "sha256": report["sha256"], "version": args.version,
                        "render_sha256": report["render_sha256"],
                        "viewport": report["viewport"], "scale": args.scale,
                        "measured": {k: measured[k] for k in
                                     ("page_height", "page_width", "viewport_width", "viewport_height",
                                      "leftmost_edge", "last_block_bottom", "buttons", "links", "controls",
                                      "smallest_tap", "weakest_text_contrast", "weakest_control_border",
                                      "button_label_contrast", "fits_one_screen")}})
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
        report["manifest"] = str(args.manifest)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

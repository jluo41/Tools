#!/usr/bin/env python3
"""Render one UI Design Unit (an HTML screen) to a picture and measure it. Never judges, never adopts.

    python3 render_screen.py --html content/screen.html --png delivery/render/<stem>-ITEM03-v2.png
    python3 render_screen.py --html … --png … --manifest delivery/render/manifest.json \
                             --item ITEM03 --candidate rd26_generate_item03 --version 2

A `visual` criterion is an observation method, so this script reports what a
headless browser sees and writes nothing into a Result: the worker reads the
numbers and the picture, then writes its own checks.  Reported for the screen:
its height against the viewport, how far the last block reaches, the number of
buttons and links, the smallest tap target, and the weakest text contrast.

With --manifest it appends one entry naming the picture, the draft it belongs
to (`candidate`) and its version, which is what the Design plugin reads to show
a screen as its picture.  A picture is written once per version; a changed
screen is a new version, never an overwrite.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHROMES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
)

MEASURE = """
<script>
(function(){
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
    page_width: document.body.getBoundingClientRect().width,
    body_box: Math.round(document.body.getBoundingClientRect().height),
    last_block_bottom: seen ? Math.round(seen.getBoundingClientRect().bottom) : 0,
    buttons: document.querySelectorAll('button').length,
    links: document.querySelectorAll('a').length,
    scripts: document.querySelectorAll('script').length - 1,
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
  document.title='MEASURE'+JSON.stringify(out);
})();
</script>
"""


def chrome() -> str:
    found = os.environ.get("CHROME") or next((c for c in CHROMES if Path(c).is_file() or shutil.which(c)), "")
    if not found:
        sys.exit("no Chrome or Chromium found; set CHROME=<path to the browser>")
    return found


def run(browser: str, size: str, args: list[str]) -> str:
    done = subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-first-run",
                           "--no-default-browser-check", "--hide-scrollbars",
                           f"--window-size={size}", *args],
                          capture_output=True, text=True, timeout=180)
    return done.stdout


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--html", type=Path, required=True, help="the screen to render (a Design Unit artifact)")
    ap.add_argument("--png", type=Path, required=True, help="where to write the picture; never overwritten")
    ap.add_argument("--width", type=int, default=390)
    ap.add_argument("--height", type=int, default=844)
    ap.add_argument("--scale", type=int, default=2, help="device pixel ratio of the picture")
    ap.add_argument("--json", type=Path, help="also write the measurements here")
    ap.add_argument("--manifest", type=Path, help="delivery/render/manifest.json to append an entry to")
    ap.add_argument("--item", help="Design Item id, required with --manifest")
    ap.add_argument("--candidate", help="the Generate run this picture belongs to, required with --manifest")
    ap.add_argument("--version", type=int, help="picture version, required with --manifest")
    ap.add_argument("--force", action="store_true", help="allow replacing an existing picture")
    args = ap.parse_args()

    if not args.html.is_file():
        sys.exit(f"no screen at {args.html}")
    if args.png.exists() and not args.force:
        sys.exit(f"{args.png} exists; a changed screen is a new version, not an overwrite (--force to replace)")
    if args.manifest and not (args.item and args.candidate and args.version):
        sys.exit("--manifest needs --item, --candidate and --version")

    browser = chrome()
    size = f"{args.width},{args.height}"
    args.png.parent.mkdir(parents=True, exist_ok=True)
    run(browser, size, [f"--screenshot={args.png}", f"--force-device-scale-factor={args.scale}",
                        args.html.resolve().as_uri()])
    if not args.png.is_file():
        sys.exit("the browser wrote no picture")

    with tempfile.TemporaryDirectory() as td:
        probe = Path(td) / args.html.name
        probe.write_text(args.html.read_text(encoding="utf-8").replace("</body>", MEASURE + "</body>"),
                         encoding="utf-8")
        dom = run(browser, size, ["--dump-dom", "--virtual-time-budget=2000", probe.resolve().as_uri()])
    hit = re.search(r"MEASURE(\{.*?\})</title>", dom, re.S)
    if not hit:
        sys.exit("the browser returned no measurements")
    measured = json.loads(hit.group(1))
    measured["viewport"] = f"{args.width}x{args.height}"
    measured["scale"] = args.scale
    measured["fits_one_screen"] = (measured["page_height"] <= args.height
                                   and measured["last_block_bottom"] <= args.height)
    report = {"screen": str(args.html), "sha256": sha(args.html), "picture": str(args.png),
              "render_sha256": sha(args.png), **measured}

    if args.manifest:
        entries = json.loads(args.manifest.read_text()) if args.manifest.is_file() else []
        entries = [e for e in entries if not (e.get("item") == args.item and e.get("version") == args.version)]
        entries.append({"item": args.item, "render": args.png.name, "candidate": args.candidate,
                        "sha256": report["sha256"], "version": args.version,
                        "render_sha256": report["render_sha256"],
                        "viewport": report["viewport"], "scale": args.scale,
                        "measured": {k: measured[k] for k in
                                     ("page_height", "last_block_bottom", "buttons", "links", "controls",
                                      "smallest_tap", "weakest_text_contrast", "weakest_control_border",
                                      "button_label_contrast", "fits_one_screen")}})
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
        report["manifest"] = str(args.manifest)
    if args.json:
        args.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

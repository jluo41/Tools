"""Render an .excalidraw file with real Excalidraw (exportToSvg) in headless Chrome, crop to content.

    python render_excalidraw.py <in.excalidraw> <out.html> <out.png> [--frame first|<frame name>]

--frame renders one frame only (the frame and the elements inside it). A report drawing's `.png`
is its preview in the workbench's Report column, so render the first frame, the one whose headline
is the answer: frames side by side shrink to an unreadable strip. The full drawing still opens in
the Excalidraw viewer.
"""
import json
import subprocess
import sys

from PIL import Image

args = [a for a in sys.argv[1:] if not a.startswith("--")]
if "--frame" in sys.argv:
    args.remove(sys.argv[sys.argv.index("--frame") + 1])
src, html_path, png = args[0], args[1], args[2]
data = json.load(open(src))
if "--frame" in sys.argv:
    want = sys.argv[sys.argv.index("--frame") + 1]
    frames = [e for e in data["elements"] if e.get("type") == "frame"]
    pick = frames[0] if want == "first" else next(f for f in frames if f.get("name") == want)
    data["elements"] = [e for e in data["elements"] if e["id"] == pick["id"] or e.get("frameId") == pick["id"]]
W = int(max(e["x"] + e["width"] for e in data["elements"]) + 80)
H = int(max(e["y"] + e["height"] for e in data["elements"]) + 80)
open(html_path, "w").write("""<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;background:#fff}</style></head><body>
<script type="module">
window.EXCALIDRAW_ASSET_PATH = "https://esm.sh/@excalidraw/excalidraw@0.18.0/dist/prod/";
const data = %s;
const mod = await import("https://esm.sh/@excalidraw/excalidraw@0.18.0?bundle-deps");
const svg = await mod.exportToSvg({elements: data.elements, appState: {...data.appState, exportBackground: true, viewBackgroundColor: "#ffffff"}, files: data.files || {}});
const vb = svg.viewBox.baseVal;
svg.setAttribute("width", vb.width); svg.setAttribute("height", vb.height);
svg.style.width = vb.width + "px"; svg.style.height = vb.height + "px"; svg.style.display = "block";
document.body.appendChild(svg);
</script></body></html>""" % json.dumps(data))
chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# Chrome cuts a screenshot at about 2**26 pixels, so a very large drawing renders at less than 2x.
scale = round(min(2.0, (60e6 / (W * H)) ** 0.5), 2)
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--force-device-scale-factor={scale}",
                "--virtual-time-budget=40000", f"--window-size={W},{H}", f"--screenshot={png}", "file://" + html_path],
               capture_output=True)
im = Image.open(png).convert("RGB")
bbox = Image.eval(im, lambda v: 255 - v).getbbox()
pad = 20
im.crop((max(0, bbox[0] - pad), max(0, bbox[1] - pad), min(im.width, bbox[2] + pad), min(im.height, bbox[3] + pad))).save(png)
print("rendered", Image.open(png).size)

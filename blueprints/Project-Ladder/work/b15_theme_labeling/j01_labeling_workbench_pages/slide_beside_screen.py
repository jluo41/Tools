"""Each Task view beside the slides it is drawn from, as one picture per view, gathered as the topic's Slides deck
(JL 261101: "this need to be rewrite to follow what we designed in the slides"; the method: the step slide is the
frame, its close-up screens draw the Results, and COVER in task_views.py places every slide box).

    .venv/bin/python slide_beside_screen.py t03_task_page/s58-task-ui-work

Writes <topic>/delivery/deck/<L>-<view>.png (the slides on the left, the view's screen on the right) and
<topic>/<topic>.slides.json (one slide per view, its notes the coverage rows), then runs haipipe-studio's
topic_slides.py, so the topic's Slides button shows them. The deck's pictures are the s03 deck's own renders
(s03-agent-role/delivery/deck/build/v12/slide-N.png, N the file number); nothing here is drawn by hand.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import labeling_ui_cells as cells  # noqa: E402
import task_views as views  # noqa: E402

DECK = HERE.parent / "s03-agent-role" / "delivery" / "deck"
SLIDES = {                       # a view: its step slide first, then its close-ups (file numbers; printed() is the slide's)
    "C1": (8,), "C2": (9, 18), "C3": (10, 16, 17), "C4": (11, 19),
    "D1": (12,), "D2": (12, 22), "D3": (12, 13, 20), "D4": (14,),
    "E1": (15, 21), "E2": (15, 23), "E3": (15,),
}
FONTS = ("/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")


def font(size):
    for f in FONTS:
        if Path(f).is_file():
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def printed(n):
    """The number printed on a slide: the file number, except the round report (file 13) is 12a and later ones shift."""
    return str(n) if n <= 12 else ("12a" if n == 13 else str(n - 1))


def titles():
    """The deck's own slide titles, by file number."""
    deck = json.loads((DECK / "source" / "deck-content-v12.json").read_text())
    return {i: s.get("title", "") for i, s in enumerate(deck["slides"], 1)}


def view_name(key):
    """C3 → ('🧭', 'meaning', 'Preferences')."""
    letter, n = key[0], int(key[1:] or 1)
    _, icon, kind, _, steps = next(t for t in cells.TYPES if t[0] == letter)
    return icon, kind, steps[n - 1]


def compose(key, screen_png, out, title):
    """The slides stacked on the left, each under its number and title; the screen on the right, at its own size."""
    screen = Image.open(screen_png).convert("RGB")
    sw = 800                                                     # each slide 800 × 450
    left = [(n, Image.open(DECK / "build" / "v12" / f"slide-{n}.png").convert("RGB").resize((sw, 450))) for n in SLIDES[key]]
    head, cap, gap = 76, 34, 26
    left_h = sum(cap + 450 + gap for _ in left)
    h = head + max(left_h, screen.height) + 30
    w = 40 + sw + 50 + screen.width + 30
    pic = Image.new("RGB", (w, h), "#ffffff")
    d = ImageDraw.Draw(pic)
    icon, kind, step = view_name(key)
    d.text((40, 22), f"{key} · {kind} · {step}: the slides it is drawn from, and its screen", fill="#1864ab", font=font(30))
    y = head
    for k, (n, img) in enumerate(left):
        role = "step slide" if k == 0 else "close-up"
        d.text((40, y + 4), f"slide {printed(n)} · {role} · {title.get(n, '')}"[:78], fill="#343a40", font=font(20))
        pic.paste(img, (40, y + cap))
        d.rectangle((40, y + cap, 40 + sw - 1, y + cap + 449), outline="#ced4da", width=2)
        y += cap + 450 + gap
    x = 40 + sw + 50
    d.line((x - 25, head, x - 25, h - 20), fill="#e9ecef", width=2)
    pic.paste(screen, (x, head))
    pic.save(out)
    return out


def notes(key, title):
    """What the reader checks: which slide box landed where on the screen."""
    first = SLIDES[key][0]
    rows = [f"Drawn from slide {printed(first)} ({title.get(first, '')})"
            + (f", close-ups {', '.join(printed(n) for n in SLIDES[key][1:])}" if len(SLIDES[key]) > 1 else "") + "."]
    rows += [f"{box} → {place}" for box, place in views.COVER.get(key, [])]
    return "\n".join(rows)


def build(topic: Path):
    topic = topic.resolve()
    title = titles()
    out_dir = topic / "delivery" / "deck"
    out_dir.mkdir(parents=True, exist_ok=True)
    slides = []
    with tempfile.TemporaryDirectory() as tmp:
        for key in SLIDES:
            icon, kind, step = view_name(key)
            png = cells.letter_png(topic, key, Path(tmp) / key)
            name = f"{key}-{step.lower().replace(' ', '-')}.png"
            compose(key, png, out_dir / name, title)
            slides.append({"id": key, "idea": f"{key} · {icon} {kind} · {step}, beside slide {printed(SLIDES[key][0])}",
                           "image": f"delivery/deck/{name}", "notes": notes(key, title)})
    overview = {"id": "00", "idea": f"{topic.name}: every view, drawn", "image": f"{topic.name}.png",
                "notes": "The topic's own drawing first (its card keeps this picture); then each meaning, expression and "
                         "scanning view beside the slides it is drawn from."}
    slides.insert(0, overview)
    spec = {"topic": topic.name,
            "source": "each view's screen (labeling_ui_cells.py, task_views.py) beside the s03 deck's slides it is drawn "
                      "from (version 12, build/v12/slide-N.png); written by j01's slide_beside_screen.py",
            "slides": slides}
    (topic / f"{topic.name}.slides.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n")
    tool = cells.TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/topic_slides.py"
    subprocess.run([sys.executable, str(tool), str(topic)], check=True, stdout=subprocess.DEVNULL)
    return [s["image"] for s in slides]  # the overview first, then one per view


if __name__ == "__main__":
    for p in build(Path(sys.argv[1])):
        print(p)

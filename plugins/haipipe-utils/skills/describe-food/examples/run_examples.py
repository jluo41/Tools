"""
Generate the worked examples: real calls, real replies, written to disk.

    python examples/run_examples.py                 # against $FOODNORM_URL

Every case writes a folder holding exactly three things:

    curl.sh       the call, reproducible by hand
    request.json  what went in   (image cases note the file instead of the bytes)
    response.json what came back, verbatim

Nothing here is hand-written. If a reply in this tree looks wrong, the service
is wrong -- which is the only reason to keep transcripts rather than prose.
"""
import base64
import json
import os
import pathlib
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

URL = os.environ.get("FOODNORM_URL", "http://127.0.0.1:8077").rstrip("/")
# Where the generated artifacts land. Defaults beside this script; `--out`
# points it at a workspace instead, which is how the same cases get published
# into `_WorkSpace/0-RawDataStore/0-EventNorm/_FoodInfo/5-api-examples/` without the CODE moving
# there -- `_WorkSpace` is not a git tree, so a script living in it would have
# no version history. That rule is _FoodInfo's own and is quoted in its README.
_ARG_OUT = None
for _i, _a in enumerate(sys.argv):
    if _a == "--out" and _i + 1 < len(sys.argv):
        _ARG_OUT = sys.argv[_i + 1]
    elif _a.startswith("--out="):
        _ARG_OUT = _a.split("=", 1)[1]
OUT = (pathlib.Path(_ARG_OUT).expanduser().resolve() if _ARG_OUT
       else pathlib.Path(__file__).resolve().parent / "api")
PHOTOS = pathlib.Path("/nvme1/group_share/0-RawDataStore/CGMacros/Source/CGMacros-001/photos")


def write(case_dir, curl, request, response, note, frames=()):
    """A case must be SELF-CONTAINED. An image case that stored only a path to
    /nvme1/... was reproducible on exactly one machine, and would break silently
    the day the raw store moved -- while still looking like a worked example.
    So the frames are copied in beside the transcript and curl.sh names them
    relatively."""
    case_dir.mkdir(parents=True, exist_ok=True)
    for src in frames:
        shutil.copy2(src, case_dir / pathlib.Path(src).name)
    (case_dir / "curl.sh").write_text(
        "#!/usr/bin/env bash\n# " + note + "\n"
        "# run from inside this folder\n" + curl + "\n")
    (case_dir / "request.json").write_text(json.dumps(request, indent=2, ensure_ascii=False) + "\n")
    (case_dir / "response.json").write_text(json.dumps(response, indent=2, ensure_ascii=False) + "\n")


def _curl_json(path, payload):
    body = json.dumps(payload, ensure_ascii=False)
    return (f"curl -s -X POST {URL}{path} \\\n"
            f"     -H 'Content-Type: application/json' \\\n"
            f"     -d {json.dumps(body, ensure_ascii=False)}")


def post_json(path, payload, timeout=600):
    req = urllib.request.Request(URL + path, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def post_files(path, files, timeout=600):
    """files: [(filename, bytes, content_type)]"""
    boundary = "----foodnormexamples"
    body = b""
    for fname, data, ctype in files:
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"files\"; "
                 f"filename=\"{fname}\"\r\nContent-Type: {ctype}\r\n\r\n").encode()
        body += data + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(URL + path, data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


# Which frames. Chosen deliberately, not "the first on disk": one plate, one
# before/after pair, and one frame with NO visible food, because the honest MISS
# is as important to show as the hit.
FRAMES = {
    "plate":  ["00000007-PHOTO-2020-5-1-20-48-0.jpg"],
    "pair":   ["00000007-PHOTO-2020-5-1-20-48-0.jpg", "00000008-PHOTO-2020-5-1-20-57-0.jpg"],
    "nofood": ["00000002-PHOTO-2020-4-30-8-53-0.jpg"],
}

CATEGORIES = []
_PENDING_BODIES = {}

# The index header lives HERE, not in the file it writes: the runner overwrites
# README.md on every run, so a header hand-edited in the output is lost the next
# time anyone regenerates.
README_HEAD = """# API examples

Real calls against a live `describe-food` service, three per category. Every
`response.json` is a verbatim reply. Nothing here is hand-written: if a reply in
this tree looks wrong, the service is wrong. Regenerate with

    python examples/run_examples.py

Each case folder holds:

    curl.sh        the call, reproducible by hand -- `cd` in and `bash curl.sh`
    request.json   what went in
    response.json  what came back, verbatim
    *.jpg          image cases only: the actual frames, so the case is
                   self-contained and curl.sh names them relatively
    body.json      image-batch cases only: the same frames base64-encoded,
                   which is the real body curl.sh posts

THE FRAMES ARE GITIGNORED. They are real CGMacros subject photographs and stay
out of the repository until their redistribution terms are settled: a photo
pushed once is in the history forever. A fresh clone therefore has the
transcripts but not the images, and `bash curl.sh` will not run until you
regenerate. The transcripts are what these examples are FOR, and those are
tracked.


## Read a response in this order

    1. NutritionConf    GOOD | PARTIAL | MISS
                        PARTIAL means some item did not resolve, so the totals
                        UNDERSTATE the meal. MISS means all five are null.

    2. NutritionBasis   per_meal | per_100g | null   <- read BEFORE the numbers
                        per_meal   a portion was stated; this IS the meal
                        per_100g   none was stated; this is the sum of each
                                   item's per-100g row. NOT a meal.
                        Compare 03-text-with-grams against 02-text-item-list:
                        identical shape, and only one of them is a meal.

    3. NutritionSource  bank_usda                looked up from a typed name
                        bank_usda|img:<engine>   the NAME came from a model
                        none                     nothing resolved

    4. NameSource / NameConf / FoodNameResolved
                        present when this library DERIVED the name rather than
                        reading it. FoodNameResolved is the exact string the
                        bank was asked for -- the audit trail for a photo.


## The image cases are not deterministic

`06-image-upload/3-image-nofood` is a sealed opaque BlenderBottle: no food is
visible anywhere in the frame. Across runs the engine sometimes declines to name
it and sometimes infers `protein shake` from the bottle, at a low `NameConf`.

Both outcomes are correct, and the pair is the reason `NameConf` exists. A
consumer reading only `Carbs` sees a confident-looking number; one reading
`NameConf` sees that the system is barely guessing. It is also why the test
suite asserts the CONTRACT rather than a specific food name.

## Cases
"""




def cat(n, slug, blurb):
    def deco(fn):
        CATEGORIES.append((n, slug, blurb, fn)); return fn
    return deco


@cat(1, "text-single-item", "One food, one string. The simplest call there is.")
def c1():
    for i, food in enumerate(["fried rice", "boiled egg", "chinese cabbage"], 1):
        s, d = post_json("/normalize", {"food": food})
        curl = _curl_json("/normalize", {"food": food})
        yield i, food.replace(" ", "-"), curl, {"food": food}, d, f"one item -> {d.get('NutritionConf')}"


@cat(2, "text-item-list", "A meal written as a ';' list, the WellDoc dialect.")
def c2():
    cases = ["Toasted Bread; Decaf Coffee",
             "Cheese Pizza; Greek Salad; Banana Berry Muffin",
             "Nacho Cheese Tortilla Chips (28g); Diet Coke"]
    for i, food in enumerate(cases, 1):
        s, d = post_json("/normalize", {"food": food})
        yield i, f"list-{i}", _curl_json("/normalize", {"food": food}), {"food": food}, d, \
            f"{d.get('NutritionConf')} / {d.get('NutritionBasis')}"


@cat(3, "text-with-grams", "Portions stated, so the answer IS the meal: basis=per_meal.")
def c3():
    cases = ["Cucumber 100g",
             "Egg 50 g\nRice 25 g\nVegetable 100 g",
             "Coarse grain steamed bread 50 g\nEgg 39 g\nSteamed pork dumplings 64 g"]
    for i, food in enumerate(cases, 1):
        s, d = post_json("/normalize", {"food": food})
        yield i, f"grams-{i}", _curl_json("/normalize", {"food": food}), {"food": food}, d, \
            f"basis={d.get('NutritionBasis')}"


@cat(4, "text-names-no-food", "The string names no food. A clean MISS that claims nothing.")
def c4():
    for i, food in enumerate(["Just Carbs", "Unknown", "dinner"], 1):
        s, d = post_json("/normalize", {"food": food})
        yield i, food.replace(" ", "-").lower(), _curl_json("/normalize", {"food": food}), \
            {"food": food}, d, f"{d.get('NutritionConf')}, all five nutrients null"


@cat(5, "text-batch", "Many strings, one call. One result per input, in order.")
def c5():
    cases = [["white rice", "butter", "lettuce"],
             ["fried rice; egg", "milk", "fried rice; egg"],
             ["Cucumber 100g", "Just Carbs", "xiaolongbao"]]
    notes = ["3 distinct foods, order preserved",
             "a duplicate returns the identical record",
             "a hit, a declaration and an item the bank does not have"]
    for i, (foods, note) in enumerate(zip(cases, notes), 1):
        s, d = post_json("/normalize/batch", {"foods": foods})
        yield i, f"batch-{i}", _curl_json("/normalize/batch", {"foods": foods}), \
            {"foods": foods}, d, note


@cat(6, "image-upload", "Photo bytes over the wire. The caller shares no filesystem.")
def c6():
    specs = [("plate", "one frame, a plated meal"),
             ("pair", "the before/after pair CGMacros logs for one meal"),
             ("nofood", "a sealed opaque bottle: nothing edible is visible")]
    for i, (key, note) in enumerate(specs, 1):
        paths = [PHOTOS / f for f in FRAMES[key]]
        if not all(p.exists() for p in paths):
            continue
        files = [(p.name, p.read_bytes(), "image/jpeg") for p in paths]
        s, d = post_files("/normalize/image", files)
        curl = ("curl -s " + " ".join(f"-F files=@{p.name}" for p in paths)
                + f" \\\n     {URL}/normalize/image")
        yield i, f"image-{key}", curl, \
            {"_multipart": "files",
             "frames": [p.name for p in paths],
             "_frames_are_here": "the .jpg files sit in this folder; curl.sh uploads them",
             "_origin": [str(p) for p in paths]}, \
            d, note, paths


@cat(7, "image-batch-base64", "Many meals of frames in one JSON call.")
def c7():
    specs = [(["plate"], "one meal, one frame"),
             (["pair"], "one meal, two frames"),
             (["plate", "nofood"], "two meals in one call: a hit and an honest MISS")]
    for i, (keys, note) in enumerate(specs, 1):
        meals, shown = [], []
        for k in keys:
            paths = [PHOTOS / f for f in FRAMES[k]]
            if not all(p.exists() for p in paths):
                meals = []; break
            meals.append([base64.b64encode(p.read_bytes()).decode() for p in paths])
            shown.append(list(paths))
        if not meals:
            continue
        s, d = post_json("/normalize/image/batch", {"meals": meals})
        curl = ("# body.json in this folder holds the same frames, base64-encoded\n"
                f"curl -s -X POST {URL}/normalize/image/batch \\\n"
                "     -H 'Content-Type: application/json' -d @body.json")
        _PENDING_BODIES[f"imgbatch-{i}"] = {"meals": meals}
        flat = [q for m in shown for q in m]
        yield i, f"imgbatch-{i}", curl, \
            {"meals": [["<base64 of " + q.name + ">" for q in m] for m in shown],
             "_frames_are_here": "the .jpg files sit in this folder; body.json carries them base64-encoded",
             "_note": "base64 elided here for readability",
             "_origin": [str(q) for q in flat]}, \
            d, note, flat


@cat(8, "errors", "What a wrong call looks like. Never a 500, never a silent empty answer.")
def c8():
    s1, d1 = post_files("/normalize/image", [("notes.txt", b"not an image", "text/plain")])
    yield 1, "415-not-an-image", f"curl -s -F files=@notes.txt {URL}/normalize/image", \
        {"_multipart": "files", "frames": ["notes.txt (text/plain)"]}, {"status": s1, **d1}, \
        f"{s1} - only image types are accepted"

    s2, d2 = post_json("/normalize/batch", {"foods": "rice"})
    yield 2, "422-wrong-shape", _curl_json("/normalize/batch", {"foods": "rice"}), \
        {"foods": "rice"}, {"status": s2, **d2}, f"{s2} - foods must be a list, not a string"

    s3, d3 = post_files("/normalize/image",
                        [(f"f{i}.jpg", b"\xff\xd8\xff" + b"0" * 50, "image/jpeg") for i in range(5)])
    yield 3, "413-too-many-frames", \
        f"curl -s {' '.join(f'-F files=@f{i}.jpg' for i in range(5))} {URL}/normalize/image", \
        {"_multipart": "files", "frames": [f"f{i}.jpg" for i in range(5)]}, {"status": s3, **d3}, \
        f"{s3} - one meal is one or two frames"


if __name__ == "__main__":
    if OUT.exists():
        shutil.rmtree(OUT)
    index = [README_HEAD]
    for n, slug, blurb, fn in CATEGORIES:
        cat_dir = OUT / f"{n:02d}-{slug}"
        print(f"\n{n:02d}-{slug}  · {blurb}")
        index.append(f"\n## {n:02d}-{slug}\n\n{blurb}\n")
        for row in fn():
            i, name, curl, request, response, note = row[:6]
            frames = row[6] if len(row) > 6 else ()
            d = cat_dir / f"{i}-{name}"
            write(d, curl, request, response, note, frames)
            if name in _PENDING_BODIES:
                (d / "body.json").write_text(json.dumps(_PENDING_BODIES[name]))
            print(f"   {i}. {name:<22s} {note}")
            index.append(f"- `{i}-{name}/` — {note}\n")
    (OUT / "README.md").write_text("".join(index))
    print(f"\nwrote {OUT}")

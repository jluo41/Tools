"""Build the three independent Block previews and optional inline response copies."""
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "PRINCIPLE.md").is_file())
EXAMPLES = ROOT / "examples/Project-Ladder/labeling"
BLOCKS = (
    ("b03_itemization", "itemization-block"),
    ("b04_guideline_generation", "guideline-generation-block"),
    ("b05_labeling_at_scale", "labeling-at-scale-block"),
)


def fragment(model: dict) -> str:
    template = (HERE / "block-template.html").read_text()
    replacements = {
        "__BLOCK_NAME__": model["name"],
        "__BLOCK_MODEL__": json.dumps(model, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"),
        "__BLOCK_STYLE__": (HERE / "block-preview.css").read_text(),
        "__BLOCK_SCRIPT__": (HERE / "block-preview.js").read_text(),
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    return template.replace("__BLOCK_ID__", model["blockId"])


def build(inline_dir: Path | None = None) -> list[Path]:
    written = []
    for name, inline_name in BLOCKS:
        folder = EXAMPLES / name
        model = json.loads((folder / "delivery/ui/model.json").read_text())
        content = fragment(model)
        target = folder / "delivery/ui/block.html"
        target.write_text(content)
        written.append(target)
        if inline_dir is not None:
            inline_dir.mkdir(parents=True, exist_ok=True)
            target = inline_dir / (inline_name + ".html")
            target.write_text(content)
            written.append(target)
    return written


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inline-dir", type=Path)
    for path in build(parser.parse_args().inline_dir):
        print(path)

"""Rebuild Paper-family Structure trees through the shared b17 renderer."""
from pathlib import Path
import sys
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'PRINCIPLE.md').is_file())
BLOCK = ROOT / 'examples/Project-Ladder/blueprint/b16_theme_paper'
TOPICS = ('s01-idea-block-structure', 's02-grant-block-structure', 's03-paper-block-structure')
def render(topic, shared=None):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from build_block_structures import structure_document
    return structure_document(topic)
def main():
    for name in TOPICS:
        topic = BLOCK / name
        (topic / 'structure/jobs.html').write_text(render(topic), encoding='utf-8')
        print(name)
if __name__ == '__main__':
    main()

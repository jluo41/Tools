"""Every venue folder keeps the contract in venues/README.md, and the shared scripts name no venue (AgreeableJama-Board 261122)."""
import ast
import re
import tomllib
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
VENUES = SKILL / "venues"
HOOKS = {"build_word"}


def _folders():
    return sorted(p for p in VENUES.iterdir() if p.is_dir() and not p.name.startswith(("_", ".")))


def test_every_venue_has_a_profile_and_its_layout_exists():
    assert _folders()
    for folder in _folders():
        prof = tomllib.loads((folder / "profile.toml").read_text(encoding="utf-8"))
        layout = str(prof.get("layout", "generic"))
        assert layout == "generic" or (VENUES / layout).is_dir(), (folder.name, layout)


def test_a_venue_py_defines_a_contract_hook():
    for folder in _folders():
        if (folder / "venue.py").is_file():
            tree = ast.parse((folder / "venue.py").read_text(encoding="utf-8"))
            names = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
            assert names & HOOKS, folder.name


def test_shared_scripts_name_no_venue():
    names = [f.name for f in _folders()]
    for script in sorted((SKILL / "scripts").glob("*.py")):
        code = "\n".join(line.split("#", 1)[0] for line in script.read_text(encoding="utf-8").splitlines())
        for name in names:
            assert not re.search(rf"[\"']{re.escape(name)}[\"']", code), (script.name, name)
        assert "venue_jama" not in code and "build_jama" not in code, script.name

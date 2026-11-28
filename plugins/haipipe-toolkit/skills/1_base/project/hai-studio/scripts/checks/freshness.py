"""Reuse the owning generators in memory; never write while checking."""
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path

from checks.paths import owner, using_root
from checks.results import Result


OWN = "build_type_pages.py"   # a type topic may carry its own generator: built(type_only=True) -> {path: text}


def own_outputs(topic: Path, root: Path) -> dict | None:
    """What the topic's own generator would write for the type itself, or None when its SPACE is not this one."""
    spec = spec_from_file_location(f"own_{topic.name.replace('-', '_')}", topic / OWN)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.built(True) if Path(module.ROOT).resolve() == root.resolve() else None


def check(topic: Path, data: dict, kind: str, root: Path) -> list[Result]:
    manifest = topic / "studio-views.json"
    own = kind == "type" and (topic / OWN).is_file() and (topic / OWN).resolve().is_relative_to(root.resolve())
    if kind == "skills":
        module = owner("skills_views")
        with using_root(module, root):
            skills = module.skills_of(topic)
            if not skills:
                return [Result("FAIL", "skill-files", manifest,
                               "each skill must start with its actual SKILL.md; regenerate with skills_views.py")]
            expected = dict(data, views=json.loads(module.views_text(skills, topic))["views"])
        if data.get("check_type"):
            outputs = owner("check_views").build(topic, expected, root)
        else:
            outputs = {manifest: json.dumps(expected, indent=2, ensure_ascii=False) + "\n"}
        instruction = "skills_views.py"
    elif own:
        outputs = own_outputs(topic, root)
        if outputs is None:
            return [Result("FAIL", "generated", topic / OWN, "its generator reads another SPACE")]
        instruction = OWN
    elif kind == "type":
        module = owner("type_requirements")
        with using_root(module, root):
            outputs = module.build(topic)
        if not outputs or not json.loads(outputs[manifest])["views"]:
            return [Result("FAIL", "generated", manifest, "type has no requirement views")]
        instruction = "type_requirements.py"
    elif data.get("check_type"):
        outputs = owner("check_views").build(topic, data, root)
        instruction = "check_views.py"
    else:
        return [Result("UNCOVERED", "generated", topic, "no registered generator for this topic")]
    stale = [p for p, expected in outputs.items() if not p.is_file() or p.read_text() != expected]
    if kind == "type" and not own:
        stale += [p for p in (topic / "delivery/requirements").glob("*.html") if p not in outputs]
    if stale:
        return [Result("FAIL", "generated", p, f"out of date; regenerate this topic with {instruction}") for p in stale]
    detail = "generated files match their owners"
    if data.get("check_type"):
        detail += "; Check criteria were not executed"
    return [Result("PASS", "generated", topic, detail)]

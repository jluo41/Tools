"""Persona loader.

A persona = a folder with three files:
    persona.yaml   metadata (audience, tone, model preference, safety_rules)
    system.md      the system prompt the LLM sees
    schema.md      reference description of the <report> XML schema (kept
                   alongside the system prompt so persona authors can tweak
                   it; the loader concatenates schema.md into the system
                   prompt so the model always sees both)

`--persona` accepts either:
    - a name like 'patient-friendly' (resolves under SHIPPED_PERSONAS_DIR), OR
    - an absolute path to any folder on disk

This means downstream users (Samsung, clinicians) can keep proprietary
personas outside this plugin and just point --persona at them.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml

SHIPPED_PERSONAS_DIR = Path(__file__).resolve().parents[1] / "personas"

REQUIRED_YAML_KEYS = {"audience", "tone"}


def resolve_persona_dir(persona: str) -> Path:
    """Accept a name (resolved under shipped/) or an absolute path."""
    p = Path(persona)
    if p.is_absolute() and p.exists():
        return p
    candidate = SHIPPED_PERSONAS_DIR / persona
    if candidate.exists():
        return candidate
    raise FileNotFoundError(
        f"Persona not found: {persona!r}. Looked in {SHIPPED_PERSONAS_DIR} "
        f"and as absolute path."
    )


def load_persona(persona: str) -> Dict[str, Any]:
    """Load a persona folder into a dict. Required files: persona.yaml,
    system.md, schema.md."""
    pdir = resolve_persona_dir(persona)

    yaml_path = pdir / "persona.yaml"
    sys_path = pdir / "system.md"
    schema_path = pdir / "schema.md"

    for f, label in [(yaml_path, "persona.yaml"),
                     (sys_path, "system.md"),
                     (schema_path, "schema.md")]:
        if not f.exists():
            raise FileNotFoundError(f"Persona {pdir.name!r} missing {label}: {f}")

    meta = yaml.safe_load(yaml_path.read_text()) or {}
    missing = REQUIRED_YAML_KEYS - set(meta.keys())
    if missing:
        raise ValueError(
            f"Persona {pdir.name!r} persona.yaml missing required keys: {missing}"
        )

    system_md = sys_path.read_text()
    schema_md = schema_path.read_text()

    full_system_prompt = (
        f"{system_md.strip()}\n\n"
        f"=== OUTPUT SCHEMA ===\n"
        f"{schema_md.strip()}\n"
    )

    return {
        "persona_dir": str(pdir),
        "persona_name": pdir.name,
        "meta": meta,
        "system_prompt": full_system_prompt,
    }

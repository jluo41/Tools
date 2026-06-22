"""Persona loader (judge edition).

Identical convention to haipipe-individual-inference-report's loader,
applied to JUDGE personas. Same three files:
    persona.yaml   metadata (rubric, target_audience, model preference)
    system.md      the system prompt the LLM judge sees
    schema.md      reference description of the <judgment> XML schema

`--persona` accepts either:
    - a name like 'patient-comprehension' (resolves under shipped/), OR
    - an absolute path to any folder on disk

External judge libraries (Samsung clinical-review, IRB safety panels,
research-only rubrics) live OUTSIDE the plugin.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml

SHIPPED_PERSONAS_DIR = Path(__file__).resolve().parents[1] / "personas"

REQUIRED_YAML_KEYS = {"rubric", "target_audience"}


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

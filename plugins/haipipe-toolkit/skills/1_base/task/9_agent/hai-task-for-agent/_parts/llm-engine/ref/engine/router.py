"""Model string -> transport selection."""
from __future__ import annotations


CLAUDE_KEYWORDS = {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-5",
    "opus": "claude-opus-5",
}

CODEX_KEYWORDS = {
    "luna": "gpt-5.6-luna",
    "terra": "gpt-5.6-terra",
    "sol": "gpt-5.6-sol",
}


def resolve_transport(model: str, transport: str = "auto") -> tuple[str, str]:
    """Return (transport_name, resolved_model_id).

    Model string conventions:
      "opus" / "sonnet" / "haiku"   -> claude_sdk, expanded model id
      "claude-opus-5"               -> claude_sdk, as-is
      "luna" / "terra" / "sol"    -> openai_codex_sdk, expanded model id
      "codex/gpt-5.6-sol"           -> openai_codex_sdk, strip prefix
      "api:claude-opus-5"           -> claude_api, strip prefix
    """
    if transport != "auto":
        if transport == "codex_oauth":
            transport = "openai_codex_sdk"
        resolved_model = CLAUDE_KEYWORDS.get(model, CODEX_KEYWORDS.get(model, model))
        return transport, resolved_model

    if model.startswith("api:"):
        return "claude_api", model[4:]

    if model.startswith("codex/"):
        return "openai_codex_sdk", model[6:]

    if model in CLAUDE_KEYWORDS:
        return "claude_sdk", CLAUDE_KEYWORDS[model]

    if model in CODEX_KEYWORDS:
        return "openai_codex_sdk", CODEX_KEYWORDS[model]

    if "gpt" in model.lower() or "o4" in model.lower() or "o3" in model.lower():
        return "openai_codex_sdk", model

    return "claude_sdk", model

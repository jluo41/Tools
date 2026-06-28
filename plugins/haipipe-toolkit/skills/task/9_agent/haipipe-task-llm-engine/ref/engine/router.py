"""Model string -> transport selection."""
from __future__ import annotations


CLAUDE_KEYWORDS = {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6",
    "opus": "claude-opus-4-7",
}


def resolve_transport(model: str, transport: str = "auto") -> tuple[str, str]:
    """Return (transport_name, resolved_model_id).

    Model string conventions:
      "opus" / "sonnet" / "haiku"   -> claude_sdk, expanded model id
      "claude-opus-4-7"             -> claude_sdk, as-is
      "codex/gpt-5.5"              -> codex_oauth, strip prefix
      "api:claude-opus-4-7"        -> claude_api, strip prefix
    """
    if transport != "auto":
        resolved_model = CLAUDE_KEYWORDS.get(model, model)
        return transport, resolved_model

    if model.startswith("api:"):
        return "claude_api", model[4:]

    if model.startswith("codex/"):
        return "codex_oauth", model[6:]

    if model in CLAUDE_KEYWORDS:
        return "claude_sdk", CLAUDE_KEYWORDS[model]

    if "gpt" in model.lower() or "o4" in model.lower() or "o3" in model.lower():
        return "codex_oauth", model

    return "claude_sdk", model

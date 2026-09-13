from __future__ import annotations

from typing import Any

from .config import Settings

try:
    from strands import Agent
    from strands.models import BedrockModel
except ImportError:  # pragma: no cover
    Agent = None  # type: ignore[assignment,misc]
    BedrockModel = None  # type: ignore[assignment,misc]

SYSTEM_PROMPT = """You are CogniSync Professional, a background work agent.
Reduce repetitive professional coordination work while preserving human control.
Analyze supplied project signals, identify changes, blockers and follow-ups, then produce
concise evidence-backed work. Never claim an external action happened unless a real tool
confirms it. Treat consequential side effects as authorization-gated operations. Prefer
useful, quiet background work over unnecessary notifications."""


def build_strands_agent(settings: Settings | None = None) -> Any:
    """Build the real Strands/Bedrock agent when AWS dependencies are installed."""
    if Agent is None or BedrockModel is None:
        raise RuntimeError("Install the project with the 'aws' extra to use the Strands adapter.")
    settings = settings or Settings.from_env()
    model = BedrockModel(
        model_id=settings.model_id,
        region_name=settings.region,
        temperature=settings.temperature,
        streaming=True,
    )
    return Agent(model=model, system_prompt=SYSTEM_PROMPT)

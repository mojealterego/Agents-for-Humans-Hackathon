from __future__ import annotations

import re
from typing import Any

from .config import Settings

try:
    from strands import Agent, tool
    from strands.models import BedrockModel
except ImportError:  # pragma: no cover
    Agent = None  # type: ignore[assignment,misc]
    BedrockModel = None  # type: ignore[assignment,misc]
    tool = None  # type: ignore[assignment,misc]

SYSTEM_PROMPT = """You are CogniSync Professional, a background work agent.
Reduce repetitive professional coordination work while preserving human control.
Analyze supplied project signals, identify changes, blockers and follow-ups, then produce
concise evidence-backed work. Use the read-only signal inspection tool when useful.
Never claim an external action happened unless a real tool confirms it. Treat consequential
side effects as authorization-gated operations. Prefer useful, quiet background work over
unnecessary notifications. Model reasoning can propose work, but it cannot authorize side effects."""


def _inspect_signal(signal: str) -> dict[str, Any]:
    words = re.findall(r"[A-Za-z0-9_-]+", signal.lower())
    signals = {
        marker: signal.lower().count(marker)
        for marker in ("pending", "blocked", "review", "deadline", "needs")
        if marker in signal.lower()
    }
    return {
        "word_count": len(words),
        "character_count": len(signal),
        "coordination_signals": signals,
        "side_effects_performed": False,
    }


if tool is not None:

    @tool
    def inspect_project_signal(signal: str) -> dict[str, Any]:
        """Inspect a project signal using a read-only deterministic analyzer.

        Args:
            signal: Project text supplied for analysis. The tool never writes, sends,
                publishes, changes records, or calls external services.
        """
        return _inspect_signal(signal)

else:
    inspect_project_signal = _inspect_signal


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
    return Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[inspect_project_signal],
    )

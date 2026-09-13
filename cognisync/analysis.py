from __future__ import annotations

import re
from collections import Counter

from .models import Insight, ProjectItem

_STOPWORDS = {
    "about", "after", "again", "before", "could", "from", "have", "into", "needs", "only",
    "that", "their", "there", "these", "this", "what", "when", "with", "would", "your",
    "still", "next", "final", "asked", "client", "project", "progress", "remaining",
}
_PENDING_SIGNALS = ("pending", "needs", "remaining", "review")


def _tokens(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{3,}", text.lower())
        if token not in _STOPWORDS
    ]


def _evidence_quality(items: list[ProjectItem], evidence: list[str]) -> float:
    """Score evidence coverage/consistency, never model confidence."""
    if not items or not evidence:
        return 0.0
    nonempty = sum(bool(item.content.strip()) for item in items)
    distinct_sources = len({item.source for item in items if item.source.strip()})
    source_factor = min(1.0, distinct_sources / 3.0)
    completeness = nonempty / len(items)
    volume_factor = min(1.0, len(items) / 5.0)
    return round(0.35 * completeness + 0.35 * source_factor + 0.30 * volume_factor, 3)


def analyze_items(items: list[ProjectItem]) -> tuple[list[Insight], list[str]]:
    evidence = [f"{item.source}: {item.title}" for item in items]
    corpus = Counter(token for item in items for token in _tokens(item.content))
    top_terms = [term for term, _ in corpus.most_common(8)]
    pending = [
        item.title
        for item in items
        if any(signal in item.content.lower() for signal in _PENDING_SIGNALS)
    ]
    summary = (
        f"Processed {len(items)} source items. Key signals: {', '.join(top_terms) or 'no dominant terms'}; "
        f"potentially pending work: {', '.join(pending) or 'none detected'}."
    )
    evidence_quality = _evidence_quality(items, evidence)
    insight = Insight(
        title="Decision-ready project signal",
        summary=summary,
        evidence=evidence,
        confidence=evidence_quality,
        recommended_action="Review the evidence-backed brief; approve only consequential external actions.",
    )
    return [insight], evidence

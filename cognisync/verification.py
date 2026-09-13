from __future__ import annotations

from dataclasses import dataclass

from .models import Insight


@dataclass(frozen=True, slots=True)
class VerificationResult:
    passed: bool
    status: str
    checks: tuple[str, ...]
    failures: tuple[str, ...]


def verify_insight(insight: Insight) -> VerificationResult:
    failures: list[str] = []
    if not insight.title.strip():
        failures.append("missing title")
    if not insight.summary.strip():
        failures.append("missing summary")
    if not insight.evidence:
        failures.append("missing evidence")
    if not 0.0 <= insight.evidence_quality <= 1.0:
        failures.append("evidence quality outside [0,1]")
    if not insight.recommended_action.strip():
        failures.append("missing recommended action")
    return VerificationResult(
        passed=not failures,
        status="passed" if not failures else "failed",
        checks=("schema", "evidence", "evidence_quality", "actionability"),
        failures=tuple(failures),
    )


def verify_insights(insights: list[Insight], evidence: list[str]) -> VerificationResult:
    failures: list[str] = []
    if not insights:
        failures.append("no insights produced")
    if not evidence:
        failures.append("no evidence produced")

    for index, insight in enumerate(insights, start=1):
        result = verify_insight(insight)
        failures.extend(f"insight[{index}]: {failure}" for failure in result.failures)

    return VerificationResult(
        passed=not failures,
        status="passed" if not failures else "failed",
        checks=("collection", "schema", "evidence", "evidence_quality", "actionability"),
        failures=tuple(failures),
    )

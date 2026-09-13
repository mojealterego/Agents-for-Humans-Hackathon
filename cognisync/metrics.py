from __future__ import annotations

from dataclasses import dataclass

from .models import DecisionStatus, RunResult


@dataclass(frozen=True, slots=True)
class AttentionMetrics:
    """Observable run metrics for the human-attention research objective.

    A pending decision is an escalation, not evidence that a human has already
    intervened. Human intervention is counted only after an explicit resolution.
    """

    human_interventions: int
    evidence_coverage: float
    consequence_gates: int
    autonomous_insights: int
    decision_requests: int
    approved_decisions: int
    rejected_decisions: int
    executed_actions: int
    failed_actions: int


def measure(result: RunResult) -> AttentionMetrics:
    total = len(result.insights)
    evidenced = sum(1 for insight in result.insights if insight.evidence)
    decision = result.decision_request
    status = decision.status if decision else None
    resolved = status in {
        DecisionStatus.APPROVED,
        DecisionStatus.REJECTED,
        DecisionStatus.EXECUTED,
        DecisionStatus.FAILED,
    }
    approved = {
        DecisionStatus.APPROVED,
        DecisionStatus.EXECUTED,
        DecisionStatus.FAILED,
    }
    return AttentionMetrics(
        human_interventions=1 if resolved else 0,
        evidence_coverage=(evidenced / total) if total else 0.0,
        consequence_gates=1 if decision else 0,
        autonomous_insights=total,
        decision_requests=1 if decision else 0,
        approved_decisions=1 if status in approved else 0,
        rejected_decisions=1 if status is DecisionStatus.REJECTED else 0,
        executed_actions=1 if status is DecisionStatus.EXECUTED else 0,
        failed_actions=1 if status is DecisionStatus.FAILED else 0,
    )

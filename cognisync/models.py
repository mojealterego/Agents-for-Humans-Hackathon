from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DecisionStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    FAILED = "failed"


@dataclass(slots=True)
class ProjectItem:
    id: str
    source: str
    title: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Insight:
    title: str
    summary: str
    evidence: list[str]
    confidence: float
    recommended_action: str


@dataclass(slots=True)
class DecisionRequest:
    decision_id: str
    action: str
    reason: str
    risk: RiskLevel
    evidence: list[str]
    proposed_payload: dict[str, Any]
    status: DecisionStatus = DecisionStatus.PENDING


@dataclass(slots=True)
class RunResult:
    run_id: str
    status: str
    summary: str
    insights: list[Insight]
    decision_request: DecisionRequest | None = None
    audit_events: list[dict[str, Any]] = field(default_factory=list)

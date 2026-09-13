from __future__ import annotations

import hashlib
import json
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


def payload_fingerprint(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def policy_fingerprint(
    safe_actions: frozenset[str],
    approval_actions: frozenset[str],
    capability_rules: dict[str, tuple[str, bool, bool]] | None = None,
) -> str:
    canonical = json.dumps(
        {
            "safe_actions": sorted(safe_actions),
            "approval_actions": sorted(approval_actions),
            "capability_rules": sorted((capability_rules or {}).items()),
        },
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


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
    evidence_quality: float
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
    authorized_payload_hash: str | None = None
    policy_hash: str | None = None


@dataclass(slots=True)
class RunResult:
    run_id: str
    status: str
    summary: str
    insights: list[Insight]
    decision_request: DecisionRequest | None = None
    audit_events: list[dict[str, Any]] = field(default_factory=list)

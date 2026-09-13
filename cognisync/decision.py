from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .audit import AuditLog
from .models import DecisionRequest, DecisionStatus, payload_fingerprint
from .policy import AutonomyPolicy


@dataclass(frozen=True, slots=True)
class DecisionResolution:
    status: DecisionStatus
    message: str
    request: DecisionRequest


class DecisionGate:
    """Single consequence boundary for consequential agent capabilities."""

    def __init__(self, policy: AutonomyPolicy, audit: AuditLog) -> None:
        self.policy = policy
        self.audit = audit

    def _validate_policy_binding(self, decision: DecisionRequest) -> None:
        if decision.policy_hash is None:
            decision.policy_hash = self.policy.fingerprint
        if decision.policy_hash != self.policy.fingerprint:
            raise ValueError("Decision was authorized under a different policy")
        if self.policy.classify(decision.action) is not decision.risk:
            raise ValueError("Decision risk no longer matches the active policy")

    def request(
        self,
        *,
        action: str,
        reason: str,
        evidence: list[str],
        payload: dict[str, Any],
    ) -> DecisionRequest | None:
        decision = self.policy.gate(action, reason, evidence, payload)
        if decision is None:
            return None
        self.audit.record(
            "decision.requested",
            decision_id=decision.decision_id,
            action=decision.action,
            risk=decision.risk.value,
            evidence_count=len(decision.evidence),
            payload_hash=payload_fingerprint(decision.proposed_payload),
            policy_hash=decision.policy_hash,
        )
        return decision

    def resolve(
        self,
        decision: DecisionRequest,
        approved: bool,
        actor: str = "human",
    ) -> DecisionResolution:
        if decision.status is not DecisionStatus.PENDING:
            raise ValueError(f"Decision {decision.decision_id} is already {decision.status.value}")
        self._validate_policy_binding(decision)

        status = DecisionStatus.APPROVED if approved else DecisionStatus.REJECTED
        event = "decision.approved" if approved else "decision.rejected"
        if approved:
            decision.authorized_payload_hash = payload_fingerprint(decision.proposed_payload)
        decision.status = status
        self.audit.record(
            event,
            decision_id=decision.decision_id,
            action=decision.action,
            risk=decision.risk.value,
            actor=actor,
            payload_hash=payload_fingerprint(decision.proposed_payload),
            policy_hash=decision.policy_hash,
        )
        message = (
            f"Human approval recorded for {decision.action}. External execution may proceed through a trusted connector."
            if approved
            else f"Human rejection recorded for {decision.action}. No external effect is authorized."
        )
        return DecisionResolution(status, message, decision)

    def record_execution(
        self,
        decision: DecisionRequest,
        *,
        success: bool,
        connector: str,
        external_reference: str | None = None,
    ) -> None:
        """Record one connector-confirmed execution after a separately approved decision."""
        if decision.status is not DecisionStatus.APPROVED:
            raise ValueError("Only an approved decision may be recorded as executed")
        self._validate_policy_binding(decision)
        current_hash = payload_fingerprint(decision.proposed_payload)
        if decision.authorized_payload_hash != current_hash:
            raise ValueError("Approved payload was modified after human authorization")

        decision.status = DecisionStatus.EXECUTED if success else DecisionStatus.FAILED
        self.audit.record(
            "action.executed" if success else "action.failed",
            decision_id=decision.decision_id,
            action=decision.action,
            connector=connector,
            external_reference=external_reference,
            payload_hash=current_hash,
            policy_hash=decision.policy_hash,
        )

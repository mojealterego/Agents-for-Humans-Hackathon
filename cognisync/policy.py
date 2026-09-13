from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from .capabilities import CAPABILITIES
from .models import DecisionRequest, RiskLevel, policy_fingerprint


@dataclass(frozen=True, slots=True)
class AutonomyPolicy:
    """Model-independent authorization policy.

    Authorization depends on the capability consequence class, never on model confidence.
    Unknown capabilities are critical and require explicit human resolution.
    """

    safe_actions: frozenset[str]
    approval_actions: frozenset[str]

    @property
    def fingerprint(self) -> str:
        """Stable hash of authorization rules and capability semantics."""
        capability_rules = {
            name: (capability.risk.value, capability.requires_human, capability.external_side_effect)
            for name, capability in CAPABILITIES.items()
        }
        return policy_fingerprint(self.safe_actions, self.approval_actions, capability_rules)

    def classify(self, action: str) -> RiskLevel:
        normalized = self.normalize(action)
        capability = CAPABILITIES.get(normalized)
        if capability is not None:
            return capability.risk
        if normalized in self.safe_actions:
            return RiskLevel.LOW
        if normalized in self.approval_actions:
            return RiskLevel.HIGH
        return RiskLevel.CRITICAL

    def requires_approval(self, action: str) -> bool:
        return self.classify(action) in {RiskLevel.HIGH, RiskLevel.CRITICAL}

    def gate(
        self,
        action: str,
        reason: str,
        evidence: list[str],
        payload: dict,
    ) -> DecisionRequest | None:
        normalized = self.normalize(action)
        risk = self.classify(normalized)
        if risk is RiskLevel.LOW:
            return None
        from uuid import uuid4

        return DecisionRequest(
            decision_id=str(uuid4()),
            action=normalized,
            reason=reason,
            risk=risk,
            evidence=list(evidence),
            proposed_payload=dict(payload),
            policy_hash=self.fingerprint,
        )

    @staticmethod
    def normalize(action: str) -> str:
        return "_".join(action.strip().lower().split())


SAFE_ACTIONS: Final = frozenset(
    {
        "read_project_data",
        "summarize",
        "classify",
        "draft_followup",
        "draft_report",
        "search_knowledge",
    }
)

APPROVAL_ACTIONS: Final = frozenset(
    {
        "send_external_message",
        "publish_document",
        "modify_calendar",
        "change_crm_record",
        "make_payment",
        "delete_data",
    }
)

DEFAULT_POLICY = AutonomyPolicy(SAFE_ACTIONS, APPROVAL_ACTIONS)

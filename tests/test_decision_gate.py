from pathlib import Path

import pytest

from cognisync.audit import AuditLog
from cognisync.decision import DecisionGate
from cognisync.models import DecisionStatus, RiskLevel
from cognisync.policy import DEFAULT_POLICY, AutonomyPolicy


def test_unknown_capability_creates_critical_decision(tmp_path: Path) -> None:
    audit = AuditLog(tmp_path / "audit.jsonl")
    gate = DecisionGate(DEFAULT_POLICY, audit)

    decision = gate.request(
        action="unknown_side_effect",
        reason="unknown",
        evidence=["source-1"],
        payload={"x": 1},
    )

    assert decision is not None
    assert decision.risk is RiskLevel.CRITICAL
    assert decision.status is DecisionStatus.PENDING
    assert decision.decision_id
    assert decision.policy_hash == DEFAULT_POLICY.fingerprint


def test_decision_is_single_use(tmp_path: Path) -> None:
    audit = AuditLog(tmp_path / "audit.jsonl")
    gate = DecisionGate(DEFAULT_POLICY, audit)
    decision = gate.request(
        action="send_external_message",
        reason="external communication",
        evidence=["source-1"],
        payload={"message": "hello"},
    )
    assert decision is not None

    result = gate.resolve(decision, approved=True, actor="reviewer")
    assert result.status is DecisionStatus.APPROVED

    with pytest.raises(ValueError):
        gate.resolve(decision, approved=True, actor="reviewer")


def test_execution_requires_approval_and_is_terminal(tmp_path: Path) -> None:
    audit = AuditLog(tmp_path / "audit.jsonl")
    gate = DecisionGate(DEFAULT_POLICY, audit)
    decision = gate.request(
        action="send_external_message",
        reason="external communication",
        evidence=["source-1"],
        payload={},
    )
    assert decision is not None

    with pytest.raises(ValueError):
        gate.record_execution(decision, success=True, connector="demo")

    gate.resolve(decision, approved=True)
    gate.record_execution(
        decision,
        success=True,
        connector="demo",
        external_reference="simulated-001",
    )
    assert decision.status is DecisionStatus.EXECUTED

    with pytest.raises(ValueError):
        gate.record_execution(decision, success=True, connector="demo")


def test_failed_execution_is_terminal(tmp_path: Path) -> None:
    audit = AuditLog(tmp_path / "audit.jsonl")
    gate = DecisionGate(DEFAULT_POLICY, audit)
    decision = gate.request(
        action="send_external_message",
        reason="external communication",
        evidence=["source-1"],
        payload={},
    )
    assert decision is not None

    gate.resolve(decision, approved=True)
    gate.record_execution(decision, success=False, connector="demo")
    assert decision.status is DecisionStatus.FAILED

    with pytest.raises(ValueError):
        gate.record_execution(decision, success=True, connector="demo")


def test_modified_payload_cannot_use_previous_approval(tmp_path: Path) -> None:
    audit = AuditLog(tmp_path / "audit.jsonl")
    gate = DecisionGate(DEFAULT_POLICY, audit)
    decision = gate.request(
        action="send_external_message",
        reason="external communication",
        evidence=["source-1"],
        payload={"recipient": "alice", "message": "approved"},
    )
    assert decision is not None

    gate.resolve(decision, approved=True)
    decision.proposed_payload["recipient"] = "mallory"

    with pytest.raises(ValueError, match="payload was modified"):
        gate.record_execution(decision, success=True, connector="demo")


def test_execution_rejects_policy_mismatch(tmp_path: Path) -> None:
    audit = AuditLog(tmp_path / "audit.jsonl")
    original = DEFAULT_POLICY
    gate = DecisionGate(original, audit)
    decision = gate.request(
        action="send_external_message",
        reason="external communication",
        evidence=["source-1"],
        payload={"message": "approved"},
    )
    assert decision is not None
    gate.resolve(decision, approved=True)

    changed_policy = AutonomyPolicy(
        original.safe_actions,
        original.approval_actions | frozenset({"new_consequential_capability"}),
    )
    changed_gate = DecisionGate(changed_policy, audit)

    with pytest.raises(ValueError, match="different policy"):
        changed_gate.record_execution(decision, success=True, connector="demo")

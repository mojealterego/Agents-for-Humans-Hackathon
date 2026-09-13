from cognisync.audit import AuditLog
from cognisync.decision import DecisionGate
from cognisync.models import DecisionRequest, RiskLevel
from cognisync.policy import DEFAULT_POLICY


def test_decision_gate_records_rejection(tmp_path) -> None:
    audit = AuditLog(tmp_path / "audit.jsonl")
    gate = DecisionGate(DEFAULT_POLICY, audit)
    request = DecisionRequest(
        action="send_external_message",
        reason="External communication",
        risk=RiskLevel.HIGH,
        evidence=["email: Client"],
        proposed_payload={"message": "draft"},
    )
    result = gate.resolve(request, approved=False, actor="demo-user")
    assert result.status == "rejected"
    assert request.policy_hash == DEFAULT_POLICY.fingerprint
    assert "No external effect" in result.message
    lines = (tmp_path / "audit.jsonl").read_text(encoding="utf-8").splitlines()
    assert '"event": "decision.rejected"' in lines[-1]

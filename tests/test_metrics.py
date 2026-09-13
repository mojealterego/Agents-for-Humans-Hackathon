from pathlib import Path

from cognisync.audit import AuditLog
from cognisync.engine import CogniSyncEngine
from cognisync.metrics import measure
from cognisync.models import ProjectItem
from cognisync.store import ProjectStore


def test_metrics_reflect_completed_background_run(tmp_path: Path) -> None:
    data = tmp_path / "data"
    audit = AuditLog(data / "audit.jsonl")
    result = CogniSyncEngine(ProjectStore(data), audit).run(
        "prepare brief",
        [ProjectItem("1", "email", "Launch", "Accessibility review is pending.")],
    )

    metrics = measure(result)
    assert metrics.human_interventions == 0
    assert metrics.consequence_gates == 0
    assert metrics.decision_requests == 0
    assert metrics.approved_decisions == 0
    assert metrics.rejected_decisions == 0
    assert metrics.executed_actions == 0
    assert metrics.failed_actions == 0
    assert metrics.autonomous_insights == 1
    assert metrics.evidence_coverage == 1.0


def test_pending_decision_is_escalation_not_intervention(tmp_path: Path) -> None:
    data = tmp_path / "data"
    audit = AuditLog(data / "audit.jsonl")
    result = CogniSyncEngine(ProjectStore(data), audit).run(
        "prepare and send follow-up",
        [ProjectItem("1", "email", "Client", "Approval needed.")],
    )

    metrics = measure(result)
    assert metrics.human_interventions == 0
    assert metrics.consequence_gates == 1
    assert metrics.decision_requests == 1
    assert metrics.approved_decisions == 0
    assert metrics.executed_actions == 0

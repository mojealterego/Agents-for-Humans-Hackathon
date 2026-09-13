from pathlib import Path

from cognisync.audit import AuditLog
from cognisync.engine import CogniSyncEngine
from cognisync.models import ProjectItem
from cognisync.store import ProjectStore


def test_empty_input_remains_idle(tmp_path: Path) -> None:
    data = tmp_path / "data"
    audit = AuditLog(data / "audit.jsonl")
    result = CogniSyncEngine(ProjectStore(data), audit).run("prepare brief", [])

    assert result.status == "idle"
    assert result.insights == []
    assert "fabricating work" in result.summary


def test_verification_failure_does_not_promote_candidates(tmp_path: Path, monkeypatch) -> None:
    data = tmp_path / "data"
    audit = AuditLog(data / "audit.jsonl")

    def fake_analysis(items):
        from cognisync.models import Insight
        return [
            Insight(
                title="Candidate",
                summary="Unsupported",
                evidence=[],
                evidence_quality=0.5,
                recommended_action="Investigate",
            )
        ], []

    monkeypatch.setattr("cognisync.engine.analyze_items", fake_analysis)
    result = CogniSyncEngine(ProjectStore(data), audit).run(
        "prepare brief",
        [ProjectItem("1", "notes", "Test", "Input")],
    )

    assert result.status == "verification_failed"
    assert result.insights == []
    assert "verification" in result.summary.lower()

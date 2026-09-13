from pathlib import Path

import pytest

from cognisync.audit import AuditLog


def test_audit_chain_verifies(tmp_path: Path) -> None:
    path = tmp_path / "audit.jsonl"
    audit = AuditLog(path)
    audit.record("run.started", run_id="r1")
    audit.record("run.completed", run_id="r1", status="completed")

    ok, checked, error = audit.verify_integrity()
    assert ok is True
    assert checked == 2
    assert error is None


def test_audit_tamper_is_detected(tmp_path: Path) -> None:
    path = tmp_path / "audit.jsonl"
    audit = AuditLog(path)
    audit.record("run.started", run_id="r1")
    audit.record("run.completed", run_id="r1", status="completed")

    lines = path.read_text(encoding="utf-8").splitlines()
    lines[0] = lines[0].replace('"run_id": "r1"', '"run_id": "tampered"')
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="invalid audit log"):
        AuditLog(path)


def test_audit_refuses_append_after_malformed_json(tmp_path: Path) -> None:
    path = tmp_path / "audit.jsonl"
    audit = AuditLog(path)
    audit.record("run.started", run_id="r1")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("not-json\n")

    with pytest.raises(RuntimeError, match="invalid audit log"):
        AuditLog(path)

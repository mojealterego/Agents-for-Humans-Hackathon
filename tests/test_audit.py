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


def test_audit_records_schema_version(tmp_path: Path) -> None:
    path = tmp_path / "audit.jsonl"
    AuditLog(path).record("run.started", run_id="r1")

    record = path.read_text(encoding="utf-8").strip()
    assert '"schema_version": 1' in record


def test_audit_tamper_is_detected(tmp_path: Path) -> None:
    path = tmp_path / "audit.jsonl"
    audit = AuditLog(path)
    audit.record("run.started", run_id="r1")
    audit.record("run.completed", run_id="r1", status="completed")

    lines = path.read_text(encoding="utf-8").splitlines()
    lines[0] = lines[0].replace('"run_id": "r1"', '"run_id": "tampered"')
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    ok, _, error = AuditLog(path).verify_integrity()
    assert ok is False
    assert error is not None


def test_audit_refuses_append_after_tampering(tmp_path: Path) -> None:
    path = tmp_path / "audit.jsonl"
    AuditLog(path).record("run.started", run_id="r1")
    lines = path.read_text(encoding="utf-8").splitlines()
    lines[0] = lines[0].replace('"run_id": "r1"', '"run_id": "tampered"')
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="invalid audit log"):
        AuditLog(path)

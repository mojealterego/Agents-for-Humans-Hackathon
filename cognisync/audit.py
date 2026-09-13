from __future__ import annotations

import hashlib
import json
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class AuditLog:
    """Append-only, hash-chained JSONL audit trail."""

    SCHEMA_VERSION = 1

    def __init__(self, path: str | Path = "data/audit.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._previous_hash = self._load_previous_hash()

    def record(self, event: str, **fields: Any) -> dict[str, Any]:
        if self.path.exists():
            valid, _, error = self.verify_integrity()
            if not valid:
                raise RuntimeError(f"Refusing to append to an invalid audit log: {error}")
        payload = {
            "schema_version": self.SCHEMA_VERSION,
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.now(UTC).isoformat(),
            "event": event,
            "prev_hash": self._previous_hash,
            **fields,
        }
        canonical = self._canonical_payload(payload)
        event_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        payload["event_hash"] = event_hash
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
        self._previous_hash = event_hash
        return payload

    def verify_integrity(self) -> tuple[bool, int, str | None]:
        previous = ""
        checked = 0
        if not self.path.exists():
            return True, 0, None

        for line_no, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                return False, checked, f"line {line_no}: invalid JSON"
            if not isinstance(record, dict):
                return False, checked, f"line {line_no}: record is not an object"
            if record.get("schema_version") != self.SCHEMA_VERSION:
                return False, checked, f"line {line_no}: unsupported schema_version"

            expected_previous = record.get("prev_hash", "")
            if expected_previous != previous:
                return False, checked, f"line {line_no}: prev_hash mismatch"

            supplied_hash = record.get("event_hash")
            if not isinstance(supplied_hash, str):
                return False, checked, f"line {line_no}: missing event_hash"

            unsigned = dict(record)
            unsigned.pop("event_hash", None)
            expected_hash = hashlib.sha256(self._canonical_payload(unsigned).encode("utf-8")).hexdigest()
            if supplied_hash != expected_hash:
                return False, checked, f"line {line_no}: event_hash mismatch"

            previous = supplied_hash
            checked += 1

        return True, checked, None

    @staticmethod
    def _canonical_payload(payload: dict[str, Any]) -> str:
        return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    def _load_previous_hash(self) -> str:
        if not self.path.exists():
            return ""
        valid, _, _ = self.verify_integrity()
        if not valid:
            raise RuntimeError("Existing audit log is invalid; repair or replace it before recording events")
        lines = [line for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not lines:
            return ""
        payload = json.loads(lines[-1])
        return payload["event_hash"]

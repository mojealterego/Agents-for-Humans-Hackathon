from __future__ import annotations

import json
from pathlib import Path

from cognisync.audit import AuditLog
from cognisync.engine import CogniSyncEngine
from cognisync.store import ProjectStore


def main() -> None:
    data_dir = Path("data")
    audit_path = data_dir / "demo-audit.jsonl"
    if audit_path.exists():
        audit_path.unlink()

    engine = CogniSyncEngine(ProjectStore(data_dir), AuditLog(audit_path))

    print("\nCOGNISYNC PROFESSIONAL — LOCAL DEMO\n")

    background = engine.run("prepare today's project brief and identify decision points")
    print("[1/4] BACKGROUND INTELLIGENCE")
    print(json.dumps({
        "status": background.status,
        "summary": background.summary,
        "insights": [
            {
                "title": insight.title,
                "summary": insight.summary,
                "evidence": insight.evidence,
                "evidence_quality": insight.evidence_quality,
            }
            for insight in background.insights
        ],
    }, indent=2, ensure_ascii=False))

    gated = engine.run("prepare and send the client follow-up")
    print("\n[2/4] CONSEQUENCE BOUNDARY")
    print(json.dumps({
        "status": gated.status,
        "decision_id": gated.decision_request.decision_id if gated.decision_request else None,
        "action": gated.decision_request.action if gated.decision_request else None,
        "risk": gated.decision_request.risk.value if gated.decision_request else None,
        "evidence": gated.decision_request.evidence if gated.decision_request else [],
        "policy_fingerprint": gated.decision_request.policy_hash if gated.decision_request else None,
        "proposed_payload_fingerprint": (
            __import__("cognisync.models", fromlist=["payload_fingerprint"])
            .payload_fingerprint(gated.decision_request.proposed_payload)
            if gated.decision_request else None
        ),
        "external_execution": "not_performed",
    }, indent=2, ensure_ascii=False))

    print("\n[3/4] HUMAN RESOLUTION — LOCAL ONLY")
    if gated.decision_request:
        resolution = engine.gate.resolve(gated.decision_request, approved=True, actor="demo-reviewer")
        print(json.dumps({
            "decision_id": resolution.request.decision_id,
            "status": resolution.status.value,
            "authorized_payload_fingerprint": resolution.request.authorized_payload_hash,
            "message": resolution.message,
            "external_execution": "not_performed",
        }, indent=2, ensure_ascii=False))

    ok, checked, error = AuditLog(audit_path).verify_integrity()
    print("\n[4/4] AUDIT INTEGRITY")
    print(json.dumps({"verified": ok, "events_checked": checked, "error": error}, indent=2))
    print(f"\nAudit trail: {audit_path}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .audit import AuditLog
from .decision import DecisionGate
from .engine import CogniSyncEngine
from .policy import DEFAULT_POLICY
from .store import ProjectStore


def _serialize(result: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "run_id": result.run_id,
        "status": result.status,
        "summary": result.summary,
        "insights": [
            {
                "title": insight.title,
                "summary": insight.summary,
                "evidence": insight.evidence,
                "evidence_quality": insight.evidence_quality,
                "recommended_action": insight.recommended_action,
            }
            for insight in result.insights
        ],
        "decision_request": None,
    }
    if result.decision_request:
        decision = result.decision_request
        payload["decision_request"] = {
            "decision_id": decision.decision_id,
            "action": decision.action,
            "risk": decision.risk.value,
            "reason": decision.reason,
            "evidence": decision.evidence,
            "proposed_payload": decision.proposed_payload,
            "decision_status": decision.status.value,
            "policy_fingerprint": decision.policy_hash,
            "authorized_payload_fingerprint": decision.authorized_payload_hash,
            "external_execution": "not_performed",
        }
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="CogniSync background professional agent")
    parser.add_argument("--request", default="Prepare today's project brief and identify decision points.")
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument(
        "--demo-gate",
        action="store_true",
        help="Request an external action to demonstrate HITL gating",
    )
    parser.add_argument(
        "--approve",
        action="store_true",
        help="Resolve a demo decision as approved; never executes a real side effect",
    )
    args = parser.parse_args()

    request = args.request
    if args.demo_gate:
        request = "Prepare the brief and send the external follow-up."

    store = ProjectStore(args.data_dir)
    audit = AuditLog(Path(args.data_dir) / "audit.jsonl")
    result = CogniSyncEngine(store, audit).run(request)

    if result.decision_request and args.approve:
        resolution = DecisionGate(DEFAULT_POLICY, audit).resolve(
            result.decision_request,
            approved=True,
        )
        result.summary += f" {resolution.message} No external side effect was performed by the local demo."

    print(json.dumps(_serialize(result), ensure_ascii=False, indent=2 if args.pretty else None))
    if result.status == "decision_required" and not args.approve:
        print(
            "\nHuman decision required: rerun with --approve only for the local demo resolution path.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()

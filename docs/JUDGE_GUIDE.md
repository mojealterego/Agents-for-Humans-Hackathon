# Judge / Reviewer Guide

## What to evaluate

CogniSync is a background-first professional agent. The core question is not whether it can generate text; it is whether it can absorb repetitive coordination work without silently acquiring authority over consequential outcomes.

The key invariant is:

`prepared ≠ authorized ≠ executed`

## 5-minute path

### 1. Install

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

### 2. Verify the repository

```bash
pytest -q
ruff check .
python scripts/repo_quality_check.py
```

### 3. Run autonomous background work

```bash
python -m cognisync --pretty
```

Expected behavior: local project inputs are processed without an approval prompt; useful insights include source evidence and deterministic evidence-quality scoring; no consequential effect is executed.

### 4. Trigger the consequence boundary

```bash
python -m cognisync --demo-gate --pretty
```

Expected behavior: a `decision_required` result exposes the capability, risk, reason, evidence and proposed payload. The local prototype does not send a real message.

### 5. Resolve the local demo decision

```bash
python -m cognisync --demo-gate --approve --pretty
```

Expected behavior: the decision changes from `pending` to `approved`; the approval is bound to a SHA-256 fingerprint of the exact proposed payload; the audit stream records the transition; no external side effect is claimed.

For an integration that actually calls a trusted connector, execution must be recorded only after connector confirmation. If the approved payload changes, execution is rejected. A successful or failed execution is terminal and cannot be replayed through the same decision object.

Inspect:

```text
data/audit.jsonl
```

The audit stream is hash chained and independently verifiable through `AuditLog.verify_integrity()`.

## What is implemented

- deterministic local project analysis;
- evidence-backed insight objects;
- deterministic evidence-quality scoring rather than fabricated model confidence;
- verification contract;
- model-independent policy classification;
- fail-closed unknown capabilities;
- explicit human decision request;
- terminal decision lifecycle: pending → approved/rejected → executed/failed;
- payload-bound human authorization;
- single-use decision resolution and execution recording;
- deterministic read-only Strands signal-inspection tool;
- tamper-evident audit chain;
- automated positive and negative-path tests;
- validated AWS region/model configuration for the Strands/Bedrock adapter.

## What is not claimed

- no provisioned AWS production environment is represented as complete;
- no real outbound message is sent by the public demo;
- no production MCP connector is silently assumed;
- no performance or productivity percentage is presented without measured evidence;
- no exactly-once external delivery guarantee is claimed.

The Strands/Bedrock adapter and AgentCore-oriented architecture describe the intended production path and should be evaluated separately from the deterministic local proof.

## Reviewer questions the repository should answer

1. What happens when evidence is missing? → verification fails closed.
2. What happens when the requested capability is unknown? → critical risk and approval required.
3. Can approval be reused? → no; resolved decisions cannot be resolved again.
4. Can an executed decision be replayed? → no; execution is terminal.
5. Can an approved payload be swapped before execution? → no; its fingerprint must match the payload fingerprint captured at approval.
6. Can the model's confidence authorize a side effect? → no; policy is model-independent.
7. Can the model-facing tool surface directly perform a side effect? → the included signal-inspection tool is explicitly read-only; consequential connectors remain outside the model's authorization authority.
8. Can a timeout be treated as success? → no; production connectors must require definitive confirmation.
9. Can the audit history be silently edited? → edits break hash-chain verification.

## Evidence map

| Question | File |
|---|---|
| Core orchestration | `cognisync/engine.py` |
| Authorization policy | `cognisync/policy.py` |
| Decision lifecycle | `cognisync/decision.py` |
| Verification contract | `cognisync/verification.py` |
| Audit integrity | `cognisync/audit.py` |
| Attention metrics | `cognisync/metrics.py` |
| Strands/Bedrock adapter + read-only tool | `cognisync/agent.py` |
| Configuration validation | `cognisync/config.py` |
| Threat model | `docs/THREAT_MODEL.md` |
| Research metrics | `docs/EVALUATION_AND_IMPACT_PLAN.md` |
| Claim discipline | `docs/CLAIM_LEDGER.md` |
| Release criteria | `docs/MILESTONE_ACCEPTANCE.md` |
| Grant argument | `docs/GRANT_PROPOSAL.md` |

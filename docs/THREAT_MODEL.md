# CogniSync Professional — Threat Model

## Security objective

Prevent the agent from turning a correct inference into an unauthorized, unverifiable, or irreversible real-world action.

## Threats and controls

| Threat | Example | Primary control | Required evidence |
|---|---|---|---|
| Prompt injection | A document asks the agent to reveal secrets or bypass policy | Treat external content as untrusted; authorization policy is outside content | Policy tests |
| Over-permission | Agent can call destructive tools | Narrow typed capability catalog + explicit action classification | Capability inventory |
| Credential exposure | API key appears in prompt or shell output | Credentials stay at integration boundary; never place secrets in repo | Secret scan / runtime config review |
| Silent side effect | Agent sends or publishes without consent | High/critical capabilities require an explicit decision | Decision-gate tests |
| Hallucinated completion | Agent claims it sent a message | Require connector-confirmed execution status | Connector contract tests |
| Context poisoning | Low-quality memory changes future behavior | Evidence/provenance + controlled memory-write policy | Memory evaluation |
| Runaway execution | Repeated tool loops or budget exhaustion | Invocation, time, output and cancellation limits | Failure-injection tests |
| Tool failure | Timeout, malformed result or ambiguous response | Fail closed; retry only where policy allows and operation semantics are safe | Connector failure tests |
| Replay / payload substitution | An approved message is changed before connector execution | Approval stores a SHA-256 fingerprint of the exact proposed payload; execution rejects a mismatch | Payload-mutation negative test |
| Confused deputy | One actor causes the agent to use another actor's authority | Per-actor identity, least privilege and connector-side authorization | Identity/integration tests |
| Data leakage | Cross-user context appears in output | Per-session/per-actor state partitioning and least privilege | Isolation tests |
| Audit tampering | A record is edited after the fact | Hash-chained audit verification | Integrity tests |

## Trust boundaries

1. **Untrusted input boundary** — documents, messages, web content and external records.
2. **Model boundary** — model output is advisory and is not itself authorization.
3. **Policy boundary** — capability risk is determined independently of model confidence.
4. **Tool boundary** — model-facing tools are narrowly scoped; consequential connectors perform effects only under policy, identity and human authorization controls.
5. **Human boundary** — the human authorizes consequential operations.
6. **Infrastructure boundary** — runtime isolation, IAM, secrets, networking and logging enforce the deployment perimeter.

## Failure semantics

CogniSync follows a conservative state model:

`candidate → verified → prepared → decision_pending → approved/rejected → connector_confirmed`

The system must not infer `connector_confirmed` from intention, model text, HTTP request creation, or a local simulation. Ambiguous or timeout outcomes remain non-success until a trusted connector reports a definitive result.

The repository does not claim exactly-once delivery for external systems. Production connectors must define idempotency, retryability, timeout behavior and reconciliation for each capability.

## Security invariants

- The model never receives raw long-lived credentials.
- Unknown side effects default to critical risk.
- Verification failures block promotion of candidate output.
- Approval is a distinct state from preparation.
- Human approval is bound to the exact payload presented for authorization.
- A payload change after approval invalidates execution for that decision.
- A resolved decision cannot be reused through the decision gate.
- External execution is successful only when a trusted connector confirms it.
- Audit records are produced for important state transitions.
- The audit chain is independently verifiable.
- Synthetic local demo data contains no production secrets.

## Residual risk

No framework, prompt, or policy file can replace infrastructure security. Production operation requires correctly scoped IAM, network boundaries, secret management, connector authentication, observability, rate limits, data retention controls, incident response and continuous adversarial testing.

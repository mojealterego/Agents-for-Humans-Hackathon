# Claim Ledger

This document separates what the submission **demonstrates now** from what it **proposes or hypothesizes**.

| Claim | Status | Verification / evidence |
|---|---|---|
| CogniSync can process local project inputs without a human operating a dashboard continuously. | Implemented | `cognisync/engine.py`, local CLI demo, `tests/test_engine.py` |
| Important insights must carry evidence. | Implemented | `cognisync/verification.py`, `tests/test_verification.py` |
| Safe preparation capabilities remain autonomous under the default policy. | Implemented | `cognisync/policy.py`, `tests/test_policy.py` |
| Consequential capabilities require an explicit decision request. | Implemented | `cognisync/decision.py`, `tests/test_decision_gate.py` |
| Unknown capabilities fail closed as critical. | Implemented | `cognisync/policy.py`, policy and decision-gate tests |
| Approval is a distinct state transition from preparation. | Implemented | `DecisionStatus`, `DecisionGate.resolve()` |
| Approved execution must still be connector-confirmed. | Contract | `DecisionGate.record_execution()` records connector confirmation; the local demo performs no external effect. |
| A resolved or executed decision cannot be reused through the same decision lifecycle. | Implemented | terminal `DecisionStatus` states and `tests/test_decision_gate.py` |
| Audit events are tamper-evident through hash chaining. | Implemented | `cognisync/audit.py`, audit integrity tests |
| Attention metrics distinguish an escalation from an actual human intervention. | Implemented | `cognisync/metrics.py`, `tests/test_metrics.py` |
| Runtime configuration validates region, model identifier and temperature bounds. | Implemented | `cognisync/config.py`, `tests/test_config.py` |
| Strands/Bedrock is the intended model execution path. | Adapter / roadmap | `cognisync/agent.py`; cloud resources are not claimed as provisioned. |
| AgentCore Runtime, Memory, Gateway/MCP and bounded A2A can form the production control plane. | Architecture proposal | `docs/ARCHITECTURE.md` and grant proposal; deployment remains future work. |
| Background-first operation improves useful work per unit of human attention. | Research hypothesis | `docs/EVALUATION_AND_IMPACT_PLAN.md`; requires empirical pilot data. |
| Specific percentage improvements in productivity, trust or time savings. | Not claimed | No numerical performance claim is made without benchmark evidence. |
| Real-world external side effects are executed by the current public demo. | False / explicitly not claimed | The local demo only demonstrates the authorization transition and records simulated resolution. |

## Evidence discipline

Use the following vocabulary consistently in the proposal, README and implementation notes:

- **Implemented** — visible in the repository and covered by executable checks.
- **Contract** — an enforced interface or invariant, but not necessarily a real external integration.
- **Adapter / roadmap** — the production path is designed, but deployment is not represented as complete.
- **Research hypothesis** — measurable proposition that may be falsified.
- **Not claimed** — deliberately excluded until evidence exists.

The project should not convert an architecture diagram, source note, SDK dependency, or future milestone into a claim of operational deployment.

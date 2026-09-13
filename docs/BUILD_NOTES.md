# Build Notes

## Source baseline

The supplied material described CogniSync as a background multi-agent system using Strands Agents, Amazon Bedrock AgentCore Runtime, AgentCore Memory, MCP/Gateway, A2A and Human-in-the-Loop. It also proposed a Python prototype with memory/session management and a CLI-oriented deployment path. The concept is retained, but the implementation is intentionally more conservative and reproducible.

## Improvements made

### 1. Replaced speculative claims with explicit architecture boundaries

The repository does not claim that an AWS resource exists merely because code is prepared for it. Cloud deployment remains an explicit next step.

### 2. Made autonomy a first-class policy

The policy engine is independent from the model. Low-risk work is autonomous; high-risk and unknown capabilities fail closed.

### 3. Added a deterministic local mode

Judges can execute the core without AWS credentials. This lowers the barrier to verification and makes safety behavior testable.

### 4. Added explicit evidence semantics

Insights carry source references and an explicitly named `evidence_quality` field. The score is a deterministic measure of evidence coverage/consistency, not a claim about model confidence or truth probability.

### 5. Added payload- and policy-bound authorization

Human approval is bound to the exact proposed payload and the policy fingerprint active at authorization time. Execution rejects payload substitution and policy drift before a connector outcome can be recorded.

### 6. Added evidence and auditability

Runs and decision gates are recorded in an append-only JSONL audit stream with hash chaining. Important authorization transitions include decision, payload and policy fingerprints.

### 7. Added explicit threat model

Prompt injection, privilege escalation, credential exposure, hallucinated completion, context poisoning and runaway execution are treated as system design concerns rather than prompt-only concerns.

### 8. Kept production security claims proportional to the evidence

The local prototype demonstrates policy enforcement, verification and tamper-evident audit logging. Production isolation and connector hardening remain deployment responsibilities and are not represented as already completed.

### 9. Kept cloud architecture claims proportional to implementation state

The repository documents a production path around Strands Agents, Amazon Bedrock AgentCore and bounded tool/agent protocols, but does not present future integrations as currently provisioned infrastructure.

## Important implementation note

Exact production APIs, IAM configuration, network boundaries, connector contracts and runtime parameters must be pinned and validated in the target deployment environment before cloud rollout. The repository intentionally avoids encoding unverified legacy snippets as guaranteed current interfaces.

## Evidence classification

Public documentation should use four states consistently:

`implemented` → visible and testable now.

`contract` → enforced behavior or interface, without implying a real external integration.

`roadmap` → planned production work not yet demonstrated by the repository.

`hypothesis` → measurable proposition requiring empirical evaluation.

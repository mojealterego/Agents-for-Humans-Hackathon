# Submission Checklist — Agents for Humans Hackathon 2026

## Repository readiness

- [x] Public GitHub repository
- [x] Strands Agents integration surface
- [x] Professional Agents positioning
- [x] Runnable local prototype without cloud credentials
- [x] README with quick start, architecture and scope boundaries
- [x] Mermaid architecture diagram
- [x] MIT license
- [x] Automated tests and CI workflow
- [x] Explicit human decision gate
- [x] Fail-closed unknown-capability policy
- [x] Evidence and provenance model
- [x] Explicit evidence-quality semantics
- [x] Verification contract
- [x] Hash-chained audit trail
- [x] Payload-fingerprint-bound authorization
- [x] Policy-fingerprint-bound authorization
- [x] Policy-drift and payload-substitution negative paths
- [x] Judgeable five-minute demo scenario
- [x] Final English grant proposal
- [x] Threat model
- [x] Evaluation and impact plan
- [x] Claim ledger
- [x] Milestone acceptance criteria
- [x] Reproducibility protocol
- [x] Data governance boundary

## Final submission actions

- [ ] Confirm current hackathon registration and entry requirements on the official submission platform
- [ ] Confirm final submission form fields and required URLs
- [ ] Record final demo video within the published time limit
- [ ] Add the final demo URL to the submission
- [ ] Confirm any current AWS credit or program request requirements from the official program page
- [ ] Perform a clean-room clone/install/test from the public repository
- [ ] Run `pytest -q`
- [ ] Run `ruff check .`
- [ ] Run `python scripts/repo_quality_check.py`
- [ ] Review `docs/CLAIM_LEDGER.md` against the final submission wording

## What the demo must prove

1. Background work happens without continuous human supervision.
2. Important outputs retain evidence.
3. Evidence quality is explicitly distinguished from model confidence.
4. A consequential capability crosses an explicit policy boundary.
5. Approval is a distinct state transition.
6. Approval is bound to the exact payload and active policy fingerprint.
7. Payload substitution and policy drift fail closed.
8. A resolved decision cannot be reused through the decision gate.
9. Unknown capabilities fail closed.
10. Audit integrity can detect tampering.
11. No external completion is claimed without trusted connector confirmation.

## Current honest scope

The repository contains a functional local prototype and production-oriented architecture. Live cloud deployment, real MCP integrations, external notification channels, durable production memory and cloud telemetry remain environment-specific implementation steps and must not be represented as already deployed unless they have been provisioned and verified.

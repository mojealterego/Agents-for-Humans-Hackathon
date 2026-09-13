# CogniSync Professional

> **A background-first professional agent that owns repetitive coordination work while humans retain authority over consequential decisions.**

**Grant submission repository — Agents for Humans Hackathon 2026**

**Applicant:** Andrzej Mikulski  
**Track:** Professional Agents  
**Primary artifact:** `cognisync/`  
**Grant proposal:** [`docs/GRANT_PROPOSAL_FINAL.md`](docs/GRANT_PROPOSAL_FINAL.md)  
**Full proposal archive:** [`docs/GRANT_PROPOSAL.md`](docs/GRANT_PROPOSAL.md)

---

## The thesis

> **Let the agent own the repetition. Let the human own the consequence.**

CogniSync is designed for professionals who are overloaded by coordination work rather than by the absence of another chat interface. It runs a controlled workflow:

`observe → interpret → verify → prepare → evaluate consequence → act or wait → audit`

The key authorization invariant is:

`prepared ≠ authorized ≠ executed`

Routine read/analyze/prepare work can remain autonomous. Consequential operations require an explicit decision request. Unknown capabilities fail closed.

## What this repository proves today

The public prototype is deterministic and runnable without cloud credentials. It demonstrates:

- evidence-backed insight generation;
- explicit evidence-quality scoring rather than a misleading model-confidence field;
- verification gates before work is promoted;
- model-independent autonomy policy;
- a bounded, read-only Strands custom tool for project-signal inspection;
- human decision requests for consequential capabilities;
- single-use approval/rejection transitions;
- authorization bound to the exact proposed payload;
- authorization bound to the policy fingerprint active when the decision was created;
- prevention of execution before approval, after payload modification, or across policy drift;
- tamper-evident, schema-versioned hash-chained audit events;
- refusal to append to a corrupted audit history;
- automated tests for positive and failure paths;
- a local demo that never pretends to perform a real external side effect.

The Strands/Bedrock integration is an adapter and production path, not a claim that cloud resources are already provisioned. The model can reason and invoke bounded read-only tooling, but it cannot authorize consequential execution.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest -q
ruff check .
python scripts/repo_quality_check.py
```

Run the core demo:

```bash
python -m cognisync --pretty
```

Demonstrate the consequence boundary:

```bash
python -m cognisync --demo-gate --pretty
python -m cognisync --demo-gate --approve --pretty
```

The `--approve` path resolves a **local demo decision only**. No real email, publication, payment, calendar mutation, CRM update or deletion is performed by the public prototype.

## Architecture

```text
                    ┌──────────────────────────────┐
                    │ Strands / Bedrock Reasoning   │
                    │ proposes, interprets, plans  │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │ Bounded Read-Only Tools      │
                    │ project-signal inspection    │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │ Evidence + Context           │
                    │ provenance / source signals  │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │ Deterministic Verification   │
                    │ evidence + integrity checks  │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │ Policy / Consequence Gate    │
                    │ model-independent authority  │
                    │ policy fingerprint           │
                    └──────────────┬───────────────┘
                                   │
                          consequential only
                                   │
                    ┌──────────────▼───────────────┐
                    │ Human Decision               │
                    │ approve / reject             │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │ Trusted Connector Boundary   │
                    │ payload fingerprint checked  │
                    │ policy fingerprint checked   │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │ Hash-Chained Audit           │
                    └──────────────────────────────┘
```

The architectural rule is stronger than a prompt instruction: **reasoning is not authorization**. A model output, tool result, or proposed action cannot cross the consequence boundary without deterministic policy evaluation and explicit human resolution. The approval is bound to both the exact payload and the policy fingerprint under which the decision was created.

## Repository map

| Path | Purpose |
|---|---|
| `cognisync/` | Core engine, policy, verification, decision gate, audit and adapters |
| `tests/` | Executable safety and behavior checks |
| `docs/GRANT_PROPOSAL_FINAL.md` | Submission-ready grant proposal aligned with the hardened prototype |
| `docs/GRANT_PROPOSAL.md` | Earlier full proposal archive |
| `docs/CLAIM_LEDGER.md` | Distinguishes implemented behavior from contracts, roadmap and hypotheses |
| `docs/MILESTONE_ACCEPTANCE.md` | Objective milestone and release acceptance criteria |
| `docs/EVALUATION_AND_IMPACT_PLAN.md` | Research protocol and measurement plan |
| `docs/ARCHITECTURE.md` | Detailed system architecture and production evolution |
| `docs/THREAT_MODEL.md` | Threats, trust boundaries and security invariants |
| `docs/DEMO_SCENARIO_V2.md` | Five-minute judge demonstration |
| `docs/JUDGE_GUIDE.md` | Reviewer-oriented inspection path |
| `scripts/repo_quality_check.py` | Public-repository hygiene and syntax gate |

## Evidence discipline

Documentation uses explicit evidence states:

**implemented** — visible and testable in this repository.  
**contract** — an enforced interface/invariant without implying an external deployment.  
**roadmap** — planned production work.  
**hypothesis** — a proposition requiring measurement.

See [`docs/CLAIM_LEDGER.md`](docs/CLAIM_LEDGER.md).

## Scope and non-goals

CogniSync is not a universal autonomous operating system and is not designed to maximize unchecked agent activity. The prototype does not autonomously perform high-consequence external actions. It also does not turn covert persuasion material into an operational manipulation system.

The goal is narrower and measurable: **maximize useful work per unit of human supervisory attention while keeping consequential authority explicit.**

## Status

This repository is the hackathon/grant artifact. The broader research portfolio and source-derived knowledge base live separately in [`Open-AI-Agents-`](https://github.com/fotografandrzejmikulski-bit/Open-AI-Agents-).

## License

MIT.

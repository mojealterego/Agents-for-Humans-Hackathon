from cognisync.models import RiskLevel
from cognisync.policy import AutonomyPolicy, DEFAULT_POLICY


def test_safe_work_stays_autonomous() -> None:
    assert DEFAULT_POLICY.classify("draft_report") == RiskLevel.LOW
    assert DEFAULT_POLICY.requires_approval("draft_report") is False


def test_external_side_effect_is_gated() -> None:
    assert DEFAULT_POLICY.classify("send_external_message") == RiskLevel.HIGH
    assert DEFAULT_POLICY.requires_approval("send_external_message") is True


def test_unknown_action_is_fail_closed() -> None:
    assert DEFAULT_POLICY.classify("unknown_side_effect") == RiskLevel.CRITICAL
    assert DEFAULT_POLICY.requires_approval("unknown_side_effect") is True


def test_policy_fingerprint_is_stable_and_changes_with_rules() -> None:
    equivalent = AutonomyPolicy(
        frozenset(reversed(tuple(DEFAULT_POLICY.safe_actions))),
        frozenset(reversed(tuple(DEFAULT_POLICY.approval_actions))),
    )
    assert equivalent.fingerprint == DEFAULT_POLICY.fingerprint

    changed = AutonomyPolicy(
        DEFAULT_POLICY.safe_actions,
        DEFAULT_POLICY.approval_actions | frozenset({"new_consequential_capability"}),
    )
    assert changed.fingerprint != DEFAULT_POLICY.fingerprint

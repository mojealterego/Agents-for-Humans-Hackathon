from cognisync.analysis import analyze_items
from cognisync.models import ProjectItem


def test_analysis_extracts_pending_signals_and_evidence() -> None:
    items = [
        ProjectItem("1", "email", "Launch", "Homepage review is pending before launch."),
        ProjectItem("2", "notes", "Accessibility", "Accessibility checks are still pending."),
    ]
    insights, evidence = analyze_items(items)
    assert insights
    assert "pending" in insights[0].summary.lower()
    assert evidence == ["email: Launch", "notes: Accessibility"]
    assert 0.0 <= insights[0].confidence <= 1.0


def test_evidence_quality_rewards_complete_multi_source_evidence() -> None:
    items = [
        ProjectItem("1", "drive", "Brief", "deadline pending client review"),
        ProjectItem("2", "calendar", "Meeting", "delivery remaining"),
        ProjectItem("3", "crm", "Lead", "follow-up needs scheduling"),
    ]
    insights, evidence = analyze_items(items)

    assert len(evidence) == 3
    assert insights[0].confidence == 0.88
    assert "Brief" in insights[0].summary


def test_evidence_quality_caps_repeated_single_source() -> None:
    item = ProjectItem("1", "drive", "Brief", "deadline pending")
    insights, _ = analyze_items([item, item])

    assert insights[0].confidence == 0.82
    assert insights[0].confidence < 0.88

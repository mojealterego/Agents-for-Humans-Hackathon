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
    assert insights[0].evidence_quality == 0.9


def test_analysis_quality_reflects_source_coverage() -> None:
    one = ProjectItem("1", "email", "Launch", "Review pending")
    many = [
        one,
        ProjectItem("2", "notes", "QA", "Accessibility review"),
        ProjectItem("3", "calendar", "Launch", "Release review"),
    ]
    one_score = analyze_items([one])[0][0].evidence_quality
    many_score = analyze_items(many)[0][0].evidence_quality
    assert one_score < many_score
    assert 0.0 <= one_score <= 1.0
    assert 0.0 <= many_score <= 1.0


def test_empty_analysis_has_zero_evidence_quality() -> None:
    insights, evidence = analyze_items([])
    assert insights[0].evidence_quality == 0.0
    assert evidence == []

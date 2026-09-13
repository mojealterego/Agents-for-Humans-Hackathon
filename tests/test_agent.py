from cognisync.agent import _inspect_signal


def test_inspect_project_signal_is_read_only_and_structured() -> None:
    result = _inspect_signal("deadline pending; review needed before delivery")

    assert result["word_count"] == 6
    assert result["coordination_signals"] == {"pending": 1, "review": 1}
    assert result["side_effects_performed"] is False

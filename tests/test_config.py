import pytest

from cognisync.config import Settings


def test_settings_accept_valid_values() -> None:
    settings = Settings(region="eu-central-1", model_id="model", temperature=0.7)
    assert settings.region == "eu-central-1"
    assert settings.model_id == "model"
    assert settings.temperature == 0.7


def test_settings_reject_invalid_temperature() -> None:
    with pytest.raises(ValueError, match="temperature"):
        Settings(temperature=2.1)


def test_settings_reject_empty_region() -> None:
    with pytest.raises(ValueError, match="region"):
        Settings(region="   ")

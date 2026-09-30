import pytest
from pydantic import ValidationError

from masamune.settings import Settings


def test_independence_rejects_same_provider_and_model() -> None:
    with pytest.raises(ValidationError):
        Settings(
            masa_provider_id="same",
            masa_model="model",
            mune_provider_id="same",
            mune_model="model",
            require_independence=True,
        )


def test_shared_provider_is_rejected_when_independence_required() -> None:
    with pytest.raises(ValidationError):
        Settings(
            masa_provider_id="same",
            masa_model="model-a",
            mune_provider_id="same",
            mune_model="model-b",
            require_independence=True,
        )


def test_shared_provider_allowed_only_when_independence_disabled() -> None:
    settings = Settings(
        masa_provider_id="same",
        masa_model="model-a",
        mune_provider_id="same",
        mune_model="model-b",
        require_independence=False,
    )
    assert settings.require_independence is False

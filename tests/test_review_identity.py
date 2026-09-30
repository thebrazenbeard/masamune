from masamune.context import ReviewContext
from masamune.models import Subject
from masamune.orchestrator import review_id_for
from masamune.policy import RepoPolicy
from masamune.settings import Settings


def _context() -> ReviewContext:
    return ReviewContext(
        subject=Subject(
            repository="owner/repo",
            kind="PULL_REQUEST",
            number=1,
            head_sha="a" * 40,
            base_sha="b" * 40,
            title="test",
            url="https://github.com/owner/repo/pull/1",
        ),
        text="source",
        policy=RepoPolicy(),
    )


def test_review_identity_changes_with_sampling_configuration() -> None:
    context = _context()
    settings = Settings(
        masa_provider_id="groq",
        masa_model="model-a",
        mune_provider_id="google",
        mune_model="model-b",
        masa_base_url="https://masa.example/v1",
        mune_base_url="https://mune.example/v1",
    )
    base = review_id_for(context, settings)
    assert base != review_id_for(
        context, settings.model_copy(update={"masa_temperature": 0.5})
    )
    assert base != review_id_for(
        context, settings.model_copy(update={"mune_temperature": 0.5})
    )
    assert base != review_id_for(
        context, settings.model_copy(update={"masa_base_url": "https://other.example/v1"})
    )
import pytest


@pytest.mark.challenge
def test_user_never_gets_alert_for_project_without_access() -> None:
    """
    Starter failing invariant test.

    Replace this with an end-to-end or integration-level test once the
    subscription model, alert generation worker, and alert API/UI are added.
    """
    assert False, (
        "TODO: implement permission invariant test: candidate_user must not "
        "receive alerts containing issues from project-b or shadow-private."
    )

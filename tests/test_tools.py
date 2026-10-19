import pytest

from assistant_core.errors import InvalidRequest
from assistant_core.tools import parse_credits, tuition


def test_parse_with_retake() -> None:
    assert parse_credits("tuition for 18 credits and 2 retake") == (18, 2)


def test_parse_without_retake() -> None:
    assert parse_credits("tuition for 18 credits") == (18, 0)


def test_parse_retake_without_credit_count_raises() -> None:
    with pytest.raises(InvalidRequest):
        parse_credits("2 retake")


def test_tuition_value_matches_lab_example() -> None:
    assert tuition(18, 2, 450_000, 1.5, 30) == 9_450_000


@pytest.mark.parametrize("credits", [0, 31, -1])
def test_tuition_rejects_credit_count_out_of_range(credits: int) -> None:
    with pytest.raises(InvalidRequest):
        tuition(credits, 0, 450_000, 1.5, 30)


def test_tuition_rejects_negative_retake_credits() -> None:
    with pytest.raises(InvalidRequest):
        tuition(10, -1, 450_000, 1.5, 30)

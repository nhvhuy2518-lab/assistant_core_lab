import pytest

from assistant_core.errors import InvalidRequest
from assistant_core.tools import parse_credits, tuition


def test_parse_with_retake():
    assert parse_credits("tuition for 18 credits and 2 retake") == (18, 2)


def test_tuition_value():
    # Characterisation test: 18 * 450k + 2 * 450k * 1.5 = 9,450,000 VND
    assert tuition(18, 2, 450_000, 1.5, 30) == 9_450_000


@pytest.mark.parametrize("credits", [0, 31])
def test_tuition_out_of_range(credits):
    with pytest.raises(InvalidRequest):
        tuition(credits, 0, 450_000, 1.5, 30)

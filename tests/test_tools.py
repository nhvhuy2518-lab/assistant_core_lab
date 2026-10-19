
import pytest

from assistant_core.errors import InvalidRequest
from assistant_core.tools import parse_credits, tuition


def test_parse_credits_with_retake():
    """Parse credits and retake credits from a complete message."""
    result = parse_credits("tuition for 18 credits and 2 retake")
    assert result == (18, 2)


def test_parse_credits_without_retake():
    """A message without retake should have zero retake credits."""
    result = parse_credits("tuition for 18 credits")
    assert result == (18, 0)


def test_parse_credits_without_credits():
    """Raise InvalidRequest when no credit number is provided."""
    with pytest.raises(InvalidRequest):
        parse_credits("How much is the tuition?")


def test_tuition_characterisation():
    """Preserve the tuition result from the original program."""
    result = tuition(18, 2, 450_000, 1.5, 30)
    assert result == 9_450_000


@pytest.mark.parametrize("credits", [0, 31])
def test_tuition_out_of_range(credits):
    """Reject credits outside the permitted range."""
    with pytest.raises(InvalidRequest):
        tuition(credits, 0, 450_000, 1.5, 30)


def test_tuition_without_retake():
    """Calculate tuition when there are no retake credits."""
    result = tuition(18, 0, 450_000, 1.5, 30)
    assert result == 8_100_000

import pytest

from assistant_core.models import Intent
from assistant_core.router import route


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("hello", Intent.GREETING),
        ("Hi!", Intent.GREETING),
        ("tuition for 18 credits", Intent.FEE),
        ("How much is the fee?", Intent.FEE),
        ("Where is the Library?", Intent.OFFICE),
        ("thesis registration credits", Intent.RULE),
    ],
)
def test_route_by_intent(text: str, expected: Intent) -> None:
    assert route(text, {"library", "student affairs"}) is expected

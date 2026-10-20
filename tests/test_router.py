from assistant_core.models import Intent
from assistant_core.router import route

OFFICES = {"library", "academic affairs"}


def test_route_greeting():
    assert route("hello", OFFICES) == Intent.GREETING


def test_route_fee():
    assert route("how much is the tuition for 10 credits?", OFFICES) == Intent.FEE


def test_route_office():
    assert route("where is the library?", OFFICES) == Intent.OFFICE


def test_route_rule():
    assert route("what is the rule for thesis registration?", OFFICES) == Intent.RULE
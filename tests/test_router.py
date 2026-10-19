
from assistant_core.models import Intent
from assistant_core.router import route


def test_route_greeting():
    assert route("hello!", set()) == Intent.GREETING


def test_route_fee():
    assert route("tuition for 18 credits", set()) == Intent.FEE


def test_route_office():
    assert route("where is library?", {"library"}) == Intent.OFFICE


def test_route_rule():
    assert route("exam absence policy", set()) == Intent.RULE


def test_route_case_insensitive():
    assert route("HELLO", set()) == Intent.GREETING


def test_route_with_spaces():
    assert route("  hello!  ", set()) == Intent.GREETING

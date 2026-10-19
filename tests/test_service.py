import pytest
from pydantic import ValidationError

from assistant_core.errors import InvalidRequest
from assistant_core.models import Intent, Message
from assistant_core.responder import StubLLMResponder


def test_greeting_response(service) -> None:
    response = service.handle(Message(text="hello"))
    assert response.intent is Intent.GREETING
    assert "help" in response.answer.lower()


def test_fee_response(service) -> None:
    response = service.handle(Message(text="tuition for 18 credits and 2 retake"))
    assert response.intent is Intent.FEE
    assert "9,450,000 VND" in response.answer


def test_office_response(service) -> None:
    response = service.handle(Message(text="Where is the Library?"))
    assert response.intent is Intent.OFFICE
    assert "B.201" in response.answer


def test_rule_response_includes_source(service) -> None:
    response = service.handle(Message(text="thesis registration credits"))
    assert response.intent is Intent.RULE
    assert response.sources[0].id == "H26-5.3"


def test_unknown_rule_returns_unknown_intent(service) -> None:
    response = service.handle(Message(text="quantum teleportation"))
    assert response.intent is Intent.UNKNOWN
    assert not response.sources


def test_fallback_when_provider_fails(service) -> None:
    service.responder = StubLLMResponder(fail=True)
    response = service.handle(Message(text="thesis registration credits"))
    assert response.degraded is True
    assert response.sources
    assert "Thesis registration" in response.answer


def test_empty_message_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Message(text="")


def test_fee_request_without_credits_raises(service) -> None:
    with pytest.raises(InvalidRequest):
        service.handle(Message(text="tuition fee please"))

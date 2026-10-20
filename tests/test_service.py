import pytest
from pydantic import ValidationError
from assistant_core.models import Intent, Message
from assistant_core.responder import StubLLMResponder


def test_service_greeting(service):
    res = service.handle(Message(text="hi"))
    assert res.intent == Intent.GREETING
    assert "Hello!" in res.answer


def test_service_fee(service):
    res = service.handle(Message(text="tuition for 18 credits and 2 retake"))
    assert res.intent == Intent.FEE
    assert "9,450,000" in res.answer


def test_service_office(service):
    res = service.handle(Message(text="where is the library?"))
    assert res.intent == Intent.OFFICE
    assert "B.201" in res.answer


def test_fallback_when_provider_fails(service):
    service.responder = StubLLMResponder(fail=True)
    r = service.handle(Message(text="thesis registration credits"))
    assert r.degraded is True
    assert len(r.sources) > 0


def test_empty_message_rejected():
    with pytest.raises(ValidationError):
        Message(text="")
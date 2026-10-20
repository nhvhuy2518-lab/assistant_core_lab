"""Integration and unit tests for AssistantService."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from assistant_core.config import Settings
from assistant_core.knowledge import Handbook, OfficeDirectory
from assistant_core.models import Intent, Message
from assistant_core.responder import StubLLMResponder
from assistant_core.service import AssistantService


@pytest.fixture
def service():
    data_dir = Path("data")
    settings = Settings(data_dir=data_dir)
    offices = OfficeDirectory.from_csv(data_dir / "offices.csv")
    handbook = Handbook.from_json(data_dir / "handbook.json")
    responder = StubLLMResponder(fail=False)
    return AssistantService(settings, offices, handbook, responder)


def test_greeting_intent(service):
    res = service.handle(Message(text="xin chao"))
    assert res.intent == Intent.GREETING
    assert "Hello!" in res.answer
    assert not res.degraded


def test_fee_intent(service):
    res = service.handle(Message(text="tuition for 18 credits and 2 retake"))
    assert res.intent == Intent.FEE
    assert "9,450,000 VND" in res.answer
    assert not res.degraded


def test_office_intent(service):
    res = service.handle(Message(text="where is the library"))
    assert res.intent == Intent.OFFICE
    assert "library" in res.answer.lower()
    assert "B.201" in res.answer
    assert not res.degraded


def test_rule_normal_with_responder(service):
    res = service.handle(Message(text="graduation requirements"))
    assert res.intent == Intent.RULE
    assert len(res.sources) == 1
    assert res.sources[0].id == "H26-1.1"
    assert not res.degraded
    assert "Based on 'Graduation Requirements'" in res.answer


def test_fallback_when_provider_fails(service):
    """Test required fallback mechanism: degraded flag and template answer."""
    service.responder = StubLLMResponder(fail=True)
    res = service.handle(Message(text="graduation requirements"))
    assert res.intent == Intent.RULE
    assert res.degraded is True
    assert len(res.sources) == 1
    assert "Graduation Requirements:" in res.answer


def test_empty_message_validation():
    """Empty messages must be rejected by Pydantic Message boundary."""
    with pytest.raises(ValidationError):
        Message(text="")
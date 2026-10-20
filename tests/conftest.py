import pytest
from assistant_core.config import Settings
from assistant_core.knowledge import Handbook, Office, OfficeDirectory, Rule
from assistant_core.responder import StubLLMResponder
from assistant_core.service import AssistantService


@pytest.fixture
def dummy_settings():
    return Settings(credit_rate_vnd=450_000, retake_multiplier=1.5, max_credits=30)


@pytest.fixture
def dummy_offices():
    return OfficeDirectory({"library": Office("Library", "B.201", "Mon-Sat 07:00-20:00")})


@pytest.fixture
def dummy_handbook():
    return Handbook([Rule("H26-5.3", "Thesis Registration Credits", "Thesis requires 110 credits.")])


@pytest.fixture
def service(dummy_settings, dummy_offices, dummy_handbook):
    responder = StubLLMResponder(fail=False)
    return AssistantService(dummy_settings, dummy_offices, dummy_handbook, responder)
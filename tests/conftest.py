from pathlib import Path

import pytest

from assistant_core.config import Settings
from assistant_core.knowledge import Handbook, Office, OfficeDirectory, Rule
from assistant_core.responder import StubLLMResponder
from assistant_core.service import AssistantService

DATA = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture
def dummy_settings():
    return Settings(credit_rate_vnd=450_000, retake_multiplier=1.5, max_credits=30)


@pytest.fixture
def settings():
    return Settings(data_dir=DATA)


@pytest.fixture
def dummy_offices():
    return OfficeDirectory({"library": Office("Library", "B.201", "Mon-Sat 07:00-20:00")})


@pytest.fixture
def dummy_handbook():
    return Handbook([Rule("H26-5.3", "Thesis Registration Credits", "Thesis requires 110 credits.")])


@pytest.fixture
def service(settings):
    return AssistantService(
        settings,
        OfficeDirectory.from_csv(DATA / "offices.csv"),
        Handbook.from_json(DATA / "handbook.json"),
        StubLLMResponder(),
    )

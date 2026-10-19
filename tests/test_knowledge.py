from pathlib import Path

import pytest

from assistant_core.errors import DataError
from assistant_core.knowledge import Handbook, OfficeDirectory


def test_office_directory_finds_office(knowledge_dir: Path) -> None:
    offices = OfficeDirectory.from_csv(knowledge_dir / "offices.csv")
    office = offices.find("Where is the Library?")
    assert office is not None
    assert office.room == "B.201"


def test_missing_office_file_raises_data_error(tmp_path: Path) -> None:
    with pytest.raises(DataError):
        OfficeDirectory.from_csv(tmp_path / "missing.csv")


def test_handbook_search_returns_rule(knowledge_dir: Path) -> None:
    handbook = Handbook.from_json(knowledge_dir / "handbook.json")
    rule = handbook.search("thesis registration")
    assert rule is not None
    assert rule.id == "H26-5.3"


def test_malformed_handbook_raises_data_error(tmp_path: Path) -> None:
    path = tmp_path / "handbook.json"
    path.write_text("{not json}", encoding="utf-8")
    with pytest.raises(DataError):
        Handbook.from_json(path)

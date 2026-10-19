from pathlib import Path

import pytest

from assistant_core.errors import DataError
from assistant_core.knowledge import Handbook, OfficeDirectory

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def test_office_directory_loads_and_finds_library() -> None:
    directory = OfficeDirectory.from_csv(DATA_DIR / "offices.csv")
    assert "library" in directory.names
    office = directory.find("Where is the Library located?")
    assert office is not None
    assert office.name.lower() == "library"
    assert office.room != ""


def test_office_directory_returns_none_when_no_match() -> None:
    directory = OfficeDirectory.from_csv(DATA_DIR / "offices.csv")
    assert directory.find("Where is the swimming pool?") is None


def test_office_directory_missing_file_raises_data_error(tmp_path: Path) -> None:
    with pytest.raises(DataError):
        OfficeDirectory.from_csv(tmp_path / "missing_offices.csv")


def test_office_directory_malformed_csv_raises_data_error(tmp_path: Path) -> None:
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("wrong_col1,wrong_col2\nval1,val2\n", encoding="utf-8")
    with pytest.raises(DataError):
        OfficeDirectory.from_csv(bad_csv)


def test_handbook_loads_and_searches_by_keyword_overlap() -> None:
    handbook = Handbook.from_json(DATA_DIR / "handbook.json")
    rule = handbook.search("thesis registration credits")
    assert rule is not None
    assert rule.id != ""
    assert rule.title != ""


def test_handbook_search_returns_none_for_unrelated_query() -> None:
    handbook = Handbook.from_json(DATA_DIR / "handbook.json")
    assert handbook.search("xyz123nonexistentword999") is None


def test_handbook_missing_file_raises_data_error(tmp_path: Path) -> None:
    with pytest.raises(DataError):
        Handbook.from_json(tmp_path / "missing_handbook.json")


def test_handbook_malformed_json_raises_data_error(tmp_path: Path) -> None:
    bad_json = tmp_path / "bad.json"
    bad_json.write_text("{not valid json", encoding="utf-8")
    with pytest.raises(DataError):
        Handbook.from_json(bad_json)

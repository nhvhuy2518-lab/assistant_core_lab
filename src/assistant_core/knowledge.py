"""Load and search office and handbook data."""

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from assistant_core.errors import DataError


@dataclass(frozen=True)
class Office:
    name: str
    room: str
    hours: str


@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    text: str
    keywords: tuple[str, ...]


class OfficeDirectory:
    def __init__(self, offices: dict[str, Office]) -> None:
        self._offices = dict(offices)

    @classmethod
    def from_csv(cls, path: Path) -> "OfficeDirectory":
        try:
            with path.open(encoding="utf-8", newline="") as file:
                rows = list(csv.DictReader(file))
        except OSError as exc:
            raise DataError(f"Office file could not be read: {path}") from exc

        if rows and not {"name", "room", "hours"}.issubset(rows[0]):
            raise DataError("Office CSV must contain name, room, and hours columns.")
        if not rows:
            raise DataError("Office CSV is empty or has no data rows.")
        try:
            offices = {
                row["name"].strip().lower(): Office(
                    name=row["name"].strip(),
                    room=row["room"].strip(),
                    hours=row["hours"].strip(),
                )
                for row in rows
            }
        except (KeyError, AttributeError) as exc:
            raise DataError("Office CSV contains an invalid row.") from exc
        if any(not office.name or not office.room or not office.hours for office in offices.values()):
            raise DataError("Office CSV rows must not contain blank values.")
        return cls(offices)

    @property
    def names(self) -> set[str]:
        return set(self._offices)

    def find(self, text: str) -> Office | None:
        normalized = text.lower()
        return next((office for name, office in self._offices.items() if name in normalized), None)


class Handbook:
    def __init__(self, rules: list[Rule]) -> None:
        self._rules = tuple(rules)

    @classmethod
    def from_json(cls, path: Path) -> "Handbook":
        try:
            with path.open(encoding="utf-8") as file:
                raw: Any = json.load(file)
        except (OSError, json.JSONDecodeError) as exc:
            raise DataError(f"Handbook file could not be read or parsed: {path}") from exc
        if not isinstance(raw, list) or not raw:
            raise DataError("Handbook JSON must be a non-empty list of rules.")

        rules: list[Rule] = []
        try:
            for item in raw:
                if not isinstance(item, dict):
                    raise TypeError
                keywords = item.get("keywords", [])
                if not isinstance(keywords, list):
                    raise TypeError
                rules.append(
                    Rule(
                        id=str(item["id"]),
                        title=str(item["title"]),
                        text=str(item["text"]),
                        keywords=tuple(str(word).lower() for word in keywords),
                    )
                )
        except (KeyError, TypeError, ValueError) as exc:
            raise DataError("Each handbook rule needs id, title, text, and a keywords list.") from exc
        return cls(rules)

    def search(self, query: str) -> Rule | None:
        """Return the rule with the most keyword overlaps, or None if no keyword matches."""
        words = set(query.lower().split())
        best_rule: Rule | None = None
        best_score = 0
        for rule in self._rules:
            score = sum(1 for keyword in rule.keywords if keyword in words)
            if score > best_score:
                best_rule = rule
                best_score = score
        return best_rule

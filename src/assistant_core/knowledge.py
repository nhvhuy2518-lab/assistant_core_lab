from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path

from assistant_core.errors import DataError


@dataclass(frozen=True)
class Office:
    name: str
    room: str
    hours: str


class OfficeDirectory:
    def __init__(self, offices: dict[str, Office]) -> None:
        self._offices = offices

    @classmethod
    def from_csv(cls, path: Path) -> OfficeDirectory:
        try:
            with path.open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
        except FileNotFoundError as exc:
            raise DataError(f"office file not found: {path}") from exc
        except (OSError, csv.Error, UnicodeDecodeError) as exc:
            raise DataError(f"failed to read office file: {path}") from exc

        try:
            offices = {
                r["name"].strip().lower(): Office(
                    name=r["name"].strip(),
                    room=r["room"].strip(),
                    hours=r["hours"].strip(),
                )
                for r in rows
            }
        except (KeyError, AttributeError, TypeError) as exc:
            raise DataError(f"malformed office CSV schema in: {path}") from exc

        return cls(offices)

    @property
    def names(self) -> set[str]:
        return set(self._offices)

    def find(self, text: str) -> Office | None:
        t = text.lower()
        return next((o for name, o in self._offices.items() if name in t), None)


@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    text: str
    keywords: tuple[str, ...] = ()


class Handbook:
    def __init__(self, rules: list[Rule]) -> None:
        self._rules = list(rules)

    @classmethod
    def from_json(cls, path: Path) -> Handbook:
        try:
            with path.open(encoding="utf-8") as f:
                raw_data = json.load(f)
        except FileNotFoundError as exc:
            raise DataError(f"handbook file not found: {path}") from exc
        except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise DataError(f"malformed handbook JSON in: {path}") from exc

        if isinstance(raw_data, dict):
            items = raw_data.get("rules", [])
        elif isinstance(raw_data, list):
            items = raw_data
        else:
            raise DataError(f"handbook JSON must be a list or dict: {path}")

        rules: list[Rule] = []
        try:
            for item in items:
                kw = item.get("keywords", [])
                keywords = tuple(str(k).lower() for k in kw) if isinstance(kw, list) else ()
                rules.append(
                    Rule(
                        id=str(item["id"]),
                        title=str(item["title"]),
                        text=str(item.get("text") or item.get("body") or item.get("content") or ""),
                        keywords=keywords,
                    )
                )
        except (KeyError, TypeError, AttributeError) as exc:
            raise DataError(f"missing required fields in handbook: {path}") from exc

        return cls(rules)

    @property
    def rules(self) -> list[Rule]:
        return list(self._rules)

    def search(self, query: str) -> Rule | None:
        q_tokens = set(re.findall(r"\w+", query.lower()))
        if not q_tokens:
            return None

        best_rule: Rule | None = None
        best_score = 0

        for rule in self._rules:
            rule_tokens = set(re.findall(r"\w+", f"{rule.title} {rule.text}".lower()))
            rule_tokens.update(rule.keywords)
            score = len(q_tokens & rule_tokens)
            if score > best_score:
                best_score = score
                best_rule = rule

        return best_rule

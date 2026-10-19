"""Replaceable response-generation interface and offline implementations."""

from typing import Protocol

from assistant_core.errors import ProviderError
from assistant_core.knowledge import Rule


class Responder(Protocol):
    def explain(self, question: str, rule: Rule) -> str:
        """Generate an answer grounded in a handbook rule."""
        ...


class TemplateResponder:
    def explain(self, question: str, rule: Rule) -> str:
        del question
        return f"{rule.title}: {rule.text}"


class StubLLMResponder:
    """Predictable stand-in for a provider; never makes a network call."""

    def __init__(self, fail: bool = False) -> None:
        self.fail = fail

    def explain(self, question: str, rule: Rule) -> str:
        del question
        if self.fail:
            raise ProviderError("Stub provider unavailable.")
        return f"Based on '{rule.title}': {rule.text}"

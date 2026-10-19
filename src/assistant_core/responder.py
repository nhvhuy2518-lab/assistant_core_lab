"""Responder interface and implementations for generating rule explanations."""

from typing import Protocol

from assistant_core.errors import ProviderError
from assistant_core.models import Rule


class Responder(Protocol):
    """Protocol defining the interface for response generators."""

    def explain(self, question: str, rule: Rule) -> str:
        """Generate an explanation based on the question and rule."""
        ...


class TemplateResponder:
    """Fallback responder using a predefined template (no external LLM call)."""

    def explain(self, question: str, rule: Rule) -> str:
        return f"{rule.title}: {rule.text}"


class StubLLMResponder:
    """Deterministic stub simulating an LLM provider for tests and local runs."""

    def __init__(self, fail: bool = False) -> None:
        self.fail = fail

    def explain(self, question: str, rule: Rule) -> str:
        if self.fail:
            raise ProviderError("stub provider unavailable")
        return f"Based on '{rule.title}': {rule.text}"

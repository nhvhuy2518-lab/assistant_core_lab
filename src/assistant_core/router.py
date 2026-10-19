"""Simple, deterministic message routing."""

from assistant_core.models import Intent

GREETINGS = frozenset({"hi", "hello", "hey", "xin chao", "chao", "xin chào"})


def route(text: str, office_names: set[str]) -> Intent:
    """Choose the intent using predictable keyword rules."""
    normalized = text.lower().strip().rstrip("?!. ")
    if normalized in GREETINGS:
        return Intent.GREETING
    if "fee" in normalized or "tuition" in normalized or "hoc phi" in normalized or "học phí" in normalized:
        return Intent.FEE
    if any(name.lower() in normalized for name in office_names):
        return Intent.OFFICE
    return Intent.RULE

"""UI logic without Streamlit, so it can be unit-tested."""

from __future__ import annotations

<<<<<<< HEAD
WELCOME = ("Hi! I can answer questions about fees, offices and the student handbook. "
           "Try: “Can I register my thesis with 118 credits?”")
EXAMPLES = ["Can I register my thesis with 118 credits?", "Tuition for 18 credits and 2 retake",
            "Where is the library?", "I lost my student card"]
=======
from ui.api_client import ChatResult

WELCOME = (
    "Hi! I can answer questions about fees, offices and the student handbook. "
    "Try: “Can I register my thesis with 118 credits?”"
)
EXAMPLES = [
    "Can I register my thesis with 118 credits?",
    "Tuition for 18 credits and 2 retake",
    "Where is the library?",
    "I lost my student card",
]
>>>>>>> 95043df (Format Python files with Ruff)


def validate_input(text: str) -> str | None:
    """Return an error message for bad input, or None if it is fine."""
    t = text.strip()
    if not t:
        return "Please type a question."
    if len(t) > 2000:
        return "Your question is too long (max 2000 characters)."
    return None


def format_sources(sources):
    """Convert retrieved sources into display-friendly dictionaries."""

    formatted = []

    if not sources:
        return formatted

    for source in sources:
        if isinstance(source, dict):
            item = {
                "title": source.get("title", "Unknown source"),
                "content": source.get("content", ""),
                "score": source.get("score"),
            }
        else:
            item = {
                "title": getattr(source, "title", "Unknown source"),
                "content": getattr(source, "content", ""),
                "score": getattr(source, "score", None),
            }

        formatted.append(item)

    return formatted


def status_note(result):
    """Return a user-friendly note describing the response status."""

    status = getattr(result, "status", None)

    if status == "success":
        return "Response generated successfully."

    if status == "fallback":
        return "The response was generated using fallback information."

    if status == "error":
        return "The request could not be completed."

    if status is None:
        return "Response received."

    return f"Response status: {status}"

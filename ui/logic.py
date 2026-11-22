"""UI logic without Streamlit, so it can be unit-tested."""

from __future__ import annotations

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


def validate_input(text: str) -> str | None:
    """Return an error message for bad input, or None if it is fine."""
    t = text.strip()
    if not t:
        return "Please type a question."
    if len(t) > 2000:
        return "Your question is too long (max 2000 characters)."
    return None


def format_sources(sources):
    """Format retrieved sources for display in the chat UI."""

    if not sources:
        return ""

    formatted = []
    for source in sources:
        if isinstance(source, dict):
            source_id = source.get("id", "")
            title = source.get("title", "")
        else:
            source_id = getattr(source, "id", "")
            title = getattr(source, "title", "")

        source_id = str(source_id).strip()
        title = str(title).strip()
        if source_id and title:
            formatted.append(f"{source_id} — {title}")
        elif title:
            formatted.append(title)
        elif source_id:
            formatted.append(source_id)

    if not formatted:
        return ""
    return "Sources: " + "; ".join(formatted)


def status_note(result):
    """Return a user-friendly note describing the response status."""

    if not result.ok:
        return result.error or "The request could not be completed."

    notes = []
    if result.degraded:
        notes.append("The response was generated using fallback information.")
    if result.escalate:
        notes.append("Please verify this information with the Training Office.")

    return " ".join(notes) if notes else None

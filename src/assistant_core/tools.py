"""Pure, deterministic tuition helpers."""

import re

from assistant_core.errors import InvalidRequest


def parse_credits(text: str) -> tuple[int, int]:
    """Extract (credits, retake_credits) from text such as 'fee for 18 credits and 2 retake'."""
    retake_match = re.search(r"(\d+)\s*retake\b", text, flags=re.IGNORECASE)
    numbers = [int(number) for number in re.findall(r"\d+", text)]
    retake_credits = int(retake_match.group(1)) if retake_match else 0
    other_numbers = numbers.copy()
    if retake_match:
        other_numbers.remove(retake_credits)
    if not other_numbers:
        raise InvalidRequest("Please include the number of credits, for example: 'tuition for 18 credits'.")
    return other_numbers[0], retake_credits


def tuition(
    credits: int,
    retake: int,
    rate: int,
    retake_multiplier: float,
    max_credits: int,
) -> int:
    """Calculate tuition in VND without I/O or external state."""
    if not 1 <= credits <= max_credits:
        raise InvalidRequest(f"Credits must be between 1 and {max_credits}.")
    if retake < 0:
        raise InvalidRequest("Retake credits cannot be negative.")
    if rate <= 0:
        raise InvalidRequest("The credit rate must be positive.")
    if retake_multiplier < 0:
        raise InvalidRequest("The retake multiplier cannot be negative.")
    return int(credits * rate + retake * rate * retake_multiplier)

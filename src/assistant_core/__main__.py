"""Command-line interface for assistant_core."""

import argparse
import logging
import sys

from assistant_core.config import load_settings
from assistant_core.errors import AssistantError
from assistant_core.knowledge import Handbook, OfficeDirectory
from assistant_core.logging_setup import configure_logging
from assistant_core.models import Message
from assistant_core.responder import StubLLMResponder, TemplateResponder
from assistant_core.service import AssistantService


def main() -> int:
    parser = argparse.ArgumentParser(description="Smart Virtual Assistant")
    parser.add_argument("text", nargs="+", help="Message to send to the assistant")
    args = parser.parse_args()

    try:
        settings = load_settings()
        configure_logging(settings.log_level)
        offices = OfficeDirectory.from_csv(settings.data_dir / "offices.csv")
        handbook = Handbook.from_json(settings.data_dir / "handbook.json")
        responder = StubLLMResponder() if settings.llm_provider == "stub" else TemplateResponder()
        service = AssistantService(settings, offices, handbook, responder)
        response = service.handle(Message(text=" ".join(args.text)))
    except AssistantError as exc:
        logging.getLogger("assistant_core").error("startup_or_request_error: %s", exc)
        return 2

    print(response.answer)
    return 0


if __name__ == "__main__":
    sys.exit(main())

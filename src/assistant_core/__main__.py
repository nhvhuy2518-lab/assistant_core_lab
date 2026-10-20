import logging
import sys
import time

from assistant_core.config import load_settings
from assistant_core.knowledge import Handbook, OfficeDirectory
from assistant_core.logging_setup import setup_logging
from assistant_core.models import Message
from assistant_core.responder import StubLLMResponder
from assistant_core.service import AssistantService

log = logging.getLogger("assistant_core")


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m assistant_core '<message>'")
        sys.exit(1)

    settings = load_settings()
    setup_logging(settings.log_level)

    offices = OfficeDirectory.from_csv(settings.data_dir / "offices.csv")
    handbook = Handbook.from_json(settings.data_dir / "handbook.json")
    responder = StubLLMResponder()
    service = AssistantService(settings, offices, handbook, responder)

    user_query = sys.argv[1]
    msg = Message(text=user_query)

    start = time.perf_counter()
    response = service.handle(msg)
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

    extra = {
        "intent": response.intent.value,
        "latency_ms": elapsed_ms,
        "session": msg.session_id,
        "degraded": response.degraded,
    }
    log.info("handled", extra=extra)
    print(response.answer)


if __name__ == "__main__":
    main()

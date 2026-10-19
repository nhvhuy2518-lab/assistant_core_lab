import sys
import time

from assistant_core.config import load_settings
from assistant_core.knowledge import Handbook, OfficeDirectory
from assistant_core.logging_setup import setup_logging
from assistant_core.models import Message
from assistant_core.responder import StubLLMResponder
from assistant_core.service import AssistantService


def main() -> None:
    settings = load_settings()
    logger = setup_logging(settings.log_level)

    try:
        offices = OfficeDirectory.from_csv(settings.data_dir / "offices.csv")
        handbook = Handbook.from_json(settings.data_dir / "handbook.json")
    except Exception as exc: # noqa: BLE001
        logger.error(f"Startup error loading knowledge data: {exc}")
        sys.exit(1)

    responder = StubLLMResponder()
    service = AssistantService(
        settings=settings,
        offices=offices,
        handbook=handbook,
        responder=responder,
    )

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        start_time = time.time()

        msg = Message(text=query, session_id="cli")
        res = service.handle(msg)

        latency = round((time.time() - start_time) * 1000, 2)
        logger.info(
            "handled",
            extra={
                "intent": res.intent.value,
                "latency_ms": latency,
                "session": msg.session_id,
                "degraded": res.degraded,
            },
        )

        print(res.answer)
        return

    print("assistant ready (type 'quit' to exit)", file=sys.stdout)
    while True:
        try:
            query = input("> ")
        except (KeyboardInterrupt, EOFError):
            break

        if query.strip().lower() in ("quit", "exit"):
            break

        if not query.strip():
            continue

        start_time = time.time()
        try:
            msg = Message(text=query, session_id="cli")
            res = service.handle(msg)
            latency = round((time.time() - start_time) * 1000, 2)

            logger.info(
                "handled",
                extra={
                    "intent": res.intent.value,
                    "latency_ms": latency,
                    "session": msg.session_id,
                    "degraded": res.degraded,
                },
            )
            print(res.answer, file=sys.stdout)
        except Exception as exc: # noqa: BLE001
            print(f"Error: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
"""Application service: the only entry point clients need to call."""

import logging
from time import perf_counter

from assistant_core.config import Settings
from assistant_core.errors import ProviderError
from assistant_core.knowledge import Handbook, OfficeDirectory
from assistant_core.models import Intent, Message, Response, Source
from assistant_core.responder import Responder, TemplateResponder
from assistant_core.router import route
from assistant_core.tools import parse_credits, tuition

log = logging.getLogger("assistant_core")


class AssistantService:
    def __init__(
        self,
        settings: Settings,
        offices: OfficeDirectory,
        handbook: Handbook,
        responder: Responder,
    ) -> None:
        self.settings = settings
        self.offices = offices
        self.handbook = handbook
        self.responder = responder
        self.fallback = TemplateResponder()

    def handle(self, msg: Message) -> Response:
        """Route a validated message and return a typed response."""
        started = perf_counter()
        intent = route(msg.text, self.offices.names)
        if intent is Intent.GREETING:
            response = Response(
                answer="Hello! I can help with offices, fees and rules.",
                intent=intent,
            )
        elif intent is Intent.FEE:
            response = self._fee(msg.text)
        elif intent is Intent.OFFICE:
            office = self.offices.find(msg.text)
            if office is None:
                response = Response(answer="Sorry, I could not find that office.", intent=Intent.UNKNOWN)
            else:
                response = Response(
                    answer=f"{office.name}: room {office.room}, open {office.hours}.",
                    intent=intent,
                )
        else:
            response = self._rule(msg.text)

        log.info(
            "handled",
            extra={
                "intent": response.intent.value,
                "latency_ms": round((perf_counter() - started) * 1000, 2),
                "session": msg.session_id,
                "degraded": response.degraded,
            },
        )
        return response

    def _fee(self, text: str) -> Response:
        credits, retake_credits = parse_credits(text)
        amount = tuition(
            credits,
            retake_credits,
            self.settings.credit_rate_vnd,
            self.settings.retake_multiplier,
            self.settings.max_credits,
        )
        return Response(answer=f"Your tuition is {amount:,} VND.", intent=Intent.FEE)

    def _rule(self, text: str) -> Response:
        rule = self.handbook.search(text)
        if rule is None:
            return Response(answer="Sorry, I don't know that yet.", intent=Intent.UNKNOWN)

        sources = [Source(id=rule.id, title=rule.title)]
        try:
            answer = self.responder.explain(text, rule)
            return Response(answer=answer, intent=Intent.RULE, sources=sources)
        except ProviderError:
            log.warning("provider failed; using template fallback")
            answer = self.fallback.explain(text, rule)
            return Response(answer=answer, intent=Intent.RULE, sources=sources, degraded=True)

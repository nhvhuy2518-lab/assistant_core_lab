
"""Answer policy questions with retrieval + LLM, safely."""

from __future__ import annotations

import logging
from collections.abc import Callable

from assistant_core.errors import InvalidRequest, ProviderError
from assistant_core.llm import LLM, AnswerDraft, build_prompt, parse_draft
from assistant_core.models import Intent, Response, Source
from assistant_core.rag.index import QUERY_SYNONYMS, Index, tokenize

log = logging.getLogger("assistant_core.rag")

ESCALATE_MSG = (
    "I'm not confident I can answer that from the official documents. "
    "Please contact the Training Office (room I.101) or ask your academic advisor."
)


class RagAnswerer:
    def __init__(
        self,
        index: Index,
        llm: LLM | None,
        min_score: float = 2.0,
        k: int = 3,
        prompt_version: str = "answer_v1",
        retries: int = 1,
        tool_runner: Callable[[str], str | None] | None = None,
    ):
        self.index = index
        self.llm = llm
        self.min_score = min_score
        self.k = k
        self.prompt_version = prompt_version
        self.retries = retries
        self.tool_runner = tool_runner

    def _has_sufficient_coverage(
        self, question: str, source_text: str
    ) -> bool:
        """Check lexical coverage of the retrieved source."""

        query_tokens = tokenize(question)

        query_terms = {
            synonym
            for token in query_tokens
            for synonym in QUERY_SYNONYMS.get(token, (token,))
            if not token.isdigit()
        }

        source_terms = set(tokenize(source_text))

        if not query_terms:
            return False

        coverage = len(query_terms & source_terms) / len(query_terms)

        return coverage > 0.5

    def answer(self, question: str) -> Response:
        hits = self.index.search(question, self.k)

        if not hits or hits[0].score < self.min_score:
            return Response(
                answer=ESCALATE_MSG,
                intent=Intent.UNKNOWN,
                path="abstain",
                escalate=True,
                confidence=0.0,
            )

        top = hits[0].chunk

        sources = {
            hit.chunk.id: Source(
                id=hit.chunk.id,
                title=hit.chunk.title,
            )
            for hit in hits
        }

        # Retrieval-only baseline.
        if self.llm is None:
            source_text = top.title + " " + top.text

            if not self._has_sufficient_coverage(
                question, source_text
            ):
                return Response(
                    answer=ESCALATE_MSG,
                    intent=Intent.UNKNOWN,
                    path="abstain",
                    escalate=True,
                    confidence=0.0,
                )

            return Response(
                answer=f"{top.title}: {top.text}",
                intent=Intent.RULE,
                sources=[sources[top.id]],
                path="retrieval",
                confidence=None,
            )

        prompt = build_prompt(
            question, hits, self.prompt_version
        )

        for attempt in range(self.retries + 1):
            try:
                raw = self.llm.complete(prompt)

                if self.tool_runner is not None:
                    try:
                        result = self.tool_runner(raw)
                    except InvalidRequest as exc:
                        return Response(
                            answer=str(exc),
                            intent=Intent.FEE,
                            path="tool",
                            degraded=True,
                        )

                    if result is not None:
                        return Response(
                            answer=result,
                            intent=Intent.FEE,
                            path="tool",
                        )

                source_text = top.title + " " + top.text

                if not self._has_sufficient_coverage(
                    question, source_text
                ):
                    return Response(
                        answer=ESCALATE_MSG,
                        intent=Intent.UNKNOWN,
                        path="abstain",
                        escalate=True,
                        confidence=0.0,
                    )

                draft: AnswerDraft = parse_draft(
                    raw, set(sources)
                )

                if draft.abstain:
                    return Response(
                        answer=ESCALATE_MSG,
                        intent=Intent.UNKNOWN,
                        path="abstain",
                        escalate=True,
                        confidence=draft.confidence,
                    )

                return Response(
                    answer=draft.answer,
                    intent=Intent.RULE,
                    path="llm",
                    confidence=draft.confidence,
                    sources=[
                        sources[source_id]
                        for source_id in draft.source_ids
                    ],
                )

            except ProviderError as exc:
                log.warning(
                    "llm attempt %d failed: %s",
                    attempt + 1,
                    exc,
                )

        return Response(
            answer=f"{top.title}: {top.text}",
            intent=Intent.RULE,
            sources=[sources[top.id]],
            path="retrieval",
            degraded=True,
        )

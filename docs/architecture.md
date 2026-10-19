# Assistant Core Architecture

## Module responsibilities

| Module | Responsibility |
|---|---|
| `config.py` | Read and validate settings from environment variables and `.env`. |
| `errors.py` | Define named application exceptions. |
| `models.py` | Define validated `Message`, `Response`, `Source`, and `Intent` contracts. |
| `router.py` | Map message text to a deterministic intent. |
| `knowledge.py` | Load and search offices from CSV and handbook rules from JSON. |
| `tools.py` | Parse credit counts and calculate tuition deterministically. |
| `responder.py` | Hide response-generation details behind a replaceable interface. |
| `service.py` | Coordinate routing, tools, knowledge, and response generation. |
| `logging_setup.py` | Emit structured JSON logs without request text or secrets. |
| `__main__.py` | Provide the command-line entry point. |

## Service interface

`AssistantService.handle(msg: Message) -> Response`

`Message` contains `text` (1–2000 characters) and `session_id`. `Response` contains `answer`, `intent`, `sources`, and `degraded`. Empty messages are rejected by Pydantic. A missing or malformed knowledge file raises `DataError`; invalid fee inputs raise `InvalidRequest`. When a responder raises `ProviderError`, the service answers with the template fallback and sets `degraded=True`.

## Key design decisions

1. **Tuition calculation lives in `tools.py`.** It is deterministic and can be tested without file access or an AI provider.
2. **The responder is injected into the service.** Tests can simulate provider failure, and a future provider can be swapped without rewriting service routing.
3. **Configuration is external.** `.env.example` documents settings, `.env` is ignored by Git, and the API key field is excluded from the settings representation.
4. **Knowledge is loaded by dedicated classes.** Startup failures use `DataError` rather than silently continuing with incomplete data.
5. **Logs contain operational metadata only.** They include intent, latency, session identifier, and fallback status; they do not include message text or API keys.

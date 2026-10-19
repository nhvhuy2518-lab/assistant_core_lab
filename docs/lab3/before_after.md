# Before and After Maintainability Worksheet

| Question | Monolith | `assistant_core` |
|---|---|---|
| Places to change the credit rate | 1 constant in code (`RATE`) | 1 variable in `.env` (`CREDIT_RATE_VND`) |
| Tests run offline and deterministically? | no (random failure in `llm()`) | yes (injected `StubLLMResponder` / `TemplateResponder`) |
| Missing `handbook.json` | prints and continues silently (bare `except:`) | raises `DataError` at startup |
| Secret printed or logged? | yes (`API_KEY` printed in debug output) | no (`repr=False` on `llm_api_key`, structured JSON logging) |
| Module-level globals | 9 (3 mutable: `history`, `offices`, `handbook`) | 0 |
| Bare `except:` | 3 | 0 |
| Longest function (lines) | ~65 (`handle`) | ~15 |
| Swap the LLM without touching the service? | no | yes (via `Responder` Protocol adapter) |

## Reflection
- **What got more complex?** More files, explicit data models (`Pydantic` / `dataclass`), and dependency injection wiring across modules.
- **When is that trade-off worth it?** When multiple developers collaborate on the same codebase, and when the service must be unit-tested deterministically, configured safely across environments, and extended.

# Lab 3 — Before / after maintainability comparison

Fill in for the monolith (before) and your refactored package (after).

| Question | Before | After |
|---|---|---|
| Where would you change the credit rate? How many places? | 1 constant hard-coded in code (`RATE = 450000`) | 1 place in `.env` (`CREDIT_RATE_VND=450000`) |
| Can you run the tests without internet or an API key? | No (simulated random LLM failures, hardcoded API key) | Yes (`StubLLMResponder` runs offline and deterministically) |
| What happens if `handbook.json` is missing? | Prints `"could not load handbook"` and continues silently | Raises explicit `DataError` at startup |
| Is any secret printed or logged? | Yes (`API_KEY` printed in debug log) | No (`repr=False` in Pydantic Settings, masked in logs) |
| How long does it take a new teammate to find the fee logic? | Needs to read through 160+ lines of monolith script | Seconds (located cleanly in `src/assistant_core/tools.py`) |
| Number of global variables | 9 (`API_KEY`, `MODEL`, `RATE`, `RETAKE_RATE`, `DEBUG`, `history`, `offices`, `handbook`, `BASE`) | 0 (injected via `AssistantService.__init__`) |
| Number of bare `except:` blocks | 3 (in `load()` and `main()`) | 0 (replaced with typed custom exceptions) |
| Lines in the longest function | ~65 lines (`handle()`) | ~15 lines |
| `ruff check` issues | Multiple (unused imports, globals, BLE001, bare except) | 0 issues (All checks passed!) |
| Can you swap the LLM without touching the service? | No (tightly coupled to `llm()` function inside script) | Yes (implements `Responder` protocol via Dependency Injection) |

**Three sentences:**
The codebase improved most by decoupling the LLM provider behind a typed `Responder` Protocol and extracting config to `.env`, allowing reliable offline testing. Complexity slightly increased with multiple files and Pydantic boilerplate, but this overhead pays off through contract enforcement and separation of concerns. In the future, I would still introduce a vector-based semantic search to replace the simple keyword-matching in `knowledge.py`.
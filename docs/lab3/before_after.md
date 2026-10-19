# Lab 3 — Before/After Maintainability Worksheet

| Question | Monolith (before) | `assistant_core` (after) |
|---|---|---|
| Places to change the credit rate | 1 constant in code | 1 variable in `.env` |
| Tests run offline and deterministically? | No | Yes |
| Missing `handbook.json` | Prints and continues silently | `DataError` at startup |
| Secret printed or logged? | Yes | No |
| Module-level globals | 9 (3 mutable) | 0 |
| Bare `except:` | 3 | 0 |
| Longest function (lines) | About 65 (`handle`) | About 15 |
| Swap the LLM without touching the service? | No | Yes |

## Reflection

The refactor adds files and a few concepts, but each module now has one responsibility. This trade-off is worthwhile when multiple teammates maintain the application or when tests and later extensions must remain reliable.

The before-state figures above follow the Lab 3 tutorial's Part E comparison table. Each member should still review the original monolith supplied with the course and personalize the worksheet for their own branch. The uploaded tutorial PDF references that source file but does not include its full source code.

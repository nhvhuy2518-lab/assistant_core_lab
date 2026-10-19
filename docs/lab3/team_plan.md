# Lab 3 Team Plan — Six Members (Parts A–F only)

## Scope

Included: monolith smell review, target package, refactoring, tests, Ruff/formatting, pinned dependencies, architecture note, and before/after worksheet. Excluded: all Homework items H1, H2, and H3.

## Important individual/team distinction

The lab specifies an individual refactored package on each member's branch, with tests passing and `ruff check` clean. Each member should therefore make a complete working refactor branch and submit a PR/worksheet. The roles below are each member's **primary review and improvement focus**, not permission to leave their individual package incomplete. After reviewing all six PRs, select one base implementation, incorporate the strongest improvements, merge one team version, then use the post-merge owners below for follow-up maintenance.

## Primary focus and integrated ownership

| Member | Primary focus in their individual branch | Follow-up owner after team integration |
|---|---|---|
| `kknguyen_25127107` | `service.py`, `__main__.py`, service interface and architecture note | Service/CLI and architecture note; coordinate merge and `v0.3-core` tag |
| `lhphieu_25127049` | `config.py`, `.env.example`, `.gitignore`, `logging_setup.py` | Config, environment example, logging and secret-safety review |
| `nhvhuy_25127060` | `knowledge.py`, office CSV and handbook JSON loading/search | Knowledge module and validation of supplied course data |
| `hqtuan_25127543` | `tools.py`, tuition parsing/calculation, `test_tools.py` | Tools and deterministic calculation tests |
| `ltdat_25127293` | `models.py`, `errors.py`, `router.py`, `test_router.py` | Typed contracts, named errors, routing and routing tests |
| `ntmduc_25127300` | `responder.py`, fallback behavior, `test_service.py`, final quality gate | Responder, fallback/service tests, full test and Ruff verification |

## Per-member checklist

- [ ] Create branch `refactor/assistant-core-<username>` from the team `main`.
- [ ] Refactor the monolith into the complete `src/assistant_core/` package; do not only commit one module.
- [ ] Include tests and run `pytest -q` (target: at least 10 passing tests).
- [ ] Run `ruff format .`, `ruff check .`, and `ruff check --select BLE .`.
- [ ] Complete `docs/lab3/before_after.md` for the member's own work; verify before-state figures against the original monolith.
- [ ] Open a PR and provide its link for the individual deliverable.

## Team integration checklist

- [ ] Review all six candidate PRs; compare clarity, module boundaries, error handling, tests and secret-safe logs.
- [ ] Select one clear base; record useful improvements from other PRs and give credit for co-authored work where applicable.
- [ ] Merge one integrated `assistant_core` version into `main`.
- [ ] Create follow-up issues using the ownership table above.
- [ ] Confirm `.env` is ignored and only `.env.example` is committed.
- [ ] Confirm dependencies are pinned in `requirements.txt` and compatibility ranges are in `pyproject.toml`.
- [ ] Run all tests and Ruff checks from a clean environment; inspect the final diff and CI result.
- [ ] Member 1 creates tag `v0.3-core` after the integrated version is merged and validated.

## Suggested review agenda (15 minutes)

1. 3 minutes: verify package structure and public API (`AssistantService.handle(Message) -> Response`).
2. 4 minutes: inspect configuration, data errors and secret-safe logging.
3. 4 minutes: inspect deterministic tools, responder fallback and tests.
4. 2 minutes: compare architecture notes and worksheets.
5. 2 minutes: choose the base and list improvements/issues for the integrated version.

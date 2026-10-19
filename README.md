# CSC10014 Lab 3 — Maintainable Python Service

This project is a runnable `assistant_core` refactor aligned with the **pre-Homework** parts of the Lab 3 tutorial (Parts A–F). It does not include the H1, H2, or H3 homework tasks.

## Important data note

The tutorial PDF references the course's `lab03/monolith` source and data files, but those source/data files were not included with the uploaded PDF. The `data/offices.csv` and `data/handbook.json` in this project are sample fixtures for running the service. Replace them with the instructor-provided course data before treating outputs as official university policy.

## Setup

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate

python -m pip install -r requirements.txt
python -m pip install -e .
copy .env.example .env  # Windows; on macOS/Linux use: cp .env.example .env
```

## Run

Run these commands from this project directory:

```bash
python -m assistant_core "hello"
python -m assistant_core "Where is the Library?"
python -m assistant_core "tuition for 18 credits and 2 retake"
python -m assistant_core "thesis registration credits"
```

Application answers go to stdout; JSON operational logs go to stderr. Do not add real secrets to `.env.example` or commit `.env`.

## Quality checks

```bash
pytest -q
ruff format .
ruff check .
ruff check --select BLE .
```

## Team integration

Each member should create their own branch and PR for the individual deliverable. The team should review all six PRs, select the clearest implementation as the base, incorporate worthwhile improvements, then merge one integrated package. Each member also submits a completed before/after worksheet with their individual PR.

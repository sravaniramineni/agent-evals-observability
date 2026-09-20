# Architecture

## Components
- `data/eval_cases.jsonl`: scenario, expected tool, expected outcome.
- `src/eval.py`: runs scenarios against an agent runner, checks assertions.
- `report.html`: pass/fail summary for CI or review.

## Key decisions
- Evals run offline and in CI, not only in notebooks.
- Every failure links to the trace that caused it.
- Add human review for high-risk failures.

## Production hardening
- Export OpenTelemetry traces, add dashboards, alert on regression.

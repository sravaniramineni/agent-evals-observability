# Agent Evals & Observability

A regression-eval starter kit for AI agents: define scenarios as JSONL, run them through your agent, and get pass rate, latency stats, failure clustering, and an HTML report — with CI failing the build when the pass rate drops.

## When to use this

Agents fail in subtle ways — wrong tool chosen, hallucinated answer, unsafe action. Before every release you want a regression suite that answers *"did we break anything?"* in one command. This kit gives you the harness; you plug in your real agent.

## How it works

1. **Define scenarios** in `data/eval_cases.jsonl`, one JSON object per line:
   ```jsonl
   {"id": "refund-01", "scenario": "Customer wants a refund for order O-99", "expected_tool": "issue_refund"}
   {"id": "login-02", "scenario": "User cannot log in to the portal", "expected_tool": "create_ticket"}
   ```
2. **Run the eval**: `python src/eval.py`
   - Each scenario goes through `run_agent()` (currently a stub — **replace it with your LangGraph/agent runner** and capture the real trace)
   - Results are scored against `expected_tool`, latencies recorded, failures labeled by type
   - `src/metrics.py` computes `pass_rate`, `avg_latency_ms`, and `failures_by_type`
3. **Read the report**: `report.html` opens in any browser with per-case pass/fail, pass rate, avg latency, and failure clusters.
4. **Gate CI**: the script exits non-zero unless pass rate is 100% — wire it into `.github/workflows/ci.yml` so regressions block the merge.

## Project structure

```
src/eval.py            Eval runner: executes scenarios, scores, writes report.html
src/metrics.py         summarize(): pass rate, latency stats, failure clustering
src/main.py            (reserved for a future observability API)
data/eval_cases.jsonl  Scenario dataset — add yours here
docs/ARCHITECTURE.md   Design notes
docs/ADR-001.md        Why JSONL + HTML for v1
Dockerfile           Container image
.github/workflows/ci.yml   CI: runs the eval suite on every push
```

## Prerequisites

- Python 3.11+ (pydantic only, per `requirements.txt`)

## Quickstart

```bash
pip install -r requirements.txt
python src/eval.py
open report.html   # or just open the file in a browser
```

Example output:

```
refund-01 PASS
login-02 PASS
Wrote report.html {'pass_rate': 1.0, 'passed': 2, 'total': 2, 'avg_latency_ms': 0.4, 'failures_by_type': {}}
```

The command exits `0` on full pass and `1` otherwise, so CI stays red until the agent is fixed.

## Adding your own agent

Open `src/eval.py` and replace `run_agent()`:

```python
def run_agent(scenario: str) -> dict:
    trace = my_langgraph_app.invoke({"input": scenario})   # your agent here
    return {"tool": trace["tool_called"], "output": trace["answer"],
            "latency_ms": trace["latency_ms"]}
```

Then add scenarios to `data/eval_cases.jsonl` — include adversarial cases (ambiguous requests, PII in the prompt, conflicting instructions) so regressions actually get caught.

## Running the tests / CI

Every push runs the eval suite via `.github/workflows/ci.yml`:

```bash
python src/eval.py
```

## Deploy with Docker

```bash
docker build -t agent-evals .
docker run -v "$PWD:/app" agent-evals   # mounts your data/ and writes report.html
```

## Taking this to production

- Persist every run (timestamp, git SHA, scores) to a database and plot pass rate over time — that's your agent's health dashboard.
- Add judge-based evals (LLM-as-judge) for open-ended answers alongside these deterministic tool-choice checks.
- Export OpenTelemetry traces per scenario so a failure links straight to the failing span.

## Further reading

- `docs/ARCHITECTURE.md` — design notes
- `docs/ADR-001.md` — why JSONL + HTML for v1

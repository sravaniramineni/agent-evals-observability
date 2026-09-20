"""Agent eval runner with metrics and HTML report."""
import json
import time
from pathlib import Path
from .metrics import summarize

DATA = Path(__file__).parent.parent / "data" / "eval_cases.jsonl"

def run_agent(scenario: str) -> dict:
    # Production: invoke your LangGraph/agent runner here and capture the trace.
    start = time.time()
    tool = "lookup_customer" if "refund" in scenario.lower() or "login" in scenario.lower() else "create_ticket"
    return {"tool": tool, "output": "ok", "latency_ms": round((time.time() - start) * 1000, 1)}

def main():
    results = []
    for line in DATA.read_text().splitlines():
        case = json.loads(line)
        started = time.time()
        result = run_agent(case["scenario"])
        result["latency_ms"] = round((time.time() - started) * 1000, 1)
        passed = result["tool"] == case["expected_tool"]
        results.append({"id": case["id"], "passed": passed,
                        "latency_ms": result["latency_ms"],
                        "failure_type": None if passed else "wrong_tool"})
        print(case["id"], "PASS" if passed else "FAIL")
    summary = summarize(results)
    rows = "".join(f"<li>{r['id']}: {'PASS' if r['passed'] else 'FAIL'} ({r['latency_ms']}ms)</li>" for r in results)
    html = (f"<html><body><h1>Agent Evals</h1>"
            f"<p>Pass rate: {summary['pass_rate']} ({summary['passed']}/{summary['total']})</p>"
            f"<p>Avg latency: {summary['avg_latency_ms']}ms</p>"
            f"<p>Failures: {summary['failures_by_type']}</p><ul>{rows}</ul></body></html>")
    Path("report.html").write_text(html)
    print("Wrote report.html", summary)
    raise SystemExit(0 if summary["pass_rate"] == 1.0 else 1)

if __name__ == "__main__":
    main()

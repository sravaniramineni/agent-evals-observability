"""Eval metrics: pass rate, latency, and failure clustering."""


def summarize(results: list[dict]) -> dict:
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    latencies = [r.get("latency_ms", 0) for r in results]
    failures = {}
    for r in results:
        if not r["passed"]:
            failures[r.get("failure_type", "unknown")] = failures.get(r.get("failure_type", "unknown"), 0) + 1
    return {
        "total": total,
        "passed": passed,
        "pass_rate": round(passed / total, 3) if total else 0,
        "avg_latency_ms": round(sum(latencies) / len(latencies), 1) if latencies else 0,
        "failures_by_type": failures,
    }

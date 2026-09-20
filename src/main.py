"""Agent eval runner (starter)."""
import json
from pathlib import Path

DATA = Path(__file__).parent.parent / "data" / "eval_cases.jsonl"

def run_agent(scenario: str) -> dict:
    # Production: invoke your LangGraph/agent runner here.
    return {"tool": "lookup_customer", "output": "ok"}

def main():
    rows = []
    for line in DATA.read_text().splitlines():
        case = json.loads(line)
        result = run_agent(case["scenario"])
        passed = result["tool"] == case["expected_tool"]
        rows.append((case["id"], passed))
        print(case["id"], "PASS" if passed else "FAIL")
    html = "<html><body><h1>Agent Evals</h1><ul>" + "".join(
        f"<li>{cid}: {'PASS' if ok else 'FAIL'}</li>" for cid, ok in rows
    ) + "</ul></body></html>"
    Path("report.html").write_text(html)
    print("Wrote report.html")

if __name__ == "__main__":
    main()

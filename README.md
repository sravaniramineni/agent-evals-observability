# Agent Evals & Observability

Starter kit for evaluating AI agents before production.

## Problem
Agents fail in subtle ways: wrong tool, missing citation, unsafe action. You need regression tests.

## What it does
- Eval dataset format for agent scenarios
- Trace analyzer over JSONL logs
- Pass/fail report with HTML output

## Quickstart
```bash
pip install -r requirements.txt
python src/eval.py
open report.html
```

# CLAUDE.md — trajectory-tracing

## What this project is

Trajectory evaluation for AI agents doing mathematical research. Complements trust-boundaries (output trust) with trajectory trust (was the reasoning path sound?).

## Architecture

- `tracecheck/` — Python validator (stdlib only, mirrors trustcheck.py from trust-boundaries)
- `deployments/` — per-agent JSON descriptors (currently Clio only)
- `theory/` — mathematical foundations
- `lean/` — Lean 4 formalization (future)

## Running

```bash
python3 tracecheck/tracecheck.py validate <trajectory.jsonl>
python3 tracecheck/tracecheck.py check --deployment deployments/clio.json <trajectory.jsonl>
python3 tracecheck/tracecheck.py report --deployment deployments/clio.json <trajectory.jsonl>
```

## Testing

```bash
python3 -m pytest tracecheck/tests/ -v
# or manually:
python3 tracecheck/tracecheck.py check --deployment deployments/clio.json tracecheck/tests/circular_verification/trajectory.jsonl
```

## Conventions

- Python 3.10+, stdlib only (no pip dependencies)
- One deployment descriptor per agent
- Event schema: JSONL, one event per line
- Seven event kinds: compute, read, claim, verify, cite, delegate, decide
- Trajectory grade chain: unsupported < shallow < independent < cross-verified < mechanically-checked

## Adding a new agent

1. Create `deployments/<agent>.json` with the agent's trajectory chain, boundary, and rules
2. The schema and rules are agent-agnostic — only the deployment config varies

## Adding a new rule

1. Add detection function to `tracecheck/rules.py`
2. Register it in the `ALL_RULES` list
3. Add a test fixture under `tracecheck/tests/<rule_name>/`

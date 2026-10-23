# trajectory-tracing

[![Lean CI](https://github.com/RaggedR/trajectory-tracing/actions/workflows/lean_action_ci.yml/badge.svg)](https://github.com/RaggedR/trajectory-tracing/actions/workflows/lean_action_ci.yml)

Trajectory evaluation for AI agents doing mathematical research. Complements [trust-boundaries](../trust-boundaries/) which evaluates **output** (are claims structurally justified?) by evaluating **trajectory** (did the agent take a sound path to arrive at its claims?).

## Motivation

Five failure modes from the agents' own dream journals motivate this system:

1. **Circular verification** — testing a definition against itself produces `True` but proves nothing
2. **Tautological transport** — defining X via F, then congratulating F for preserving X
3. **Estimand substitution** — a correct number cited against the wrong mathematical object
4. **Shallow source depth** — relying on agent-summaries instead of deep reads leads to novelty errors
5. **Brief-as-deme** — the brief itself was the error source, but the trajectory looked correct

All five share a property: the output can look correct (and pass trust-boundaries validation) while the reasoning path is epistemically broken.

## Core abstraction

A trajectory is a DAG of **events** (actions the agent took). Anti-patterns are graph-theoretic properties of this DAG. Trajectory evaluation is structurally analogous to trust evaluation: both are well-foundedness checks on DAGs, both compose across agents, both admit a canonical grading by recursion.

Trajectory systems ARE trust systems — the same `(D, T, s)` triple from trust-boundaries, instantiated on agent actions instead of mathematical claims.

## Currently deployed

- **Clio** (algebraic combinatorics) — trajectory chain, circular verification detection

Future: Rick, MacBeth, Warnaar loop (add a deployment descriptor per agent).

## Usage

```bash
# Validate event schema
python3 tracecheck/tracecheck.py validate trajectory.jsonl

# Check trajectory rules
python3 tracecheck/tracecheck.py check --deployment deployments/clio.json trajectory.jsonl

# Report trajectory grades
python3 tracecheck/tracecheck.py report --deployment deployments/clio.json trajectory.jsonl
```

## Emitting events (for agents)

```python
from tracecheck.emit import init, emit

init("clio", "prove")
e1 = emit("read", "read Koroteev-Smirnov 2412.19383", source_depth="deep-read")
e2 = emit("compute", "computed p-curvature spectrum at q=zeta_p", inputs=[e1])
e3 = emit("claim", "p-curvature reproduces mod-4 box", inputs=[e2])
```

## Design principles

- **stdlib only** (matching trust-boundaries)
- **One deployment descriptor per agent** — add Rick/MacBeth by adding a JSON file
- **Composable with trust-boundaries** via a morphism psi: TrajectoryChain -> TrustChain
- **Lean-formalizable** — trajectory systems reuse Trust.lean's System/tau/Mor

## Related

- [trust-boundaries](../trust-boundaries/) — output trust evaluation
- [dreaming-agent](../dreaming-agent/) — agent lifecycle (where emit hooks go)
- Google, "The New SDLC With Vibe Coding" (May 2026) — the output/trajectory distinction

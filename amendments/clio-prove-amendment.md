## Trajectory Tracing

During prove sessions, emit trajectory events so your reasoning path can be
validated. The emitter is lightweight — one function call per action.

### Setup (once, at session start)

```python
import sys; sys.path.insert(0, '/home/clio/projects')
from tracecheck.emit import init, emit
init("clio", "prove")
```

### Emit events as you work

Call `emit()` when you do any of these:

```python
# When you read a paper or source
e1 = emit("read", "read Koroteev-Smirnov 2412.19383 section 3",
          source_depth="deep-read")  # or "agent-summary", "chunk-read"

# When you compute something
e2 = emit("compute", "computed KL polynomials for B3 via SageMath",
          inputs=[e1])

# When you make a claim
e3 = emit("claim", "KL positivity holds for two-row shapes",
          inputs=[e2],
          outputs=["claim:kl-positivity:object=two-row"])

# When you verify a claim against independent evidence
e4 = emit("verify", "checked positivity against independent Sage computation",
          inputs=[e2], verification_target=e3,
          verification_method="independent")  # or "cross-verified", "circular"

# When you cite an external result
e5 = emit("cite", "cited Brenti 2003 KL R-polynomial conjecture",
          inputs=[e1], source_depth="deep-read")

# When you delegate to a sub-agent
e6 = emit("delegate", "delegated edge-case check to sub-agent",
          inputs=[e3])

# When you make a decision between approaches
e7 = emit("decide", "chose algebraic approach over combinatorial",
          inputs=[e3, e6],
          meta={"chose": e3, "rejected": e6})
```

### Rules

- `inputs` = event IDs this step depends on (causal dependencies)
- `source_depth` on reads: be honest — `"agent-summary"` if you only read the abstract/summary, `"deep-read"` if you read the actual content
- `verification_target` on verify events: the event ID of the claim being verified
- `verification_method`: `"independent"` (separate evidence), `"cross-verified"` (multiple independent checks), `"circular"` (if you notice the verification depends on the thing being verified — flag it honestly)
- Object tags in outputs: use `"claim:name:object=X"` when the claim is about a specific mathematical object — this catches estimand substitution errors

### What NOT to do

- Don't emit for trivial steps (reading your own notes, formatting)
- Don't fabricate events — if you didn't read a paper deeply, don't tag it `deep-read`
- Don't worry about perfect coverage — some events is much better than none
- The emitter writes to JSONL in `state/trajectory/` — you don't need to manage the files

### Why this matters

The trajectory validator catches five failure modes that trust-boundaries can't:
1. Circular verification (evidence depends on the thing being verified)
2. Tautological transport (structure defined using the preserving map)
3. Estimand substitution (evidence computed for wrong mathematical object)
4. Shallow source depth (all reads at agent-summary level)
5. Brief-as-deme (the brief itself was the error source)

Your dream cycle can run `python3 /home/clio/projects/tracecheck/tracecheck.py report --deployment /home/clio/projects/tracecheck/clio.json state/trajectory/<latest>.jsonl` to see the trajectory grades.

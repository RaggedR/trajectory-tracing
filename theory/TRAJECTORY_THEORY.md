# Trajectory Systems Theory

## Definitions

### Trajectory event

A **trajectory event** is a record of one action an agent took. It carries:
- An identifier
- A kind (compute, read, claim, verify, cite, delegate, decide)
- A list of input event IDs (causal dependencies)
- Optional: verification target, source depth, output artifacts

### Trajectory graph

A **trajectory graph** G = (V, E) where V is a set of events and E is the dependency relation (event A is in event B's `inputs`). G must be a DAG (acyclic).

### Trajectory grading

A **trajectory chain** T is a totally ordered set of grades:

    unsupported < shallow < independent < cross-verified < mechanically-checked

A **trajectory grading** is a function s : V -> T assigning each event a grade.

### Canonical trajectory grade (tau)

The canonical grade is computed by well-founded recursion on the DAG:

    tau(e) = min(own_grade(e), min(tau(d) for d in inputs(e)))

where own_grade(e) is determined by the event's kind and properties.

This is an instance of the trust system tau from trust-boundaries (Trust.lean, Definition 2.1). The certificate lemma applies: tau is the greatest sound assignment, and any over-claiming is detectable.

### Trajectory boundary rule

A trajectory grade at or above the boundary (default: `independent`) requires all input events to also be at or above the boundary. This is the same structural rule as trust-boundaries' boundary rule, instantiated on trajectory events.

## Anti-pattern rules

### Rule 1: Circular verification

**Definition.** A verify event e has circular verification if its verification_target t is an ancestor of e in the dependency DAG. That is, there exists a path from t to e through the `inputs` relation.

**Why this is unsound.** If the evidence (inputs of e) was derived FROM the thing being verified (t), then the verification can only confirm what was already assumed. The check is tautological.

**Consequence.** By analogy with `cyc_sound_top` / `cyc_not_wf` in Trust.lean: circular verification implies trajectory_tau = unsupported on the cycle.

**Example (MacBeth Day 96).** Defined the Dirichlet tensor product by transporting along the extension functor. Then verified that the extension functor preserves the Dirichlet tensor. But the tensor was defined via the functor, so the verification tested a tautology.

### Rules 2-5 (future)

2. **Tautological transport** — the preserved structure was defined using the preserving map
3. **Estimand substitution** — evidence object tag disagrees with claim object tag
4. **Shallow source depth** — all reads in claim ancestry at agent-summary depth
5. **Brief-as-deme** — retrospective: brief path died, contradicting sub-agent path proved correct

## Composition with trust-boundaries

A trajectory system composes with a trust system via a monotone map:

    psi : TrajectoryChain -> TrustChain

The composition rule: if a trust-boundaries registry node claims grade g, and the trajectory events supporting that claim have trajectory_tau below psi^{-1}(g), the composition checker flags a mismatch.

This is an instance of tau_transport (Lemma 3.2 in Trust.lean): morphisms transport trust laxly, and the transported grade is a lower bound.

## Relationship to Trust.lean

Trajectory systems ARE trust systems in the sense of Trust.lean:
- V (events) = C (claims)
- Dependency edges = checking steps
- trajectory_tau = tau
- Anti-pattern rules = additional predicates on the System

The Lean formalization (future) instantiates System, reuses tau_sound/sound_le_tau/tau_transport, and adds anti-pattern predicates as new definitions with proofs that violations imply tau = bot.

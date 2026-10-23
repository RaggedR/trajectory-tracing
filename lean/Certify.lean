import Trajectory
import Composition

/-!
# Certification

`#print axioms` on the headline results. CI runs this file and fails if the output
mentions `sorryAx` (a `sorry` reached the result) or if any report is missing (a
name that failed to resolve — a vacuous "proof"). A clean report lists only Lean's
foundational axioms, or none.

This development has **no Mathlib dependency** and is `sorry`-free. The headline
results formalize epistemic-honesty trajectory tracing: a trajectory of agent
reasoning is well-founded, each event is assigned a trust level (`tau`), and the
trust map `psi` composes monotonically — so an honest trajectory stays honest and a
circular one collapses to ⊥.
-/

-- The circular-reasoning trajectory is well-founded, and its trust collapses to ⊥.
#print axioms Trajectory.circularTraj_wf
#print axioms Trajectory.circularTraj_tau_bot

-- An honest trajectory keeps a non-degenerate trust level at the key event.
#print axioms Trajectory.honest_tau_e3

-- Trust composition is monotone, and the honest trajectory's composite stays honest.
#print axioms Trajectory.psi_mono
#print axioms Trajectory.psi_honest_e4

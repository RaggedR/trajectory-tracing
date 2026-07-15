"""Trajectory anti-pattern detection rules.

Each rule is a function: (TrajectoryGraph, Deployment) -> list[Violation].
Rules are registered in ALL_RULES and run by tracecheck.py.
"""


class Violation:
    """A detected anti-pattern in a trajectory."""

    def __init__(self, rule, event_id, message, severity="error"):
        self.rule = rule
        self.event_id = event_id
        self.message = message
        self.severity = severity  # "error" or "warning"

    def __str__(self):
        return f"[{self.severity}] {self.rule} at {self.event_id}: {self.message}"


# ---------------------------------------------------------------------------
# Rule 1: Circular verification
#
# For each 'verify' event, check if verification_target is an ancestor of
# the verify event in the dependency DAG. If yes, the verification is
# testing something that depends on itself — it can only return True.
#
# Real example (Lyra Day 96): defined strictness via a circular definition,
# then ran a computation testing that definition. The compute event depended
# on the definition; the verify targeted the compute. The circle:
#   definition -> compute -> verify -> (targets definition)
# ---------------------------------------------------------------------------

def check_circular_verification(graph, deployment=None):
    """Detect verify events whose target is reachable from themselves."""
    violations = []

    for event in graph.verify_events():
        target_id = event.verification_target
        if target_id is None:
            continue

        # The verify event depends on its inputs. If the verification_target
        # is an ancestor (transitive input) of the verify event, then the
        # verification is circular: it is checking something that its own
        # evidence depends on.
        #
        # More precisely: we check if target_id is in the transitive input
        # closure of any of the verify event's inputs. If the target is an
        # ancestor, the evidence was derived FROM the thing being verified.
        ancestors = graph.ancestors(event.id)
        # Remove the event itself — we want to check the path through inputs
        ancestors.discard(event.id)

        if target_id in ancestors:
            # Find the cycle path for the error message
            violations.append(Violation(
                rule="circular-verification",
                event_id=event.id,
                message=(
                    f"verification target '{target_id}' is an ancestor of this "
                    f"verify event — the evidence depends on the thing being "
                    f"verified, making the check tautological"
                ),
            ))

    return violations


# ---------------------------------------------------------------------------
# Rule 2: Shallow source depth (placeholder for Phase 2)
# Rule 3: Tautological transport (placeholder for Phase 2)
# Rule 4: Estimand substitution (placeholder for Phase 2)
# Rule 5: Brief-as-deme (placeholder for Phase 2)
# ---------------------------------------------------------------------------


ALL_RULES = [
    ("circular-verification", check_circular_verification),
]

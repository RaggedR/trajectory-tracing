import Lake
open Lake DSL

package «trajectory» where
  leanOptions := #[
    ⟨`autoImplicit, false⟩
  ]

-- Trust.lean from trust-boundaries, copied into Containers/
@[default_target]
lean_lib «Containers» where
  srcDir := "."

@[default_target]
lean_lib «Trajectory» where
  srcDir := "."
  roots := #[`Trajectory, `Composition]

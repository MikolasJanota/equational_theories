
import Mathlib.Data.Finite.Prod
import equational_theories.Equations.All
import equational_theories.FactsSyntax
import equational_theories.MemoFinOp
import equational_theories.DecideBang

/-!
This file is generated from the following operator table:
[[0,0,1],[1,1,2],[2,2,1]]
-/

set_option linter.unusedVariables false

/-! The magma definition -/
def «All4x4Tables [[0,0,1],[1,1,2],[2,2,1]]» : Magma (Fin 3) where
  op := finOpTable "[[0,0,1],[1,1,2],[2,2,1]]"

/-! The facts -/
@[equational_result]
theorem «Facts from All4x4Tables [[0,0,1],[1,1,2],[2,2,1]]» :
  ∃ (G : Type) (_ : Magma G) (_: Finite G), Facts G [647, 1252] [622, 630, 1229, 1248, 3306, 3464, 3509, 3511, 3665, 4068] :=
    ⟨Fin 3, «All4x4Tables [[0,0,1],[1,1,2],[2,2,1]]», Finite.of_fintype _, by decideFin!⟩

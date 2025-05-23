
import Mathlib.Data.Finite.Prod
import equational_theories.Equations.All
import equational_theories.FactsSyntax
import equational_theories.MemoFinOp
import equational_theories.DecideBang

/-!
This file is generated from the following operator table:
[[0,4,4,4,4,0,0,0],[2,1,5,7,1,5,1,7],[3,6,2,7,2,2,6,7],[6,6,5,3,3,5,6,3],[0,4,4,4,4,4,4,4],[5,6,5,3,5,5,6,3],[6,6,2,7,6,5,6,7],[7,6,2,7,7,2,6,7]]
-/

set_option linter.unusedVariables false

/-! The magma definition -/
def «All4x4Tables [[0,4,4,4,4,0,0,0],[2,1,5,7,1,5,1,7],[3,6,2,7,2,2,6,7],[6,6,5,3,3,5,6,3],[0,4,4,4,4,4,4,4],[5,6,5,3,5,5,6,3],[6,6,2,7,6,5,6,7],[7,6,2,7,7,2,6,7]]» : Magma (Fin 8) where
  op := finOpTable "[[0,4,4,4,4,0,0,0],[2,1,5,7,1,5,1,7],[3,6,2,7,2,2,6,7],[6,6,5,3,3,5,6,3],[0,4,4,4,4,4,4,4],[5,6,5,3,5,5,6,3],[6,6,2,7,6,5,6,7],[7,6,2,7,7,2,6,7]]"

/-! The facts -/
@[equational_result]
theorem «Facts from All4x4Tables [[0,4,4,4,4,0,0,0],[2,1,5,7,1,5,1,7],[3,6,2,7,2,2,6,7],[6,6,5,3,3,5,6,3],[0,4,4,4,4,4,4,4],[5,6,5,3,5,5,6,3],[6,6,2,7,6,5,6,7],[7,6,2,7,7,2,6,7]]» :
  ∃ (G : Type) (_ : Magma G) (_: Finite G), Facts G [645] [832] :=
    ⟨Fin 8, «All4x4Tables [[0,4,4,4,4,0,0,0],[2,1,5,7,1,5,1,7],[3,6,2,7,2,2,6,7],[6,6,5,3,3,5,6,3],[0,4,4,4,4,4,4,4],[5,6,5,3,5,5,6,3],[6,6,2,7,6,5,6,7],[7,6,2,7,7,2,6,7]]», Finite.of_fintype _, by decideFin!⟩

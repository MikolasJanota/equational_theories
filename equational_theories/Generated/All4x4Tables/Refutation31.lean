
import Mathlib.Data.Finite.Prod
import equational_theories.Equations.All
import equational_theories.FactsSyntax
import equational_theories.MemoFinOp
import equational_theories.DecideBang

/-!
This file is generated from the following operator table:
[[0,2,1,4,3,6,5,8,7],[3,1,5,0,7,2,8,4,6],[4,6,2,8,0,7,1,5,3],[7,5,8,3,6,1,4,0,2],[8,7,6,5,4,3,2,1,0],[6,8,4,7,2,5,0,3,1],[5,3,7,1,8,0,6,2,4],[2,4,0,6,1,8,3,7,5],[1,0,3,2,5,4,7,6,8]]
-/

set_option linter.unusedVariables false

/-! The magma definition -/
def «All4x4Tables [[0,2,1,4,3,6,5,8,7],[3,1,5,0,7,2,8,4,6],[4,6,2,8,0,7,1,5,3],[7,5,8,3,6,1,4,0,2],[8,7,6,5,4,3,2,1,0],[6,8,4,7,2,5,0,3,1],[5,3,7,1,8,0,6,2,4],[2,4,0,6,1,8,3,7,5],[1,0,3,2,5,4,7,6,8]]» : Magma (Fin 9) where
  op := finOpTable "[[0,2,1,4,3,6,5,8,7],[3,1,5,0,7,2,8,4,6],[4,6,2,8,0,7,1,5,3],[7,5,8,3,6,1,4,0,2],[8,7,6,5,4,3,2,1,0],[6,8,4,7,2,5,0,3,1],[5,3,7,1,8,0,6,2,4],[2,4,0,6,1,8,3,7,5],[1,0,3,2,5,4,7,6,8]]"

/-! The facts -/
@[equational_result]
theorem «Facts from All4x4Tables [[0,2,1,4,3,6,5,8,7],[3,1,5,0,7,2,8,4,6],[4,6,2,8,0,7,1,5,3],[7,5,8,3,6,1,4,0,2],[8,7,6,5,4,3,2,1,0],[6,8,4,7,2,5,0,3,1],[5,3,7,1,8,0,6,2,4],[2,4,0,6,1,8,3,7,5],[1,0,3,2,5,4,7,6,8]]» :
  ∃ (G : Type) (_ : Magma G) (_: Finite G), Facts G [2700] [2709, 2736, 2910, 2912, 4658] :=
    ⟨Fin 9, «All4x4Tables [[0,2,1,4,3,6,5,8,7],[3,1,5,0,7,2,8,4,6],[4,6,2,8,0,7,1,5,3],[7,5,8,3,6,1,4,0,2],[8,7,6,5,4,3,2,1,0],[6,8,4,7,2,5,0,3,1],[5,3,7,1,8,0,6,2,4],[2,4,0,6,1,8,3,7,5],[1,0,3,2,5,4,7,6,8]]», Finite.of_fintype _, by decideFin!⟩

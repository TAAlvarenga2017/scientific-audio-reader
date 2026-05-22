from verbalizers.math_verbalizer_1 import simplify_math_for_speech

def test_basic_beta():
    result = simplify_math_for_speech("β̂ = (X'X)^−1 X'y")
    assert "beta" in result.lower()

def test_sigma_square():
    result = simplify_math_for_speech("σ² = ∑(yi - ŷi)² / n")
    assert "sigma ao quadrado" in result.lower()

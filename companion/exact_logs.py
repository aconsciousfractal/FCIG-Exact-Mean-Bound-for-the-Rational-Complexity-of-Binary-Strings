"""Directed logarithm bounds using a rational atanh series and remainder.

For z=(x-1)/(x+1) in [0,1/3], ln(x)=2*sum(z**(2j+1)/(2j+1)).
The remaining positive tail is at most
2*z**(2*TERMS+1)/((2*TERMS+1)*(1-z*z)). Arithmetic is rational throughout.
Division by directed positive bounds for ln(2), then floor/ceiling at
scale 2**60, encloses log2(h). No floating inputs or arithmetic are used.
"""
from fractions import Fraction
from functools import lru_cache

TERMS = 40
SCALE = 1 << 60

def _require(ok, message):
    if not ok:
        raise ValueError(message)

def _exact_fraction(value):
    if type(value) is int:
        return Fraction(value)
    if type(value) is Fraction:
        return value
    raise TypeError("expected an exact built-in int or Fraction; bool and inexact inputs are rejected")

def ln_unit_interval(value):
    """Enclose ln(value) for 1<=value<=2 with Fraction endpoints."""
    value = _exact_fraction(value)
    _require(1 <= value <= 2, "atanh reduction requires 1<=value<=2")
    z = (value - 1) / (value + 1)
    partial = Fraction(0)
    power = z
    for j in range(TERMS):
        partial += 2 * power / (2 * j + 1)
        power *= z * z
    remainder = 2 * power / ((2 * TERMS + 1) * (1 - z * z))
    return partial, partial + remainder

LN2 = ln_unit_interval(2)

@lru_cache(None, typed=True)
def log2_fixed(height):
    """Outward integer endpoints for log2(height), scaled by 2^60."""
    if type(height) is not int:
        raise TypeError("height must be an exact built-in integer, excluding bool")
    _require(height >= 1, "positive integer logarithm required")
    k = height.bit_length() - 1
    if height == 1 << k:
        return k * SCALE, k * SCALE
    lower, upper = ln_unit_interval(Fraction(height, 1 << k))
    lower = k + lower / LN2[1]
    upper = k + upper / LN2[0]
    return ((lower.numerator * SCALE) // lower.denominator,
            -((-upper.numerator * SCALE) // upper.denominator))


"""Complete exact dyadic-height histogram by collision and even-cusp batching.

O(M log M) elementary integer-arithmetic operations, O(M) storage.
No defining oracle, all-threshold recount or timing-based complexity claim.
Here M=2**N; heights minimize max(abs(a), b) subject to a=r*b modulo M
and positive odd b. Zero is included in the uniform residue population.
This bound is for the histogram, not logarithm precision or bit operations.
The manuscript proves the central shell, collision and two-neighbor formulas.
"""
from fractions import Fraction
from math import gcd, isqrt

def require(ok, message):
    if not ok:
        raise ValueError(message)

def modulus_guard(m):
    if type(m) is not int:
        raise TypeError("modulus must be an exact built-in integer, excluding bool")
    require(m >= 2 and (m & (m - 1)) == 0, "M must be a power of two >=2")

def ceildiv(n, d):
    require(d > 0, "positive denominator required")
    return -((-n) // d)

def totients(limit):
    phi = list(range(limit + 1))
    if limit >= 1:
        phi[1] = 1
    for p in range(2, limit + 1):
        if phi[p] == p:
            for multiple in range(p, limit + 1, p):
                phi[multiple] -= phi[multiple] // p
    return phi

def initial_holes(m, threshold):
    """Generate disjoint integer survivor pieces, computing each inverse once."""
    for q in range(2, (m - 1) // threshold + 1, 2):
        for a in range(1, q):
            if gcd(a, q) != 1:
                continue
            inverse = pow(a, -1, q)
            left_b = inverse + q * ((threshold - inverse) // q)
            right_class = q - inverse
            right_b = right_class + q * ((threshold - right_class) // q)
            require(left_b > 0 and right_b > 0, "missing neighbor denominator")
            low_num = a * m * left_b - m + q * threshold
            high_num = a * m * right_b + m - q * threshold
            first = low_num // (q * left_b) + 1
            last = ceildiv(high_num, q * right_b) - 1
            yield a, q, inverse, first, last

def survivor_height(m, threshold, r, a, q, inverse):
    """Two determinant-one candidate heights; inverse supplied once per cusp."""
    d = abs(a * m - q * r)
    require(q < threshold and d < threshold and d * d < m, "survivor phase outside initial hole bounds")
    u = inverse if q * r <= a * m else q - inverse
    bminus = u + q * ((m - u * (q + d)) // (q * (q + d)))
    bplus = bminus + q
    numerator = m - d * bminus
    require(bminus > 0 and numerator >= 0 and numerator % q == 0, "invalid determinant-one witness")
    height = min(numerator // q, bplus)
    require(threshold < height <= m // 2, "height not a surviving support value")
    return height

def batched_histogram(m):
    """Return all bins, including zero bins, and bounded operation counters."""
    modulus_guard(m)
    bound = m // 2
    limit = isqrt(m)
    threshold = limit + (limit * limit < m)
    phi = totients(limit)
    collisions = [0] * (limit + 1)
    stats = {"central_coprime_pairs": 0, "central_collision_events": 0,
             "initial_cusps": 0, "survivor_residues": 0, "bridge_atom": 0}
    for b in range(1, limit + 1, 2):
        for d in range(1, limit + 1, 2):
            if gcd(b, d) != 1:
                continue
            stats["central_coprime_pairs"] += 1
            a0 = (m * pow(d, -1, b)) % b if b > 1 else 0
            zlow = ceildiv(m - b * limit - d * a0, b * d)
            zhigh = (limit - a0) // b
            require(zhigh - zlow + 1 <= 1, "central phase not unique")
            if zlow <= zhigh:
                a = a0 + b * zlow
                e = (m - a * d) // b
                require(1 <= a <= limit and 1 <= e <= limit and a * d + e * b == m,
                        "invalid central collision")
                collisions[max(a, e, b, d)] += 1
                stats["central_collision_events"] += 1
    bins = [0] * (bound + 1)
    for h in range(1, limit + 1):
        shell = 1 if h == 1 else phi[h] if h % 2 == 0 else 3 * phi[h] // 2
        bins[h] = (1 if h == 1 else 0) + 2 * shell - collisions[h]
        require(bins[h] >= 0, "negative central mass")
    central_mass = sum(bins)
    if threshold < bound:
        for a, q, inverse, first, last in initial_holes(m, threshold):
            stats["initial_cusps"] += 1
            for r in range(first, last + 1):
                require(0 <= r < m, "survivor outside residue interval")
                height = survivor_height(m, threshold, r, a, q, inverse)
                bins[height] += 1
                stats["survivor_residues"] += 1
        if threshold > limit:
            bridge = m - central_mass - stats["survivor_residues"]
            require(bridge >= 0, "negative bridge atom")
            bins[threshold] = bridge
            stats["bridge_atom"] = bridge
        else:
            require(central_mass + stats["survivor_residues"] == m, "square-root splice mass mismatch")
    require(bins[0] == 0 and sum(bins) == m, "complete histogram mass mismatch")
    return bins, stats


def validate_histogram(bins):
    """Check the dense representation (entry zero is a sentinel)."""
    if type(bins) not in (list, tuple):
        raise TypeError("histogram must be a list or tuple of exact integers")
    require(len(bins) >= 2, "histogram must contain a positive height")
    if any(type(count) is not int for count in bins):
        raise TypeError("histogram counts must be exact built-in integers")
    require(bins[0] == 0 and all(count >= 0 for count in bins), "invalid histogram count")
    m = sum(bins)
    modulus_guard(m)
    require(len(bins) == m // 2 + 1 and bins[-1] > 0, "histogram support must end at M/2")
    return m


def exact_raw_moments(bins):
    """Return exact E[R], E[R**2] and Var(R) as rational finite values."""
    m = validate_histogram(bins)
    first = Fraction(sum(h * c for h, c in enumerate(bins)), m)
    second = Fraction(sum(h * h * c for h, c in enumerate(bins)), m)
    return first, second, second - first * first


def log_moment_coefficients(bins):
    """Exact coefficients: E[(log2 R)**j] = sum(weight * log2(h)**j).

    For j=1,2 this gives the exact finite mean and second moment; subtract
    the square of the j=1 expression to obtain the logarithmic variance.
    Evaluating logarithms with a chosen precision is a separate operation.
    """
    m = validate_histogram(bins)
    return tuple((h, Fraction(c, m)) for h, c in enumerate(bins) if c)


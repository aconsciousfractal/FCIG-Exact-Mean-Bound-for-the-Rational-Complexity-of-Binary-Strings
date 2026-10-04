"""Replay a fixed finite distribution and moment panel (Python >=3.10).

The production histogram is recomputed for N=1,...,11. A separate defining
minimum oracle is deliberately confined to N=1,...,8. Finite agreement is
not a proof for every N, an asymptotic theorem, or a bit-complexity bound.
"""
import argparse
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from math import gcd
from pathlib import Path

from companion.distribution import (batched_histogram, exact_raw_moments,
                                    initial_holes, log_moment_coefficients,
                                    modulus_guard, require, validate_histogram)
from companion.exact_logs import SCALE, TERMS, ln_unit_interval, log2_fixed

BASE = Path(__file__).resolve().parent
MANUAL_LAWS = {
    1: [[1, 2]],
    2: [[1, 3], [2, 1]],
    3: [[1, 3], [2, 2], [3, 2], [4, 1]],
    4: [[1, 3], [2, 2], [3, 6], [4, 2], [5, 2], [8, 1]],
}


def sparse_histogram(bins):
    return [[h, c] for h, c in enumerate(bins) if c]


def logarithmic_enclosures(bins):
    """Rational enclosures of mean, second moment and logarithmic variance.

    log2(h) is nonnegative. Thus squaring its directed endpoints preserves
    order. Var(X)=E[X**2]-E[X]**2 yields [slo-mhi**2, shi-mlo**2].
    Intersect the lower end with zero, a mathematical nonnegativity bound.
    """
    m = validate_histogram(bins)
    first_lo = first_hi = second_lo = second_hi = 0
    for h, c in enumerate(bins):
        if not c:
            continue
        lo, hi = log2_fixed(h)
        require(0 <= lo <= hi, "unordered logarithm endpoints")
        first_lo += c * lo
        first_hi += c * hi
        second_lo += c * lo * lo
        second_hi += c * hi * hi
    mean = (Fraction(first_lo, m * SCALE), Fraction(first_hi, m * SCALE))
    second = (Fraction(second_lo, m * SCALE**2), Fraction(second_hi, m * SCALE**2))
    variance = (max(Fraction(0), second[0] - mean[1]**2), second[1] - mean[0]**2)
    require(variance[0] <= variance[1], "unordered variance enclosure")
    return {"mean": [str(x) for x in mean], "second_moment": [str(x) for x in second],
            "variance": [str(x) for x in variance]}


def defining_oracle(m):
    """Independent bounded minimization, with no production formula calls.

    b=1 proves height<=M/2, so no larger b can improve the minimum. For
    each odd b<=M/2 choose the centered congruent numerator (either sign
    at the tie); common odd content can be divided out without changing
    the residue. Primitive candidates suffice and are checked explicitly.
    This is quadratic arithmetic work, excluded from the histogram claim.
    """
    if type(m) is not int or not (2 <= m <= 256 and m & (m - 1) == 0):
        raise ValueError("oracle is confined to dyadic moduli 2,...,256")
    bins = [0] * (m // 2 + 1)
    candidates = 0
    for r in range(m):
        minimum = m // 2
        for b in range(1, m // 2 + 1, 2):
            residue = (r * b) % m
            a = residue if 2 * residue <= m else residue - m
            candidates += 1
            if gcd(a, b) == 1:
                minimum = min(minimum, max(abs(a), b))
        bins[minimum] += 1
    return bins, candidates


def validate_row(row, bins):
    """Compare all data against the recomputed histogram; fail closed."""
    require(type(row) is dict, "certificate row must be an object")
    n = row["N"]
    require(type(n) is int and 1 <= n <= 11, "certificate N domain")
    m = 1 << n
    require(type(row["M"]) is int and row["M"] == m, "certificate modulus")
    require(validate_histogram(bins) == m, "certificate mass")
    hist = row["histogram"]
    require(type(hist) is list and all(type(pair) is list and len(pair) == 2
            and all(type(x) is int for x in pair) and pair[0] >= 1 and pair[1] > 0
            for pair in hist), "certificate sparse histogram shape")
    require(hist == sparse_histogram(bins), "complete histogram mismatch")
    expected_raw = dict(zip(("mean", "second_moment", "variance"),
                           map(str, exact_raw_moments(bins))))
    require(row["raw_moments"] == expected_raw, "exact raw moment mismatch")
    require(row["logarithmic_enclosures"] == logarithmic_enclosures(bins),
            "directed logarithmic enclosure mismatch")
    coefficients = log_moment_coefficients(bins)
    require(sum(weight for _, weight in coefficients) == 1, "log coefficient mass")
    cumulative = previous = 0
    for count in bins:
        cumulative += count
        require(previous <= cumulative <= m, "CDF range or monotonicity")
        previous = cumulative
    require(cumulative == m, "terminal CDF mass")
    return len(bins)


def invalid_input_checks():
    """Warm integer cache keys before attempts with numerically equal types."""
    log2_fixed(1)
    log2_fixed(3)
    cases = [(log2_fixed, x) for x in (True, 3.0, Fraction(3), "3", None, 3+0j, [3], 0, -1)]
    cases += [(ln_unit_interval, x) for x in (True, 1.0, "1", None, 1+0j, [1],
                                             Fraction(0), 0, Fraction(3), 3)]
    cases += [(modulus_guard, x) for x in (True, 8.0, Fraction(8), "8", 0, 1, 6)]
    for function, value in cases:
        try:
            function(value)
        except (ValueError, TypeError):
            pass
        else:
            raise ValueError("invalid input accepted by " + function.__name__)
    for x in (1, 2):
        require(ln_unit_interval(x) == ln_unit_interval(Fraction(x)), "integer/Fraction compatibility")
    require(log2_fixed(1) == (0, 0) and log2_fixed(8) == (3*SCALE, 3*SCALE),
            "exact power-of-two logarithms")
    return len(cases)


def open_endpoint_check():
    """At M=32,K=6 the cusp 1/2 has hole (14,18), not [14,18]."""
    pieces = [piece for piece in initial_holes(32, 6) if piece[:2] == (1, 2)]
    require(pieces == [(1, 2, 1, 15, 17)], "open even-hole endpoints")
    for r, a in ((14, 6), (18, -6)):
        require((a - 5*r) % 32 == 0 and max(abs(a), 5) == 6,
                "closed coverage must include both hole endpoints")
    return {"open_integer_survivors": 3, "endpoint_witnesses": 2}


def negative_certificate_checks(first_row, bins):
    """Check altered data, including equal-valued bools, cannot pass."""
    rejected = []
    for name in ("mass", "boolean_count", "modulus", "raw_moment", "log_endpoint"):
        altered = deepcopy(first_row)
        if name == "mass":
            altered["histogram"][0][1] += 1
        elif name == "boolean_count":
            altered["histogram"][0][1] = True
        elif name == "modulus":
            altered["M"] *= 2
        elif name == "raw_moment":
            altered["raw_moments"]["variance"] = "1"
        else:
            altered["logarithmic_enclosures"]["mean"][1] = "1"
        try:
            validate_row(altered, bins)
        except (ValueError, TypeError, KeyError):
            rejected.append(name)
        else:
            raise ValueError("altered certificate accepted: " + name)
    return rejected


def replay(data):
    require(data["schema"] == "dyadic-distribution-certificates-v1", "certificate schema")
    require(data["log_terms"] == TERMS and type(data["log_terms"]) is int
            and data["log_scale"] == SCALE and type(data["log_scale"]) is int,
            "certificate logarithm precision")
    rows = data["levels"]
    require(type(rows) is list and len(rows) == 11
            and [row["N"] for row in rows] == list(range(1, 12)), "fixed N=1,...,11 panel")
    counts = {"histograms": 0, "histogram_population": 0, "cdf_values": 0,
              "raw_moment_values": 0, "log_moment_enclosures": 0, "manual_laws": 0,
              "oracle_histograms": 0, "oracle_residues": 0, "oracle_candidates": 0}
    operation_counts = {}
    first_bins = None
    for row in rows:
        n, m = row["N"], row["M"]
        require(type(n) is int and type(m) is int and m == 1 << n, "level integer type")
        bins, stats = batched_histogram(m)
        counts["cdf_values"] += validate_row(row, bins)
        counts["histograms"] += 1
        counts["histogram_population"] += m
        counts["raw_moment_values"] += 3
        counts["log_moment_enclosures"] += 3
        for key, value in stats.items():
            operation_counts[key] = operation_counts.get(key, 0) + value
        if n == 1:
            first_bins = bins
        if n in MANUAL_LAWS:
            require(sparse_histogram(bins) == MANUAL_LAWS[n], "manual small law mismatch")
            counts["manual_laws"] += 1
        if n <= 8:
            independent, candidates = defining_oracle(m)
            require(bins == independent, "independent defining minimum mismatch")
            counts["oracle_histograms"] += 1
            counts["oracle_residues"] += m
            counts["oracle_candidates"] += candidates
    counts["invalid_input_rejections"] = invalid_input_checks()
    counts["negative_certificate_rejections"] = len(negative_certificate_checks(rows[0], first_bins))
    endpoints = open_endpoint_check()
    panel = [[row["N"], row["histogram"]] for row in rows]
    panel_bytes = json.dumps(panel, sort_keys=True, separators=(",", ":")).encode("utf8")
    require(data["histogram_panel_sha256"] == hashlib.sha256(panel_bytes).hexdigest(),
            "fixed histogram panel digest mismatch")
    require(counts["oracle_residues"] == 510 and counts["histogram_population"] == 4094,
            "finite panel population budget")
    return {"status": "PASS_FINITE_DISTRIBUTION_AND_MOMENT_PREMISES", "counts": counts,
            "histogram_operation_counts": operation_counts, "open_endpoints": endpoints,
            "scope": "N=1,...,11 only; defining oracle N=1,...,8 only; all-N and asymptotic conclusions require manuscript proofs"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional deterministic JSON result file")
    args = parser.parse_args()
    certificate = BASE / "distribution_certificates.json"
    result = replay(json.loads(certificate.read_text(encoding="utf8")))
    inputs = [BASE / name for name in ("distribution.py", "exact_logs.py", "verify_distribution.py",
                                      "distribution_certificates.json")]
    result["sha256"] = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in inputs}
    rendered = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf8", newline="\n")
    print(rendered, end="")


if __name__ == "__main__":
    main()

"""Small finite laws, certificate failures and exact-input regression tests."""
from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path
import unittest

from companion.distribution import (batched_histogram, exact_raw_moments,
                                    log_moment_coefficients, validate_histogram)
from companion.exact_logs import SCALE, ln_unit_interval, log2_fixed
from companion.verify_distribution import (MANUAL_LAWS, defining_oracle,
    invalid_input_checks, logarithmic_enclosures, negative_certificate_checks,
    open_endpoint_check, sparse_histogram, validate_row)


class DistributionTests(unittest.TestCase):
    def test_manual_small_laws(self):
        for n, law in MANUAL_LAWS.items():
            with self.subTest(N=n):
                bins, stats = batched_histogram(1 << n)
                self.assertEqual(sparse_histogram(bins), law)
                self.assertEqual(sum(bins), 1 << n)
                self.assertEqual(stats["survivor_residues"], sum(bins[5:]) if n == 4 else
                                 (1 if n == 3 else 0))

    def test_moments_against_expanded_manual_population(self):
        for n, law in MANUAL_LAWS.items():
            population = [h for h, count in law for _ in range(count)]
            bins = [0] * ((1 << n) // 2 + 1)
            for h in population:
                bins[h] += 1
            mean = Fraction(sum(population), len(population))
            variance = sum((Fraction(h) - mean)**2 for h in population) / len(population)
            actual = exact_raw_moments(bins)
            self.assertEqual(actual[0], mean)
            self.assertEqual(actual[2], variance)
            self.assertEqual(sum(weight for _, weight in log_moment_coefficients(bins)), 1)

    def test_power_of_two_log_moments_are_exact(self):
        bins = [0, 3, 1]
        result = logarithmic_enclosures(bins)
        self.assertEqual(result["mean"], ["1/4", "1/4"])
        self.assertEqual(result["second_moment"], ["1/4", "1/4"])
        self.assertEqual(result["variance"], ["3/16", "3/16"])
        self.assertEqual(log2_fixed(8), (3*SCALE, 3*SCALE))

    def test_invalid_and_cache_types(self):
        self.assertEqual(invalid_input_checks(), 26)
        log2_fixed.cache_clear()
        log2_fixed(1)
        log2_fixed(3)
        for x in (True, 1.0, Fraction(1), 3.0, Fraction(3)):
            with self.subTest(value=repr(x)):
                with self.assertRaises(TypeError):
                    log2_fixed(x)
        self.assertEqual(ln_unit_interval(2), ln_unit_interval(Fraction(2)))

    def test_analytic_atanh_endpoints(self):
        lo, hi = ln_unit_interval(2)
        self.assertEqual(ln_unit_interval(1), (Fraction(0), Fraction(0)))
        self.assertIs(type(lo), Fraction)
        self.assertIs(type(hi), Fraction)
        # Independent elementary bounds: 2/3 < ln(2) < 7/10.
        self.assertLess(Fraction(2, 3), lo)
        self.assertLess(hi, Fraction(7, 10))
        self.assertLess(hi - lo, Fraction(1, 10**38))

    def test_histogram_rejects_wrong_types_and_support(self):
        for bins in ([0, True, 1], [1, 1], [0, 2, 0], [0, -1, 5], [0, 2.0], [0, 3]):
            with self.subTest(bins=bins):
                with self.assertRaises((ValueError, TypeError)):
                    validate_histogram(bins)
        for m in (True, 8.0, Fraction(8), 0, 1, 6):
            with self.subTest(modulus=repr(m)):
                with self.assertRaises((ValueError, TypeError)):
                    batched_histogram(m)

    def test_open_endpoint_witnesses(self):
        self.assertEqual(open_endpoint_check(), {"open_integer_survivors": 3, "endpoint_witnesses": 2})

    def test_certificate_negative_controls(self):
        path = Path(__file__).resolve().parents[1] / "companion/distribution_certificates.json"
        row = json.loads(path.read_text(encoding="utf8"))["levels"][0]
        bins = [0, 2]
        self.assertEqual(validate_row(row, bins), 2)
        self.assertEqual(len(negative_certificate_checks(row, bins)), 5)
        altered = deepcopy(row)
        altered["N"] = True
        with self.assertRaises(ValueError):
            validate_row(altered, bins)

    def test_oracle_budget_is_enforced(self):
        for m in (512, True, 256.0, 6):
            with self.assertRaises(ValueError):
                defining_oracle(m)


if __name__ == "__main__":
    unittest.main()

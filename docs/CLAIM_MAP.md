# Claim and artifact map

| Statement | Written evidence | Executable premise |
| --- | --- | --- |
| Uniform ordinary mean <= N/2, every N>=1 | Theorem 1.1 and its proof in Section 6 | Both finite interfaces below |
| Two-lift product and noninductive budget reduction | Section 2 | No numerical premise |
| Actual odd-coset tail bound | Section 3 | No phase-average substitution |
| Lattice-sum estimate and two-prime sieve | Section 4 | No numerical premise |
| Central credit and analytic parent n>=26 | Section 5 | Rational comparisons checked by `cutoff()`; analytic inequalities are in the proof |
| Parent n=1,...,12 budget | Section 6, exact product inequality | Every residue in `small`, exact witnesses/minimality/products |
| Parent n=13,...,25 budget | Section 6, positive directed-log margin | Every dyadic cell in `bridge`, recomputed integer sums |
| Directed logarithmic rounding | Appendix A | `unit_log` and `log_upper` |

The source and PDF are in `paper/`. The complete author-generated data are in
`companion/finite_certificates.json`; the standard-library checker is
`companion/verify_mean.py`. [REPRODUCE.md](../REPRODUCE.md) specifies the reader commands.
The manuscript proves the analytic portion; the program validates finite premises.

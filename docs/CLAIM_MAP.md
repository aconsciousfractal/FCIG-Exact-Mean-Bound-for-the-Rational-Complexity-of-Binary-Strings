# Claim and artifact map

Every result below uses the uniform ensemble on all `M = 2^N` residues,
including zero, and the positive-odd-denominator height `R_N`.
The written proof is in the manuscript source and PDF in [paper/](../paper/).

| Statement | Written evidence | Executable evidence and its scope |
| --- | --- | --- |
| Ordinary unrounded mean `E log_2 R_N <= N/2`, every `N >= 1` | Theorem 1.1, proved in Sections 2–6: two-lift product, tail budget, primitive lattice sums, sieve and central credit | [verify_mean.py](../companion/verify_mean.py) checks the finite premises in [finite_certificates.json](../companion/finite_certificates.json); it does not replace the analytic proof |
| Parent lengths 1–12 and 13–25 in that proof | Section 6: exact product inequalities for the first range; directed-log margins for the second; analytic parent cutoff at 26 in Section 5 | `small`, `bridge` and `cutoff()` in the mean checker recompute the relevant witnesses, products and integer sums |
| Complete finite distribution for every `N >= 1` | Theorem 7.1: primitive central count and collisions through `sqrt(M)`; disjoint open even-Farey holes above it; closed endpoint and small-length conventions | [distribution.py](../companion/distribution.py) implements the formulas and histogram; [verify_distribution.py](../companion/verify_distribution.py) checks the bounded panel in [distribution_certificates.json](../companion/distribution_certificates.json) against separate finite routes |
| Exact finite `Var(log_2 R_N)` | Theorem 7.2: finite survival-sum identities for the first two log moments, followed by subtraction of the squared mean | [exact_logs.py](../companion/exact_logs.py) provides rational logarithmic enclosures; finite computed enclosures remain conditional on the arithmetic formulas and analytic log bounds |
| `R_N / 2^(N/2)` converges to a positive variable with survival `G_2(t^2)` | Sections 9–10: Lemma 9.1 marked-lattice bridge, checked equidistribution and mixing imports, Haar-null boundaries, and identification of the known Boca–Gologan law | No finite panel proves this limiting theorem |
| Logarithmic mean offset and variance limit `0.892302571204274625294755...` | Theorem 11.2 and Lemma 11.1: bilateral tails give uniform integrability; explicit integrals of the squared-limit density give the moments and base-two factors | [limit_constants.py](../companion/limit_constants.py) checks the closed expression and displayed rational enclosure; it does not prove distributional or moment convergence |
| `E R_N ~ [32 ln(1+sqrt(2))/(3 pi^2)] 2^(N/2)` | Proposition 12.1: positive-tail uniform integrability and an elementary half-moment evaluation of the known law | Finite raw means are diagnostics, not the asymptotic proof |
| Strictly positive limiting Jensen gap | Proposition 12.1: raw-mean and log-mean convergence, with strict Jensen for the nonconstant limiting variable | No numerical finite gap is used as a theorem premise |
| Joint histogram in `O(N 2^N)` arithmetic operations, `O(2^N)` stored integers | Proposition 8.1: batched central events and exact two-neighbor heights in persistent even holes; the proof counts the events and operations | The standalone histogram implementation is separate from the slower verification oracles; diagnostic runtime does not establish the complexity bound |

[REPRODUCE.md](../REPRODUCE.md) gives reader commands. The two certificate
sets have different roles: the mean certificates are premises of its hybrid
proof; the distribution panel verifies bounded cases of a separately proved
all-length formula. The finite law, limiting law and constant evaluation are
separate claims. Neither the histogram cost nor a successful checker run
establishes bit complexity, a convergence rate, raw-height variance, external
priority or a Collatz consequence.

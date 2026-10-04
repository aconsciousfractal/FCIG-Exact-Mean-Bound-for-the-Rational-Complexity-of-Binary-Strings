# Rational complexity of binary strings: exact mean, finite distribution and logarithmic variance

**Oleksiy Babanskyy** · [ORCID](https://orcid.org/0009-0001-6176-6208)

This repository accompanies the [paper](paper/Exact-Mean-Bound-for-the-Rational-Complexity-of-Binary-Strings.pdf)
and its [standalone LaTeX source](paper/Exact-Mean-Bound-for-the-Rational-Complexity-of-Binary-Strings.tex).

For $M=2^N$, $N\ge1$, let
$$
R_N(r)=\min\{\max(|a|,b):a\equiv rb\pmod M,\ b>0\text{ odd}\},
$$
with uniform weight on all $M$ residues, including zero, and unrounded logarithms.

The paper proves $\mathbb E\log_2R_N\le N/2$ at every length, gives the complete
finite distribution and an exact arithmetic-logarithmic formula for
$\operatorname{Var}(\log_2R_N)$, and evaluates
$$
\mathbb E\log_2R_N=N/2+c_R+o(1),\qquad
\operatorname{Var}(\log_2R_N)=\sigma_R^2+o(1),
$$
where
$$
c_R=\frac{7\zeta(3)/(2\pi^2)-1}{2\log2},\qquad
\sigma_R^2=0.892302571204274625294755\ldots.
$$
The closed variance expression is in the paper. Further corollaries are
$$
\mathbb E R_N\sim\frac{32\log(1+\sqrt2)}{3\pi^2}\,2^{N/2},
$$
a positive limiting Jensen gap, and a complete-histogram algorithm using
$O(N2^N)$ arithmetic operations and $O(2^N)$ storage.

These address [Lin-Xiao-Chen (2026), Question 3.1](https://doi.org/10.3934/math.2026823)
through an all-length mean inequality, a finite variance formula and an evaluated
limiting variance. The finite formula is a sum, rather than a short elementary
expression in $N$. The limiting geometric law is identified with a previously
known Boca-Gologan law, with its published normalization and method antecedents credited.

## Verify

Python >=3.10; standard library only. From the repository root:

~~~text
python -B scripts/check_manifest.py
python -B scripts/reproduce.py
python -B -O scripts/reproduce.py
python -B scripts/reproduce_distribution.py
python -B -O scripts/reproduce_distribution.py
python -B scripts/reproduce_constants.py
python -B -O scripts/reproduce_constants.py
python -B -m unittest discover -s tests -v
python -B -O -m unittest discover -s tests -v
~~~

Mean replay checks 8,190 exact minima and 9,068,656 positive primitive pairs.
Distribution replay recomputes eleven histograms and finite moments, with a
smaller independent defining oracle. Constant replay encloses the limiting
expressions by rational series. Each replay is deterministic in normal and
optimized Python. The manuscript supplies the all-length and limiting proofs.

[Reproduction](REPRODUCE.md) · [Reviewer path](README_REVIEWER.md) ·
[Claim map](docs/CLAIM_MAP.md) · [Sources](docs/SOURCES.md) ·
[Limits](docs/KNOWN_LIMITS.md)

## Scope and attribution

Known geometric laws and general moment methods are distinguished from their
application and evaluation here. Chen-Winterhof locators refer to arXiv v1;
the final journal body was not read. No universal priority is certified.

No effective rate, polynomial algorithm in $N$, bit-complexity bound, raw-height
variance theorem or Collatz consequence is asserted.
[AI_USE.md](AI_USE.md) discloses shared AI assistance and review exposure.

Version **0.2.0**. [Changes](CHANGELOG.md).
Code, certificates and documentation: [MIT](LICENSE).
Original manuscript source/PDF: [CC BY 4.0](LICENSE_MANUSCRIPT.md).
[License scopes](LICENSE_SCOPE.md) · [Third-party notices](THIRD_PARTY_NOTICES.md).

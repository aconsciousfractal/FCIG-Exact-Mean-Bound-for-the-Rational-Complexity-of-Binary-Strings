# An exact mean bound for the rational complexity of binary strings

**Oleksiy Babanskyy** · [ORCID](https://orcid.org/0009-0001-6176-6208)

This repository accompanies the [paper](paper/Exact-Mean-Bound-for-the-Rational-Complexity-of-Binary-Strings.pdf)
and its [standalone LaTeX source](paper/Exact-Mean-Bound-for-the-Rational-Complexity-of-Binary-Strings.tex).

For every integer $N\ge1$, put $M=2^N$ and define
$R_N(r)=\min\{\max(|a|,b):a\equiv rb\pmod M,\ b>0\text{ odd}\}$.
The paper proves
$$
\frac1{2^N}\sum_{r=0}^{2^N-1}\log_2R_N(r)\le\frac N2.
$$
The logarithm is unrounded and the average includes all binary strings,
including zero. This answers the **mean part** of Question 3.1 in
[Lin–Xiao–Chen (2026)](https://doi.org/10.3934/math.2026823).

The proof combines an analytic argument for lengths $N\ge27$ with exact
finite certificates for the remaining lengths. Its two-lift product estimate
reduces the mean bound to a balance between short primitive representations and
the large-height tail. The finite computation is an essential premise of the proof.

## Verify

Python 3.10 or newer; standard library only. From the repository root:

```text
python -B scripts/check_manifest.py
python -B scripts/reproduce.py
python -B -O scripts/reproduce.py
python -B -m unittest discover -s tests -v
```

The two full replay commands produce the same mathematical JSON, including
8,190 exact minima and 9,068,656 positive primitive pairs.
The checker verifies the finite premises; the manuscript supplies the analytic proof.
`--quick` is a structural check and does not recompute the bridge sums.

[Reproduction details](REPRODUCE.md) · [Reviewer path](README_REVIEWER.md) ·
[Claim map](docs/CLAIM_MAP.md) · [Sources](docs/SOURCES.md) ·
[Limits](docs/KNOWN_LIMITS.md)

## Scope and attribution

Tian–Qi and Chen–Winterhof studied the same ordinary mean. Classical counting,
growth and geometry tools are credited in the paper. Detailed Chen–Winterhof
theorem locators refer to arXiv v1; the journal final body was not read.
No universal priority claim follows from the source comparison.
The variance question, individual infinite 2-adic values and Collatz trajectories
remain outside the result.

Version: **0.1.0**. [AI-use disclosure](AI_USE.md).
Companion code, certificates and repository documentation: [MIT](LICENSE).
Original manuscript source and PDF: [CC BY 4.0](LICENSE_MANUSCRIPT.md).
See [license scopes](LICENSE_SCOPE.md) and [third-party notices](THIRD_PARTY_NOTICES.md).

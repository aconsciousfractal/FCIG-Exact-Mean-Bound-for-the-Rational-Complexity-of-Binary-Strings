# Reproduce the finite premises

## Environment and commands

Python >=3.10, standard library only. No package installation, external data,
network access or Git command is required. Run from the repository root:

```text
python -B scripts/check_manifest.py
python -B scripts/reproduce.py
python -B -O scripts/reproduce.py
python -B -m unittest discover -s tests -v
python -B -O -m unittest discover -s tests -v
```

A full replay usually takes minutes on a desktop. It enumerates a fixed finite
domain rather than searching for a cutoff. Expected status:
`PASS_FINITE_PREMISES`; exit code 0; small population 8,190; bridge population
9,068,656 positive primitive pairs out of 11,182,008 raw pairs; all 13 margins
strictly positive; seven negative controls rejected.
Normal and optimized runs print identical JSON for the same distributed files.

For a fast partial check, run `python -B scripts/reproduce.py --quick`.
Its status is `PASS_QUICK_STRUCTURAL_ONLY`: it omits bridge resummation and
cannot substitute for the full finite replay.

## What is checked

Parent lengths 1–12: every residue's primitive witness and minimum, followed by
the exact product inequality for the truncated logarithmic budget.
Parent lengths 13–25: exact Möbius counts and dyadic cells; twelve-term atanh
sums at scale $2^{40}$ with integer rounding directed toward the required
bound, plus a rigorous remainder; cell/aggregate sums and margins.
The rational cutoff comparisons are checked as arithmetic, with their analytic
meaning justified in the manuscript.

[companion/finite_certificates.json](companion/finite_certificates.json)
contains the complete finite data; [the checker](companion/verify_mean.py)
recomputes all mathematical assertions used by these finite interfaces.
Its explicit `require` guards remain active under `python -O`.
Certificates are author-generated integer data, not downloaded third-party tables.

## Optional PDF build

The distributed paper can be read without TeX. To rebuild with an existing
`pdflatex`, run:

```text
python -B scripts/build_pdf.py
```

The builder disables shell escape and, for MiKTeX, automatic package installation.
A missing TeX installation or package is reported rather than installed.
Auxiliaries are placed in `paper/build/`. The rebuilt PDF may differ bytewise
because of toolchain metadata. Verify the distributed manifest **before** rebuilding;
a changed PDF needs a new content manifest if it is redistributed.
No PDF rebuild is required for the standard finite replay.

# Reproduce the premises and constant evaluation

Python >=3.10, standard library only. No installation, network, external data or
Git command is required. Run from the repository root:

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

Each replay pair prints identical mathematical JSON. Mean replay usually takes
minutes; observed runtimes do not prove an arithmetic complexity bound.

## Exact-mean premises

PASS_FINITE_PREMISES checks 8,190 minima, 9,068,656 positive primitive pairs out
of 11,182,008 raw pairs, thirteen positive margins and seven negative controls.
Parent lengths1-12 use exact minima; lengths13-25 recompute Möbius counts,
dyadic cells and outward integer logarithmic bounds.

[finite_certificates.json](companion/finite_certificates.json) and
[verify_mean.py](companion/verify_mean.py) retain the original proof premises.
The optional --quick command is structural only and omits bridge resummation.

## Finite distribution and moments

[distribution.py](companion/distribution.py) uses primitive shells, collision
timestamps and one initial hole decomposition. Its $O(M\log M)$ bound counts
arithmetic operations, with $O(M)$ storage; the production route does not run
the defining oracle or recount every threshold.

[distribution_certificates.json](companion/distribution_certificates.json)
contains exact author-generated histograms for $N=1,\ldots,11$ and moment
enclosures. [verify_distribution.py](companion/verify_distribution.py)
recomputes all eleven histograms, checks2058 CDF entries, and derives finite raw
and logarithmic moments. An independent oracle covers only $N=1,\ldots,8$
(510 residues); four small laws are also specified by hand.

[exact_logs.py](companion/exact_logs.py) uses forty rational atanh terms, a
geometric remainder and directed rounding at scale $2^{60}$. Integer inputs are
converted before division; bool/inexact inputs are rejected. Variance enclosures
subtract the enclosed square of the mean with outward endpoints. Explicit guards
remain active under -O. These finite checks do not prove the limit theorem.

## Limiting constants

[limit_constants.py](companion/limit_constants.py) uses Euler-transformed eta
sums for $\zeta(2),\zeta(3),\zeta(4)$ (96 terms), an atanh series for $\log2$
(40 terms), and $\operatorname{Li}_4(1/2)$ (96 terms). Arithmetic and remainders
are rational; decimal endpoints are rounded outward to24 places:
$$
-0.413852654438430019863271\le c_R\le-0.413852654438430019863270,
$$
$$
0.892302571204274625294755\le\sigma_R^2\le0.892302571204274625294756.
$$
This certifies evaluation conditional on the analytic formula and classical
identities, not the limiting-law theorem or a formal proof.

Each replay accepts --output PATH; its parent directory must exist.
Keep generated output outside the distributed tree or in an excluded build/
directory so it does not alter the manifest file set.

## Optional PDF build

With an existing pdflatex installation:

~~~text
python -B scripts/build_pdf.py
~~~

The builder disables shell escape and MiKTeX automatic installation. Missing TeX
or packages are reported rather than installed. Auxiliaries go to paper/build/.
PDF metadata can change bytes: check the distributed manifest before rebuilding,
and generate a new manifest before redistributing a changed PDF.
Source/PDF filenames are retained so preceding repository links resolve.

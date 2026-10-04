# Sources and positioning

The ensemble is uniform on all residues modulo `M = 2^N`, including zero.
The height is `R_N = min max(|a|, b)` over positive odd `b` with
`a = rb (mod M)`. The ordinary logarithmic mean, logarithmic variance and
raw-height mean are different observables.

| Source | Identity, locator and use |
| --- | --- |
| Tian–Qi, *Expected values for the rational complexity of finite binary sequences* | DCC 55 (2010), 65–79, [DOI](https://doi.org/10.1007/s10623-009-9331-x). Same ordinary logarithmic mean; primitive counts, high-valuation family, and weaker upper bound. Lemma 8, p.74, supplies the two heights beside the half-modulus; Lemma 10, p.77, gives the unique maximum. The two different means and their gap are discussed on p.78. |
| Chen–Winterhof, *Probabilistic results on the 2-adic complexity* | [arXiv:2501.16785v1](https://arxiv.org/abs/2501.16785v1), 28 January 2025. Theorems 2–3 give the lower `N/2 − 1` and upper bound with logarithmic error; the short primitive count and finite recurrence are antecedent ingredients. Detailed locators refer to this version. |
| Chen–Winterhof, journal version | DCC 93 (2025), 2191–2203, [DOI](https://doi.org/10.1007/s10623-025-01592-1). Bibliographic identity and abstract inspected; full body unread. Theorem-by-theorem equivalence with v1 is not established. |
| Lin–Xiao–Chen, *A brief view on the linear and 2-adic complexities of pseudorandom binary sequences* | AIMS Mathematics 11(7) (2026), 20267–20290, [DOI](https://doi.org/10.3934/math.2026823). Question 3.1, p.20282, asks the exact mean upper bound and a separate variance question. |
| Boca–Gologan, *On the distribution of the free path length of the linear flow in a honeycomb* | Ann. Inst. Fourier 59(3) (2009), 1043–1075, [primary PDF](https://www.numdam.org/item/10.5802/aif.2457.pdf), [DOI](https://doi.org/10.5802/aif.2457). Theorem 1.1(i), p.1045: the known congruence-restricted vertical-segment law, specialized to modulus 2. The manuscript proves that the binary limit has survival `G_2(t^2)`, using the horizontal parameter `epsilon q`. The density is differentiated from the survival formula; the tail sign in the printed density on p.1069 is corrected in that differentiation. |
| Heersink, *Equidistribution of Farey sequences on horospheres in covers* | [arXiv:1712.03258v2](https://arxiv.org/abs/1712.03258v2), §2, pp.3–4, and Theorem 4, p.7. Continuous expanding horospheres on every finite-index cover, with the source torus and quotient each normalized to probability. Applied to `Gamma^0(2)` and `Gamma(2)`; the discrete dyadic transfer is proved in the manuscript. Heersink credits the Marklof–Strömbergsson horosphere method. |
| Howe–Moore; Ciobotaru, *A unified proof of the Howe–Moore property* | Classical result: J. Funct. Anal. 32 (1979), 72–96, [DOI](https://doi.org/10.1016/0022-1236(79)90078-8). Inspected primary proof: [arXiv:1403.0223v2](https://arxiv.org/abs/1403.0223v2), Theorem 1.1 and Definition 2.6. Matrix coefficients vanish for unitary representations without invariant vectors of a connected, noncompact, simple real Lie group with finite center. Applied to `PSL_2(R)` on the mean-zero subspace to obtain time-one mixing. The original 1979 full text was not read. |
| Boca–Gologan–Zaharescu, *The average length of a trajectory in a certain billiard in a flat two-torus* | New York J. Math. 9 (2003), 303–330, [primary PDF](https://nyjm.albany.edu/j/2003/9-16p.pdf). Theorems 1.1–1.2 and Corollary 1.3, pp.304–305, evaluate positive real free-path moments and relate them to distributions. Positive methodological antecedent; its unmarked, compactly supported law has different constants. |
| Marklof, *Smallest denominators* | [arXiv:2310.11251v2](https://arxiv.org/abs/2310.11251v2), Proposition 6, p.9, gives discrete complex moment convergence in `|Re alpha| < n+1`. Section 4, Proposition 9 and (4.8)–(4.13), provide the invariance, smearing and ergodic-extremality strategy adapted in the manuscript. Its interval-denominator observable differs from the present marked rectangle. |
| Marklof, *The log moments of smallest denominators* | INTEGERS 24 (2024), A55, [primary PDF](https://math.colgate.edu/~integers/y55/y55.pdf), Proposition 2 and (1.7)–(1.12), pp.2–4. Explicit antecedent for log-moment convergence, a complex moment transform, differentiation at zero and variance evaluation. These general methods are established; the present constants use a different law. |
| Ren–Winterhof, *Symmetric measures of pseudorandomness for binary sequences* | [arXiv:2603.23166v1](https://arxiv.org/abs/2603.23166v1), 24 March 2026. Reversal-symmetric complexity is a different random variable. |
| Goresky–Klapper, *Algebraic Shift Register Sequences* | Cambridge (2012), [DOI](https://doi.org/10.1017/CBO9781139057448). Chen–Winterhof credits published Lemma 18.5.1 for growth. The inspected [author draft](https://www.cs.uky.edu/~klapper/pdf/algebraic.pdf), dated 14 October 2009, has Lemma 21.5.1, pp.486–488; these numberings remain distinct. |
| Cassels, *An Introduction to the Geometry of Numbers* | Springer 1997 reprint, Chapter III §1, [chapter DOI](https://doi.org/10.1007/978-3-642-62035-5_4). Minkowski's theorem is used with strict volume and then discreteness. |

The exact all-length mean inequality has a separate hybrid proof. The finite
distribution and variance use arithmetic interval counts and elementary Farey
arguments supplied in the manuscript. The limiting law uses the external
theorems above, with its dyadic transfer and geometric identification proved
there. Bilateral tail bounds justify moment convergence. Evaluation of the
known law yields the logarithmic constants, raw-height coefficient and Jensen
gap. Neither weak convergence alone nor a finite numerical panel supplies
those proofs.

The moment integrals use `Lambda = Z^2`: the natural-log mean of `Lambda`
is divided by `2 ln(2)` for the base-two mean offset, and its log variance
by `4 ln(2)^2`. [limit_constants.py](../companion/limit_constants.py) evaluates
the resulting closed expression with rational bounds. This checks the
constant evaluation conditional on the analytic proof and classical
identities; it supplies no distributional theorem or convergence rate.

These references distinguish known laws and methods from the particular
binary-statistic derivations. The inspected sources do not certify universal
originality or priority; the unread Chen–Winterhof journal body remains a
limit to that comparison. No claim of a new general moment method, new
geometric law or first publication is made.

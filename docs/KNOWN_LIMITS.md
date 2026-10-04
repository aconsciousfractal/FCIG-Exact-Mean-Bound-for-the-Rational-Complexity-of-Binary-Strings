# Known limits

- The ensemble contains every length-`N` binary string with uniform weight,
  including zero. The mean inequality concerns the ordinary, unrounded
  `log_2 R_N`; it supplies no bound `R_N <= 2^(N/2)` for each string.
- The finite variance formula is exact for every `N >= 1`, as a finite sum
  with logarithms and arithmetic coefficients. It is not a short elementary
  expression in `N`, and the logarithmic variance need not be rational.
- The evaluated variance limit is for `Var(log_2 R_N)`. Raw-height variance
  `Var(R_N)` is a separate observable. The raw mean and Jensen-gap statements
  are asymptotic corollaries, with no convergence rate or all-length gap bound.
- The limiting geometric law is already known. The proof identifies its
  normalization for this binary ensemble and verifies the discrete transfer;
  it imports continuous equidistribution and Howe–Moore explicitly.
- The all-length mean proof is hybrid. Exact finite certificates are essential
  for parent lengths 1–25; the analytic argument covers parent lengths at least
  26. The finite distribution and limiting variance have separate proofs.
- The histogram algorithm uses `O(N 2^N)` arithmetic operations and `O(2^N)`
  stored integers. This is exponential in `N`. No bit-complexity bound or
  complexity bound for arbitrary precision logarithmic evaluation is claimed.
- Successful checker runs validate their finite premises and bounded panels;
  they do not validate all analytic proof steps or imply a convergence rate.
- No conclusion about every prescribed infinite 2-adic number, the cone
  denominator statistic, a periodic or reversal-symmetric ensemble, or a
  Collatz orbit follows from these results.
- The full Chen–Winterhof journal final body was not read. Universal
  originality, firstness and priority remain uncertified.
- AI-assisted reviews shared model and material exposure. They provide no
  independent human peer review or proof-assistant verification.
- A local revised candidate does not update an existing published version or
  deposit. Hosted CI execution is not inferred from a workflow file.

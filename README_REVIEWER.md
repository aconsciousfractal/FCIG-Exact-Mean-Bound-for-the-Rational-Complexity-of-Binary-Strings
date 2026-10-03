# Reviewer path

## Ten minutes

Read the paper's definition and main theorem, [claim map](docs/CLAIM_MAP.md),
[source comparison](docs/SOURCES.md) and [limits](docs/KNOWN_LIMITS.md).
Check that the average includes all residues, the denominator is odd, and the
logarithm is unrounded.

## Proof review

Read Sections 2–5 for the two-lift product, the actual odd completion class,
the lattice-sum estimate and the analytic cutoff. Section 6 and Appendix A
connect those estimates to the exact finite certificate arithmetic.
The original length $N=1$ is separate; parent lengths 1–12, 13–25 and at least
26 correspond to child lengths 2–13, 14–26 and at least 27. There is no gap.

## Replay

Run the commands in [REPRODUCE.md](REPRODUCE.md). A full replay checks 8,190
minima and recomputes 9,068,656 positive primitive pairs with directed integer
logarithms. A second run under Python optimization must return identical JSON.
The seven built-in negative controls reject missing or duplicate levels, a bad
witness, wrong height, changed margin, population drift and a false certificate flag.

Check [MANIFEST_SHA256.txt](MANIFEST_SHA256.txt) with
`python -B scripts/check_manifest.py`.
Verification works from an extracted archive or a normal working copy containing
`.git`; it does not require clean Git state.

The manuscript contains the all-length argument. Finite replay alone neither
proves that analytic argument nor certifies originality.
[AI_USE.md](AI_USE.md) describes the role of AI assistance.

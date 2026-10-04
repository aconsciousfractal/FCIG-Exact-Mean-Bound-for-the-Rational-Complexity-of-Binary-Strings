# Reviewer path

## First reading

Read the definition and result statements, [claim map](docs/CLAIM_MAP.md),
[sources](docs/SOURCES.md) and [limits](docs/KNOWN_LIMITS.md).
Check all-residue weighting, positive odd denominator, max-height and unrounded
base-two logarithms. Separate finite and limiting assertions.

## Proof checks

The exact-mean proof uses two lifts, the actual odd completion class, a lattice
sum and an analytic cutoff. Parent ranges1-12,13-25,at least26 correspond to
child lengths2-13,14-26,at least27; original length1 is separate.

For the finite distribution, check primitive counts, determinant collisions,
strict even-cusp cutoff, open grid endpoints and the square-root splice.
Then verify the layer-cake moment identity.

For the limit, check row-vector/parity normalization, exact time-one
invariance and smearing, tightness, mixing and the ergodic-extreme argument.
The marked conjugation and weighted full-period identification must precede
application of the known Boca-Gologan law.

For moments, check the parameter square and factor four in variance,
positive tail expansion, intermediate primitives and uniform integrability
including its boundary term. Raw mean/Jensen are corollaries.
Algorithm complexity concerns the standalone route, not its defining oracle.

## Replay and identity

Follow [REPRODUCE.md](REPRODUCE.md): mean replay checks8,190 minima/9,068,656
primitive pairs; distribution replay recomputes eleven histograms and moments
with a510-residue oracle; constant replay encloses the closed expressions.
Normal/-O must agree and all guards remain active.

[MANIFEST_SHA256.txt](MANIFEST_SHA256.txt) is checked by scripts/check_manifest.py,
in an extracted archive or a working copy containing .git, without requiring
clean Git state. The manuscript supplies the proofs; finite replay and rational
evaluation do not certify originality or independent human review.
[AI-use disclosure](AI_USE.md).

"""Canonical reference cases shared by tests (and usable in docs/examples).

There is no dataset: the package is analytical and its only inputs are the
sufficient statistic ``(x, n)`` plus ``alpha`` and prior/adjustment parameters.
These fixed cases — the paper's worked example and its boundary behaviour — are
the single source of truth for golden tests. See the engineering spec in
``planning/`` (§3 Sample data & canonical reference cases).
"""

# Paper's worked example: Subbiah & Rajeswaran (2017), Table 2 / Examples.
N = 5
ALPHA = 0.05
A = B = 1  # flat conjugate Beta(1, 1) prior
T1, T2 = 0.93, 0.97  # coverage tolerance band

# Wald CI limits for n = 5, alpha = 0.05, read directly from the paper's Table 2.
# x -> (LWD, UWD)   (golden; independent of statsmodels/R)
WALD_N5 = {
    0: (0.0000, 0.0000),
    1: (0.0000, 0.5506),
    2: (0.0000, 0.8294),
    3: (0.1706, 1.0000),
    4: (0.4494, 1.0000),
    5: (1.0000, 1.0000),
}

# ArcSine CI limits for n = 5, alpha = 0.05. No third-party library implements the
# arcsine method, so these are the independent oracle: sin^2(arcsin(sqrt(p)) +/- z/(2*sqrt(n)))
# computed from the published closed form (Subbiah & Rajeswaran 2017). Note the signature
# boundary failure at x = 0 and x = n: the interval collapses to a nonzero point
# (a ZWI) that excludes the observed proportion 0 (resp. 1).
# x -> (LAS, UAS)
ARCSINE_N5 = {
    0: (0.1801, 0.1801),
    1: (0.0006, 0.6155),
    2: (0.0595, 0.8125),
    3: (0.1875, 0.9405),
    4: (0.3845, 0.9994),
    5: (0.8199, 0.8199),
}

# Logit-Wald CI limits for n = 5, alpha = 0.05. No third-party library implements the
# logit method either, so these are the independent oracle: expit(logit(p) +/- z/sqrt(n*p*q))
# in the interior, and the exact one-sided (Clopper-Pearson) substitution at the boundaries
# where logit(0) / logit(1) are undefined -- [0, 1-(a/2)^(1/n)] at x=0 and [(a/2)^(1/n), 1]
# at x=n. Unlike Wald/ArcSine there is no zero-width interval anywhere.
# x -> (LLT, ULT)
LOGIT_N5 = {
    0: (0.0000, 0.5218),
    1: (0.0272, 0.6910),
    2: (0.1002, 0.7996),
    3: (0.2004, 0.8998),
    4: (0.3090, 0.9728),
    5: (0.4782, 1.0000),
}

# Wald-T CI limits for n = 5, alpha = 0.05. No third-party library implements the Wald-T
# (Pan 2002) method, so these are the independent oracle: p +/- t(nu) * sqrt(p*q/n), where
# nu = 2*V^2 / Var(V) is the Satterthwaite d.o.f. of the variance estimator V = p*q/n, and
# at x = 0, n the centre is the Agresti-Coull estimate (x+2)/(n+4) (boundary modification).
# The t quantile (nu finite) always exceeds the normal z, so every interval is WIDER than the
# plain Wald one, and the boundary modification means there is no zero-width interval.
# x -> (LTW, UTW)
WALDT_N5 = {
    0: (0.0000, 0.6640),
    1: (0.0000, 0.6437),
    2: (0.0000, 0.8528),
    3: (0.1472, 1.0000),
    4: (0.3563, 1.0000),
    5: (0.3360, 1.0000),
}

# Likelihood-ratio CI limits for n = 5, alpha = 0.05. No third-party library implements the
# LR interval for a single proportion, so these are the independent oracle: the two roots p of
# 2*[loglik(p_hat) - loglik(p)] = z^2, i.e. loglik(p) = loglik(p_hat) - z^2/2, computed here by
# an independent brentq root-find (the code uses minimize_scalar; the two agree to ~4e-6). The
# interval brackets the MLE p_hat = x/n and there is no zero-width interval at the boundaries.
# x -> (LLR, ULR)
LR_N5 = {
    0: (0.0000, 0.3190),
    1: (0.0126, 0.6282),
    2: (0.0807, 0.8009),
    3: (0.1991, 0.9193),
    4: (0.3718, 0.9874),
    5: (0.6810, 1.0000),
}

# Blaker exact CI limits for n = 5, alpha = 0.05. Blaker is NEW in binomcikit (absent from the R
# proportion package) and no bundled third-party library implements it, so these frozen constants are
# the golden fixture. Correctness rests on Blaker's two defining theorems, checked in the tests:
# the interval is nested inside Clopper-Pearson (never wider) and its coverage is >= 1 - alpha.
# x -> (LBK, UBK)
BLAKER_N5 = {
    0: (0.0000, 0.5000),
    1: (0.0102, 0.6574),
    2: (0.0764, 0.8107),
    3: (0.1893, 0.9236),
    4: (0.3426, 0.9898),
    5: (0.5000, 1.0000),
}

# Mid-P (exact family, e = 0.5) CI limits for n = 5, alpha = 0.05. statsmodels implements only the
# Clopper-Pearson end (e = 1, method="beta"), which the code matches exactly; it has no Mid-P, so
# these frozen constants are the independent oracle for e = 0.5. Mid-P puts only HALF the point mass
# Pr(X=x) in the tail, so it is less conservative (narrower) than Clopper-Pearson everywhere.
# x -> (LEX, UEX)
MIDP_N5 = {
    0: (0.0000, 0.4507),
    1: (0.0100, 0.6656),
    2: (0.0735, 0.8176),
    3: (0.1824, 0.9265),
    4: (0.3344, 0.9900),
    5: (0.5493, 1.0000),
}

# Base all-x CI functions and their (lower, upper) column names.
BASE_CI = {
    "wald": ("ciwd", "LWD", "UWD"),
    "score": ("cisc", "LSC", "USC"),
    "arcsine": ("cias", "LAS", "UAS"),
    "logit": ("cilt", "LLT", "ULT"),
    "waldt": ("citw", "LTW", "UTW"),
    "lr": ("cilr", "LLR", "ULR"),
}

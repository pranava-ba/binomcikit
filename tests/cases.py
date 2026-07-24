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

# Base all-x CI functions and their (lower, upper) column names.
BASE_CI = {
    "wald": ("ciwd", "LWD", "UWD"),
    "score": ("cisc", "LSC", "USC"),
    "arcsine": ("cias", "LAS", "UAS"),
    "logit": ("cilt", "LLT", "ULT"),
    "waldt": ("citw", "LTW", "UTW"),
    "lr": ("cilr", "LLR", "ULR"),
}

"""2xx family - Coverage probability for the base CI methods (port of R file 201).

For each method the coverage probability is evaluated over ``s`` hypothetical
success probabilities drawn from a Beta(a, b) prior, and summarised by:

    mcp      mean coverage probability
    micp     minimum coverage probability
    RMSE_N   RMSE of coverage from the nominal level (1 - alp)
    RMSE_M   RMSE of coverage from its own mean
    RMSE_MI  RMSE of coverage from its own minimum
    tol      percentage of simulated p with coverage in (t1, t2)

The interval limits themselves are reused from the 1xx ``ci`` family, so the
coverage engine is method-agnostic.

Note: the R package uses ``set.seed``-driven ``rbeta`` draws. NumPy's RNG differs
from R's, so results match R only in distribution, not draw-for-draw. Pass
``seed`` for reproducible output.
"""

import numpy as np
import pandas as pd

from .._accel import coverage_series
from ..ci import cias, ciblaker, cilr, cilt, cisc, citw, ciwd

_S = 5000  # simulation runs, matching the R package


def _validate(n, alp, a, b, t1, t2):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if a is None:
        raise ValueError("'a' is missing")
    if b is None:
        raise ValueError("'b' is missing")
    if t1 is None:
        raise ValueError("'t1' is missing")
    if t2 is None:
        raise ValueError("'t2' is missing")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(a, (int, float)) or a < 0:
        raise ValueError("'a' has to be greater than or equal to 0")
    if not isinstance(b, (int, float)) or b < 0:
        raise ValueError("'b' has to be greater than or equal to 0")
    if t1 > t2:
        raise ValueError("t1 has to be lesser than t2")
    if not isinstance(t1, (int, float)) or not 0 <= t1 <= 1:
        raise ValueError("'t1' has to be between 0 and 1")
    if not isinstance(t2, (int, float)) or not 0 <= t2 <= 1:
        raise ValueError("'t2' has to be between 0 and 1")


def _coverage_core(n, alp, lower, upper, hp, t1, t2):
    """Coverage-probability summary given per-x limits and hypothetical p (hp).

    Shared by every coverage function: the base/adjusted/CC variants pass Beta
    draws for ``hp`` (via :func:`_coverage`), while the general variants pass an
    explicit or user-simulated ``hp`` vector.
    """
    cpp = _coverage_series(n, lower, upper, hp)
    ctr = int(np.sum((cpp > t1) & (cpp < t2)))

    mcp = cpp.mean()
    micp = cpp.min()
    rmse_n = np.sqrt(np.mean((cpp - (1 - alp)) ** 2))
    rmse_m = np.sqrt(np.mean((cpp - mcp) ** 2))
    rmse_mi = np.sqrt(np.mean((cpp - micp) ** 2))
    tol = 100.0 * ctr / len(cpp)

    return pd.DataFrame(
        [
            {
                "mcp": mcp,
                "micp": micp,
                "RMSE_N": rmse_n,
                "RMSE_M": rmse_m,
                "RMSE_MI": rmse_mi,
                "tol": tol,
            }
        ]
    )


def _coverage_series(n, lower, upper, hp):
    """Coverage probability at each hypothetical p in ``hp``.

    Delegates to :mod:`binomcikit._accel`: a compiled (numba) kernel for large
    ``n`` when ``binomcikit[fast]`` is installed, else a vectorised numpy
    reduction — the results are identical either way.
    """
    return coverage_series(n, lower, upper, hp)


def _coverage_curve(n, lower, upper, hp, method):
    """Per-hp coverage curve (hp, cp, method), for plotting (R gcovp* helpers)."""
    cpp = _coverage_series(n, lower, upper, hp)
    return pd.DataFrame({"hp": np.asarray(hp, dtype=float), "cp": cpp, "method": method})


def _coverage(n, alp, a, b, t1, t2, lower, upper, seed=None, s=_S):
    """Coverage over ``s`` Beta(a, b) draws of hypothetical p (base/adj/CC)."""
    rng = np.random.default_rng(seed)
    hp = np.sort(rng.beta(a, b, s))
    return _coverage_core(n, alp, lower, upper, hp, t1, t2)


# One coverage function per base method. Each reuses the matching ci* limits. --
def covpwd(n, alp, a, b, t1, t2, seed=None):
    """Coverage probability of the Wald interval (R covpWD)."""
    _validate(n, alp, a, b, t1, t2)
    df = ciwd(n, alp)
    return _coverage(n, alp, a, b, t1, t2, df["LWD"], df["UWD"], seed)


def covpsc(n, alp, a, b, t1, t2, seed=None):
    """Coverage probability of the Score (Wilson) interval (R covpSC)."""
    _validate(n, alp, a, b, t1, t2)
    df = cisc(n, alp)
    return _coverage(n, alp, a, b, t1, t2, df["LSC"], df["USC"], seed)


def covpblaker(n, alp, a, b, t1, t2, seed=None):
    """Coverage probability of the Blaker interval (new; not in R ``proportion``)."""
    _validate(n, alp, a, b, t1, t2)
    df = ciblaker(n, alp)
    return _coverage(n, alp, a, b, t1, t2, df["LBK"], df["UBK"], seed)


def covpas(n, alp, a, b, t1, t2, seed=None):
    """Coverage probability of the ArcSine interval (R covpAS)."""
    _validate(n, alp, a, b, t1, t2)
    df = cias(n, alp)
    return _coverage(n, alp, a, b, t1, t2, df["LAS"], df["UAS"], seed)


def covplr(n, alp, a, b, t1, t2, seed=None):
    """Coverage probability of the Likelihood-Ratio interval (R covpLR)."""
    _validate(n, alp, a, b, t1, t2)
    df = cilr(n, alp)
    return _coverage(n, alp, a, b, t1, t2, df["LLR"], df["ULR"], seed)


def covptw(n, alp, a, b, t1, t2, seed=None):
    """Coverage probability of the Wald-T interval (R covpTW)."""
    _validate(n, alp, a, b, t1, t2)
    df = citw(n, alp)
    return _coverage(n, alp, a, b, t1, t2, df["LTW"], df["UTW"], seed)


def covplt(n, alp, a, b, t1, t2, seed=None):
    """Coverage probability of the Logit-Wald interval (R covpLT)."""
    _validate(n, alp, a, b, t1, t2)
    df = cilt(n, alp)
    return _coverage(n, alp, a, b, t1, t2, df["LLT"], df["ULT"], seed)


def covpall(n, alp, a, b, t1, t2, seed=None):
    """Coverage probability summary for all six base methods (R covpAll)."""
    _validate(n, alp, a, b, t1, t2)
    methods = {
        "Wald": covpwd,
        "ArcSine": covpas,
        "Likelihood": covplr,
        "Score": covpsc,
        "Wald-T": covptw,
        "Logit-Wald": covplt,
    }
    rows = []
    for name, fn in methods.items():
        row = fn(n, alp, a, b, t1, t2, seed).iloc[0].to_dict()
        row["method"] = name
        rows.append(row)
    out = pd.DataFrame(rows)
    return out[["method", "mcp", "micp", "RMSE_N", "RMSE_M", "RMSE_MI", "tol"]]

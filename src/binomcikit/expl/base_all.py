"""3xx family - Expected length of the base CI methods (R files 301, 304).

For each method the interval length U - L is computed per x, then the expected
length is averaged over hypothetical p drawn from Beta(a, b):

    sumLen    sum of interval lengths across x = 0..n (deterministic)
    explMean  mean expected length over the simulated p
    explSD    sample standard deviation of the expected length
    explMax   maximum expected length
    explLL    explMean - explSD
    explUL    explMean + explSD

The interval limits are reused from the 1xx ``ci`` family. As with 2xx, the
simulation uses NumPy's RNG so results match R in distribution, not draw-for-draw
(pass ``seed`` for reproducibility).
"""

import numpy as np
import pandas as pd
import scipy.stats as stats

from ..ci import cias, ciblaker, ciex, cilr, cilt, cisc, citw, ciwd

_S = 5000


def _validate(n, alp, a, b):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if a is None:
        raise ValueError("'a' is missing")
    if b is None:
        raise ValueError("'b' is missing")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(a, (int, float)) or a < 0:
        raise ValueError("'a' has to be greater than or equal to 0")
    if not isinstance(b, (int, float)) or b < 0:
        raise ValueError("'b' has to be greater than or equal to 0")


def _expl_series(n, lengths, hp):
    """Expected interval length at each hypothetical p in ``hp``.

    Vectorised over the hypothetical-p grid (one broadcast binomial-PMF matrix,
    reduced against ``lengths``) instead of a Python loop. The elementwise-then-
    sum reduction matches the per-p loop it replaces term for term.
    """
    x = np.arange(n + 1)
    lengths = np.asarray(lengths, dtype=float)
    hp = np.asarray(hp, dtype=float)
    pmf = stats.binom.pmf(x[None, :], n, hp[:, None])  # (|hp| x (n+1))
    return (pmf * lengths[None, :]).sum(axis=1)


def _expl_summary(lengths, ew):
    """Summarise interval lengths and their expected values (R lengthWD tail)."""
    sum_len = float(np.sum(lengths))
    expl_mean = float(np.mean(ew))
    expl_sd = float(np.std(ew, ddof=1))  # ddof=1 to match R stats::sd
    expl_max = float(np.max(ew))
    return pd.DataFrame(
        [
            {
                "sumLen": sum_len,
                "explMean": expl_mean,
                "explSD": expl_sd,
                "explMax": expl_max,
                "explLL": expl_mean - expl_sd,
                "explUL": expl_mean + expl_sd,
            }
        ]
    )


def _expl_curve(n, lengths, hp, method):
    """Per-hp expected-length curve (hp, ew, method), for plotting."""
    ew = _expl_series(n, lengths, hp)
    return pd.DataFrame({"hp": np.asarray(hp, dtype=float), "ew": ew, "method": method})


def _beta_hp(a, b, seed, s=_S):
    return np.sort(np.random.default_rng(seed).beta(a, b, s))


def _length(n, alp, a, b, lower, upper, seed=None):
    lengths = np.asarray(upper, dtype=float) - np.asarray(lower, dtype=float)
    ew = _expl_series(n, lengths, _beta_hp(a, b, seed))
    return _expl_summary(lengths, ew)


# limits provider per base method
_BASE = {
    "Wald": (ciwd, "LWD", "UWD"),
    "ArcSine": (cias, "LAS", "UAS"),
    "Likelihood": (cilr, "LLR", "ULR"),
    "Score": (cisc, "LSC", "USC"),
    "Wald-T": (citw, "LTW", "UTW"),
    "Logit-Wald": (cilt, "LLT", "ULT"),
}


def _base_lengths(method, n, alp):
    fn, lo, hi = _BASE[method]
    df = fn(n, alp)
    return df[hi].to_numpy() - df[lo].to_numpy()


def lengthwd(n, alp, a, b, seed=None):
    """Expected length of the Wald interval (R lengthWD)."""
    _validate(n, alp, a, b)
    df = ciwd(n, alp)
    return _length(n, alp, a, b, df["LWD"], df["UWD"], seed)


def lengthsc(n, alp, a, b, seed=None):
    """Expected length of the Score interval (R lengthSC)."""
    _validate(n, alp, a, b)
    df = cisc(n, alp)
    return _length(n, alp, a, b, df["LSC"], df["USC"], seed)


def lengthblaker(n, alp, a, b, seed=None):
    """Expected length of the Blaker interval (new; not in R ``proportion``)."""
    _validate(n, alp, a, b)
    df = ciblaker(n, alp)
    return _length(n, alp, a, b, df["LBK"], df["UBK"], seed)


def lengthas(n, alp, a, b, seed=None):
    """Expected length of the ArcSine interval (R lengthAS)."""
    _validate(n, alp, a, b)
    df = cias(n, alp)
    return _length(n, alp, a, b, df["LAS"], df["UAS"], seed)


def lengthlt(n, alp, a, b, seed=None):
    """Expected length of the Logit-Wald interval (R lengthLT)."""
    _validate(n, alp, a, b)
    df = cilt(n, alp)
    return _length(n, alp, a, b, df["LLT"], df["ULT"], seed)


def lengthtw(n, alp, a, b, seed=None):
    """Expected length of the Wald-T interval (R lengthTW)."""
    _validate(n, alp, a, b)
    df = citw(n, alp)
    return _length(n, alp, a, b, df["LTW"], df["UTW"], seed)


def lengthlr(n, alp, a, b, seed=None):
    """Expected length of the Likelihood-Ratio interval (R lengthLR)."""
    _validate(n, alp, a, b)
    df = cilr(n, alp)
    return _length(n, alp, a, b, df["LLR"], df["ULR"], seed)


def lengthex(n, alp, e, a, b, seed=None):
    """Expected length of the Exact interval (R lengthEX)."""
    _validate(n, alp, a, b)
    if e is None:
        raise ValueError("'e' is missing")
    df = ciex(n, alp, [e])
    return _length(n, alp, a, b, df["LEX"], df["UEX"], seed)


def lengthall(n, alp, a, b, seed=None):
    """Expected-length summary for all six base methods (R lengthAll)."""
    _validate(n, alp, a, b)
    rows = []
    for name in _BASE:
        row = _length(n, alp, a, b, *(_split_limits(name, n, alp)), seed).iloc[0].to_dict()
        row["method"] = name
        rows.append(row)
    out = pd.DataFrame(rows)
    return out[["method", "sumLen", "explMean", "explSD", "explMax", "explLL", "explUL"]]


def _split_limits(method, n, alp):
    fn, lo, hi = _BASE[method]
    df = fn(n, alp)
    return df[lo], df[hi]


def explall(n, alp, a, b, seed=None):
    """Expected-length curves for all six base methods (R explAll)."""
    _validate(n, alp, a, b)
    hp = _beta_hp(a, b, seed)
    return pd.concat(
        [_expl_curve(n, _base_lengths(m, n, alp), hp, m) for m in _BASE], ignore_index=True
    )

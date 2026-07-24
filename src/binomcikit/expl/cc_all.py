"""3xx family - Expected length of the continuity-corrected CI methods (R files 321, 325).

Five methods (no Likelihood-Ratio), matching the CC coverage family.
"""

import pandas as pd

from ..ci import cicas, ciclt, cicsc, cictw, cicwd
from .base_all import _beta_hp, _expl_curve, _length, _validate

_CC = {
    "Wald": (cicwd, "LCW", "UCW"),
    "ArcSine": (cicas, "LCA", "UCA"),
    "Score": (cicsc, "LCS", "UCS"),
    "Wald-T": (cictw, "LCTW", "UCTW"),
    "Logit-Wald": (ciclt, "LCLT", "UCLT"),
}


def _validate_cc(n, alp, c, a, b):
    if c is None:
        raise ValueError("'c' is missing")
    if not isinstance(c, (int, float)) or c < 0:
        raise ValueError("'c' has to be positive")
    _validate(n, alp, a, b)


def _cc_length(method, n, alp, c, a, b, seed):
    fn, lo, hi = _CC[method]
    df = fn(n, alp, c)
    return _length(n, alp, a, b, df[lo], df[hi], seed)


def lengthcwd(n, alp, c, a, b, seed=None):
    """Expected length of the continuity-corrected Wald interval (R lengthCWD)."""
    _validate_cc(n, alp, c, a, b)
    return _cc_length("Wald", n, alp, c, a, b, seed)


def lengthcsc(n, alp, c, a, b, seed=None):
    """Expected length of the continuity-corrected Score interval (R lengthCSC)."""
    _validate_cc(n, alp, c, a, b)
    return _cc_length("Score", n, alp, c, a, b, seed)


def lengthcas(n, alp, c, a, b, seed=None):
    """Expected length of the continuity-corrected ArcSine interval (R lengthCAS)."""
    _validate_cc(n, alp, c, a, b)
    return _cc_length("ArcSine", n, alp, c, a, b, seed)


def lengthclt(n, alp, c, a, b, seed=None):
    """Expected length of the continuity-corrected Logit-Wald interval (R lengthCLT)."""
    _validate_cc(n, alp, c, a, b)
    return _cc_length("Logit-Wald", n, alp, c, a, b, seed)


def lengthctw(n, alp, c, a, b, seed=None):
    """Expected length of the continuity-corrected Wald-T interval (R lengthCTW)."""
    _validate_cc(n, alp, c, a, b)
    return _cc_length("Wald-T", n, alp, c, a, b, seed)


def lengthcall(n, alp, c, a, b, seed=None):
    """Expected-length summary for all five CC methods (R lengthCAll)."""
    _validate_cc(n, alp, c, a, b)
    rows = []
    for name in _CC:
        row = _cc_length(name, n, alp, c, a, b, seed).iloc[0].to_dict()
        row["method"] = name
        rows.append(row)
    out = pd.DataFrame(rows)
    return out[["method", "sumLen", "explMean", "explSD", "explMax", "explLL", "explUL"]]


def explcall(n, alp, c, a, b, seed=None):
    """Expected-length curves for all five CC methods (R explCAll)."""
    _validate_cc(n, alp, c, a, b)
    hp = _beta_hp(a, b, seed)
    curves = []
    for name, (fn, lo, hi) in _CC.items():
        df = fn(n, alp, c)
        lengths = df[hi].to_numpy() - df[lo].to_numpy()
        curves.append(_expl_curve(n, lengths, hp, name))
    return pd.concat(curves, ignore_index=True)

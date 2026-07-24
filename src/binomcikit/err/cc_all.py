"""5xx family - Error and failure for the continuity-corrected CI methods (R file 521).

Five methods (no Likelihood-Ratio). Note the R argument order is
(n, alp, phi, c, f).
"""

import pandas as pd

from ..ci import cicas, ciclt, cicsc, cictw, cicwd
from .base_all import _error, _validate

_CC = {
    "Wald": (cicwd, "LCW", "UCW"),
    "ArcSine": (cicas, "LCA", "UCA"),
    "Score": (cicsc, "LCS", "UCS"),
    "Wald-T": (cictw, "LCTW", "UCTW"),
    "Logit-Wald": (ciclt, "LCLT", "UCLT"),
}


def _validate_cc(n, alp, phi, c, f):
    if c is None:
        raise ValueError("'c' is missing")
    if not isinstance(c, (int, float)) or c < 0:
        raise ValueError("'c' has to be positive")
    _validate(n, alp, phi, f)


def _cc(method, n, alp, phi, c, f):
    fn, lo, hi = _CC[method]
    df = fn(n, alp, c)
    return _error(n, alp, phi, f, df[lo], df[hi])


def errcwd(n, alp, phi, c, f):
    """Error/failure of the continuity-corrected Wald interval (R errCWD)."""
    _validate_cc(n, alp, phi, c, f)
    return _cc("Wald", n, alp, phi, c, f)


def errcsc(n, alp, phi, c, f):
    """Error/failure of the continuity-corrected Score interval (R errCSC)."""
    _validate_cc(n, alp, phi, c, f)
    return _cc("Score", n, alp, phi, c, f)


def errcas(n, alp, phi, c, f):
    """Error/failure of the continuity-corrected ArcSine interval (R errCAS)."""
    _validate_cc(n, alp, phi, c, f)
    return _cc("ArcSine", n, alp, phi, c, f)


def errclt(n, alp, phi, c, f):
    """Error/failure of the continuity-corrected Logit-Wald interval (R errCLT)."""
    _validate_cc(n, alp, phi, c, f)
    return _cc("Logit-Wald", n, alp, phi, c, f)


def errctw(n, alp, phi, c, f):
    """Error/failure of the continuity-corrected Wald-T interval (R errCTW)."""
    _validate_cc(n, alp, phi, c, f)
    return _cc("Wald-T", n, alp, phi, c, f)


def errcall(n, alp, phi, c, f):
    """Error/failure for all five CC methods (R errCAll)."""
    _validate_cc(n, alp, phi, c, f)
    frames = []
    for name in _CC:
        d = _cc(name, n, alp, phi, c, f)
        d["method"] = name
        frames.append(d)
    return pd.concat(frames, ignore_index=True)[["method", "delalp", "theta", "Fail_Pass"]]

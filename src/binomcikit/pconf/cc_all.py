"""4xx family - p-confidence and p-bias for the continuity-corrected CI methods (R file 421).

Five methods (no Likelihood-Ratio).
"""
import pandas as pd

from ..ci import cicwd, cicsc, cicas, ciclt, cictw
from .base_all import _validate, _pconf_pbias

_CC = {
    "Wald": (cicwd, 'LCW', 'UCW'), "ArcSine": (cicas, 'LCA', 'UCA'),
    "Score": (cicsc, 'LCS', 'UCS'), "Wald-T": (cictw, 'LCTW', 'UCTW'),
    "Logit-Wald": (ciclt, 'LCLT', 'UCLT'),
}


def _validate_cc(n, alp, c):
    if c is None:
        raise ValueError("'c' is missing")
    if not isinstance(c, (int, float)) or c < 0:
        raise ValueError("'c' has to be positive")
    _validate(n, alp)


def _cc(method, n, alp, c):
    fn, lo, hi = _CC[method]
    df = fn(n, alp, c)
    return _pconf_pbias(n, df[lo], df[hi])


def pcopbicwd(n, alp, c):
    """p-confidence and p-bias of the continuity-corrected Wald interval (R pCOpBICWD)."""
    _validate_cc(n, alp, c)
    return _cc("Wald", n, alp, c)


def pcopbicsc(n, alp, c):
    """p-confidence and p-bias of the continuity-corrected Score interval (R pCOpBICSC)."""
    _validate_cc(n, alp, c)
    return _cc("Score", n, alp, c)


def pcopbicas(n, alp, c):
    """p-confidence and p-bias of the continuity-corrected ArcSine interval (R pCOpBICAS)."""
    _validate_cc(n, alp, c)
    return _cc("ArcSine", n, alp, c)


def pcopbiclt(n, alp, c):
    """p-confidence and p-bias of the continuity-corrected Logit-Wald interval (R pCOpBICLT)."""
    _validate_cc(n, alp, c)
    return _cc("Logit-Wald", n, alp, c)


def pcopbictw(n, alp, c):
    """p-confidence and p-bias of the continuity-corrected Wald-T interval (R pCOpBICTW)."""
    _validate_cc(n, alp, c)
    return _cc("Wald-T", n, alp, c)


def pcopbicall(n, alp, c):
    """p-confidence and p-bias for all five CC methods (R pCOpBICAll)."""
    _validate_cc(n, alp, c)
    frames = []
    for name in _CC:
        d = _cc(name, n, alp, c)
        d['method'] = name
        frames.append(d)
    return pd.concat(frames, ignore_index=True)[
        ['method', 'x1', 'pconf', 'pbias']]

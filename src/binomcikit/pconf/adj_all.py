"""4xx family - p-confidence and p-bias for the adjusted CI methods (R file 411)."""

import pandas as pd

from ..ci import ciaas, cialr, cialt, ciasc, ciatw, ciawd
from .base_all import _pconf_pbias, _validate

_ADJ = {
    "Wald": (ciawd, "LAWD", "UAWD"),
    "ArcSine": (ciaas, "LAAS", "UAAS"),
    "Likelihood": (cialr, "LALR", "UALR"),
    "Score": (ciasc, "LASC", "UASC"),
    "Wald-T": (ciatw, "LATW", "UATW"),
    "Logit-Wald": (cialt, "LALT", "UALT"),
}


def _validate_adj(n, alp, h):
    if h is None:
        raise ValueError("'h' is missing")
    if not isinstance(h, (int, float)) or h < 0:
        raise ValueError("'h' has to be greater than or equal to 0")
    _validate(n, alp)


def _adj(method, n, alp, h):
    fn, lo, hi = _ADJ[method]
    df = fn(n, alp, h)
    return _pconf_pbias(n, df[lo], df[hi])


def pcopbiawd(n, alp, h):
    """p-confidence and p-bias of the adjusted Wald interval (R pCOpBIAWD)."""
    _validate_adj(n, alp, h)
    return _adj("Wald", n, alp, h)


def pcopbiasc(n, alp, h):
    """p-confidence and p-bias of the adjusted Score interval (R pCOpBIASC)."""
    _validate_adj(n, alp, h)
    return _adj("Score", n, alp, h)


def pcopbiaas(n, alp, h):
    """p-confidence and p-bias of the adjusted ArcSine interval (R pCOpBIAAS)."""
    _validate_adj(n, alp, h)
    return _adj("ArcSine", n, alp, h)


def pcopbialt(n, alp, h):
    """p-confidence and p-bias of the adjusted Logit-Wald interval (R pCOpBIALT)."""
    _validate_adj(n, alp, h)
    return _adj("Logit-Wald", n, alp, h)


def pcopbiatw(n, alp, h):
    """p-confidence and p-bias of the adjusted Wald-T interval (R pCOpBIATW)."""
    _validate_adj(n, alp, h)
    return _adj("Wald-T", n, alp, h)


def pcopbialr(n, alp, h):
    """p-confidence and p-bias of the adjusted Likelihood-Ratio interval (R pCOpBIALR)."""
    _validate_adj(n, alp, h)
    return _adj("Likelihood", n, alp, h)


def pcopbiaall(n, alp, h):
    """p-confidence and p-bias for all six adjusted methods (R pCOpBIAAll)."""
    _validate_adj(n, alp, h)
    frames = []
    for name in _ADJ:
        d = _adj(name, n, alp, h)
        d["method"] = name
        frames.append(d)
    return pd.concat(frames, ignore_index=True)[["method", "x1", "pconf", "pbias"]]

"""5xx family - Error and failure for the adjusted CI methods (R file 511)."""
import pandas as pd

from ..ci import ciawd, ciasc, ciaas, cialt, ciatw, cialr
from .base_all import _validate, _error

_ADJ = {
    "Wald": (ciawd, 'LAWD', 'UAWD'), "ArcSine": (ciaas, 'LAAS', 'UAAS'),
    "Likelihood": (cialr, 'LALR', 'UALR'), "Score": (ciasc, 'LASC', 'UASC'),
    "Wald-T": (ciatw, 'LATW', 'UATW'), "Logit-Wald": (cialt, 'LALT', 'UALT'),
}


def _validate_adj(n, alp, h, phi, f):
    if h is None:
        raise ValueError("'h' is missing")
    if not isinstance(h, (int, float)) or h < 0:
        raise ValueError("'h' has to be greater than or equal to 0")
    _validate(n, alp, phi, f)


def _adj(method, n, alp, h, phi, f):
    fn, lo, hi = _ADJ[method]
    df = fn(n, alp, h)
    return _error(n, alp, phi, f, df[lo], df[hi])


def errawd(n, alp, h, phi, f):
    """Error/failure of the adjusted Wald interval (R errAWD)."""
    _validate_adj(n, alp, h, phi, f)
    return _adj("Wald", n, alp, h, phi, f)


def errasc(n, alp, h, phi, f):
    """Error/failure of the adjusted Score interval (R errASC)."""
    _validate_adj(n, alp, h, phi, f)
    return _adj("Score", n, alp, h, phi, f)


def erraas(n, alp, h, phi, f):
    """Error/failure of the adjusted ArcSine interval (R errAAS)."""
    _validate_adj(n, alp, h, phi, f)
    return _adj("ArcSine", n, alp, h, phi, f)


def erralt(n, alp, h, phi, f):
    """Error/failure of the adjusted Logit-Wald interval (R errALT)."""
    _validate_adj(n, alp, h, phi, f)
    return _adj("Logit-Wald", n, alp, h, phi, f)


def erratw(n, alp, h, phi, f):
    """Error/failure of the adjusted Wald-T interval (R errATW)."""
    _validate_adj(n, alp, h, phi, f)
    return _adj("Wald-T", n, alp, h, phi, f)


def erralr(n, alp, h, phi, f):
    """Error/failure of the adjusted Likelihood-Ratio interval (R errALR)."""
    _validate_adj(n, alp, h, phi, f)
    return _adj("Likelihood", n, alp, h, phi, f)


def erraall(n, alp, h, phi, f):
    """Error/failure for all six adjusted methods (R errAAll)."""
    _validate_adj(n, alp, h, phi, f)
    frames = []
    for name in _ADJ:
        d = _adj(name, n, alp, h, phi, f)
        d['method'] = name
        frames.append(d)
    return pd.concat(frames, ignore_index=True)[
        ['method', 'delalp', 'theta', 'Fail_Pass']]

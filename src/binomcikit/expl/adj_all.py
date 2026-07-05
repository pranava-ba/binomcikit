"""3xx family - Expected length of the adjusted CI methods (R files 311, 314)."""
import pandas as pd

from ..ci import ciawd, ciasc, ciaas, cialt, ciatw, cialr
from .base_all import _validate, _length, _expl_curve, _beta_hp

_ADJ = {
    "Wald": (ciawd, 'LAWD', 'UAWD'), "ArcSine": (ciaas, 'LAAS', 'UAAS'),
    "Likelihood": (cialr, 'LALR', 'UALR'), "Score": (ciasc, 'LASC', 'UASC'),
    "Wald-T": (ciatw, 'LATW', 'UATW'), "Logit-Wald": (cialt, 'LALT', 'UALT'),
}


def _validate_adj(n, alp, h, a, b):
    if h is None:
        raise ValueError("'h' is missing")
    if not isinstance(h, (int, float)) or h < 0:
        raise ValueError("'h' has to be greater than or equal to 0")
    _validate(n, alp, a, b)


def _adj_length(method, n, alp, h, a, b, seed):
    fn, lo, hi = _ADJ[method]
    df = fn(n, alp, h)
    return _length(n, alp, a, b, df[lo], df[hi], seed)


def lengthawd(n, alp, h, a, b, seed=None):
    """Expected length of the adjusted Wald interval (R lengthAWD)."""
    _validate_adj(n, alp, h, a, b)
    return _adj_length("Wald", n, alp, h, a, b, seed)


def lengthasc(n, alp, h, a, b, seed=None):
    """Expected length of the adjusted Score interval (R lengthASC)."""
    _validate_adj(n, alp, h, a, b)
    return _adj_length("Score", n, alp, h, a, b, seed)


def lengthaas(n, alp, h, a, b, seed=None):
    """Expected length of the adjusted ArcSine interval (R lengthAAS)."""
    _validate_adj(n, alp, h, a, b)
    return _adj_length("ArcSine", n, alp, h, a, b, seed)


def lengthalt(n, alp, h, a, b, seed=None):
    """Expected length of the adjusted Logit-Wald interval (R lengthALT)."""
    _validate_adj(n, alp, h, a, b)
    return _adj_length("Logit-Wald", n, alp, h, a, b, seed)


def lengthatw(n, alp, h, a, b, seed=None):
    """Expected length of the adjusted Wald-T interval (R lengthATW)."""
    _validate_adj(n, alp, h, a, b)
    return _adj_length("Wald-T", n, alp, h, a, b, seed)


def lengthalr(n, alp, h, a, b, seed=None):
    """Expected length of the adjusted Likelihood-Ratio interval (R lengthALR)."""
    _validate_adj(n, alp, h, a, b)
    return _adj_length("Likelihood", n, alp, h, a, b, seed)


def lengthaall(n, alp, h, a, b, seed=None):
    """Expected-length summary for all six adjusted methods (R lengthAAll)."""
    _validate_adj(n, alp, h, a, b)
    rows = []
    for name in _ADJ:
        row = _adj_length(name, n, alp, h, a, b, seed).iloc[0].to_dict()
        row['method'] = name
        rows.append(row)
    out = pd.DataFrame(rows)
    return out[['method', 'sumLen', 'explMean', 'explSD', 'explMax',
                'explLL', 'explUL']]


def explaall(n, alp, h, a, b, seed=None):
    """Expected-length curves for all six adjusted methods (R explAAll)."""
    _validate_adj(n, alp, h, a, b)
    hp = _beta_hp(a, b, seed)
    curves = []
    for name, (fn, lo, hi) in _ADJ.items():
        df = fn(n, alp, h)
        lengths = df[hi].to_numpy() - df[lo].to_numpy()
        curves.append(_expl_curve(n, lengths, hp, name))
    return pd.concat(curves, ignore_index=True)

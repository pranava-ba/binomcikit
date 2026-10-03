"""1xx family: Confidence intervals for a single binomial proportion.

base / adjusted / continuity-corrected methods, for all x (given n) and for a
single given x, plus their plotting counterparts (which require the optional
``[plots]`` extra).
"""

import functools
import inspect

from .adj_n import ciaall, ciaas, cialr, cialt, ciasc, ciatw, ciawd
from .adj_n_x import (
    ciaallx,
    ciaasx,
    cialrx,
    cialtx,
    ciascx,
    ciatwx,
    ciawdx,
)
from .base_n import ciall, cias, ciex, cilr, cilt, cisc, citw, ciwd
from .base_n_x import (
    ciallx,
    ciasx,
    ciexx,
    cilrx,
    ciltx,
    ciscx,
    citwx,
    ciwdx,
)
from .bayes_n import ciba
from .bayes_n_x import cibax
from .blaker import ciblaker, ciblakerx
from .bootstrap import ciboot, cibootx
from .cc_n import cicall, cicas, ciclt, cicsc, cictw, cicwd
from .cc_n_x import (
    cicallx,
    cicasx,
    cicltx,
    cicscx,
    cictwx,
    cicwdx,
)


def _as_int(n):
    """A whole-number float (``8.0``, e.g. from pandas or numpy) becomes an int; any other float is an error."""
    if isinstance(n, float):
        if n != n or n in (float("inf"), float("-inf")) or n != int(n):
            raise ValueError("'n' has to be an integer")
        return int(n)
    return n


def _integral_n(fn):
    """Accept ``n = 8.0`` like ``n = 8``: several ``ci*`` functions otherwise fail with an opaque ``TypeError``."""
    params = list(inspect.signature(fn).parameters)
    if "n" not in params:
        return fn
    pos = params.index("n")

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if "n" in kwargs:
            kwargs["n"] = _as_int(kwargs["n"])
        elif len(args) > pos:
            args = args[:pos] + (_as_int(args[pos]),) + args[pos + 1 :]
        return fn(*args, **kwargs)

    return wrapper


for _name in [_n for _n in dir() if _n.startswith("ci") and callable(globals()[_n])]:
    globals()[_name] = _integral_n(globals()[_name])
del _name


# Plotting counterparts need plotnine (the [plots] extra); they are imported on first use so that
# numeric-only users do not pay for plotnine at ``import binomcikit``.
_LAZY_PLOTS = {
    "plotciaall": ".all_graph",
    "plotciaallg": ".all_graph",
    "plotciaallx": ".all_graph",
    "plotciaallxg": ".all_graph",
    "plotciaas": ".adj_n_graph",
    "plotciall": ".all_graph",
    "plotciallg": ".all_graph",
    "plotciallx": ".base_n_x_graph",
    "plotciallxg": ".base_n_x_graph",
    "plotcialr": ".adj_n_graph",
    "plotcialt": ".adj_n_graph",
    "plotcias": ".base_n_graph",
    "plotciasc": ".adj_n_graph",
    "plotciatw": ".adj_n_graph",
    "plotciawd": ".adj_n_graph",
    "plotciba": ".all_graph",
    "plotcicall": ".all_graph",
    "plotcicallg": ".all_graph",
    "plotcicallx": ".all_graph",
    "plotcicallxg": ".all_graph",
    "plotcicas": ".cc_n_graph",
    "plotciclt": ".cc_n_graph",
    "plotcicsc": ".cc_n_graph",
    "plotcictw": ".cc_n_graph",
    "plotcicwd": ".cc_n_graph",
    "plotciex": ".base_n_graph",
    "plotciexx": ".base_n_x_graph",
    "plotcilr": ".base_n_graph",
    "plotcilt": ".base_n_graph",
    "plotcisc": ".base_n_graph",
    "plotcitw": ".base_n_graph",
    "plotciwd": ".base_n_graph",
}

# Public API = every function bound above (submodules excluded); plotting names resolve lazily.
__all__ = sorted(_n for _n in dir() if not _n.startswith("_") and callable(globals()[_n]))


def __getattr__(name):
    from .._lazy import resolve

    return resolve(__name__, _LAZY_PLOTS, name)


def __dir__():
    return sorted(set(globals()) | set(_LAZY_PLOTS))

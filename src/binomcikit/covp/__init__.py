"""2xx family: Coverage probability (numeric + plots, fully ported).

Numeric: base (base_all), adjusted (adj_all), continuity-corrected (cc_all),
general given/simulated-p (general). Plots: plots.
"""

from .adj_all import (
    covpaall,
    covpaas,
    covpalr,
    covpalt,
    covpasc,
    covpatw,
    covpawd,
)
from .base_all import (
    covpall,
    covpas,
    covpblaker,
    covpboot,
    covplr,
    covplt,
    covpsc,
    covptw,
    covpwd,
)
from .cc_all import (
    covpcall,
    covpcas,
    covpclt,
    covpcsc,
    covpctw,
    covpcwd,
)
from .exact_bayes import covpba, covpex
from .general import covpgen, covpsim

# Plotting counterparts need plotnine (the [plots] extra); they are imported on first use so that
# numeric-only users do not pay for plotnine at ``import binomcikit``.
_LAZY_PLOTS = {
    "plotcovpaall": ".plots",
    "plotcovpaas": ".plots",
    "plotcovpall": ".plots",
    "plotcovpalr": ".plots",
    "plotcovpalt": ".plots",
    "plotcovpas": ".plots",
    "plotcovpasc": ".plots",
    "plotcovpatw": ".plots",
    "plotcovpawd": ".plots",
    "plotcovpba": ".plots",
    "plotcovpcall": ".plots",
    "plotcovpcas": ".plots",
    "plotcovpclt": ".plots",
    "plotcovpcsc": ".plots",
    "plotcovpctw": ".plots",
    "plotcovpcwd": ".plots",
    "plotcovpex": ".plots",
    "plotcovpgen": ".plots",
    "plotcovplr": ".plots",
    "plotcovplt": ".plots",
    "plotcovpsc": ".plots",
    "plotcovpsim": ".plots",
    "plotcovptw": ".plots",
    "plotcovpwd": ".plots",
}

# Public API = every function bound above (submodules excluded); plotting names resolve lazily.
__all__ = sorted(_n for _n in dir() if not _n.startswith("_") and callable(globals()[_n]))


def __getattr__(name):
    from .._lazy import resolve

    return resolve(__name__, _LAZY_PLOTS, name)


def __dir__():
    return sorted(set(globals()) | set(_LAZY_PLOTS))

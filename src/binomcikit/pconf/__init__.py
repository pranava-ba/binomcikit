"""4xx family: p-confidence and p-bias (numeric + plots, fully ported).

Numeric: base (base_all), adjusted (adj_all), continuity-corrected (cc_all),
general given-limits (general). Plots: plots. These quantities are deterministic
(no simulation), so results match the R package up to floating point.

Note: the Bayesian variant (pCOpBIBA / PlotpCOpBIBA) depends on the 6xx Bayesian
credible interval and is deferred until that family is ported.
"""

from .adj_all import (
    pcopbiaall,
    pcopbiaas,
    pcopbialr,
    pcopbialt,
    pcopbiasc,
    pcopbiatw,
    pcopbiawd,
)
from .base_all import (
    pcopbiall,
    pcopbias,
    pcopbiblaker,
    pcopbiboot,
    pcopbiex,
    pcopbilr,
    pcopbilt,
    pcopbisc,
    pcopbitw,
    pcopbiwd,
)
from .bayes import pcopbiba
from .cc_all import (
    pcopbicall,
    pcopbicas,
    pcopbiclt,
    pcopbicsc,
    pcopbictw,
    pcopbicwd,
)
from .general import pcopbigen

# Plotting counterparts need plotnine (the [plots] extra); they are imported on first use so that
# numeric-only users do not pay for plotnine at ``import binomcikit``.
_LAZY_PLOTS = {
    "plotpcopbiaall": ".plots",
    "plotpcopbiaas": ".plots",
    "plotpcopbiall": ".plots",
    "plotpcopbialr": ".plots",
    "plotpcopbialt": ".plots",
    "plotpcopbias": ".plots",
    "plotpcopbiasc": ".plots",
    "plotpcopbiatw": ".plots",
    "plotpcopbiawd": ".plots",
    "plotpcopbiba": ".plots",
    "plotpcopbicall": ".plots",
    "plotpcopbicas": ".plots",
    "plotpcopbiclt": ".plots",
    "plotpcopbicsc": ".plots",
    "plotpcopbictw": ".plots",
    "plotpcopbicwd": ".plots",
    "plotpcopbiex": ".plots",
    "plotpcopbigen": ".plots",
    "plotpcopbilr": ".plots",
    "plotpcopbilt": ".plots",
    "plotpcopbisc": ".plots",
    "plotpcopbitw": ".plots",
    "plotpcopbiwd": ".plots",
}

# Public API = every function bound above (submodules excluded); plotting names resolve lazily.
__all__ = sorted(_n for _n in dir() if not _n.startswith("_") and callable(globals()[_n]))


def __getattr__(name):
    from .._lazy import resolve

    return resolve(__name__, _LAZY_PLOTS, name)


def __dir__():
    return sorted(set(globals()) | set(_LAZY_PLOTS))

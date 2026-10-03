"""3xx family: Expected length and sum of lengths (numeric + plots).

Numeric: base (base_all), adjusted (adj_all), continuity-corrected (cc_all),
general given/simulated-p (general). Plots: plots.

Note: the Bayesian expected-length functions (lengthBA / PlotexplBA) depend on
the 6xx Bayesian credible interval and are deferred until that family is ported.
"""

from .adj_all import (
    explaall,
    lengthaall,
    lengthaas,
    lengthalr,
    lengthalt,
    lengthasc,
    lengthatw,
    lengthawd,
)
from .base_all import (
    explall,
    lengthall,
    lengthas,
    lengthblaker,
    lengthboot,
    lengthex,
    lengthlr,
    lengthlt,
    lengthsc,
    lengthtw,
    lengthwd,
)
from .bayes import lengthba
from .cc_all import (
    explcall,
    lengthcall,
    lengthcas,
    lengthclt,
    lengthcsc,
    lengthctw,
    lengthcwd,
)
from .general import lengthgen, lengthsim

# Plotting counterparts need plotnine (the [plots] extra); they are imported on first use so that
# numeric-only users do not pay for plotnine at ``import binomcikit``.
_LAZY_PLOTS = {
    "plotexplaall": ".plots",
    "plotexplaas": ".plots",
    "plotexplall": ".plots",
    "plotexplalr": ".plots",
    "plotexplalt": ".plots",
    "plotexplas": ".plots",
    "plotexplasc": ".plots",
    "plotexplatw": ".plots",
    "plotexplawd": ".plots",
    "plotexplba": ".plots",
    "plotexplcall": ".plots",
    "plotexplcas": ".plots",
    "plotexplclt": ".plots",
    "plotexplcsc": ".plots",
    "plotexplctw": ".plots",
    "plotexplcwd": ".plots",
    "plotexplex": ".plots",
    "plotexplgen": ".plots",
    "plotexpllr": ".plots",
    "plotexpllt": ".plots",
    "plotexplsc": ".plots",
    "plotexplsim": ".plots",
    "plotexpltw": ".plots",
    "plotexplwd": ".plots",
    "plotlengthaall": ".plots",
    "plotlengthaas": ".plots",
    "plotlengthall": ".plots",
    "plotlengthalr": ".plots",
    "plotlengthalt": ".plots",
    "plotlengthas": ".plots",
    "plotlengthasc": ".plots",
    "plotlengthatw": ".plots",
    "plotlengthawd": ".plots",
    "plotlengthba": ".plots",
    "plotlengthcall": ".plots",
    "plotlengthcas": ".plots",
    "plotlengthclt": ".plots",
    "plotlengthcsc": ".plots",
    "plotlengthctw": ".plots",
    "plotlengthcwd": ".plots",
    "plotlengthex": ".plots",
    "plotlengthgen": ".plots",
    "plotlengthlr": ".plots",
    "plotlengthlt": ".plots",
    "plotlengthsc": ".plots",
    "plotlengthsim": ".plots",
    "plotlengthtw": ".plots",
    "plotlengthwd": ".plots",
}

# Public API = every function bound above (submodules excluded); plotting names resolve lazily.
__all__ = sorted(_n for _n in dir() if not _n.startswith("_") and callable(globals()[_n]))


def __getattr__(name):
    from .._lazy import resolve

    return resolve(__name__, _LAZY_PLOTS, name)


def __dir__():
    return sorted(set(globals()) | set(_LAZY_PLOTS))

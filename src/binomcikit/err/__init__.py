"""5xx family: Error and failure (limit-based) (numeric + plots, fully ported).

Numeric: base (base_all), adjusted (adj_all), continuity-corrected (cc_all),
general given-limits (general). Plots: plots. Deterministic - results match the
R package up to floating point.

Note: the Bayesian variant (errBA / PloterrBA) depends on the 6xx Bayesian
credible interval and is deferred until that family is ported.
"""

from .adj_all import (
    erraall,
    erraas,
    erralr,
    erralt,
    errasc,
    erratw,
    errawd,
)
from .base_all import (
    errall,
    erras,
    errblaker,
    errboot,
    errex,
    errlr,
    errlt,
    errsc,
    errtw,
    errwd,
)
from .bayes import errba
from .cc_all import (
    errcall,
    errcas,
    errclt,
    errcsc,
    errctw,
    errcwd,
)
from .general import errgen

# Plotting counterparts need plotnine (the [plots] extra); they are imported on first use so that
# numeric-only users do not pay for plotnine at ``import binomcikit``.
_LAZY_PLOTS = {
    "ploterraall": ".plots",
    "ploterraas": ".plots",
    "ploterrall": ".plots",
    "ploterralr": ".plots",
    "ploterralt": ".plots",
    "ploterras": ".plots",
    "ploterrasc": ".plots",
    "ploterratw": ".plots",
    "ploterrawd": ".plots",
    "ploterrba": ".plots",
    "ploterrcall": ".plots",
    "ploterrcas": ".plots",
    "ploterrclt": ".plots",
    "ploterrcsc": ".plots",
    "ploterrctw": ".plots",
    "ploterrcwd": ".plots",
    "ploterrex": ".plots",
    "ploterrgen": ".plots",
    "ploterrlr": ".plots",
    "ploterrlt": ".plots",
    "ploterrsc": ".plots",
    "ploterrtw": ".plots",
    "ploterrwd": ".plots",
}

# Public API = every function bound above (submodules excluded); plotting names resolve lazily.
__all__ = sorted(_n for _n in dir() if not _n.startswith("_") and callable(globals()[_n]))


def __getattr__(name):
    from .._lazy import resolve

    return resolve(__name__, _LAZY_PLOTS, name)


def __dir__():
    return sorted(set(globals()) | set(_LAZY_PLOTS))

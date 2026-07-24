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

try:
    from .plots import (
        plotcovpaall,
        plotcovpaas,
        plotcovpall,
        plotcovpalr,
        plotcovpalt,
        plotcovpas,
        plotcovpasc,
        plotcovpatw,
        plotcovpawd,
        plotcovpba,
        plotcovpcall,
        plotcovpcas,
        plotcovpclt,
        plotcovpcsc,
        plotcovpctw,
        plotcovpcwd,
        plotcovpex,
        plotcovpgen,
        plotcovplr,
        plotcovplt,
        plotcovpsc,
        plotcovpsim,
        plotcovptw,
        plotcovpwd,
    )
except ImportError:  # plotnine is optional; plotting needs the [plots] extra
    pass

# Public API = every function bound above (submodules excluded).
__all__ = sorted(_n for _n in dir() if not _n.startswith("_") and callable(globals()[_n]))

"""2xx family: Coverage probability (numeric + plots, fully ported).

Numeric: base (base_all), adjusted (adj_all), continuity-corrected (cc_all),
general given/simulated-p (general). Plots: plots.
"""
from .base_all import (
    covpwd, covpsc, covpas, covplr, covptw, covplt, covpall,
)
from .adj_all import (
    covpawd, covpasc, covpaas, covpalt, covpatw, covpalr, covpaall,
)
from .cc_all import (
    covpcwd, covpcsc, covpcas, covpclt, covpctw, covpcall,
)
from .general import covpgen, covpsim
from .exact_bayes import covpex, covpba
from .plots import (
    plotcovpwd, plotcovpsc, plotcovpas, plotcovplr, plotcovptw, plotcovplt,
    plotcovpall,
    plotcovpawd, plotcovpasc, plotcovpaas, plotcovpalr, plotcovpatw, plotcovpalt,
    plotcovpaall,
    plotcovpcwd, plotcovpcsc, plotcovpcas, plotcovpctw, plotcovpclt,
    plotcovpcall,
    plotcovpgen, plotcovpsim, plotcovpex, plotcovpba,
)

# Public API = every function bound above (submodules excluded).
__all__ = sorted(_n for _n in dir() if not _n.startswith("_") and callable(globals()[_n]))

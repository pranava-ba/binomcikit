"""4xx family: p-confidence and p-bias (numeric + plots, fully ported).

Numeric: base (base_all), adjusted (adj_all), continuity-corrected (cc_all),
general given-limits (general). Plots: plots. These quantities are deterministic
(no simulation), so results match the R package up to floating point.

Note: the Bayesian variant (pCOpBIBA / PlotpCOpBIBA) depends on the 6xx Bayesian
credible interval and is deferred until that family is ported.
"""
from .base_all import (
    pcopbiwd, pcopbisc, pcopbias, pcopbilr, pcopbilt, pcopbitw, pcopbiex,
    pcopbiall,
)
from .adj_all import (
    pcopbiawd, pcopbiasc, pcopbiaas, pcopbialt, pcopbiatw, pcopbialr,
    pcopbiaall,
)
from .cc_all import (
    pcopbicwd, pcopbicsc, pcopbicas, pcopbiclt, pcopbictw, pcopbicall,
)
from .general import pcopbigen
from .bayes import pcopbiba
from .plots import (
    plotpcopbiwd, plotpcopbisc, plotpcopbias, plotpcopbilr, plotpcopbilt,
    plotpcopbitw, plotpcopbiex, plotpcopbiall,
    plotpcopbiawd, plotpcopbiasc, plotpcopbiaas, plotpcopbialr, plotpcopbialt,
    plotpcopbiatw, plotpcopbiaall,
    plotpcopbicwd, plotpcopbicsc, plotpcopbicas, plotpcopbiclt, plotpcopbictw,
    plotpcopbicall,
    plotpcopbigen, plotpcopbiba,
)

# Public API = every function bound above (submodules excluded).
__all__ = sorted(_n for _n in dir() if not _n.startswith("_") and callable(globals()[_n]))

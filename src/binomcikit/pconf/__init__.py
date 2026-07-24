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

try:
    from .plots import (
        plotpcopbiaall,
        plotpcopbiaas,
        plotpcopbiall,
        plotpcopbialr,
        plotpcopbialt,
        plotpcopbias,
        plotpcopbiasc,
        plotpcopbiatw,
        plotpcopbiawd,
        plotpcopbiba,
        plotpcopbicall,
        plotpcopbicas,
        plotpcopbiclt,
        plotpcopbicsc,
        plotpcopbictw,
        plotpcopbicwd,
        plotpcopbiex,
        plotpcopbigen,
        plotpcopbilr,
        plotpcopbilt,
        plotpcopbisc,
        plotpcopbitw,
        plotpcopbiwd,
    )
except ImportError:  # plotnine is optional; plotting needs the [plots] extra
    pass

# Public API = every function bound above (submodules excluded).
__all__ = sorted(_n for _n in dir() if not _n.startswith("_") and callable(globals()[_n]))

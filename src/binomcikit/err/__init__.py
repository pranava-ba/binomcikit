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
from .plots import (
    ploterraall,
    ploterraas,
    ploterrall,
    ploterralr,
    ploterralt,
    ploterras,
    ploterrasc,
    ploterratw,
    ploterrawd,
    ploterrba,
    ploterrcall,
    ploterrcas,
    ploterrclt,
    ploterrcsc,
    ploterrctw,
    ploterrcwd,
    ploterrex,
    ploterrgen,
    ploterrlr,
    ploterrlt,
    ploterrsc,
    ploterrtw,
    ploterrwd,
)

# Public API = every function bound above (submodules excluded).
__all__ = sorted(_n for _n in dir() if not _n.startswith("_") and callable(globals()[_n]))

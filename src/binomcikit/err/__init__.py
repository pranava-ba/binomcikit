"""5xx family: Error and failure (limit-based) (numeric + plots, fully ported).

Numeric: base (base_all), adjusted (adj_all), continuity-corrected (cc_all),
general given-limits (general). Plots: plots. Deterministic - results match the
R package up to floating point.

Note: the Bayesian variant (errBA / PloterrBA) depends on the 6xx Bayesian
credible interval and is deferred until that family is ported.
"""
from .base_all import (
    errwd, errsc, erras, errlr, errlt, errtw, errex, errall,
)
from .adj_all import (
    errawd, errasc, erraas, erralt, erratw, erralr, erraall,
)
from .cc_all import (
    errcwd, errcsc, errcas, errclt, errctw, errcall,
)
from .general import errgen
from .bayes import errba
from .plots import (
    ploterrwd, ploterrsc, ploterras, ploterrlr, ploterrlt, ploterrtw,
    ploterrex, ploterrall,
    ploterrawd, ploterrasc, ploterraas, ploterralr, ploterralt, ploterratw,
    ploterraall,
    ploterrcwd, ploterrcsc, ploterrcas, ploterrclt, ploterrctw, ploterrcall,
    ploterrgen, ploterrba,
)

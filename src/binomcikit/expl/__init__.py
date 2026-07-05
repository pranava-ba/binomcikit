"""3xx family: Expected length and sum of lengths (numeric + plots).

Numeric: base (base_all), adjusted (adj_all), continuity-corrected (cc_all),
general given/simulated-p (general). Plots: plots.

Note: the Bayesian expected-length functions (lengthBA / PlotexplBA) depend on
the 6xx Bayesian credible interval and are deferred until that family is ported.
"""
from .base_all import (
    lengthwd, lengthsc, lengthas, lengthlt, lengthtw, lengthlr, lengthex,
    lengthall, explall,
)
from .adj_all import (
    lengthawd, lengthasc, lengthaas, lengthalt, lengthatw, lengthalr,
    lengthaall, explaall,
)
from .cc_all import (
    lengthcwd, lengthcsc, lengthcas, lengthclt, lengthctw,
    lengthcall, explcall,
)
from .general import lengthgen, lengthsim
from .bayes import lengthba
from .plots import (
    plotexplall, plotexplaall, plotexplcall,
    plotexplwd, plotexplsc, plotexplas, plotexpllt, plotexpltw, plotexpllr,
    plotexplex, plotexplgen,
    plotexplawd, plotexplasc, plotexplaas, plotexplalt, plotexplatw, plotexplalr,
    plotexplcwd, plotexplcsc, plotexplcas, plotexplclt, plotexplctw,
    plotexplba, plotexplsim,
    plotlengthall, plotlengthaall, plotlengthcall,
    plotlengthwd, plotlengthsc, plotlengthas, plotlengthlt, plotlengthtw,
    plotlengthlr, plotlengthgen, plotlengthsim,
    plotlengthawd, plotlengthasc, plotlengthaas, plotlengthalt, plotlengthatw,
    plotlengthalr, plotlengthcwd, plotlengthcsc, plotlengthcas, plotlengthclt,
    plotlengthctw, plotlengthex, plotlengthba,
)

# Public API = every function bound above (submodules excluded).
__all__ = sorted(_n for _n in dir() if not _n.startswith("_") and callable(globals()[_n]))

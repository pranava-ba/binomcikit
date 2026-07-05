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
from .plots import (
    plotexplaall,
    plotexplaas,
    plotexplall,
    plotexplalr,
    plotexplalt,
    plotexplas,
    plotexplasc,
    plotexplatw,
    plotexplawd,
    plotexplba,
    plotexplcall,
    plotexplcas,
    plotexplclt,
    plotexplcsc,
    plotexplctw,
    plotexplcwd,
    plotexplex,
    plotexplgen,
    plotexpllr,
    plotexpllt,
    plotexplsc,
    plotexplsim,
    plotexpltw,
    plotexplwd,
    plotlengthaall,
    plotlengthaas,
    plotlengthall,
    plotlengthalr,
    plotlengthalt,
    plotlengthas,
    plotlengthasc,
    plotlengthatw,
    plotlengthawd,
    plotlengthba,
    plotlengthcall,
    plotlengthcas,
    plotlengthclt,
    plotlengthcsc,
    plotlengthctw,
    plotlengthcwd,
    plotlengthex,
    plotlengthgen,
    plotlengthlr,
    plotlengthlt,
    plotlengthsc,
    plotlengthsim,
    plotlengthtw,
    plotlengthwd,
)

# Public API = every function bound above (submodules excluded).
__all__ = sorted(_n for _n in dir() if not _n.startswith("_") and callable(globals()[_n]))

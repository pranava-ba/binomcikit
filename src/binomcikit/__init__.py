"""binomcikit: inference on a single binomial proportion.

Python port of the R package `proportion` (RajeswaranV). Functions are grouped
into six families, each in its own subpackage, but are re-exported here so the
public API stays flat (e.g. ``binomcikit.ciwd`` works directly):

    ci     (1xx)  Confidence intervals
    covp   (2xx)  Coverage probability
    expl   (3xx)  Expected length / sum of lengths
    pconf  (4xx)  p-confidence and p-bias
    err    (5xx)  Error and failure (limit-based)
    bayes  (6xx)  Bayesian methods

The subpackages are also available directly (e.g. ``binomcikit.ci``). Only the
public functions are re-exported at the top level — third-party names used
internally (numpy, pandas, plotnine, …) are not.
"""
from . import bayes, ci, covp, err, expl, pconf
from .bayes import *  # noqa: F401,F403
from .ci import *  # noqa: F401,F403  (respects each subpackage __all__)
from .covp import *  # noqa: F401,F403
from .err import *  # noqa: F401,F403
from .expl import *  # noqa: F401,F403
from .pconf import *  # noqa: F401,F403

__version__ = "2.0.9"

__all__ = sorted({
    *ci.__all__, *covp.__all__, *expl.__all__,
    *pconf.__all__, *err.__all__, *bayes.__all__,
})

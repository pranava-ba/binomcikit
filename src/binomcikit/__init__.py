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

A high-level dispatcher ``binomcikit.ci(x, n, method=...)`` selects any method by
name (see its docstring). The individual ``ci*`` functions (``ciwd``, ``cisc``,
…) remain available flat at the top level. The other subpackages are importable
directly (e.g. ``binomcikit.covp``); the confidence-interval modules are
importable via ``import binomcikit.ci``. Third-party names used internally
(numpy, pandas, plotnine, …) are not re-exported.
"""

from . import bayes, covp, err, expl, pconf
from . import ci as _ci_pkg  # kept private so the name ``ci`` is the dispatcher
from .bayes import *  # noqa: F401,F403
from .ci import *  # noqa: F401,F403  (respects each subpackage __all__)
from .covp import *  # noqa: F401,F403
from .err import *  # noqa: F401,F403
from .expl import *  # noqa: F401,F403
from .highlevel import ci  # noqa: E402  high-level dispatcher: binomcikit.ci(...)
from .pconf import *  # noqa: F401,F403
from .plotly_viz import plot_ci, plot_coverage  # noqa: E402  interactive plotly figures

__version__ = "3.0.8"

__all__ = sorted(
    {
        "ci",
        "plot_ci",
        "plot_coverage",
        *_ci_pkg.__all__,
        *covp.__all__,
        *expl.__all__,
        *pconf.__all__,
        *err.__all__,
        *bayes.__all__,
    }
)

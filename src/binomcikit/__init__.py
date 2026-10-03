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

from . import _lazy, bayes, covp, err, expl, pconf
from . import ci as _ci_pkg  # kept private so the name ``ci`` is the dispatcher
from . import ext as _ext_pkg  # extended methods (limit-producers beyond the R port)
from .access import (  # noqa: E402  usability layer (data input, estimates, curves, compare)
    compare,
    coverage_curve,
    from_counts,
    from_data,
    length_curve,
    point_estimate,
    posterior,
    power,
    prior,
    pvalue,
    recommend,
    reject,
    sample_size,
)
from .bayes import *  # noqa: F401,F403
from .ci import *  # noqa: F401,F403  (respects each subpackage __all__)
from .covp import *  # noqa: F401,F403
from .err import *  # noqa: F401,F403
from .expl import *  # noqa: F401,F403
from .ext import *  # noqa: F401,F403
from .ext.criteria import locally_correct  # noqa: E402  Garthwaite et al. (2024) criterion
from .highlevel import ci  # noqa: E402  high-level dispatcher: binomcikit.ci(...)
from .limits import interval, limits  # noqa: E402  lean access: floats / arrays, no DataFrame
from .methods import describe as describe_method  # noqa: E402  extended-method registry
from .methods import list_methods  # noqa: E402
from .pconf import *  # noqa: F401,F403
from .planning import (  # noqa: E402  PASS/SAS-style sample-size, width and power planning
    expected_width,
    inflate_for_dropout,
    power_equivalence,
    power_test,
    prob_width,
    sample_size_assurance,
    sample_size_bayes,
    sample_size_equivalence,
    sample_size_test,
    sample_size_upper_bound,
)
from .plotly_viz import plot_ci, plot_coverage  # noqa: E402  interactive plotly figures

__version__ = "3.0.8"

# The plotnine-based plotting functions (``plotciall``, ``plotcovpall``, ...) are resolved on first
# access, so ``import binomcikit`` does not import plotnine.
_PLOT_FAMILIES = (_ci_pkg, covp, err, expl, pconf)
_PLOT_NAMES = sorted({_n for _f in _PLOT_FAMILIES for _n in _f._LAZY_PLOTS})


def __getattr__(name):
    for family in _PLOT_FAMILIES:
        if name in family._LAZY_PLOTS:
            value = getattr(family, name)
            globals()[name] = value
            return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(set(globals()) | set(_PLOT_NAMES))


_ACCESS = [
    "from_counts",
    "from_data",
    "point_estimate",
    "posterior",
    "prior",
    "coverage_curve",
    "length_curve",
    "compare",
    "recommend",
    "pvalue",
    "reject",
    "sample_size",
    "power",
    "prob_width",
    "expected_width",
    "sample_size_assurance",
    "power_test",
    "sample_size_test",
    "power_equivalence",
    "sample_size_equivalence",
    "inflate_for_dropout",
    "sample_size_upper_bound",
    "sample_size_bayes",
    "locally_correct",
]

__all__ = sorted(
    {
        "ci",
        "plot_ci",
        "plot_coverage",
        "list_methods",
        "describe_method",
        "limits",
        "interval",
        *_ACCESS,
        *_ext_pkg.__all__,
        *_ci_pkg.__all__,
        *covp.__all__,
        *expl.__all__,
        *pconf.__all__,
        *err.__all__,
        *bayes.__all__,
        *(_PLOT_NAMES if _lazy.plotting_available() else ()),
    }
)

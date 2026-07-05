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
"""
from .ci import *
from .covp import *
from .expl import *
from .pconf import *
from .err import *
from .bayes import *

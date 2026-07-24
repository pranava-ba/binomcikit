"""6xx family: Bayesian methods (fully ported).

    empirical    empirical Bayes credible intervals (empiricalba / empiricalbax)
    predictive   posterior predictive probabilities (probpre / probprex)
    posterior    posterior probabilities below a threshold (probpos / probposx)
    bayesfactors Bayes factors BAF1..BAF6 and their given-x variants

The Bayesian credible interval itself (ciba / cibax) lives in the 1xx ``ci``
family, since the R package defines it there.
"""

# NOTE: the original R package MISSPELLS these as "empericalBA"/"empericalBAx".
# binomcikit deliberately uses the CORRECTED spelling (empiricalba/empiricalbax)
# and does NOT expose the misspelled aliases. The R spelling is kept only as
# provenance (docstrings + tests/r_exports.txt). See CHANGELOG.md (3.0.8).
from .bayesfactors import (
    hypotestbaf1,
    hypotestbaf1x,
    hypotestbaf2,
    hypotestbaf2x,
    hypotestbaf3,
    hypotestbaf3x,
    hypotestbaf4,
    hypotestbaf4x,
    hypotestbaf5,
    hypotestbaf5x,
    hypotestbaf6,
    hypotestbaf6x,
)
from .empirical import empiricalba, empiricalbax
from .posterior import probpos, probposx
from .predictive import probpre, probprex

# Public API = every function bound above (submodules excluded).
__all__ = sorted(_n for _n in dir() if not _n.startswith("_") and callable(globals()[_n]))

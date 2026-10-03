"""1xx family - Bayesian credible intervals for all x (port of R ciBA / ciBAD).

For a Beta(a, b) prior and x successes out of n, the Beta(x+a, n-x+b) posterior
gives the posterior mean, a quantile-based credible interval (LBAQ, UBAQ) and an
HPD interval (LBAH, UBAH). ``a`` and ``b`` may be scalars (same prior for every
x) or length-(n+1) vectors (per-x priors, R's ciBAD path).
"""

import numpy as np
import pandas as pd
import scipy.stats as stats

from .._hpd import hpd_beta
from . import _fast


def ciba(n, alp, a, b):
    """Bayesian credible intervals for x = 0..n (R ciBA / ciBAD)."""
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if a is None:
        raise ValueError("'a' is missing")
    if b is None:
        raise ValueError("'b' is missing")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")

    x = np.arange(n + 1)
    a_vec = np.broadcast_to(np.asarray(a, dtype=float), (n + 1,))
    b_vec = np.broadcast_to(np.asarray(b, dtype=float), (n + 1,))
    if np.any(a_vec < 0) or np.any(b_vec < 0):
        raise ValueError("'a' and 'b' have to be greater than or equal to 0")

    # Posterior Beta(s1, s2) for every x at once: quantile limits in two ppf calls, HPD limits by a
    # vectorised golden-section search. Degenerate shapes (a prior of 0, e.g. Haldane at x = 0)
    # have a non-finite quantile and fall back to the scalar search.
    s1, s2 = x + a_vec, n - x + b_vec
    pomean = (x + a_vec) / (n + a_vec + b_vec)
    lbaq = stats.beta.ppf(alp / 2, s1, s2)
    ubaq = stats.beta.ppf(1 - alp / 2, s1, s2)
    lbah, ubah = _fast.hpd_beta_vec(s1, s2, conf=1 - alp)
    for i in np.flatnonzero(np.isnan(lbah)):
        lbah[i], ubah[i] = hpd_beta(s1[i], s2[i], conf=1 - alp)

    return pd.DataFrame(
        {
            "x": x,
            "pomean": pomean,
            "LBAQ": lbaq,
            "UBAQ": ubaq,
            "LBAH": lbah,
            "UBAH": ubah,
        }
    )

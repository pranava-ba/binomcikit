"""6xx family - Posterior predictive probabilities (R files 621, 622).

Beta-Binomial predictive probability of observing ``xnew`` successes in ``m``
future trials, given x successes in n past trials under a Beta(a1, a2) prior.
"""

import numpy as np
import pandas as pd
from scipy.special import beta as beta_fn
from scipy.special import comb


def _validate(n, m, a1, a2):
    if n is None:
        raise ValueError("'n' is missing")
    if m is None:
        raise ValueError("'m' is missing")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not isinstance(m, (int, float)) or m <= 0:
        raise ValueError("'m' has to be greater than 0")
    if not isinstance(a1, (int, float)) or a1 < 0:
        raise ValueError("'a1' has to be greater than or equal to 0")
    if not isinstance(a2, (int, float)) or a2 < 0:
        raise ValueError("'a2' has to be greater than or equal to 0")


def probpre(n, m, a1, a2):
    """Predictive probability matrix over xnew=0..m and x=0..n (R probPRE)."""
    _validate(n, m, a1, a2)
    x = np.arange(n + 1)
    xnew = np.arange(m + 1)
    data = {"xnew": xnew}
    for xi in x:
        col = (
            comb(m, xnew)
            / beta_fn(xi + a1, n - xi + a2)
            * beta_fn(xnew + xi + a1, m + n - xnew - xi + a2)
        )
        data[str(int(xi))] = col
    return pd.DataFrame(data)


def probprex(x, n, xnew, m, a1, a2):
    """Predictive probability for a given x and xnew (R probPREx)."""
    if x is None:
        raise ValueError("'x' is missing")
    if xnew is None:
        raise ValueError("'xnew' is missing")
    _validate(n, m, a1, a2)
    if not isinstance(x, (int, float)) or x < 0 or x > n:
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if not isinstance(xnew, (int, float)) or xnew < 0 or xnew > m:
        raise ValueError("'xnew' has to be a positive integer between 0 and m")
    preprb = float(
        comb(m, xnew) / beta_fn(x + a1, n - x + a2) * beta_fn(xnew + x + a1, m + n - xnew - x + a2)
    )
    return pd.DataFrame([{"x": x, "n": n, "xnew": xnew, "m": m, "preprb": preprb}])

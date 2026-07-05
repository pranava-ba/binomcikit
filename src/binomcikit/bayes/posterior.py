"""6xx family - Posterior probabilities (R files 641, 642).

Posterior probability that the proportion is below a threshold ``th`` under the
Beta(x+a, n-x+b) posterior, i.e. the posterior CDF at ``th``.
"""
import numpy as np
import pandas as pd
import scipy.stats as stats


def _validate_ab(a, b, th):
    if a is None:
        raise ValueError("'a' is missing")
    if b is None:
        raise ValueError("'b' is missing")
    if th is None:
        raise ValueError("'th' is missing")
    if not isinstance(a, (int, float)) or a < 0:
        raise ValueError("'a' has to be greater than or equal to 0")
    if not isinstance(b, (int, float)) or b < 0:
        raise ValueError("'b' has to be greater than or equal to 0")
    if not isinstance(th, (int, float)) or not 0 <= th <= 1:
        raise ValueError("'th' has to be between 0 and 1")


def probpos(n, a, b, th):
    """Posterior probability P(p < th) for x = 0..n (R probPOS)."""
    if n is None:
        raise ValueError("'n' is missing")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    _validate_ab(a, b, th)
    x = np.arange(n + 1)
    posprob = stats.beta.cdf(th, x + a, n - x + b)
    return pd.DataFrame({'x': x, 'PosProb': posprob})


def probposx(x, n, a, b, th):
    """Posterior probability P(p < th) for a given x (R probPOSx)."""
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not isinstance(x, (int, float)) or x < 0 or x > n:
        raise ValueError("'x' has to be a positive integer between 0 and n")
    _validate_ab(a, b, th)
    posprob = float(stats.beta.cdf(th, x + a, n - x + b))
    return pd.DataFrame([{'x': x, 'PosProb': posprob}])

"""1xx family - Bayesian credible interval for a single x (port of R ciBAx)."""
import pandas as pd
import scipy.stats as stats

from .._hpd import hpd_beta


def cibax(x, n, alp, a, b):
    """Bayesian credible interval for a given x (R ciBAx)."""
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if a is None:
        raise ValueError("'a' is missing")
    if b is None:
        raise ValueError("'b' is missing")
    if not isinstance(x, (int, float)) or x < 0 or x > n:
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if a < 0 or b < 0:
        raise ValueError("'a' and 'b' have to be greater than or equal to 0")

    s1, s2 = x + a, n - x + b
    lbaqx = stats.beta.ppf(alp / 2, s1, s2)
    ubaqx = stats.beta.ppf(1 - alp / 2, s1, s2)
    lbahx, ubahx = hpd_beta(s1, s2, conf=1 - alp)

    return pd.DataFrame([{
        'x': x, 'LBAQx': lbaqx, 'UBAQx': ubaqx,
        'LBAHx': lbahx, 'UBAHx': ubahx,
    }])

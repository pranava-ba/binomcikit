"""6xx family - Empirical Bayes credible intervals (R files 611, 612).

For each x the Beta prior parameters (a, b) are estimated by maximising the
Beta-Binomial marginal likelihood (bounded to [sL, sU]); the resulting
Beta(x+a, n-x+b) posterior then gives the posterior mean, a quantile-based
credible interval and an HPD interval.
"""
import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.special import comb, beta as beta_fn
from scipy.optimize import minimize

from .._hpd import hpd_beta


def _neg_marginal_loglik(n, xi):
    """Negative Beta-Binomial marginal likelihood as a function of (a, b)."""
    def fun(y):
        a, b = y
        return -(comb(n, xi) / beta_fn(a, b)) * beta_fn(xi + a, n - xi + b)
    return fun


def _mle_ab(n, xi, sL, sU):
    res = minimize(_neg_marginal_loglik(n, xi), x0=np.array([0.1, 0.1]),
                   method="L-BFGS-B", bounds=[(sL, sU), (sL, sU)])
    return res.x[0], res.x[1]


def _validate(n, alp, sL, sU):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if sL is None:
        raise ValueError("'sL' is missing")
    if sU is None:
        raise ValueError("'sU' is missing")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if sL > sU:
        raise ValueError("'sL' has to be lesser than 'sU'")


def empiricalba(n, alp, sL, sU):
    """Empirical Bayes credible intervals for x = 0..n (R empericalBA)."""
    _validate(n, alp, sL, sU)
    x = np.arange(n + 1)
    pomean = np.empty(n + 1)
    lq = np.empty(n + 1)
    uq = np.empty(n + 1)
    lh = np.empty(n + 1)
    uh = np.empty(n + 1)
    for i in range(n + 1):
        a, b = _mle_ab(n, x[i], sL, sU)
        s1, s2 = x[i] + a, n - x[i] + b
        pomean[i] = (x[i] + a) / (n + a + b)
        lq[i] = stats.beta.ppf(alp / 2, s1, s2)
        uq[i] = stats.beta.ppf(1 - alp / 2, s1, s2)
        lh[i], uh[i] = hpd_beta(s1, s2, conf=1 - alp)
    df = pd.DataFrame({'x': x, 'pomean': pomean, 'LEBAQ': lq, 'UEBAQ': uq,
                       'LEBAH': lh, 'UEBAH': uh})
    return df.round(4)


def empiricalbax(x, n, alp, sL, sU):
    """Empirical Bayes credible interval for a given x (R empericalBAx)."""
    if x is None:
        raise ValueError("'x' is missing")
    _validate(n, alp, sL, sU)
    if not isinstance(x, (int, float)) or x < 0 or x > n:
        raise ValueError("'x' has to be a positive integer between 0 and n")
    a, b = _mle_ab(n, x, sL, sU)
    s1, s2 = x + a, n - x + b
    pomean = (x + a) / (n + a + b)
    lq = stats.beta.ppf(alp / 2, s1, s2)
    uq = stats.beta.ppf(1 - alp / 2, s1, s2)
    lh, uh = hpd_beta(s1, s2, conf=1 - alp)
    df = pd.DataFrame([{'x': x, 'pomean': pomean, 'LEBAQx': lq, 'UEBAQx': uq,
                        'LEBAHx': lh, 'UEBAHx': uh}])
    return df.round(4)

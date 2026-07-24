"""6xx family - Bayesian hypothesis testing via Bayes factors (R files 631, 632).

Six Bayes factor formulations (BAF1..BAF6) compare a null and an alternative
about the binomial proportion, each returning the factor BaFa01 per x together
with a Jeffreys-scale interpretation. Beta integrals reduce to the Beta CDF/SF:
integral over (th, 1) is ``beta.sf(th, .)`` (upper tail) and integral over
(0, th) is ``beta.cdf(th, .)`` (lower tail).
"""

import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.special import beta as beta_fn


def _interpret(bf):
    if bf >= 150:
        return "Evidence against H1 is very strong"
    if bf >= 20:
        return "Evidence against H1 is strong"
    if bf >= 3:
        return "Evidence against H1 is positive"
    if bf >= 1:
        return "Evidence against H1 is not worth more than a bare mention"
    if bf >= 1 / 3:
        return "Evidence against H0 is not worth more than a bare mention"
    if bf >= 1 / 20:
        return "Evidence against H0 is positive"
    if bf >= 1 / 150:
        return "Evidence against H0 is strong"
    return "Evidence against H0 is very strong"


def _frame(x, bafa):
    df = pd.DataFrame({"x": np.atleast_1d(x), "BaFa01": np.atleast_1d(bafa)})
    df["Interpretation"] = df["BaFa01"].apply(_interpret)
    return df


def _check_th(th, name="th0"):
    if th is None:
        raise ValueError(f"'{name}' is missing")
    if not isinstance(th, (int, float)) or not 0 < th <= 1:
        raise ValueError(f"'{name}' has to be between 0 and 1")


def _check_n(n):
    if n is None:
        raise ValueError("'n' is missing")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")


# --- BAF1 --------------------------------------------------------------------
def _baf1(x, n, th0, a1, b1):
    return beta_fn(a1, b1) / beta_fn(x + a1, n - x + b1) * th0**x * (1 - th0) ** (n - x)


def hypotestbaf1(n, th0, a1, b1):
    """Bayes factor with a Beta(a1,b1) alternative, point null (R hypotestBAF1)."""
    _check_n(n)
    _check_th(th0)
    x = np.arange(n + 1)
    return _frame(x, _baf1(x, n, th0, a1, b1))


def hypotestbaf1x(x, n, th0, a1, b1):
    """BAF1 for a given x (R hypotestBAF1x)."""
    _check_n(n)
    _check_th(th0)
    return _frame(x, _baf1(x, n, th0, a1, b1))


# --- BAF2 (one-sided upper) ---------------------------------------------------
def _baf2(x, n, th0, a1, b1):
    t1 = stats.beta.sf(th0, a1, b1)
    t2 = stats.beta.sf(th0, x + a1, n - x + b1)
    return (t1 / t2) * th0**x * (1 - th0) ** (n - x)


def hypotestbaf2(n, th0, a1, b1):
    """Bayes factor, one-sided upper alternative (R hypotestBAF2)."""
    _check_n(n)
    _check_th(th0)
    x = np.arange(n + 1)
    return _frame(x, _baf2(x, n, th0, a1, b1))


def hypotestbaf2x(x, n, th0, a1, b1):
    """BAF2 for a given x (R hypotestBAF2x)."""
    _check_n(n)
    _check_th(th0)
    return _frame(x, _baf2(x, n, th0, a1, b1))


# --- BAF3 (one-sided lower) ---------------------------------------------------
def _baf3(x, n, th0, a1, b1):
    t1 = stats.beta.cdf(th0, a1, b1)
    t2 = stats.beta.cdf(th0, x + a1, n - x + b1)
    return (t1 / t2) * th0**x * (1 - th0) ** (n - x)


def hypotestbaf3(n, th0, a1, b1):
    """Bayes factor, one-sided lower alternative (R hypotestBAF3)."""
    _check_n(n)
    _check_th(th0)
    x = np.arange(n + 1)
    return _frame(x, _baf3(x, n, th0, a1, b1))


def hypotestbaf3x(x, n, th0, a1, b1):
    """BAF3 for a given x (R hypotestBAF3x)."""
    _check_n(n)
    _check_th(th0)
    return _frame(x, _baf3(x, n, th0, a1, b1))


# --- BAF4 (two priors, null lower / alt upper) --------------------------------
def _baf4(x, n, th0, a0, b0, a1, b1):
    t0 = stats.beta.cdf(th0, a0, b0)
    t1 = stats.beta.sf(th0, a1, b1)
    t01 = stats.beta.cdf(th0, x + a0, n - x + b0)
    t11 = stats.beta.sf(th0, x + a1, n - x + b1)
    return t01 * t1 / (t0 * t11)


def hypotestbaf4(n, th0, a0, b0, a1, b1):
    """Bayes factor with separate null/alternative priors (R hypotestBAF4)."""
    _check_n(n)
    _check_th(th0)
    x = np.arange(n + 1)
    return _frame(x, _baf4(x, n, th0, a0, b0, a1, b1))


def hypotestbaf4x(x, n, th0, a0, b0, a1, b1):
    """BAF4 for a given x (R hypotestBAF4x)."""
    _check_n(n)
    _check_th(th0)
    return _frame(x, _baf4(x, n, th0, a0, b0, a1, b1))


# --- BAF5 (two priors, null upper / alt lower) --------------------------------
def _baf5(x, n, th0, a0, b0, a1, b1):
    t0 = stats.beta.sf(th0, a0, b0)
    t1 = stats.beta.cdf(th0, a1, b1)
    t01 = stats.beta.sf(th0, x + a0, n - x + b0)
    t11 = stats.beta.cdf(th0, x + a1, n - x + b1)
    return t01 * t1 / (t0 * t11)


def hypotestbaf5(n, th0, a0, b0, a1, b1):
    """Bayes factor with separate null/alternative priors (R hypotestBAF5)."""
    _check_n(n)
    _check_th(th0)
    x = np.arange(n + 1)
    return _frame(x, _baf5(x, n, th0, a0, b0, a1, b1))


def hypotestbaf5x(x, n, th0, a0, b0, a1, b1):
    """BAF5 for a given x (R hypotestBAF5x)."""
    _check_n(n)
    _check_th(th0)
    return _frame(x, _baf5(x, n, th0, a0, b0, a1, b1))


# --- BAF6 (interval hypotheses) ----------------------------------------------
def _baf6(x, n, th1, a1, b1, th2, a2, b2):
    t1 = stats.beta.cdf(th1, x + a1, n - x + b1)
    t2 = stats.beta.sf(th2, x + a2, n - x + b2)
    return t1 / t2


def hypotestbaf6(n, th1, a1, b1, th2, a2, b2):
    """Bayes factor for two interval hypotheses (R hypotestBAF6)."""
    _check_n(n)
    _check_th(th1, "th1")
    _check_th(th2, "th2")
    x = np.arange(n + 1)
    return _frame(x, _baf6(x, n, th1, a1, b1, th2, a2, b2))


def hypotestbaf6x(x, n, th1, a1, b1, th2, a2, b2):
    """BAF6 for a given x (R hypotestBAF6x)."""
    _check_n(n)
    _check_th(th1, "th1")
    _check_th(th2, "th2")
    return _frame(x, _baf6(x, n, th1, a1, b1, th2, a2, b2))

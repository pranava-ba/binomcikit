import numpy as np
import pandas as pd
import scipy.optimize as optimize
import scipy.stats as stats

from . import _fast


def ciwd(n, alp):
    r"""Wald confidence intervals for a binomial proportion, for every ``x``.

    The Wald interval centres on the observed proportion :math:`\hat p = x/n`
    and adds a symmetric normal-approximation margin. It is the familiar
    textbook interval, but it under-covers and gives a zero-width interval at
    ``x = 0`` and ``x = n`` -- prefer :func:`cisc` in general.

    Parameters
    ----------
    n : int
        Number of trials (``n > 0``).
    alp : float
        Significance level :math:`\alpha` in ``[0, 1]``; the interval has
        confidence :math:`1 - \alpha`.

    Returns
    -------
    pandas.DataFrame
        One row per ``x = 0..n`` with columns ``x``, ``LWD``, ``UWD`` (lower and
        upper limits) and the diagnostic flags ``LABB`` (lower clamped to 0),
        ``UABB`` (upper clamped to 1) and ``ZWI`` (zero-width interval).

    See Also
    --------
    cisc : Score (Wilson) interval -- better coverage; the usual default.
    ciwdx : Wald interval for a single observed ``x``.
    ciall : Run all six base methods at once.

    Notes
    -----
    With :math:`\hat q = 1 - \hat p` and :math:`z = \Phi^{-1}(1 - \alpha/2)`,

    .. math:: \hat p \pm z \sqrt{\hat p\,\hat q / n},

    with each limit clamped into :math:`[0, 1]`.

    Examples
    --------
    >>> import binomcikit as bk
    >>> df = bk.ciwd(20, 0.05)
    >>> list(df.columns)
    ['x', 'LWD', 'UWD', 'LABB', 'UABB', 'ZWI']
    >>> len(df)
    21
    """
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")

    # INPUT n
    x = np.arange(n + 1)

    # CRITICAL VALUES
    cv = _fast.zcrit(alp)

    # WALD METHOD (vectorised over every x)
    pW = x / n
    seW = np.sqrt(pW * (1 - pW) / n)
    LWD, UWD, LABB, UABB, ZWI = _fast.flags(pW - cv * seW, pW + cv * seW)

    return pd.DataFrame({"x": x, "LWD": LWD, "UWD": UWD, "LABB": LABB, "UABB": UABB, "ZWI": ZWI})


def cisc(n, alp):
    r"""Score (Wilson) confidence intervals, for every ``x``.

    Inverts the score test, so the interval is shifted toward :math:`1/2` and
    stays inside :math:`[0, 1]`. It has good coverage even for small ``n`` and
    extreme :math:`\hat p`, and is the usual recommended default.

    Parameters
    ----------
    n : int
        Number of trials (``n > 0``).
    alp : float
        Significance level :math:`\alpha` in ``[0, 1]``.

    Returns
    -------
    pandas.DataFrame
        One row per ``x`` with columns ``x``, ``LSC``, ``USC`` and the flags
        ``LABB``, ``UABB``, ``ZWI``.

    See Also
    --------
    ciwd : Wald interval.
    ciscx : Score interval for a single observed ``x``.

    Notes
    -----
    With :math:`z = \Phi^{-1}(1 - \alpha/2)`,

    .. math::

        \frac{n}{n+z^2}\left[\left(\hat p + \frac{z^2}{2n}\right)
        \pm z\sqrt{\frac{\hat p\,\hat q}{n} + \frac{z^2}{4n^2}}\right].

    Validated against
    :func:`statsmodels.stats.proportion.proportion_confint` (``method="wilson"``).

    Examples
    --------
    >>> import binomcikit as bk
    >>> bk.cisc(20, 0.05).columns.tolist()
    ['x', 'LSC', 'USC', 'LABB', 'UABB', 'ZWI']
    """
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if alp > 1 or alp < 0 or not isinstance(alp, (float, int)) or isinstance(alp, np.ndarray):
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")

    # INPUT n
    x = np.arange(n + 1)  # Generate values from 0 to n

    # CRITICAL VALUES
    cv = _fast.zcrit(alp)
    cv1 = (cv**2) / (2 * n)
    cv2 = (cv / (2 * n)) ** 2

    # SCORE (WILSON) METHOD (vectorised over every x)
    pS = x / n
    seS = np.sqrt((pS * (1 - pS) / n) + cv2)
    LSC, USC, LABB, UABB, ZWI = _fast.flags(
        (n / (n + cv**2)) * ((pS + cv1) - (cv * seS)),
        (n / (n + cv**2)) * ((pS + cv1) + (cv * seS)),
    )

    return pd.DataFrame({"x": x, "LSC": LSC, "USC": USC, "LABB": LABB, "UABB": UABB, "ZWI": ZWI})


def cias(n, alp):
    r"""ArcSine confidence intervals, for every ``x``.

    Builds the interval on the variance-stabilising :math:`\arcsin\sqrt{\hat p}`
    scale and transforms back, which stabilises the variance at the extremes.

    Parameters
    ----------
    n : int
        Number of trials (``n > 0``).
    alp : float
        Significance level :math:`\alpha` in ``[0, 1]``.

    Returns
    -------
    pandas.DataFrame
        One row per ``x`` with columns ``x``, ``LAS``, ``UAS`` and the flags
        ``LABB``, ``UABB``, ``ZWI``.

    Notes
    -----
    .. math:: \sin^2\!\left(\arcsin\sqrt{\hat p}
        \pm \frac{z_{\alpha/2}}{2\sqrt{n}}\right).
    """
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")

    # INPUT
    x = np.arange(n + 1)

    cv = _fast.zcrit(alp)

    # ARC-SINE METHOD (vectorised over every x)
    pA = x / n
    seA = cv / np.sqrt(4 * n)
    LAS, UAS, LABB, UABB, ZWI = _fast.flags(
        (np.sin(np.arcsin(np.sqrt(pA)) - seA)) ** 2, (np.sin(np.arcsin(np.sqrt(pA)) + seA)) ** 2
    )

    return pd.DataFrame({"x": x, "LAS": LAS, "UAS": UAS, "LABB": LABB, "UABB": UABB, "ZWI": ZWI})


# Optimized ciLR function
def cilr(n, alp):
    r"""Likelihood-Ratio confidence intervals, for every ``x``.

    Keeps the values of :math:`p` not rejected by the likelihood-ratio test,
    i.e. where twice the drop in log-likelihood from the maximum stays below the
    :math:`\chi^2_1` critical value. There is no closed form; the two endpoints
    are found numerically with :func:`scipy.optimize.brentq` on the log-likelihood
    (the MLE itself has the closed form ``x / n``).

    Parameters
    ----------
    n : int
        Number of trials (``n > 0``).
    alp : float
        Significance level :math:`\alpha` in ``[0, 1]``.

    Returns
    -------
    pandas.DataFrame
        One row per ``x`` with columns ``x``, ``LLR``, ``ULR`` and the flags
        ``LABB``, ``UABB``, ``ZWI``.

    Notes
    -----
    The interval is
    :math:`\{p : 2[\ell(\hat p) - \ell(p)] \le z^2_{\alpha/2}\}`, where
    :math:`\ell(p) = x\ln p + (n-x)\ln(1-p)`.
    """
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if not (0 < alp < 1):
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0 and an integer or float")

    x = np.arange(n + 1)  # Generate values from 0 to n

    # The MLE of a binomial proportion has a closed form, x / n -- never a numerical
    # optimisation (a raw-likelihood search underflows for large n; see
    # docs/under_the_hood.md). Each limit is the root of the *deviance*
    #   2 [ x log(p_hat / p) + (n - x) log((1 - p_hat) / (1 - p)) ] - z^2,
    # which is zero-free of the binomial coefficient, underflow-free, strictly monotone on each
    # side of p_hat, and solved for every x at once by a vectorised bisection (ci/_fast.py).
    LLR, ULR = _fast.lr_limits(n, alp)
    LLR, ULR, LABB, UABB, ZWI = _fast.flags(LLR, ULR)

    # Return with 'x' as a column, matching the other ci* methods
    return pd.DataFrame(
        {
            "x": x,
            "LLR": LLR,
            "ULR": ULR,
            "LABB": LABB,
            "UABB": UABB,
            "ZWI": ZWI,
        }
    )


def ciex(n, alp, e):
    r"""Exact confidence intervals, for every ``x``.

    Inverts the binomial tail probabilities rather than a normal approximation,
    giving guaranteed (conservative) coverage. The parameter ``e`` tunes the
    tail treatment: ``e = 1`` gives the Clopper--Pearson interval and
    ``e = 0.5`` gives the mid-*p* interval.

    Parameters
    ----------
    n : int
        Number of trials (``n > 0``).
    alp : float
        Significance level :math:`\alpha` in ``[0, 1]``.
    e : list of float
        One or more tail-tuning values in ``[0, 1]`` (pass as a list, e.g.
        ``[1]`` for Clopper--Pearson). Up to 10 values.

    Returns
    -------
    pandas.DataFrame
        Columns ``x``, ``LEX``, ``UEX``, the flags ``LABB``/``UABB``/``ZWI`` and
        ``e``, with one block of rows per value of ``e``.

    See Also
    --------
    ciex : Clopper--Pearson at ``e=1`` matches
        :func:`statsmodels.stats.proportion.proportion_confint` (``method="beta"``).

    Examples
    --------
    >>> import binomcikit as bk
    >>> bk.ciex(10, 0.05, [1]).columns.tolist()
    ['x', 'LEX', 'UEX', 'LABB', 'UABB', 'ZWI', 'e']
    """
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if e is None:
        raise ValueError("'e' is missing")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, int) or n <= 0:
        raise ValueError("'n' has to be a positive integer")

    # Check if 'e' is a float or list/array
    if isinstance(e, float):
        e = [e]  # Convert single float to a list
    elif not isinstance(e, (np.ndarray, list)) or any([i > 1 or i < 0 for i in e]):
        raise ValueError("'e' values have to be between 0 and 1")

    if len(e) > 10:
        raise ValueError("'e' can have only 10 intervals")

    nvar = len(e)
    result = pd.DataFrame()

    # Loop through each value of e and calculate limits
    for i in range(nvar):
        lu = lufn101(n, alp, e[i])
        result = pd.concat([result, lu], ignore_index=True)

    return result


# Lower and upper limit function
def lufn101(n, alp, e):
    x = np.arange(n + 1)  # Generate values from 0 to n

    # Every x at once: Clopper-Pearson (e = 1) is two beta quantiles; other e use a vectorised
    # bisection on the same tail equations the scalar helpers below solve one x at a time.
    LEX, UEX = _fast.exact_limits(n, alp, e)
    LEX, UEX, LABB, UABB, ZWI = _fast.flags(LEX, UEX)

    # Create DataFrame for this e value
    return pd.DataFrame(
        {"x": x, "LEX": LEX, "UEX": UEX, "LABB": LABB, "UABB": UABB, "ZWI": ZWI, "e": [e] * (n + 1)}
    )


# Lower limit calculation
def exlim102l(x, n, alp, e):
    if x == 0:
        return 0
    elif x == n:
        return (alp / (2 * e)) ** (1 / n)
    else:
        z = x - 1
        y = np.arange(0, z + 1)

        def f1(p):
            return (
                (1 - e) * stats.binom.pmf(x, n, p)
                + np.sum(stats.binom.pmf(y, n, p))
                - (1 - (alp / 2))
            )

        root_result = optimize.root_scalar(f1, bracket=[0, 1], method="bisect")
        return root_result.root


# Upper limit calculation
def exlim102u(x, n, alp, e):
    if x == 0:
        return 1 - (alp / (2 * e)) ** (1 / n)
    elif x == n:
        return 1
    else:
        z = x - 1
        y = np.arange(0, z + 1)

        def f2(p):
            return e * stats.binom.pmf(x, n, p) + np.sum(stats.binom.pmf(y, n, p)) - (alp / 2)

        root_result = optimize.root_scalar(f2, bracket=[0, 1], method="bisect")
        return root_result.root


def citw(n, alp):
    r"""Wald-T confidence intervals, for every ``x``.

    A Wald interval that uses a Student-*t* critical value and an adjusted
    standard error, which widens the interval slightly for small ``n``.

    Parameters
    ----------
    n : int
        Number of trials (``n > 0``).
    alp : float
        Significance level :math:`\alpha` in ``[0, 1]``.

    Returns
    -------
    pandas.DataFrame
        One row per ``x`` with columns ``x``, ``LTW``, ``UTW`` and the flags
        ``LABB``, ``UABB``, ``ZWI``.

    Notes
    -----
    :math:`\hat p \pm t_{\alpha/2}\,\mathrm{SE}^{*}`, with a *t* quantile in
    place of the normal one.
    """
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")

    # INPUT n
    x = np.arange(n + 1)

    # Helper functions
    def f1(p, n):
        return p * (1 - p) / n

    def f2(p, n):
        return (
            (p * (1 - p) / (n**3))
            + (
                p
                + ((6 * n) - 7) * (p**2)
                + (4 * (n - 1) * (n - 3) * (p**3))
                - (2 * (n - 1) * ((2 * n) - 3) * (p**4))
            )
            / (n**5)
            - (2 * (p + ((2 * n) - 3) * (p**2) - 2 * (n - 1) * (p**3))) / (n**4)
        )

    # MODIFIED_t-WALD METHOD (vectorised over every x)
    pTW = np.where((x == 0) | (x == n), (x + 2) / (n + 4), x / n)
    DOF = 2 * (f1(pTW, n) ** 2) / f2(pTW, n)
    cv = stats.t.ppf(1 - (alp / 2), df=DOF)
    seTW = cv * np.sqrt(f1(pTW, n))
    LTW, UTW, LABB, UABB, ZWI = _fast.flags(pTW - seTW, pTW + seTW)

    return pd.DataFrame({"x": x, "LTW": LTW, "UTW": UTW, "LABB": LABB, "UABB": UABB, "ZWI": ZWI})


def cilt(n, alp):
    r"""Logit-Wald confidence intervals, for every ``x``.

    Builds a Wald interval on the log-odds (logit) scale and transforms back.
    Because the logit scale is unbounded, the limits always lie strictly inside
    :math:`(0, 1)` -- helpful for extreme :math:`\hat p`.

    Parameters
    ----------
    n : int
        Number of trials (``n > 0``).
    alp : float
        Significance level :math:`\alpha` in ``[0, 1]``.

    Returns
    -------
    pandas.DataFrame
        One row per ``x`` with columns ``x``, ``LLT``, ``ULT`` and the flags
        ``LABB``, ``UABB``, ``ZWI``.

    Notes
    -----
    .. math:: \operatorname{logit}^{-1}\!\left(\ln\frac{\hat p}{\hat q}
        \pm z_{\alpha/2}\,\frac{1}{\sqrt{n\,\hat p\,\hat q}}\right).
    """
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")

    # Generate values from 0 to n
    x = np.arange(n + 1)
    k = n + 1

    # Critical value for normal distribution
    cv = _fast.zcrit(alp)

    # Logit-Wald method: closed-form boundary rows, vectorised interior
    LLT = np.zeros(k)
    ULT = np.zeros(k)
    ULT[0] = 1 - ((alp / 2) ** (1 / n))
    LLT[k - 1] = (alp / 2) ** (1 / n)
    ULT[k - 1] = 1

    j = x[1 : k - 1]
    pLT = j / n
    lgit = np.log(pLT / (1 - pLT))
    seLT = np.sqrt(pLT * (1 - pLT) * n)
    LLT[1 : k - 1] = 1 / (1 + np.exp(-lgit + (cv / seLT)))
    ULT[1 : k - 1] = 1 / (1 + np.exp(-lgit - (cv / seLT)))

    LLT, ULT, LABB, UABB, ZWI = _fast.flags(LLT, ULT)

    # Create a DataFrame for output
    return pd.DataFrame({"x": x, "LLT": LLT, "ULT": ULT, "LABB": LABB, "UABB": UABB, "ZWI": ZWI})


def ciall(n, alp):
    r"""All six base confidence-interval methods, stacked together.

    Runs :func:`ciwd`, :func:`cias`, :func:`cilr`, :func:`cisc`, :func:`citw`
    and :func:`cilt` and concatenates them into one long-format table with a
    ``method`` column -- ideal for comparing methods side by side or plotting
    them together with :func:`~binomcikit.plotciall`.

    Parameters
    ----------
    n : int
        Number of trials (``n > 0``).
    alp : float
        Significance level :math:`\alpha` in ``[0, 1]``.

    Returns
    -------
    pandas.DataFrame
        Columns ``method``, ``x``, ``LowerLimit``, ``UpperLimit``,
        ``LowerAbb``, ``UpperAbb``, ``ZWI``; ``6 * (n + 1)`` rows.

    Examples
    --------
    >>> import binomcikit as bk
    >>> sorted(bk.ciall(5, 0.05)["method"].unique())
    ['ArcSine', 'Likelihood', 'Logit-Wald', 'Score', 'Wald', 'Wald-T']
    """
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if alp > 1 or alp < 0 or isinstance(alp, (list, tuple)):
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or isinstance(n, (list, tuple)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")

    # Assuming the CI methods are defined elsewhere and return DataFrames
    WaldCI_df = ciwd(n, alp)
    ArcSineCI_df = cias(n, alp)
    LRCI_df = cilr(n, alp)
    ScoreCI_df = cisc(n, alp)
    WaldTCI_df = citw(n, alp)
    LogitWald_df = cilt(n, alp)

    # Assign method names as strings
    WaldCI_df["method"] = "Wald"
    ArcSineCI_df["method"] = "ArcSine"
    LRCI_df["method"] = "Likelihood"
    ScoreCI_df["method"] = "Score"
    WaldTCI_df["method"] = "Wald-T"
    LogitWald_df["method"] = "Logit-Wald"

    # Helper function to safely extract the 'x' column if present
    def create_generic_df(df, method, lower_col, upper_col):
        return pd.DataFrame(
            {
                "method": df["method"],
                "x": df["x"] if "x" in df.columns else None,  # Default to None if 'x' is missing
                "LowerLimit": df[lower_col],
                "UpperLimit": df[upper_col],
                "LowerAbb": df["LABB"],
                "UpperAbb": df["UABB"],
                "ZWI": df["ZWI"],
            }
        )

    # Create generic DataFrames
    Generic_1 = create_generic_df(WaldCI_df, "Wald", "LWD", "UWD")
    Generic_2 = create_generic_df(ArcSineCI_df, "ArcSine", "LAS", "UAS")
    Generic_3 = create_generic_df(LRCI_df, "Likelihood", "LLR", "ULR")
    Generic_4 = create_generic_df(ScoreCI_df, "Score", "LSC", "USC")
    Generic_5 = create_generic_df(WaldTCI_df, "Wald-T", "LTW", "UTW")
    Generic_6 = create_generic_df(LogitWald_df, "Logit-Wald", "LLT", "ULT")

    # Combine all the DataFrames
    Final_df = pd.concat(
        [Generic_1, Generic_2, Generic_3, Generic_4, Generic_5, Generic_6], ignore_index=True
    )
    Final_df.index = range(1, len(Final_df) + 1)

    return Final_df

"""High-level convenience API.

A single dispatcher, :func:`ci`, that selects any confidence-interval method by
name and delegates to the underlying ``ci*`` functions in the
:mod:`binomcikit.ci` family. The flat functions (``ciwd``, ``cisc``, …) remain
available and unchanged; this is a friendlier front door.
"""

from scipy.stats import norm

from . import ci as _cimod

# Friendly method name -> internal two-letter code used by the ci* functions.
_CODE = {
    "wald": "wd",
    "wilson": "sc",
    "score": "sc",
    "arcsine": "as",
    "arc-sine": "as",
    "logit": "lt",
    "logit-wald": "lt",
    "waldt": "tw",
    "wald-t": "tw",
    "lr": "lr",
    "likelihood": "lr",
    "likelihood-ratio": "lr",
    "exact": "ex",
    "clopper-pearson": "ex",
    "cp": "ex",
    "midp": "ex",
    "mid-p": "ex",
    "bayes": "ba",
    "bayesian": "ba",
    "jeffreys": "ba",
    "agresti-coull": "ac",
    "agresti coull": "ac",
    "ac": "ac",
}
_NO_CC = {"lr"}  # no continuity-corrected variant
_BASE_ONLY = {"ex", "ba", "ac"}  # no adjusted / CC variants


def ci(x=None, n=None, alpha=0.05, method="wilson", h=None, c=None, e=None, a=None, b=None):
    """Confidence interval for a single binomial proportion (unified entry point).

    Parameters
    ----------
    x : int, optional
        Number of successes. If ``None`` (default), intervals are returned for
        every ``x`` in ``0..n``; if given, only that ``x``.
    n : int
        Number of trials (required).
    alpha : float, default 0.05
        Significance level; the interval has confidence ``1 - alpha``.
    method : str, default ``"wilson"``
        One of ``wald``, ``wilson``/``score``, ``arcsine``, ``logit``,
        ``waldt``, ``lr``, ``exact``/``cp``, ``midp``, ``bayes``/``jeffreys``,
        ``agresti-coull``.
    h : float, optional
        Adjustment factor (pseudo-count); selects the *adjusted* variant.
    c : float, optional
        Continuity correction; selects the *continuity-corrected* variant.
    e : float, optional
        Exact-method parameter in ``[0, 1]`` (``1`` = Clopper-Pearson,
        ``0.5`` = Mid-P). Used only by the exact methods.
    a, b : float, optional
        Beta prior parameters for the Bayesian method (default ``1, 1``;
        ``jeffreys`` uses ``0.5, 0.5``).

    Returns
    -------
    pandas.DataFrame
        The same table the underlying ``ci*`` function returns.

    Examples
    --------
    >>> import binomcikit as bk
    >>> bk.ci(n=20, method="wilson")           # doctest: +SKIP
    >>> bk.ci(x=3, n=20, method="wald")        # doctest: +SKIP
    >>> bk.ci(n=20, method="exact", e=0.5)     # Mid-P   # doctest: +SKIP
    """
    if n is None:
        raise ValueError("'n' is required")
    key = str(method).lower().strip()
    code = _CODE.get(key)
    if code is None:
        raise ValueError(f"unknown method {method!r}; choose from {sorted(set(_CODE))}")
    if h is not None and c is not None:
        raise ValueError("pass at most one of 'h' (adjusted) and 'c' (continuity)")
    if h is not None and code in _BASE_ONLY:
        raise ValueError(f"method {method!r} has no adjusted (h) variant")
    if c is not None and (code in _BASE_ONLY or code in _NO_CC):
        raise ValueError(f"method {method!r} has no continuity-corrected (c) variant")

    # Agresti-Coull = adjusted Wald with h = z**2 / 2.
    if code == "ac":
        h = norm.ppf(1 - alpha / 2) ** 2 / 2
        code = "wd"

    if code == "ex":
        ev = [float(e) if e is not None else (0.5 if key in ("midp", "mid-p") else 1.0)]
        return _cimod.ciexx(x, n, alpha, ev) if x is not None else _cimod.ciex(n, alpha, ev)

    if code == "ba":
        jeff = key == "jeffreys"
        aa = a if a is not None else (0.5 if jeff else 1.0)
        bb = b if b is not None else (0.5 if jeff else 1.0)
        if x is not None:
            return _cimod.cibax(x, n, alpha, aa, bb)
        return _cimod.ciba(n, alpha, aa, bb)

    prefix = "cia" if h is not None else ("cic" if c is not None else "ci")
    suffix = "x" if x is not None else ""
    fn = getattr(_cimod, f"{prefix}{code}{suffix}")
    extra = () if (h is None and c is None) else ((h,) if h is not None else (c,))
    if x is not None:
        return fn(x, n, alpha, *extra)
    return fn(n, alpha, *extra)

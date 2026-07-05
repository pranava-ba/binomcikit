"""2xx family - Coverage probability plots (R files 202, 213, 222, 224, 225).

Each plot draws the coverage-probability curve against the hypothetical
proportion p, with reference lines for the nominal level (1 - alp), the
tolerance band (t1, t2), and the mean / minimum coverage.
"""
import numpy as np
import pandas as pd
from plotnine import aes, geom_hline, geom_line, ggplot, labs

from ..ci import (
    ciaas,
    cialr,
    cialt,
    cias,
    ciasc,
    ciatw,
    ciawd,
    ciba,
    cicas,
    ciclt,
    cicsc,
    cictw,
    cicwd,
    ciex,
    cilr,
    cilt,
    cisc,
    citw,
    ciwd,
)
from .base_all import _coverage_curve
from .general import _check_limits

_S = 5000


def _covp_plot(curve, alp, t1, t2, title):
    mcp = curve['cp'].mean()
    micp = curve['cp'].min()
    return (
        ggplot(curve, aes(x='hp', y='cp'))
        + labs(title=title, x="p", y="Coverage Probability")
        + geom_hline(yintercept=t1, color="red", linetype="dashed")
        + geom_hline(yintercept=t2, color="blue", linetype="dashed")
        + geom_hline(yintercept=micp, color="orange")
        + geom_hline(yintercept=mcp, color="green")
        + geom_hline(yintercept=1 - alp, linetype="dashed")
        + geom_line(aes(color="method"))
    )


def _beta_hp(a, b, seed):
    rng = np.random.default_rng(seed)
    return np.sort(rng.beta(a, b, _S))


# limit column names per method, for base / adjusted / continuity-corrected
_BASE = {
    "Wald": (ciwd, 'LWD', 'UWD'), "ArcSine": (cias, 'LAS', 'UAS'),
    "Likelihood": (cilr, 'LLR', 'ULR'), "Score": (cisc, 'LSC', 'USC'),
    "Wald-T": (citw, 'LTW', 'UTW'), "Logit-Wald": (cilt, 'LLT', 'ULT'),
}
_ADJ = {
    "Wald": (ciawd, 'LAWD', 'UAWD'), "ArcSine": (ciaas, 'LAAS', 'UAAS'),
    "Likelihood": (cialr, 'LALR', 'UALR'), "Score": (ciasc, 'LASC', 'UASC'),
    "Wald-T": (ciatw, 'LATW', 'UATW'), "Logit-Wald": (cialt, 'LALT', 'UALT'),
}
_CC = {
    "Wald": (cicwd, 'LCW', 'UCW'), "ArcSine": (cicas, 'LCA', 'UCA'),
    "Score": (cicsc, 'LCS', 'UCS'), "Wald-T": (cictw, 'LCTW', 'UCTW'),
    "Logit-Wald": (ciclt, 'LCLT', 'UCLT'),
}


def _base_curve(method, n, alp, a, b, seed):
    fn, lo, hi = _BASE[method]
    df = fn(n, alp)
    return _coverage_curve(n, df[lo], df[hi], _beta_hp(a, b, seed), method)


def _adj_curve(method, n, alp, h, a, b, seed):
    fn, lo, hi = _ADJ[method]
    df = fn(n, alp, h)
    return _coverage_curve(n, df[lo], df[hi], _beta_hp(a, b, seed), method)


def _cc_curve(method, n, alp, c, a, b, seed):
    fn, lo, hi = _CC[method]
    df = fn(n, alp, c)
    return _coverage_curve(n, df[lo], df[hi], _beta_hp(a, b, seed), method)


# --- Base method plots (R file 202) ------------------------------------------
def _make_base_plot(method, label):
    def _plot(n, alp, a, b, t1, t2, seed=None):
        curve = _base_curve(method, n, alp, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for {label} method")
    return _plot


plotcovpwd = _make_base_plot("Wald", "Wald")
plotcovpsc = _make_base_plot("Score", "Score")
plotcovpas = _make_base_plot("ArcSine", "ArcSine")
plotcovplr = _make_base_plot("Likelihood", "Likelihood Ratio")
plotcovptw = _make_base_plot("Wald-T", "Wald-T")
plotcovplt = _make_base_plot("Logit-Wald", "Logit Wald")


def plotcovpall(n, alp, a, b, t1, t2, seed=None):
    """Coverage curves for all six base methods overlaid (R PlotcovpAll)."""
    import pandas as pd
    curve = pd.concat(
        [_base_curve(m, n, alp, a, b, seed) for m in _BASE], ignore_index=True)
    return _covp_plot(curve, alp, t1, t2,
                      "Coverage Probability for all base methods")


# --- Adjusted method plots (R file 213) --------------------------------------
def _make_adj_plot(method, label):
    def _plot(n, alp, h, a, b, t1, t2, seed=None):
        curve = _adj_curve(method, n, alp, h, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for adjusted {label} method")
    return _plot


plotcovpawd = _make_adj_plot("Wald", "Wald")
plotcovpasc = _make_adj_plot("Score", "Score")
plotcovpaas = _make_adj_plot("ArcSine", "ArcSine")
plotcovpalr = _make_adj_plot("Likelihood", "Likelihood Ratio")
plotcovpatw = _make_adj_plot("Wald-T", "Wald-T")
plotcovpalt = _make_adj_plot("Logit-Wald", "Logit Wald")


def plotcovpaall(n, alp, h, a, b, t1, t2, seed=None):
    """Coverage curves for all six adjusted methods overlaid (R PlotcovpAAll)."""
    import pandas as pd
    curve = pd.concat(
        [_adj_curve(m, n, alp, h, a, b, seed) for m in _ADJ], ignore_index=True)
    return _covp_plot(curve, alp, t1, t2,
                      "Coverage Probability for all adjusted methods")


# --- Continuity-corrected method plots (R file 222) --------------------------
def _make_cc_plot(method, label):
    def _plot(n, alp, c, a, b, t1, t2, seed=None):
        curve = _cc_curve(method, n, alp, c, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for continuity-corrected {label} method")
    return _plot


plotcovpcwd = _make_cc_plot("Wald", "Wald")
plotcovpcsc = _make_cc_plot("Score", "Score")
plotcovpcas = _make_cc_plot("ArcSine", "ArcSine")
plotcovpctw = _make_cc_plot("Wald-T", "Wald-T")
plotcovpclt = _make_cc_plot("Logit-Wald", "Logit Wald")


def plotcovpcall(n, alp, c, a, b, t1, t2, seed=None):
    """Coverage curves for all five CC methods overlaid (R PlotcovpCAll)."""
    import pandas as pd
    curve = pd.concat(
        [_cc_curve(m, n, alp, c, a, b, seed) for m in _CC], ignore_index=True)
    return _covp_plot(curve, alp, t1, t2,
                      "Coverage Probability for all continuity-corrected methods")


# --- General plots (R files 224, 225) ----------------------------------------
def plotcovpgen(n, LL, UL, alp, hp, t1, t2):
    """Coverage curve for user-supplied limits over given hp (R PlotcovpGEN)."""
    _check_limits(n, LL, UL, alp, t1, t2)
    hp = np.atleast_1d(np.asarray(hp, dtype=float))
    curve = _coverage_curve(n, LL, UL, hp, "Given")
    return _covp_plot(curve, alp, t1, t2, "Coverage Probability (given p)")


def plotcovpsim(n, LL, UL, alp, s, a, b, t1, t2, seed=None):
    """Coverage curve for user-supplied limits over simulated hp (R PlotcovpSIM)."""
    _check_limits(n, LL, UL, alp, t1, t2)
    hp = np.sort(np.random.default_rng(seed).beta(a, b, int(s)))
    curve = _coverage_curve(n, LL, UL, hp, "Simulated")
    return _covp_plot(curve, alp, t1, t2, "Coverage Probability (simulated p)")


# --- Exact and Bayesian coverage plots (R 202) -------------------------------
def plotcovpex(n, alp, e, a, b, t1, t2, seed=None):
    """Coverage curve for the Exact interval (R PlotcovpEX)."""
    df = ciex(n, alp, [e])
    curve = _coverage_curve(n, df['LEX'], df['UEX'], _beta_hp(a, b, seed), "Exact")
    return _covp_plot(curve, alp, t1, t2,
                      "Coverage Probability for Exact method")


def plotcovpba(n, alp, a, b, t1, t2, a1, a2, seed=None):
    """Coverage curves for the Bayesian credible interval, quantile+HPD (R PlotcovpBA)."""
    ba = ciba(n, alp, a1, a2)
    hp = _beta_hp(a, b, seed)
    curve = pd.concat([
        _coverage_curve(n, ba['LBAQ'], ba['UBAQ'], hp, "Quantile"),
        _coverage_curve(n, ba['LBAH'], ba['UBAH'], hp, "HPD"),
    ], ignore_index=True)
    return _covp_plot(curve, alp, t1, t2,
                      "Coverage Probability for Bayesian method")

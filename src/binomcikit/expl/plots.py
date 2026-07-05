"""3xx family - Expected-length and sum-length plots (R files 302, 303, 312,
313, 322, 323, 327, 328).

Two plot flavours per method:
    plotexpl*    expected-length curve (expected length vs p), with mean/max lines
    plotlength*  sum-length bar (sumLen per method, with +/- SD error bars)
"""
import numpy as np
import pandas as pd
from plotnine import (
    ggplot, aes, labs, geom_line, geom_hline, geom_col, geom_errorbar,
)

from ..ci import (
    ciwd, cisc, cias, cilr, citw, cilt, ciex,
    ciawd, ciasc, ciaas, cialr, cialt, ciatw,
    cicwd, cicsc, cicas, ciclt, cictw, ciba,
)
from .base_all import _expl_curve, _beta_hp
from . import base_all, adj_all, cc_all
from .general import lengthgen, lengthsim

_S = 5000

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


def _lengths_from(fn, lo, hi, *args):
    df = fn(*args)
    return df[hi].to_numpy() - df[lo].to_numpy()


def _expl_plot(curve, title):
    """Expected-length curve with mean and max reference lines."""
    mean_ew = curve['ew'].mean()
    max_ew = curve['ew'].max()
    return (
        ggplot(curve, aes(x='hp', y='ew'))
        + labs(title=title, x="p", y="Expected length")
        + geom_line(aes(color='method'))
        + geom_hline(yintercept=mean_ew, color="orange")
        + geom_hline(yintercept=max_ew, color="red", linetype="dashed")
    )


def _length_plot(summary, title):
    """Sum-length bar chart with +/- SD error bars."""
    return (
        ggplot(summary, aes(x='method', y='sumLen', fill='method'))
        + geom_col(width=0.5)
        + geom_errorbar(aes(ymin='explLL', ymax='explUL'), width=0.25)
        + labs(title=title, x="Method", y="Sum of length")
    )


# --- Expected-length curves (302 / 312 / 322) --------------------------------
def _make_expl_plot(reg, kind, need_param):
    def _plot(n, alp, *rest, seed=None):
        if need_param:
            param, a, b = rest
        else:
            a, b = rest
        hp = _beta_hp(a, b, seed)
        curves = []
        for name, (fn, lo, hi) in reg.items():
            args = (n, alp, param) if need_param else (n, alp)
            curves.append(_expl_curve(n, _lengths_from(fn, lo, hi, *args), hp, name))
        curve = pd.concat(curves, ignore_index=True)
        return _expl_plot(curve, f"Expected length - all {kind} methods")
    return _plot


plotexplall = _make_expl_plot(_BASE, "base", False)
plotexplaall = _make_expl_plot(_ADJ, "adjusted", True)
plotexplcall = _make_expl_plot(_CC, "continuity-corrected", True)


def _single_expl(reg, name, label):
    def base_variant(n, alp, a, b, seed=None):
        fn, lo, hi = reg[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve, f"Expected length - {label} method")
    return base_variant


plotexplwd = _single_expl(_BASE, "Wald", "Wald")
plotexplsc = _single_expl(_BASE, "Score", "Score")
plotexplas = _single_expl(_BASE, "ArcSine", "ArcSine")
plotexpllt = _single_expl(_BASE, "Logit-Wald", "Logit Wald")
plotexpltw = _single_expl(_BASE, "Wald-T", "Wald-T")
plotexpllr = _single_expl(_BASE, "Likelihood", "Likelihood Ratio")


def plotexplex(n, alp, e, a, b, seed=None):
    """Expected-length curve for the Exact method (R PlotexplEX)."""
    df = ciex(n, alp, [e])
    lengths = df['UEX'].to_numpy() - df['LEX'].to_numpy()
    curve = _expl_curve(n, lengths, _beta_hp(a, b, seed), "Exact")
    return _expl_plot(curve, "Expected length - Exact method")


def _single_expl_adj(name, label):
    def _plot(n, alp, h, a, b, seed=None):
        fn, lo, hi = _ADJ[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp, h),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve, f"Expected length - adjusted {label} method")
    return _plot


plotexplawd = _single_expl_adj("Wald", "Wald")
plotexplasc = _single_expl_adj("Score", "Score")
plotexplaas = _single_expl_adj("ArcSine", "ArcSine")
plotexplalt = _single_expl_adj("Logit-Wald", "Logit Wald")
plotexplatw = _single_expl_adj("Wald-T", "Wald-T")
plotexplalr = _single_expl_adj("Likelihood", "Likelihood Ratio")


def _single_expl_cc(name, label):
    def _plot(n, alp, c, a, b, seed=None):
        fn, lo, hi = _CC[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp, c),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve,
                          f"Expected length - continuity-corrected {label} method")
    return _plot


plotexplcwd = _single_expl_cc("Wald", "Wald")
plotexplcsc = _single_expl_cc("Score", "Score")
plotexplcas = _single_expl_cc("ArcSine", "ArcSine")
plotexplclt = _single_expl_cc("Logit-Wald", "Logit Wald")
plotexplctw = _single_expl_cc("Wald-T", "Wald-T")


def plotexplba(n, alp, a, b, a1, a2, seed=None):
    """Expected-length curves for the Bayesian interval, quantile+HPD (R PlotexplBA)."""
    ba = ciba(n, alp, a1, a2)
    hp = _beta_hp(a, b, seed)
    curve = pd.concat([
        _expl_curve(n, ba['UBAQ'].to_numpy() - ba['LBAQ'].to_numpy(), hp, "Quantile"),
        _expl_curve(n, ba['UBAH'].to_numpy() - ba['LBAH'].to_numpy(), hp, "HPD"),
    ], ignore_index=True)
    return _expl_plot(curve, "Expected length - Bayesian method")


def plotexplsim(n, LL, UL, s, a, b, seed=None):
    """Expected-length curve for user-supplied limits over simulated hp (R PlotexplSIM)."""
    hp = np.sort(np.random.default_rng(seed).beta(a, b, int(s)))
    lengths = np.asarray(UL, dtype=float) - np.asarray(LL, dtype=float)
    curve = _expl_curve(n, lengths, hp, "Simulated")
    return _expl_plot(curve, "Expected length (simulated p)")


# --- Sum-length bars (303 / 313 / 323) ---------------------------------------
def plotlengthall(n, alp, a, b, seed=None):
    """Sum-length bars for all six base methods (R PlotlengthAll)."""
    return _length_plot(base_all.lengthall(n, alp, a, b, seed),
                        "Sum length - all base methods")


def plotlengthaall(n, alp, h, a, b, seed=None):
    """Sum-length bars for all six adjusted methods (R PlotlengthAAll)."""
    return _length_plot(adj_all.lengthaall(n, alp, h, a, b, seed),
                        "Sum length - all adjusted methods")


def plotlengthcall(n, alp, c, a, b, seed=None):
    """Sum-length bars for all five CC methods (R PlotlengthCAll)."""
    return _length_plot(cc_all.lengthcall(n, alp, c, a, b, seed),
                        "Sum length - all continuity-corrected methods")


def _single_length(length_fn, label):
    def _plot(n, alp, a, b, seed=None):
        summary = length_fn(n, alp, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")
    return _plot


plotlengthwd = _single_length(base_all.lengthwd, "Wald")
plotlengthsc = _single_length(base_all.lengthsc, "Score")
plotlengthas = _single_length(base_all.lengthas, "ArcSine")
plotlengthlt = _single_length(base_all.lengthlt, "Logit-Wald")
plotlengthtw = _single_length(base_all.lengthtw, "Wald-T")
plotlengthlr = _single_length(base_all.lengthlr, "Likelihood")


def _single_length_param(length_fn, label):
    """Sum-length bar for a method that takes an extra h or c parameter."""
    def _plot(n, alp, param, a, b, seed=None):
        summary = length_fn(n, alp, param, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")
    return _plot


plotlengthawd = _single_length_param(adj_all.lengthawd, "Adj Wald")
plotlengthasc = _single_length_param(adj_all.lengthasc, "Adj Score")
plotlengthaas = _single_length_param(adj_all.lengthaas, "Adj ArcSine")
plotlengthalt = _single_length_param(adj_all.lengthalt, "Adj Logit-Wald")
plotlengthatw = _single_length_param(adj_all.lengthatw, "Adj Wald-T")
plotlengthalr = _single_length_param(adj_all.lengthalr, "Adj Likelihood")
plotlengthcwd = _single_length_param(cc_all.lengthcwd, "CC Wald")
plotlengthcsc = _single_length_param(cc_all.lengthcsc, "CC Score")
plotlengthcas = _single_length_param(cc_all.lengthcas, "CC ArcSine")
plotlengthclt = _single_length_param(cc_all.lengthclt, "CC Logit-Wald")
plotlengthctw = _single_length_param(cc_all.lengthctw, "CC Wald-T")


def plotlengthex(n, alp, e, a, b, seed=None):
    """Sum-length bar for the Exact method (R PlotlengthEX)."""
    summary = base_all.lengthex(n, alp, e, a, b, seed).copy()
    summary['method'] = "Exact"
    return _length_plot(summary, "Sum length - Exact method")


def plotlengthba(n, alp, a, b, a1, a2, seed=None):
    """Sum-length bars for the Bayesian interval, quantile+HPD (R PlotlengthBA)."""
    from .bayes import lengthba
    summary = lengthba(n, alp, a, b, a1, a2, seed)
    return _length_plot(summary, "Sum length - Bayesian method")


# --- General plots (327 / 328) -----------------------------------------------
def plotexplgen(n, LL, UL, hp):
    """Expected-length curve for user-supplied limits over given hp (R PlotexplGEN)."""
    hp = np.atleast_1d(np.asarray(hp, dtype=float))
    lengths = np.asarray(UL, dtype=float) - np.asarray(LL, dtype=float)
    curve = _expl_curve(n, lengths, hp, "Given")
    return _expl_plot(curve, "Expected length (given p)")


def plotlengthgen(n, LL, UL, hp):
    """Sum-length bar for user-supplied limits over given hp (R PlotlengthGEN)."""
    summary = lengthgen(n, LL, UL, hp).copy()
    summary['method'] = "Given"
    return _length_plot(summary, "Sum length (given p)")


def plotlengthsim(n, LL, UL, s, a, b, seed=None):
    """Sum-length bar for user-supplied limits over simulated hp (R PlotlengthSIM)."""
    summary = lengthsim(n, LL, UL, s, a, b, seed).copy()
    summary['method'] = "Simulated"
    return _length_plot(summary, "Sum length (simulated p)")

"""5xx family - Error and failure plots (R files 502, 512, 522, 523).

Each plot shows the increase in nominal error (delalp) and the long-term power
(theta) as bars, in two stacked facets, coloured by pass/fail status.
"""
import pandas as pd
from plotnine import aes, facet_grid, geom_col, ggplot, labs

from . import adj_all, base_all, cc_all
from .general import errgen


def _err_plot(df, title):
    """Bar plot of delalp / theta faceted by measure, coloured by pass/fail."""
    if 'method' not in df.columns:
        df = df.copy()
        df['method'] = "Method"
    va = df[['method', 'delalp', 'Fail_Pass']].rename(
        columns={'delalp': 'value'})
    va['mark'] = "Increase in nominal error"
    vt = df[['method', 'theta', 'Fail_Pass']].rename(
        columns={'theta': 'value'})
    vt['mark'] = "Long term power of test"
    long = pd.concat([va, vt], ignore_index=True)
    return (
        ggplot(long, aes(x='method', y='value', fill='Fail_Pass'))
        + facet_grid('mark ~ .', scales='free_y')
        + geom_col(position='identity', width=0.5)
        + labs(title=title, x="Method", y="Value")
    )


# --- Base method plots (R 502) -----------------------------------------------
def _make_base_plot(fn, label):
    def _plot(n, alp, phi, f):
        return _err_plot(fn(n, alp, phi, f),
                         f"Error, long term power and pass/fail - {label} method")
    return _plot


ploterrwd = _make_base_plot(base_all.errwd, "Wald")
ploterrsc = _make_base_plot(base_all.errsc, "Score")
ploterras = _make_base_plot(base_all.erras, "ArcSine")
ploterrlr = _make_base_plot(base_all.errlr, "Likelihood Ratio")
ploterrlt = _make_base_plot(base_all.errlt, "Logit Wald")
ploterrtw = _make_base_plot(base_all.errtw, "Wald-T")


def ploterrex(n, alp, phi, f, e):
    """Error/failure plot for the Exact method (R PloterrEX)."""
    return _err_plot(base_all.errex(n, alp, phi, f, e),
                     "Error, long term power and pass/fail - Exact method")


def ploterrall(n, alp, phi, f):
    """Error/failure plot for all six base methods (R PloterrAll)."""
    return _err_plot(base_all.errall(n, alp, phi, f),
                     "Error, long term power and pass/fail - all base methods")


# --- Adjusted method plots (R 512) -------------------------------------------
def _make_adj_plot(fn, label):
    def _plot(n, alp, h, phi, f):
        return _err_plot(
            fn(n, alp, h, phi, f),
            f"Error, long term power and pass/fail - adjusted {label} method")
    return _plot


ploterrawd = _make_adj_plot(adj_all.errawd, "Wald")
ploterrasc = _make_adj_plot(adj_all.errasc, "Score")
ploterraas = _make_adj_plot(adj_all.erraas, "ArcSine")
ploterralr = _make_adj_plot(adj_all.erralr, "Likelihood Ratio")
ploterralt = _make_adj_plot(adj_all.erralt, "Logit Wald")
ploterratw = _make_adj_plot(adj_all.erratw, "Wald-T")


def ploterraall(n, alp, h, phi, f):
    """Error/failure plot for all six adjusted methods (R PloterrAAll)."""
    return _err_plot(
        adj_all.erraall(n, alp, h, phi, f),
        "Error, long term power and pass/fail - all adjusted methods")


# --- Continuity-corrected method plots (R 522) -------------------------------
def _make_cc_plot(fn, label):
    def _plot(n, alp, phi, c, f):
        return _err_plot(
            fn(n, alp, phi, c, f),
            f"Error, long term power and pass/fail - CC {label} method")
    return _plot


ploterrcwd = _make_cc_plot(cc_all.errcwd, "Wald")
ploterrcsc = _make_cc_plot(cc_all.errcsc, "Score")
ploterrcas = _make_cc_plot(cc_all.errcas, "ArcSine")
ploterrclt = _make_cc_plot(cc_all.errclt, "Logit Wald")
ploterrctw = _make_cc_plot(cc_all.errctw, "Wald-T")


def ploterrcall(n, alp, phi, c, f):
    """Error/failure plot for all five CC methods (R PloterrCAll)."""
    return _err_plot(
        cc_all.errcall(n, alp, phi, c, f),
        "Error, long term power and pass/fail - all CC methods")


# --- General plot (R 523) ----------------------------------------------------
def ploterrgen(n, LL, UL, alp, phi, f):
    """Error/failure plot for user-supplied limits (R PloterrGEN)."""
    return _err_plot(errgen(n, LL, UL, alp, phi, f),
                     "Error, long term power and pass/fail (given limits)")


# --- Bayesian plot (R 502) ---------------------------------------------------
def ploterrba(n, alp, phi, f, a, b):
    """Error/failure plot for the Bayesian interval, quantile+HPD (R PloterrBA)."""
    from .bayes import errba
    return _err_plot(errba(n, alp, phi, f, a, b),
                     "Error, long term power and pass/fail - Bayesian method")

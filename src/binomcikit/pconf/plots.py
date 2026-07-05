"""4xx family - p-confidence and p-bias plots (R files 402, 412, 422, 423).

Each plot shows p-confidence and p-bias against the number of successes, in two
stacked facets. For the "all methods" variants the lines are coloured by method.
"""
import pandas as pd
from plotnine import aes, facet_grid, geom_line, ggplot, labs

from . import adj_all, base_all, cc_all
from .general import pcopbigen


def _to_long(df):
    """Melt a (x1, pconf, pbias[, method]) frame to long form for faceting."""
    has_method = 'method' in df.columns
    id_vars = ['x1', 'method'] if has_method else ['x1']
    long = df.melt(id_vars=id_vars, value_vars=['pconf', 'pbias'],
                   var_name='Heading', value_name='Value')
    return long, has_method


def _pconf_plot(df, title):
    long, has_method = _to_long(df)
    p = (
        ggplot(long, aes(x='x1', y='Value'))
        + facet_grid('Heading ~ .', scales='free_y')
        + labs(title=title, x="No of successes", y="Confidence / Bias")
    )
    p += geom_line(aes(color='method')) if has_method else geom_line()
    return p


# --- Base method plots (R 402) -----------------------------------------------
def _make_base_plot(fn, label):
    def _plot(n, alp):
        return _pconf_plot(fn(n, alp), f"p-Confidence & p-Bias - {label} method")
    return _plot


plotpcopbiwd = _make_base_plot(base_all.pcopbiwd, "Wald")
plotpcopbisc = _make_base_plot(base_all.pcopbisc, "Score")
plotpcopbias = _make_base_plot(base_all.pcopbias, "ArcSine")
plotpcopbilr = _make_base_plot(base_all.pcopbilr, "Likelihood Ratio")
plotpcopbilt = _make_base_plot(base_all.pcopbilt, "Logit Wald")
plotpcopbitw = _make_base_plot(base_all.pcopbitw, "Wald-T")


def plotpcopbiex(n, alp, e):
    """p-confidence & p-bias plot for the Exact method (R PlotpCOpBIEX)."""
    return _pconf_plot(base_all.pcopbiex(n, alp, e),
                       "p-Confidence & p-Bias - Exact method")


def plotpcopbiall(n, alp):
    """p-confidence & p-bias plot for all six base methods (R PlotpCOpBIAll)."""
    return _pconf_plot(base_all.pcopbiall(n, alp),
                       "p-Confidence & p-Bias - all base methods")


# --- Adjusted method plots (R 412) -------------------------------------------
def _make_adj_plot(fn, label):
    def _plot(n, alp, h):
        return _pconf_plot(fn(n, alp, h),
                           f"p-Confidence & p-Bias - adjusted {label} method")
    return _plot


plotpcopbiawd = _make_adj_plot(adj_all.pcopbiawd, "Wald")
plotpcopbiasc = _make_adj_plot(adj_all.pcopbiasc, "Score")
plotpcopbiaas = _make_adj_plot(adj_all.pcopbiaas, "ArcSine")
plotpcopbialr = _make_adj_plot(adj_all.pcopbialr, "Likelihood Ratio")
plotpcopbialt = _make_adj_plot(adj_all.pcopbialt, "Logit Wald")
plotpcopbiatw = _make_adj_plot(adj_all.pcopbiatw, "Wald-T")


def plotpcopbiaall(n, alp, h):
    """p-confidence & p-bias plot for all six adjusted methods (R PlotpCOpBIAAll)."""
    return _pconf_plot(adj_all.pcopbiaall(n, alp, h),
                       "p-Confidence & p-Bias - all adjusted methods")


# --- Continuity-corrected method plots (R 422) -------------------------------
def _make_cc_plot(fn, label):
    def _plot(n, alp, c):
        return _pconf_plot(
            fn(n, alp, c),
            f"p-Confidence & p-Bias - continuity-corrected {label} method")
    return _plot


plotpcopbicwd = _make_cc_plot(cc_all.pcopbicwd, "Wald")
plotpcopbicsc = _make_cc_plot(cc_all.pcopbicsc, "Score")
plotpcopbicas = _make_cc_plot(cc_all.pcopbicas, "ArcSine")
plotpcopbiclt = _make_cc_plot(cc_all.pcopbiclt, "Logit Wald")
plotpcopbictw = _make_cc_plot(cc_all.pcopbictw, "Wald-T")


def plotpcopbicall(n, alp, c):
    """p-confidence & p-bias plot for all five CC methods (R PlotpCOpBICAll)."""
    return _pconf_plot(cc_all.pcopbicall(n, alp, c),
                       "p-Confidence & p-Bias - all continuity-corrected methods")


# --- General plot (R 423) ----------------------------------------------------
def plotpcopbigen(n, LL, UL):
    """p-confidence & p-bias plot for user-supplied limits (R PlotpCOpBIGEN)."""
    return _pconf_plot(pcopbigen(n, LL, UL),
                       "p-Confidence & p-Bias (given limits)")


# --- Bayesian plot (R 402) ---------------------------------------------------
def plotpcopbiba(n, alp, a1, a2):
    """p-confidence & p-bias plot for the Bayesian interval, quantile+HPD (R PlotpCOpBIBA)."""
    from .bayes import pcopbiba
    ba = pcopbiba(n, alp, a1, a2)
    # reshape the wide Q/H output into the (x1, pconf, pbias, method) form
    q = ba[['x1', 'pconfQ', 'pbiasQ']].rename(
        columns={'pconfQ': 'pconf', 'pbiasQ': 'pbias'})
    q['method'] = "Quantile"
    h = ba[['x1', 'pconfH', 'pbiasH']].rename(
        columns={'pconfH': 'pconf', 'pbiasH': 'pbias'})
    h['method'] = "HPD"
    return _pconf_plot(pd.concat([q, h], ignore_index=True),
                       "p-Confidence & p-Bias - Bayesian method")

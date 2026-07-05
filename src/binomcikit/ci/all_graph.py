"""1xx family - Combined "all methods" CI plots (R files 102/112/122) plus the
Bayesian CI plot (R PlotciBA).

Each numeric all-methods function returns a long frame with columns
(method, x, LowerLimit, UpperLimit, ...); these plots draw the intervals as
horizontal error bars, either overlaid (coloured by method) or faceted by
method (the ``g`` variants).
"""
import pandas as pd
from plotnine import (
    ggplot, aes, labs, geom_errorbarh, geom_point, facet_grid,
)

from .base_n import ciall
from .base_n_x import ciallx
from .adj_n import ciaall
from .adj_n_x import ciaallx
from .cc_n import cicall
from .cc_n_x import cicallx
from .bayes_n import ciba


def _all_plot(df, title, facet=False):
    """Overlaid or faceted horizontal error-bar plot of all-method intervals."""
    d = df.copy()
    d['row'] = range(1, len(d) + 1)
    y = 'method' if facet else 'row'
    p = (
        ggplot(d, aes(x='LowerLimit', y=y))
        + labs(title=title, x="Lower and Upper limits", y="Method")
        + geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit', color='method'),
                         height=0.4)
    )
    if facet:
        p += facet_grid('method ~ .')
    return p


# --- Base (R 102) ------------------------------------------------------------
def plotciall(n, alp):
    """All six base CI methods overlaid (R PlotciAll)."""
    return _all_plot(ciall(n, alp), "Confidence intervals - all base methods")


def plotciallg(n, alp):
    """All six base CI methods faceted by method (R PlotciAllg)."""
    return _all_plot(ciall(n, alp),
                     "Confidence intervals - all base methods", facet=True)


# --- Adjusted (R 112) --------------------------------------------------------
def plotciaall(n, alp, h):
    """All six adjusted CI methods overlaid (R PlotciAAll)."""
    return _all_plot(ciaall(n, alp, h),
                     "Confidence intervals - all adjusted methods")


def plotciaallg(n, alp, h):
    """All six adjusted CI methods faceted (R PlotciAAllg)."""
    return _all_plot(ciaall(n, alp, h),
                     "Confidence intervals - all adjusted methods", facet=True)


def plotciaallx(x, n, alp, h):
    """All six adjusted CI methods for a given x, overlaid (R PlotciAAllx)."""
    return _all_plot(ciaallx(x, n, alp, h),
                     "Confidence intervals - all adjusted methods given x")


def plotciaallxg(x, n, alp, h):
    """All six adjusted CI methods for a given x, faceted (R PlotciAAllxg)."""
    return _all_plot(ciaallx(x, n, alp, h),
                     "Confidence intervals - all adjusted methods given x",
                     facet=True)


# --- Continuity-corrected (R 122) --------------------------------------------
def plotcicall(n, alp, c):
    """All five CC CI methods overlaid (R PlotciCAll)."""
    return _all_plot(cicall(n, alp, c),
                     "Confidence intervals - all continuity-corrected methods")


def plotcicallg(n, alp, c):
    """All five CC CI methods faceted (R PlotciCAllg)."""
    return _all_plot(cicall(n, alp, c),
                     "Confidence intervals - all continuity-corrected methods",
                     facet=True)


def plotcicallx(x, n, alp, c):
    """All five CC CI methods for a given x, overlaid (R PlotciCAllx)."""
    return _all_plot(cicallx(x, n, alp, c),
                     "Confidence intervals - all CC methods given x")


def plotcicallxg(x, n, alp, c):
    """All five CC CI methods for a given x, faceted (R PlotciCAllxg)."""
    return _all_plot(cicallx(x, n, alp, c),
                     "Confidence intervals - all CC methods given x", facet=True)


# --- Bayesian CI plot (R PlotciBA) -------------------------------------------
def plotciba(n, alp, a, b):
    """Bayesian credible intervals (quantile + HPD) as error bars (R PlotciBA)."""
    df = ciba(n, alp, a, b)
    long = pd.concat([
        pd.DataFrame({'x': df['x'], 'LowerLimit': df['LBAQ'],
                      'UpperLimit': df['UBAQ'], 'method': "Quantile"}),
        pd.DataFrame({'x': df['x'], 'LowerLimit': df['LBAH'],
                      'UpperLimit': df['UBAH'], 'method': "HPD"}),
    ], ignore_index=True)
    return (
        ggplot(long, aes(x='LowerLimit', y='x'))
        + labs(title="Bayesian credible intervals",
               x="Lower and Upper limits", y="x")
        + geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit',
                             color='method'), height=0.4)
    )

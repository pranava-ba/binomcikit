"""Plots for base confidence-interval methods given a single x (port of R file 104).

Provides:
    plotciexx   - Exact method given x, across a vector of e values
    plotciallx  - All six base methods given x, overlaid
    plotciallxg - All six base methods given x, faceted by method
"""
import pandas as pd
from plotnine import (
    ggplot, aes, labs, geom_errorbarh, geom_point,
    scale_shape_manual, facet_grid,
)

from .base_n_x import ciexx, ciallx


def _aberration_frame(ss):
    """Build the long-format frame of aberration points (Lower/Upper/ZWI)."""
    parts = []
    ll = ss[ss['LowerAbb'] == "YES"]
    if len(ll) > 0:
        parts.append(pd.DataFrame(
            {'ID': ll['ID'], 'Value': ll['LowerLimit'], 'Aberration': "Lower"}))
    ul = ss[ss['UpperAbb'] == "YES"]
    if len(ul) > 0:
        parts.append(pd.DataFrame(
            {'ID': ul['ID'], 'Value': ul['UpperLimit'], 'Aberration': "Upper"}))
    zl = ss[ss['ZWI'] == "YES"]
    if len(zl) > 0:
        parts.append(pd.DataFrame(
            {'ID': zl['ID'], 'Value': zl['LowerLimit'], 'Aberration': "ZWI"}))
    if parts:
        return pd.concat(parts, ignore_index=True)
    return pd.DataFrame(columns=['ID', 'Value', 'Aberration'])


def plotciexx(x, n, alp, e):
    """Plot the Exact confidence interval given x across e values (R PlotciEXx)."""
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if e is None:
        raise ValueError("'e' is missing")
    if not isinstance(x, (int, float)) or x < 0 or x > n:
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")
    e_list = e if isinstance(e, (list, tuple)) else [e]
    if len(e_list) > 10:
        raise ValueError("Plot of only 10 intervals of 'e' is possible")

    ss1 = ciexx(x, n, alp, e_list)
    ss = pd.DataFrame({
        'ID': range(1, len(ss1) + 1),
        'x': x,
        'LowerLimit': ss1['LEXx'].values,
        'UpperLimit': ss1['UEXx'].values,
        'LowerAbb': ss1['LABB'].values,
        'UpperAbb': ss1['UABB'].values,
        'ZWI': ss1['ZWI'].values,
        'e': ss1['e'].values,
    })
    ss['e'] = ss['e'].astype('category')
    ldf = _aberration_frame(ss)

    plot = (
        ggplot(ss, aes(x='UpperLimit', y='ID'))
        + labs(x="Lower and Upper limits", y="x values",
               title="Exact method given x")
        + geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit', color='e'),
                         size=0.5)
    )
    if len(ldf) > 0:
        plot += geom_point(
            data=ldf, mapping=aes(x='Value', y='ID', shape='Aberration'),
            size=4, fill="red")
        plot += scale_shape_manual(values=['o', 's', 'D'])
    return plot


def plotciallx(x, n, alp):
    """Plot all six base CI methods for a given x, overlaid (R PlotciAllx)."""
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if not isinstance(x, (int, float)) or x < 0 or x > n:
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")

    ss1 = ciallx(x, n, alp)
    ss = ss1.copy()
    ss['ID'] = range(1, len(ss) + 1)
    ldf = _aberration_frame(ss)

    plot = (
        ggplot(ss, aes(x='UpperLimit', y='ID'))
        + labs(x="Lower and Upper limits", y="Method",
               title="Confidence interval for all methods given x")
        + geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit', color='method'),
                         size=0.5)
    )
    if len(ldf) > 0:
        plot += geom_point(
            data=ldf, mapping=aes(x='Value', y='ID', shape='Aberration'),
            size=4, fill="red")
        plot += scale_shape_manual(values=['o', 's', 'D'])
    return plot


def plotciallxg(x, n, alp):
    """Plot all six base CI methods for a given x, faceted by method (R PlotciAllxg)."""
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if not isinstance(x, (int, float)) or x < 0 or x > n:
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")

    ss1 = ciallx(x, n, alp)
    ss = ss1.copy()
    ss['ID'] = range(1, len(ss) + 1)

    return (
        ggplot(ss, aes(x='UpperLimit', y='method'))
        + labs(x="Lower and Upper limits", y="Method",
               title="Confidence interval for all methods given x")
        + geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit', color='method'),
                         size=0.5)
        + facet_grid('method ~ .')
    )

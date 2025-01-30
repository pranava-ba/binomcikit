from a_121_cc_n_confidence_intervals import *

###################################################################
import pandas as pd
import numpy as np
from plotnine import *

def plotcicwd(n, alp, c):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if c is None:
        raise ValueError("'c' is missing")
    if not isinstance(n, (int, float)) or n <= 0 or len(np.atleast_1d(n)) > 1:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0 or len(np.atleast_1d(alp)) > 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if c < 0 or len(np.atleast_1d(c)) > 1:
        raise ValueError("'c' has to be positive")

    # Assuming ciCWD is a previously defined function that returns a DataFrame
    WaldCI_df = cicwd(n, alp, c)

    ss1 = pd.DataFrame({
        'x': WaldCI_df['x'],
        'LowerLimit': WaldCI_df['LCW'],
        'UpperLimit': WaldCI_df['UCW'],
        'LowerAbb': WaldCI_df['LABB'],
        'UpperAbb': WaldCI_df['UABB'],
        'ZWI': WaldCI_df['ZWI']
    })
    id_col = np.arange(1, len(ss1) + 1)
    ss = pd.DataFrame({'ID': id_col, **ss1})

    ll = ss[ss['LowerAbb'] == "YES"]
    ul = ss[ss['UpperAbb'] == "YES"]
    zl = ss[ss['ZWI'] == "YES"]

    if not ll.empty:
        ll = ll[['ID', 'LowerLimit']]
        ll['Abberation'] = "Lower"
        ll.columns = ['ID', 'Value', 'Abberation']

    if not ul.empty:
        ul = ul[['ID', 'UpperLimit']]
        ul['Abberation'] = "Upper"
        ul.columns = ['ID', 'Value', 'Abberation']

    if not zl.empty:
        zl = zl[['ID', 'LowerLimit']]
        zl['Abberation'] = "ZWI"
        zl.columns = ['ID', 'Value', 'Abberation']

    ldf = pd.concat([ll, ul, zl], ignore_index=True)

    if not ldf.empty:
        plot = (ggplot(ss, aes(x='UpperLimit', y='ID')) +
                ggtitle("Confidence Interval - Continuity corrected Wald method") +
                labs(x="Lower and Upper limits", y="ID") +
                geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5) +
                geom_point(ldf, aes(x='Value', y='ID', group='Abberation', shape='Abberation'), size=4, fill="red"))# +
                #scale_shape_manual(values=[21, 22, 23]))
    else:
        plot = (ggplot(ss, aes(x='UpperLimit', y='ID')) +
                ggtitle("Confidence Interval - Continuity corrected Wald method") +
                labs(x="Lower and Upper limits", y="ID") +
                geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5))

    plot.show()
###################################################################################
def plotcicas(n, alp, c):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if c is None:
        raise ValueError("'c' is missing")
    if not isinstance(n, (int, float)) or n <= 0 or len(np.atleast_1d(n)) > 1:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0 or len(np.atleast_1d(alp)) > 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if c < 0 or len(np.atleast_1d(c)) > 1:
        raise ValueError("'c' has to be positive")

    # Assuming ciCAS is a previously defined function that returns a DataFrame
    ArcSineCI_df = cicas(n, alp, c)

    ss1 = pd.DataFrame({
        'x': ArcSineCI_df['x'],
        'LowerLimit': ArcSineCI_df['LCA'],
        'UpperLimit': ArcSineCI_df['UCA'],
        'LowerAbb': ArcSineCI_df['LABB'],
        'UpperAbb': ArcSineCI_df['UABB'],
        'ZWI': ArcSineCI_df['ZWI']
    })
    id_col = np.arange(1, len(ss1) + 1)
    ss = pd.DataFrame({'ID': id_col, **ss1})

    ll = ss[ss['LowerAbb'] == "YES"]
    ul = ss[ss['UpperAbb'] == "YES"]
    zl = ss[ss['ZWI'] == "YES"]

    if not ll.empty:
        ll = ll[['ID', 'LowerLimit']]
        ll['Abberation'] = "Lower"
        ll.columns = ['ID', 'Value', 'Abberation']

    if not ul.empty:
        ul = ul[['ID', 'UpperLimit']]
        ul['Abberation'] = "Upper"
        ul.columns = ['ID', 'Value', 'Abberation']

    if not zl.empty:
        zl = zl[['ID', 'LowerLimit']]
        zl['Abberation'] = "ZWI"
        zl.columns = ['ID', 'Value', 'Abberation']

    ldf = pd.concat([ll, ul, zl], ignore_index=True)

    if not ldf.empty:
        plot = (ggplot(ss, aes(x='UpperLimit', y='ID')) +
                ggtitle("Confidence Interval - Continuity corrected ArcSine method") +
                labs(x="Lower and Upper limits", y="ID") +
                geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5) +
                geom_point(ldf, aes(x='Value', y='ID', group='Abberation', shape='Abberation'), size=4, fill="red"))
                #+
                #scale_shape_manual(values=[21, 22, 23]))
    else:
        plot = (ggplot(ss, aes(x='UpperLimit', y='ID')) +
                ggtitle("Confidence Interval - Continuity corrected ArcSine method") +
                labs(x="Lower and Upper limits", y="ID") +
                geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5))

    plot.show()
#########################################################################################################
def plotcicsc(n, alp, c):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if c is None:
        raise ValueError("'c' is missing")
    if not isinstance(n, (int, float)) or n <= 0 or len(np.atleast_1d(n)) > 1:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0 or len(np.atleast_1d(alp)) > 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if c < 0 or len(np.atleast_1d(c)) > 1:
        raise ValueError("'c' has to be positive")

    # Assuming ciCSC is a previously defined function that returns a DataFrame
    ScoreCI_df = cicsc(n, alp, c)

    ss1 = pd.DataFrame({
        'x': ScoreCI_df['x'],
        'LowerLimit': ScoreCI_df['LCS'],
        'UpperLimit': ScoreCI_df['UCS'],
        'LowerAbb': ScoreCI_df['LABB'],
        'UpperAbb': ScoreCI_df['UABB'],
        'ZWI': ScoreCI_df['ZWI']
    })
    id_col = np.arange(1, len(ss1) + 1)
    ss = pd.DataFrame({'ID': id_col, **ss1})

    ll = ss[ss['LowerAbb'] == "YES"]
    ul = ss[ss['UpperAbb'] == "YES"]
    zl = ss[ss['ZWI'] == "YES"]

    if not ll.empty:
        ll = ll[['ID', 'LowerLimit']]
        ll['Abberation'] = "Lower"
        ll.columns = ['ID', 'Value', 'Abberation']

    if not ul.empty:
        ul = ul[['ID', 'UpperLimit']]
        ul['Abberation'] = "Upper"
        ul.columns = ['ID', 'Value', 'Abberation']

    if not zl.empty:
        zl = zl[['ID', 'LowerLimit']]
        zl['Abberation'] = "ZWI"
        zl.columns = ['ID', 'Value', 'Abberation']

    ldf = pd.concat([ll, ul, zl], ignore_index=True)

    if not ldf.empty:
        plot = (ggplot(ss, aes(x='UpperLimit', y='ID')) +
                ggtitle("Confidence Interval - Continuity corrected Score method") +
                labs(x="Lower and Upper limits", y="ID") +
                geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5) +
                geom_point(ldf, aes(x='Value', y='ID', group='Abberation', shape='Abberation'), size=4, fill="red"))# +
                #scale_shape_manual(values=[21, 22, 23]))
    else:
        plot = (ggplot(ss, aes(x='UpperLimit', y='ID')) +
                ggtitle("Confidence Interval - Continuity corrected Score method") +
                labs(x="Lower and Upper limits", y="ID") +
                geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5))

    plot.show()
#################################################
def plotciclt(n, alp, c):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if c is None:
        raise ValueError("'c' is missing")
    if not isinstance(n, (int, float)) or n <= 0 or len(np.atleast_1d(n)) > 1:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0 or len(np.atleast_1d(alp)) > 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(c, (int, float)) or len(np.atleast_1d(c)) > 1 or c < 0:
        raise ValueError("'c' has to be positive")

    # Assuming ciCLT is a previously defined function that returns a DataFrame
    WaldLCI_df = ciclt(n, alp, c)

    ss1 = pd.DataFrame({
        'x': WaldLCI_df['x'],
        'LowerLimit': WaldLCI_df['LCLT'],
        'UpperLimit': WaldLCI_df['UCLT'],
        'LowerAbb': WaldLCI_df['LABB'],
        'UpperAbb': WaldLCI_df['UABB'],
        'ZWI': WaldLCI_df['ZWI']
    })
    id_col = np.arange(1, len(ss1) + 1)
    ss = pd.DataFrame({'ID': id_col, **ss1})

    ll = ss[ss['LowerAbb'] == "YES"]
    ul = ss[ss['UpperAbb'] == "YES"]
    zl = ss[ss['ZWI'] == "YES"]

    if not ll.empty:
        ll = ll[['ID', 'LowerLimit']]
        ll['Abberation'] = "Lower"
        ll.columns = ['ID', 'Value', 'Abberation']

    if not ul.empty:
        ul = ul[['ID', 'UpperLimit']]
        ul['Abberation'] = "Upper"
        ul.columns = ['ID', 'Value', 'Abberation']

    if not zl.empty:
        zl = zl[['ID', 'LowerLimit']]
        zl['Abberation'] = "ZWI"
        zl.columns = ['ID', 'Value', 'Abberation']

    ldf = pd.concat([ll, ul, zl], ignore_index=True)

    if not ldf.empty:
        plot = (ggplot(ss, aes(x='UpperLimit', y='ID')) +
                ggtitle("Confidence Interval - Continuity corrected Logit Wald method") +
                labs(x="Lower and Upper limits", y="ID") +
                geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5) +
                geom_point(ldf, aes(x='Value', y='ID', group='Abberation', shape='Abberation'), size=4, fill="red"))# +
                #scale_shape_manual(values=[21, 22, 23]))
    else:
        plot = (ggplot(ss, aes(x='UpperLimit', y='ID')) +
                ggtitle("Confidence Interval - Continuity corrected Logit Wald method") +
                labs(x="Lower and Upper limits", y="ID") +
                geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5))

    plot.show()
###############################################################################################

def plotcictw(n, alp, c):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if c is None:
        raise ValueError("'c' is missing")
    if not isinstance(n, (int, float)) or n <= 0 or len(np.atleast_1d(n)) > 1:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0 or len(np.atleast_1d(alp)) > 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(c, (int, float)) or len(np.atleast_1d(c)) > 1 or c < 0:
        raise ValueError("'c' has to be positive")

    # Assuming ciCTW is a previously defined function that returns a DataFrame
    WaldTCI_df = cictw(n, alp, c)

    ss1 = pd.DataFrame({
        'x': WaldTCI_df['x'],
        'LowerLimit': WaldTCI_df['LCTW'],
        'UpperLimit': WaldTCI_df['UCTW'],
        'LowerAbb': WaldTCI_df['LABB'],
        'UpperAbb': WaldTCI_df['UABB'],
        'ZWI': WaldTCI_df['ZWI']
    })
    id_col = np.arange(1, len(ss1) + 1)
    ss = pd.DataFrame({'ID': id_col, **ss1})

    ll = ss[ss['LowerAbb'] == "YES"]
    ul = ss[ss['UpperAbb'] == "YES"]
    zl = ss[ss['ZWI'] == "YES"]

    if not ll.empty:
        ll = ll[['ID', 'LowerLimit']]
        ll['Abberation'] = "Lower"
        ll.columns = ['ID', 'Value', 'Abberation']

    if not ul.empty:
        ul = ul[['ID', 'UpperLimit']]
        ul['Abberation'] = "Upper"
        ul.columns = ['ID', 'Value', 'Abberation']

    if not zl.empty:
        zl = zl[['ID', 'LowerLimit']]
        zl['Abberation'] = "ZWI"
        zl.columns = ['ID', 'Value', 'Abberation']

    ldf = pd.concat([ll, ul, zl], ignore_index=True)

    if not ldf.empty:
        plot = (ggplot(ss, aes(x='UpperLimit', y='ID')) +
                ggtitle("Confidence Interval - Continuity corrected Wald-T method") +
                labs(x="Lower and Upper limits", y="ID") +
                geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5) +
                geom_point(ldf, aes(x='Value', y='ID', group='Abberation', shape='Abberation'), size=4, fill="red"))# +
                #scale_shape_manual(values=[21, 22, 23]))
    else:
        plot = (ggplot(ss, aes(x='UpperLimit', y='ID')) +
                ggtitle("Confidence Interval - Continuity corrected Wald-T method") +
                labs(x="Lower and Upper limits", y="ID") +
                geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5))
    plot.show()

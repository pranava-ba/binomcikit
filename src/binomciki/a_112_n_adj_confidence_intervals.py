from a_111_n_adj_confidence_intervals import *
import pandas as pd
from plotnine import *


def plotciawd(n, alp, h):
        # Get the WaldCI dataframe from ciAWD function
        WaldCI_df = ciawd(n, alp, h)

        # Prepare the dataframe
        ss1 = pd.DataFrame({
            'x': WaldCI_df['x'],
            'LowerLimit': WaldCI_df['LAWD'],
            'UpperLimit': WaldCI_df['UAWD'],
            'LowerAbb': WaldCI_df['LABB'],
            'UpperAbb': WaldCI_df['UABB'],
            'ZWI': WaldCI_df['ZWI']
        })
        ss1['ID'] = range(1, len(ss1) + 1)

        # Get the subsets for different aberrations
        ll = ss1[ss1['LowerAbb'] == "YES"]
        ul = ss1[ss1['UpperAbb'] == "YES"]
        zl = ss1[ss1['ZWI'] == "YES"]

        # Combine the aberration data
        ldf = pd.concat([
            ll[['ID', 'LowerLimit']].assign(Abberation='Lower').rename(columns={'LowerLimit': 'Value'}),
            ul[['ID', 'UpperLimit']].assign(Abberation='Upper').rename(columns={'UpperLimit': 'Value'}),
            zl[['ID', 'LowerLimit']].assign(Abberation='ZWI').rename(columns={'LowerLimit': 'Value'})
        ])

        plot= (ggplot(ss1, aes(x='UpperLimit', y='ID')) +
             geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5) +
             labs(x="Lower and Upper limits", title="Confidence interval for Adjusted Wald Method"))
        if not ldf.empty:
            plot+= geom_point(data=ldf, mapping=aes(x='Value', y='ID', shape='Abberation', color='Abberation'), size=4)
        plot +=scale_colour_manual(values={'LowerLimit': 'blue', 'UpperLimit': 'green', 'ZWI': 'red'})
        plot.show()








def plotciaas(n, alp, h):
    # Error checks
    if n <= 0 or not isinstance(n, (int, float)):
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")
    if h < 0 or not isinstance(h, (int, float)):
        raise ValueError("'h' has to be greater than or equal to 0")

    # Get the ArcSine CI dataframe from ciAAS function
    ArcSineCI_df = ciaas(n, alp, h)

    # Prepare the dataframe
    ss1 = pd.DataFrame({
        'x': ArcSineCI_df['x'],
        'LowerLimit': ArcSineCI_df['LAAS'],
        'UpperLimit': ArcSineCI_df['UAAS'],
        'LowerAbb': ArcSineCI_df['LABB'],
        'UpperAbb': ArcSineCI_df['UABB'],
        'ZWI': ArcSineCI_df['ZWI']
    })

    ss1['ID'] = range(1, len(ss1) + 1)

    # Subsets for aberrations
    ll = ss1[ss1['LowerAbb'] == "YES"]
    ul = ss1[ss1['UpperAbb'] == "YES"]
    zl = ss1[ss1['ZWI'] == "YES"]

    # Combine the aberration data
    ldf = pd.concat([
        ll[['ID', 'LowerLimit']].assign(Abberation='Lower').rename(columns={'LowerLimit': 'Value'}),
        ul[['ID', 'UpperLimit']].assign(Abberation='Upper').rename(columns={'UpperLimit': 'Value'}),
        zl[['ID', 'LowerLimit']].assign(Abberation='ZWI').rename(columns={'LowerLimit': 'Value'})
    ])

    # Create the plot
    plot = (ggplot(ss1, aes(x='UpperLimit', y='ID')) +
         geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5) +
         labs(x="Lower and Upper limits", y="x values", title="Confidence interval for Adjusted ArcSine Method"))

    # Add points if aberrations exist
    if not ldf.empty:
        plot+= geom_point(data=ldf, mapping=aes(x='Value', y='ID', shape='Abberation'), size=4)

        # Add custom shape scale
        plot+= scale_shape_manual(values={'LowerLimit': 21, 'UpperLimit': 22, 'ZWI': 23})

    plot.show()





def plotcialr(n, alp, h):
    # Error checks
    if n <= 0 or not isinstance(n, (int, float)):
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")
    if h < 0 or not isinstance(h, int):
        raise ValueError("'h' has to be an integer greater than or equal to 0")

    # Get the Likelihood Ratio CI dataframe from ciALR function
    LRCI_df = cialr(n, alp, round(h))

    # Prepare the dataframe
    ss1 = pd.DataFrame({
        'x': LRCI_df['x'],
        'LowerLimit': LRCI_df['LALR'],
        'UpperLimit': LRCI_df['UALR'],
        'LowerAbb': LRCI_df['LABB'],
        'UpperAbb': LRCI_df['UABB'],
        'ZWI': LRCI_df['ZWI']
    })
    ss1['ID'] = range(1, len(ss1) + 1)

    # Subsets for aberrations
    ll = ss1[ss1['LowerAbb'] == "YES"]
    ul = ss1[ss1['UpperAbb'] == "YES"]
    zl = ss1[ss1['ZWI'] == "YES"]

    # Combine the aberration data
    ldf = pd.concat([
        ll[['ID', 'LowerLimit']].assign(Abberation='Lower').rename(columns={'LowerLimit': 'Value'}),
        ul[['ID', 'UpperLimit']].assign(Abberation='Upper').rename(columns={'UpperLimit': 'Value'}),
        zl[['ID', 'LowerLimit']].assign(Abberation='ZWI').rename(columns={'LowerLimit': 'Value'})
    ])

    # Create the plot
    plot = (ggplot(ss1, aes(x='UpperLimit', y='ID')) +
         geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5) +
         labs(x="Lower and Upper limits", y="x values") +
         ggtitle("Confidence interval for adjusted Likelihood Ratio method"))

    # Add points if aberrations exist
    if not ldf.empty:
        plot += geom_point(data=ldf, mapping=aes(x='Value', y='ID', shape='Abberation'), size=4)

        # Add custom shape scale
        plot += scale_shape_manual(values={'Lower': 21, 'Upper': 22, 'ZWI': 23})

    plot.show()





def plotciasc(n, alp, h):
    # Error checks
    if n <= 0 or not isinstance(n, (int, float)):
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")
    if h < 0 or not isinstance(h, (int, float)):
        raise ValueError("'h' has to be greater than or equal to 0")
    ScoreCI_df = ciasc(n, alp, h)

    # Prepare the dataframe
    ss1 = pd.DataFrame({
        'x': ScoreCI_df['x'],
        'LowerLimit': ScoreCI_df['LASC'],
        'UpperLimit': ScoreCI_df['UASC'],
        'LowerAbb': ScoreCI_df['LABB'],
        'UpperAbb': ScoreCI_df['UABB'],
        'ZWI': ScoreCI_df['ZWI']
    })
    ss1['ID'] = range(1, len(ss1) + 1)

    # Subsets for aberrations
    ll = ss1[ss1['LowerAbb'] == "YES"]
    ul = ss1[ss1['UpperAbb'] == "YES"]
    zl = ss1[ss1['ZWI'] == "YES"]

    # Combine the aberration data
    ldf = pd.concat([
        ll[['ID', 'LowerLimit']].assign(Abberation='Lower').rename(columns={'LowerLimit': 'Value'}),
        ul[['ID', 'UpperLimit']].assign(Abberation='Upper').rename(columns={'UpperLimit': 'Value'}),
        zl[['ID', 'LowerLimit']].assign(Abberation='ZWI').rename(columns={'LowerLimit': 'Value'})
    ])

    # Create the plot
    p = (ggplot(ss1, aes(x='UpperLimit', y='ID')) +
         geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5) +
         labs(x="Lower and Upper limits", y="x values") +
         ggtitle("Confidence interval for adjusted Score method"))

    # Add points if aberrations exist
    if not ldf.empty:
        p += geom_point(data=ldf, mapping=aes(x='Value', y='ID', shape='Abberation'), size=4)

        # Add custom shape scale
        p += scale_shape_manual(values={'Lower': 21, 'Upper': 22, 'ZWI': 23})

    p.show()





def plotcialt(n, alp, h):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if h is None:
        raise ValueError("'h' is missing")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not (0 <= alp <= 1):
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(h, (int, float)) or h < 0:
        raise ValueError("'h' has to be greater than or equal to 0")

    # Assume ciALT is already defined
    WaldLCI_df = cialt(n, alp, h)

    ss1 = pd.DataFrame({
        'x': WaldLCI_df['x'],
        'LowerLimit': WaldLCI_df['LALT'],
        'UpperLimit': WaldLCI_df['UALT'],
        'LowerAbb': WaldLCI_df['LABB'],
        'UpperAbb': WaldLCI_df['UABB'],
        'ZWI': WaldLCI_df['ZWI']
    })

    ss1['ID'] = range(1, len(ss1) + 1)

    ll = ss1[ss1['LowerAbb'] == "YES"][['ID', 'LowerLimit']]
    ll['Abberation'] = 'Lower'
    ul = ss1[ss1['UpperAbb'] == "YES"][['ID', 'UpperLimit']]
    ul['Abberation'] = 'Upper'
    zl = ss1[ss1['ZWI'] == "YES"][['ID', 'LowerLimit']]
    zl['Abberation'] = 'ZWI'

    ldf = pd.concat([ll.rename(columns={'LowerLimit': 'Value'}),
                     ul.rename(columns={'UpperLimit': 'Value'}),
                     zl.rename(columns={'LowerLimit': 'Value'})])

    # Plot with plotnine
    if not ldf.empty:
        plot = (ggplot(ss1, aes(x='UpperLimit', y='ID')) +
                ggtitle("Confidence interval for adjusted Logit Wald method") +
                labs(x="Lower and Upper limits", y="x values") +
                geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5) +
                geom_point(ldf, aes(x='Value', y='ID', group='Abberation', shape='Abberation'),
                           size=4, fill='red') +
                scale_shape_manual(values=[21, 22, 23]) +
                theme())
    else:
        plot = (ggplot(ss1, aes(x='UpperLimit', y='ID')) +
                ggtitle("Confidence interval for adjusted Logit Wald method") +
                labs(x="Lower and Upper limits", y="x values") +
                geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5) +
                theme())
    plot.show()






def plotciatw(n, alp, h):
    # Input validation
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if h is None:
        raise ValueError("'h' is missing")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not (0 <= alp <= 1):
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(h, (int, float)) or h < 0:
        raise ValueError("'h' has to be greater than or equal to 0")

    # Assume ciATW is already defined
    AdWaldCI_df = ciatw(n, alp, h)

    # Create the summary dataframe
    ss1 = pd.DataFrame({
        'x': AdWaldCI_df['x'],
        'LowerLimit': AdWaldCI_df['LATW'],
        'UpperLimit': AdWaldCI_df['UATW'],
        'LowerAbb': AdWaldCI_df['LABB'],
        'UpperAbb': AdWaldCI_df['UABB'],
        'ZWI': AdWaldCI_df['ZWI']
    })

    ss1['ID'] = range(1, len(ss1) + 1)

    # Create dataframes for different types of aberrations
    ll = ss1[ss1['LowerAbb'] == "YES"][['ID', 'LowerLimit']]
    ll['Abberation'] = 'Lower'
    ul = ss1[ss1['UpperAbb'] == "YES"][['ID', 'UpperLimit']]
    ul['Abberation'] = 'Upper'
    zl = ss1[ss1['ZWI'] == "YES"][['ID', 'LowerLimit']]
    zl['Abberation'] = 'ZWI'

    # Combine all aberrations into one dataframe
    ldf = pd.concat([
        ll.rename(columns={'LowerLimit': 'Value'}),
        ul.rename(columns={'UpperLimit': 'Value'}),
        zl.rename(columns={'LowerLimit': 'Value'})
    ])

    # Create the plot
    if not ldf.empty:
        plot = (ggplot(ss1, aes(x='UpperLimit', y='ID')) +
                ggtitle("Confidence interval for adjusted Wald-T method") +
                labs(y="x values", x="Lower and Upper limits") +
                geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5) +
                geom_point(data=ldf,
                          mapping=aes(x='Value', y='ID', shape='Abberation'),
                          size=4,
                          fill='red',
                          stroke=0.5) +
                scale_shape_manual(values=['o', 's', '^']) +  # Using plotnine-compatible markers
                theme_bw())  # Adding a clean theme
    else:
        plot = (ggplot(ss1, aes(x='UpperLimit', y='ID')) +
                ggtitle("Confidence interval for adjusted Wald-T method") +
                labs(x="Lower and Upper limits", y="x values") +
                geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5) +
                theme_bw())

    plot.show()


#SJTP
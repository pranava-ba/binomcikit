from a_101_n_confidence_base import *
def plotciex(n, alp, e):
    # Input validation
    if n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if alp < 0 or alp > 1:
        raise ValueError("'alpha' has to be between 0 and 1")

    # Handle single float input for 'e'
    if isinstance(e, float):
        e = [e]  # Convert to a list if it's a single float
    elif not isinstance(e, (list, np.ndarray)):
        raise ValueError("'e' must be a float or an iterable containing floats")

    # Ensure all values in e are between 0 and 1
    if any(val < 0 or val > 1 for val in e):
        raise ValueError("'e' has to be between 0 and 1")

    if len(e) > 10:
        raise ValueError("Plot of only 10 intervals of 'e' is possible")

    # Assuming ciEX is defined elsewhere
    ss1 = ciex(n, alp, e)
    ss1['ID'] = np.arange(1, len(ss1) + 1)
    ss1['e'] = ss1['e'].astype('category')

    ll = ss1[ss1['LABB'] == "YES"]
    ul = ss1[ss1['UABB'] == "YES"]
    zl = ss1[ss1['ZWI'] == "YES"]

    ldf = pd.DataFrame()

    if not ll.empty:
        ll = ll[['ID', 'e']]
        ll['Abberation'] = "Lower"
        ll.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, ll], ignore_index=True)

    if not ul.empty:
        ul = ul[['ID', 'UEX']]
        ul['Abberation'] = "Upper"
        ul.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, ul], ignore_index=True)

    if not zl.empty:
        zl = zl[['ID', 'e']]
        zl['Abberation'] = "ZWI"
        zl.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, zl], ignore_index=True)

    # Plotting using plotnine
    p = (ggplot(ss1, aes(x='UEX', y='ID')) +
         geom_errorbarh(aes(xmin='LEX', xmax='UEX', color='e'), height=0.3) +
         labs(x="Lower and Upper limits", y="ID", title="Exact method") +
         scale_color_manual(values=["brown", "black", "blue", "cyan4", "red",
                                    "orange", "chartreuse4", "blueviolet",
                                    "deeppink", "darksalmon", "tan1"]))
         # +
         #scale_shape_manual(values=[21, 22, 23]) +
         #theme(legend_position='right'))

    if not ldf.empty:
        geom_point_layer = geom_point(
            data=ldf,
            mapping=aes(x='Value', y='ID', shape='Abberation', color='Abberation'),
            size=4
        )
        p += geom_point_layer

    p.show()





##############################################################

def plotciwd(n, alp):
    if n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if alp < 0 or alp > 1:
        raise ValueError("'alpha' has to be between 0 and 1")

    # Assume ciWD is defined elsewhere and returns a DataFrame-like object
    WaldCI_df = ciwd(n, alp)  # This should return a DataFrame with the necessary columns
    ss1 = pd.DataFrame({
        'x': WaldCI_df['x'],
        'LowerLimit': WaldCI_df['LWD'],
        'UpperLimit': WaldCI_df['UWD'],
        'LowerAbb': WaldCI_df['LABB'],
        'UpperAbb': WaldCI_df['UABB'],
        'ZWI': WaldCI_df['ZWI']
    })

    ss1['ID'] = range(1, len(ss1) + 1)

    # Filter data for aberrations
    ll = ss1[ss1['LowerAbb'] == "YES"]
    ul = ss1[ss1['UpperAbb'] == "YES"]
    zl = ss1[ss1['ZWI'] == "YES"]

    ldf = pd.DataFrame()  # Initialize an empty DataFrame for aberrations

    if not ll.empty:
        ll = ll[['ID', 'LowerLimit']].copy()
        ll['Abberation'] = "Lower"
        ll.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, ll], ignore_index=True)

    if not ul.empty:
        ul = ul[['ID', 'UpperLimit']].copy()
        ul['Abberation'] = "Upper"
        ul.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, ul], ignore_index=True)

    if not zl.empty:
        zl = zl[['ID', 'LowerLimit']].copy()
        zl['Abberation'] = "ZWI"
        zl.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, zl], ignore_index=True)

    # Create the base plot
    p = (ggplot(ss1, aes(x='UpperLimit', y='ID')) +
         labs(x="Lower and Upper limits", y="ID", title="Confidence Interval - Wald method") +
         geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5))

    # Add points for aberrations if they exist
    if not ldf.empty:
        p += (geom_point(data=ldf,
                        mapping=aes(x='Value', y='ID', shape='Abberation', color='Abberation'),
                        size=4) )
              #+ scale_shape_manual(values=[21, 22, 23]))

    p.show()  # Display the plot

# Example usage (ensure ciWD function is defined)
# PlotciWD(10, 0.05)

def plotcias(n, alp):
    if n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if alp < 0 or alp > 1:
        raise ValueError("'alpha' has to be between 0 and 1")

    # Assume ciAS is defined elsewhere and returns a DataFrame-like object
    ArcSineCI_df = cias(n, alp)  # ciAS should return a DataFrame with the necessary columns
    ss1 = pd.DataFrame({
        'x': ArcSineCI_df['x'],
        'LowerLimit': ArcSineCI_df['LAS'],
        'UpperLimit': ArcSineCI_df['UAS'],
        'LowerAbb': ArcSineCI_df['LABB'],
        'UpperAbb': ArcSineCI_df['UABB'],
        'ZWI': ArcSineCI_df['ZWI']
    })

    ss1['ID'] = range(1, len(ss1) + 1)

    ll = ss1[ss1['LowerAbb'] == "YES"]
    ul = ss1[ss1['UpperAbb'] == "YES"]
    zl = ss1[ss1['ZWI'] == "YES"]

    ldf = pd.DataFrame()  # Initialize an empty DataFrame for the lower, upper, and ZWI points

    if not ll.empty:
        ll = ll[['ID', 'LowerLimit']].copy()
        ll['Abberation'] = "Lower"
        ll.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, ll], ignore_index=True)

    if not ul.empty:
        ul = ul[['ID', 'UpperLimit']].copy()
        ul['Abberation'] = "Upper"
        ul.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, ul], ignore_index=True)

    if not zl.empty:
        zl = zl[['ID', 'LowerLimit']].copy()
        zl['Abberation'] = "ZWI"
        zl.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, zl], ignore_index=True)

    p = (ggplot(ss1, aes(x='UpperLimit', y='ID')) +
         labs(x="Lower and Upper limits", y="ID", title="Confidence Interval - ArcSine method") +
         geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5))

    if not ldf.empty:
        p += geom_point(data=ldf,
                        mapping=aes(x='Value', y='ID', group='Abberation', shape='Abberation'),
                        size=4, fill="red")
        #+ scale_shape_manual(values=[21, 22, 23])

    p.show()

def plotcilr(n, alp):
    if n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if alp < 0 or alp > 1:
        raise ValueError("'alpha' has to be between 0 and 1")

    # Assume ciLR is defined elsewhere and returns a DataFrame-like object
    LRCI_df = cilr(n, alp)  # ciLR should return a DataFrame with the necessary columns
    ss1 = pd.DataFrame({
        'x': LRCI_df['x'],
        'LowerLimit': LRCI_df['LLR'],
        'UpperLimit': LRCI_df['ULR'],
        'LowerAbb': LRCI_df['LABB'],
        'UpperAbb': LRCI_df['UABB'],
        'ZWI': LRCI_df['ZWI']
    })

    ss1['ID'] = range(1, len(ss1) + 1)

    ll = ss1[ss1['LowerAbb'] == "YES"]
    ul = ss1[ss1['UpperAbb'] == "YES"]
    zl = ss1[ss1['ZWI'] == "YES"]

    ldf = pd.DataFrame()  # Initialize an empty DataFrame for the lower, upper, and ZWI points

    if not ll.empty:
        ll = ll[['ID', 'LowerLimit']].copy()
        ll['Abberation'] = "Lower"
        ll.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, ll], ignore_index=True)

    if not ul.empty:
        ul = ul[['ID', 'UpperLimit']].copy()
        ul['Abberation'] = "Upper"
        ul.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, ul], ignore_index=True)

    if not zl.empty:
        zl = zl[['ID', 'LowerLimit']].copy()
        zl['Abberation'] = "ZWI"
        zl.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, zl], ignore_index=True)

    p = (ggplot(ss1, aes(x='UpperLimit', y='ID')) +
         labs(x="Lower and Upper limits", y="ID", title="Confidence Interval - Likelihood Ratio method") +
         geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5))

    if not ldf.empty:
        p += geom_point(data=ldf,
                        mapping=aes(x='Value', y='ID', group='Abberation', shape='Abberation'),
                        size=4, fill="red") + scale_shape_manual(values=[21, 22, 23])

    p.show()

def plotcisc(n, alp):
    if n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if alp < 0 or alp > 1:
        raise ValueError("'alpha' has to be between 0 and 1")

    # Assume ciSC is defined elsewhere and returns a DataFrame-like object
    ScoreCI_df = cisc(n, alp)  # ciSC should return a DataFrame with the necessary columns
    ss1 = pd.DataFrame({
        'x': ScoreCI_df['x'],
        'LowerLimit': ScoreCI_df['LSC'],
        'UpperLimit': ScoreCI_df['USC'],
        'LowerAbb': ScoreCI_df['LABB'],
        'UpperAbb': ScoreCI_df['UABB'],
        'ZWI': ScoreCI_df['ZWI']
    })

    ss1['ID'] = range(1, len(ss1) + 1)

    ll = ss1[ss1['LowerAbb'] == "YES"]
    ul = ss1[ss1['UpperAbb'] == "YES"]
    zl = ss1[ss1['ZWI'] == "YES"]

    ldf = pd.DataFrame()  # Initialize an empty DataFrame for the lower, upper, and ZWI points

    if not ll.empty:
        ll = ll[['ID', 'LowerLimit']].copy()
        ll['Abberation'] = "Lower"
        ll.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, ll], ignore_index=True)

    if not ul.empty:
        ul = ul[['ID', 'UpperLimit']].copy()
        ul['Abberation'] = "Upper"
        ul.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, ul], ignore_index=True)

    if not zl.empty:
        zl = zl[['ID', 'LowerLimit']].copy()
        zl['Abberation'] = "ZWI"
        zl.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, zl], ignore_index=True)

    p = (ggplot(ss1, aes(x='UpperLimit', y='ID')) +
         labs(x="Lower and Upper limits", y="ID", title="Confidence Interval - Score method") +
         geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5))

    if not ldf.empty:
        p += geom_point(data=ldf,
                        mapping=aes(x='Value', y='ID', group='Abberation', shape='Abberation'),
                        size=4, fill="red") + scale_shape_manual(values=[21, 22, 23])

    p.show()

# Example usage (assuming ciSC is defined)
# PlotciSC(5, 0.05)
import pandas as pd
from plotnine import ggplot, aes, labs, geom_errorbarh, geom_point, scale_shape_manual, scale_color_manual

def plotcitw(n, alp):
    if n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if alp < 0 or alp > 1:
        raise ValueError("'alpha' has to be between 0 and 1")

    # Assume ciTW is defined elsewhere and returns a DataFrame-like object
    WaldTCI_df = citw(n, alp)  # ciTW should return a DataFrame with the necessary columns
    ss1 = pd.DataFrame({
        'x': WaldTCI_df['x'],
        'LowerLimit': WaldTCI_df['LTW'],
        'UpperLimit': WaldTCI_df['UTW'],
        'LowerAbb': WaldTCI_df['LABB'],
        'UpperAbb': WaldTCI_df['UABB'],
        'ZWI': WaldTCI_df['ZWI']
    })

    ss1['ID'] = range(1, len(ss1) + 1)

    ll = ss1[ss1['LowerAbb'] == "YES"]
    ul = ss1[ss1['UpperAbb'] == "YES"]
    zl = ss1[ss1['ZWI'] == "YES"]

    ldf = pd.DataFrame()  # Initialize an empty DataFrame for the lower, upper, and ZWI points

    if not ll.empty:
        ll = ll[['ID', 'LowerLimit']].copy()
        ll['Abberation'] = "Lower"
        ll.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, ll], ignore_index=True)

    if not ul.empty:
        ul = ul[['ID', 'UpperLimit']].copy()
        ul['Abberation'] = "Upper"
        ul.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, ul], ignore_index=True)

    if not zl.empty:
        zl = zl[['ID', 'LowerLimit']].copy()
        zl['Abberation'] = "ZWI"
        zl.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, zl], ignore_index=True)

    p = (ggplot(ss1, aes(x='UpperLimit', y='ID')) +
         labs(x="Lower and Upper limits", y="ID", title="Confidence Interval - Wald-T method") +
         geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5))

    if not ldf.empty:
        p += (geom_point(data=ldf,
                         mapping=aes(x='Value', y='ID', shape='Abberation', color='Abberation'),
                         size=4))# +
              #scale_shape_manual(values=[21, 22, 23]) +
              #scale_color_manual(values=['red', 'blue', 'green']))  # Specify colors for each shape

    p.show() # Use print to display the plot


# Example usage (assuming ciTW is defined)
# PlotciTW(5, 0.05)
def plotcilt(n, alp):
    if n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if alp < 0 or alp > 1:
        raise ValueError("'alpha' has to be between 0 and 1")

    # Assume ciLT is defined elsewhere and returns a DataFrame-like object
    LogitWald_df = cilt(n, alp)  # ciLT should return a DataFrame with the necessary columns
    ss1 = pd.DataFrame({
        'x': LogitWald_df['x'],
        'LowerLimit': LogitWald_df['LLT'],
        'UpperLimit': LogitWald_df['ULT'],
        'LowerAbb': LogitWald_df['LABB'],
        'UpperAbb': LogitWald_df['UABB'],
        'ZWI': LogitWald_df['ZWI']
    })

    ss1['ID'] = range(1, len(ss1) + 1)

    ll = ss1[ss1['LowerAbb'] == "YES"]
    ul = ss1[ss1['UpperAbb'] == "YES"]
    zl = ss1[ss1['ZWI'] == "YES"]

    ldf = pd.DataFrame()  # Initialize an empty DataFrame for the lower, upper, and ZWI points

    if not ll.empty:
        ll = ll[['ID', 'LowerLimit']].copy()
        ll['Abberation'] = "Lower"
        ll.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, ll], ignore_index=True)

    if not ul.empty:
        ul = ul[['ID', 'UpperLimit']].copy()
        ul['Abberation'] = "Upper"
        ul.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, ul], ignore_index=True)

    if not zl.empty:
        zl = zl[['ID', 'LowerLimit']].copy()
        zl['Abberation'] = "ZWI"
        zl.columns = ['ID', 'Value', 'Abberation']
        ldf = pd.concat([ldf, zl], ignore_index=True)

    p = (ggplot(ss1, aes(x='UpperLimit', y='ID')) +
         labs(x="Lower and Upper limits", y="ID", title="Confidence Interval - Logit Wald method") +
         geom_errorbarh(aes(xmin='LowerLimit', xmax='UpperLimit'), size=0.5))

    if not ldf.empty:
        p += geom_point(data=ldf,
                        mapping=aes(x='Value', y='ID', group='Abberation', shape='Abberation'),
                        size=4, fill="red") + scale_shape_manual(values=[21, 22, 23])

    p.show()


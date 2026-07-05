import pandas as pd
import numpy as np
import scipy.stats as stats
import scipy.optimize as optimize

def ciawdx(x, n, alp, h):
    # Input validation
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if h is None:
        raise ValueError("'h' is missing")
    if not isinstance(x, (int, float)) or x < 0 or x > n or len([x]) > 1:
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if not isinstance(n, (int, float)) or n <= 0 or len([n]) > 1:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0 or len([alp]) > 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(h, (int, float)) or h < 0 or len([h]) > 1:
        raise ValueError("'h' has to be greater than or equal to 0")

    # Calculate critical values
    cv = stats.norm.ppf(1 - (alp / 2), loc=0, scale=1)

    # Calculate Wald method
    y = x + h
    m = n + (2 * h)
    pAW = y / m
    qAW = 1 - pAW
    seAW = np.sqrt(pAW * qAW / m)
    LAWDx = pAW - (cv * seAW)
    UAWDx = pAW + (cv * seAW)

    # Check for aberrations
    if LAWDx < 0:
        LABB = "YES"
        LAWDx = 0
    else:
        LABB = "NO"

    if UAWDx > 1:
        UABB = "YES"
        UAWDx = 1
    else:
        UABB = "NO"

    # Check for zero-width interval
    if UAWDx - LAWDx == 0:
        ZWI = "YES"
    else:
        ZWI = "NO"

    return pd.DataFrame({
        'x': [x],
        'LAWDx': [LAWDx],
        'UAWDx': [UAWDx],
        'LABB': [LABB],
        'UABB': [UABB],
        'ZWI': [ZWI]
    })

def ciascx(x, n, alp, h):
    # Input validation
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if h is None:
        raise ValueError("'h' is missing")
    if not isinstance(x, (int, float)) or x < 0 or x > n or len([x]) > 1:
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if not isinstance(n, (int, float)) or n <= 0 or len([n]) > 1:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0 or len([alp]) > 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(h, (int, float)) or h < 0 or len([h]) > 1:
        raise ValueError("'h' has to be greater than or equal to 0")

    # Calculate critical values
    cv = stats.norm.ppf(1 - (alp / 2), loc=0, scale=1)

    # Calculate score method
    y = x + h
    m = n + (2 * h)
    cv1 = (cv ** 2) / (2 * m)
    cv2 = (cv / (2 * m)) ** 2
    pAS = y / m
    qAS = 1 - pAS
    seAS = np.sqrt((pAS * qAS / m) + cv2)
    LASCx = (m / (m + (cv ** 2))) * ((pAS + cv1) - (cv * seAS))
    UASCx = (m / (m + (cv ** 2))) * ((pAS + cv1) + (cv * seAS))

    # Check for aberrations
    if LASCx < 0:
        LABB = "YES"
        LASCx = 0
    else:
        LABB = "NO"

    if UASCx > 1:
        UABB = "YES"
        UASCx = 1
    else:
        UABB = "NO"

    # Check for zero-width interval
    if UASCx - LASCx == 0:
        ZWI = "YES"
    else:
        ZWI = "NO"

    return pd.DataFrame({
        'x': [x],
        'LASCx': [LASCx],
        'UASCx': [UASCx],
        'LABB': [LABB],
        'UABB': [UABB],
        'ZWI': [ZWI]
    })



def ciaasx(x, n, alp, h):
    # Input validation
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if h is None:
        raise ValueError("'h' is missing")
    if not isinstance(x, (int, float)) or x < 0 or x > n or len([x]) > 1:
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if not isinstance(n, (int, float)) or n <= 0 or len([n]) > 1:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0 or len([alp]) > 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(h, (int, float)) or h < 0 or len([h]) > 1:
        raise ValueError("'h' has to be greater than or equal to 0")

    # Calculate critical values
    cv = stats.norm.ppf(1 - (alp / 2), loc=0, scale=1)

    # Calculate arc-sine method
    y = x + h
    m = n + (2 * h)
    pA = y / m
    seA = cv / np.sqrt(4 * m)
    LAASx = (np.sin(np.arcsin(np.sqrt(pA)) - seA)) ** 2
    UAASx = (np.sin(np.arcsin(np.sqrt(pA)) + seA)) ** 2

    # Check for aberrations
    if LAASx < 0:
        LABB = "YES"
        LAASx = 0
    else:
        LABB = "NO"

    if UAASx > 1:
        UABB = "YES"
        UAASx = 1
    else:
        UABB = "NO"

    # Check for zero-width interval
    if UAASx - LAASx == 0:
        ZWI = "YES"
    else:
        ZWI = "NO"

    return pd.DataFrame({
        'x': [x],
        'LAASx': [LAASx],
        'UAASx': [UAASx],
        'LABB': [LABB],
        'UABB': [UABB],
        'ZWI': [ZWI]
    })
















def cialrx(x, n, alp, h):
    # Input validation
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if h is None:
        raise ValueError("'h' is missing")
    if not isinstance(x, (int, float)) or x < 0 or x > n or len([x]) > 1:
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if not isinstance(n, (int, float)) or n <= 0 or len([n]) > 1:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0 or len([alp]) > 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(h, int) or h < 0 or len([h]) > 1:
        raise ValueError("'h' has to be an integer greater than or equal to 0")

    # Calculate critical values
    cv = stats.norm.ppf(1 - (alp / 2), loc=0, scale=1)

    # Calculate likelihood-ratio method
    y = x
    y1 = y + h
    n1 = n + (2 * h)

    def loglik(p):
        return stats.binom.logpmf(y1, n1, p)

    def likelhd(p):
        return -loglik(p)

    mle = optimize.minimize_scalar(likelhd, bounds=(0, 1), method='bounded').x

    cutoff = loglik(mle) - (cv ** 2 / 2)

    def loglik_optim(p):
        return abs(cutoff - loglik(p))

    LALRx = optimize.minimize_scalar(loglik_optim, bounds=(0, mle), method='bounded').x
    UALRx = optimize.minimize_scalar(loglik_optim, bounds=(mle, 1), method='bounded').x

    # Check for aberrations
    if LALRx < 0:
        LABB = "YES"
        LALRx = 0
    else:
        LABB = "NO"

    if UALRx > 1:
        UABB = "YES"
        UALRx = 1
    else:
        UABB = "NO"

    # Check for zero-width interval
    if UALRx - LALRx == 0:
        ZWI = "YES"
    else:
        ZWI = "NO"

    return pd.DataFrame({
        'x': [x],
        'LALRx': [LALRx],
        'UALRx': [UALRx],
        'LABB': [LABB],
        'UABB': [UABB],
        'ZWI': [ZWI]
    })












def ciatwx(x, n, alp, h):
    # Input validation
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if h is None:
        raise ValueError("'h' is missing")
    if not isinstance(x, (int, float)) or x < 0 or x > n or len([x]) > 1:
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if not isinstance(n, (int, float)) or n <= 0 or len([n]) > 1:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0 or len([alp]) > 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(h, (int, float)) or h < 0 or len([h]) > 1:
        raise ValueError("'h' has to be greater than or equal to 0")

    # Calculate modified t-adj Wald method
    y = x + h
    n1 = n + (2 * h)
    pATWx = y / n1

    def f1(p, n):
        return p * (1 - p) / n

    def f2(p, n):
        return (p * (1 - p) / (n ** 3)) + ((p + ((6 * n) - 7) * (p ** 2)) + (4 * (n - 1) * (n - 3) * (p ** 3)) - (2 * (n - 1) * ((2 * n) - 3) * (p ** 4))) / (n ** 5) - (2 * (p + ((2 * n) - 3) * (p ** 2) - 2 * (n - 1) * (p ** 3))) / (n ** 4)

    DOFx = 2 * ((f1(pATWx, n1)) ** 2) / f2(pATWx, n1)
    cvx = stats.t.ppf(1 - (alp / 2), df=DOFx)
    seATWx = cvx * np.sqrt(f1(pATWx, n1))
    LATWx = pATWx - (seATWx)
    UATWx = pATWx + (seATWx)

    # Check for aberrations
    if LATWx < 0:
        LABB = "YES"
        LATWx = 0
    else:
        LABB = "NO"

    if UATWx > 1:
        UABB = "YES"
        UATWx = 1
    else:
        UABB = "NO"

    # Check for zero-width interval
    if UATWx - LATWx == 0:
        ZWI = "YES"
    else:
        ZWI = "NO"

    return pd.DataFrame({
        'x': [x],
        'LATWx': [LATWx],
        'UATWx': [UATWx],
        'LABB': [LABB],
        'UABB': [UABB],
        'ZWI': [ZWI]
    })

def cialtx(x, n, alp, h):
    # Input validation
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if h is None:
        raise ValueError("'h' is missing")
    if not isinstance(x, (int, float)) or x < 0 or x > n or len([x]) > 1:
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if not isinstance(n, (int, float)) or n <= 0 or len([n]) > 1:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0 or len([alp]) > 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(h, (int, float)) or h < 0 or len([h]) > 1:
        raise ValueError("'h' has to be greater than or equal to 0")

    # Calculate critical values
    cv = stats.norm.ppf(1 - (alp / 2), loc=0, scale=1)

    # Calculate logit-Wald method
    y = x + h
    n1 = n + (2 * h)
    pALTx = y / n1
    qALTx = 1 - pALTx
    lgitx = np.log(pALTx / qALTx)
    seALTx = np.sqrt(pALTx * qALTx / n1)
    LALTx = 1 / (1 + np.exp(-lgitx + (cv / seALTx)))
    UALTx = 1 / (1 + np.exp(-lgitx - (cv / seALTx)))

    # Check for aberrations
    if LALTx < 0:
        LABB = "YES"
        LALTx = 0
    else:
        LABB = "NO"

    if UALTx > 1:
        UABB = "YES"
        UALTx = 1
    else:
        UABB = "NO"

    # Check for zero-width interval
    if UALTx - LALTx == 0:
        ZWI = "YES"
    else:
        ZWI = "NO"

    return pd.DataFrame({
        'x': [x],
        'LALTx': [LALTx],
        'UALTx': [UALTx],
        'LABB': [LABB],
        'UABB': [UABB],
        'ZWI': [ZWI]
    })

def ciaallx(x, n, alp, h):
    # Error handling
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if h is None:
        raise ValueError("'h' is missing")

    if not isinstance(x, (int, float)) or x < 0 or x > n:
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not isinstance(alp, (int, float)) or alp <= 0 or alp >= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(h, (int, float)) or h < 0 or not (h % 1 == 0):
        raise ValueError("'h' has to be a non-negative integer")

    # Placeholder calls to different CI functions
    WaldCI_df = ciawdx(x, n, alp, h)
    ArcSineCI_df = ciaasx(x, n, alp, h)
    LRCI_df = cialrx(x, n, alp, h)
    ScoreCI_df = ciascx(x, n, alp, h)
    WaldLCI_df = cialtx(x, n, alp, h)
    AdWaldCI_df = ciatwx(x, n, alp, h)

    # Assign methods to each DataFrame
    WaldCI_df['method'] = "Adj-Wald"
    ArcSineCI_df['method'] = "Adj-ArcSine"
    LRCI_df['method'] = "Adj-Likelihood"
    WaldLCI_df['method'] = "Adj-Logit Wald"
    ScoreCI_df['method'] = "Adj-Score"
    AdWaldCI_df['method'] = "Adj-Wald-T"

    # Generic DataFrames to store the common structure
    Generic_1 = pd.DataFrame({
        'method': WaldCI_df['method'],
        'x': WaldCI_df['x'],
        'LowerLimit': WaldCI_df['LAWDx'],
        'UpperLimit': WaldCI_df['UAWDx'],
        'LowerAbb': WaldCI_df['LABB'],
        'UpperAbb': WaldCI_df['UABB'],
        'ZWI': WaldCI_df['ZWI']
    })

    Generic_2 = pd.DataFrame({
        'method': ArcSineCI_df['method'],
        'x': ArcSineCI_df['x'],
        'LowerLimit': ArcSineCI_df['LAASx'],
        'UpperLimit': ArcSineCI_df['UAASx'],
        'LowerAbb': ArcSineCI_df['LABB'],
        'UpperAbb': ArcSineCI_df['UABB'],
        'ZWI': ArcSineCI_df['ZWI']
    })

    Generic_3 = pd.DataFrame({
        'method': LRCI_df['method'],
        'x': LRCI_df['x'],
        'LowerLimit': LRCI_df['LALRx'],
        'UpperLimit': LRCI_df['UALRx'],
        'LowerAbb': LRCI_df['LABB'],
        'UpperAbb': LRCI_df['UABB'],
        'ZWI': LRCI_df['ZWI']
    })

    Generic_4 = pd.DataFrame({
        'method': ScoreCI_df['method'],
        'x': ScoreCI_df['x'],
        'LowerLimit': ScoreCI_df['LASCx'],
        'UpperLimit': ScoreCI_df['UASCx'],
        'LowerAbb': ScoreCI_df['LABB'],
        'UpperAbb': ScoreCI_df['UABB'],
        'ZWI': ScoreCI_df['ZWI']
    })

    Generic_5 = pd.DataFrame({
        'method': WaldLCI_df['method'],
        'x': WaldLCI_df['x'],
        'LowerLimit': WaldLCI_df['LALTx'],
        'UpperLimit': WaldLCI_df['UALTx'],
        'LowerAbb': WaldLCI_df['LABB'],
        'UpperAbb': WaldLCI_df['UABB'],
        'ZWI': WaldLCI_df['ZWI']
    })

    Generic_6 = pd.DataFrame({
        'method': AdWaldCI_df['method'],
        'x': AdWaldCI_df['x'],
        'LowerLimit': AdWaldCI_df['LATWx'],
        'UpperLimit': AdWaldCI_df['UATWx'],
        'LowerAbb': AdWaldCI_df['LABB'],
        'UpperAbb': AdWaldCI_df['UABB'],
        'ZWI': AdWaldCI_df['ZWI']
    })
    Final_df = pd.concat([Generic_1, Generic_2, Generic_3, Generic_4, Generic_5, Generic_6])

    return Final_df
#SJTP
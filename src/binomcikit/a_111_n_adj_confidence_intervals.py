import numpy as np
import pandas as pd
import scipy.stats as stats
import scipy.optimize as optimize

def ciawd(n, alp, h):
    # Input validation
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if h is None:
        raise ValueError("'h' is missing")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not isinstance(h, (int, float)) or h < 0:
        raise ValueError("'h' has to be greater than or equal to 0")

    # Input n
    x = np.arange(n + 1)
    k = n + 1
    y = x + h
    n1 = n + (2 * h)

    # Initializations
    pAW = np.zeros(k)
    qAW = np.zeros(k)
    seAW = np.zeros(k)
    LAWD = np.zeros(k)
    UAWD = np.zeros(k)
    LABB = np.empty(k, dtype=object)
    UABB = np.empty(k, dtype=object)
    ZWI = np.empty(k, dtype=object)

    # Critical values
    cv = stats.norm.ppf(1 - (alp / 2))

    # WALD METHOD
    for i in range(k):
        pAW[i] = y[i] / n1
        qAW[i] = 1 - pAW[i]
        seAW[i] = np.sqrt(pAW[i] * qAW[i] / n1)
        LAWD[i] = pAW[i] - (cv * seAW[i])
        UAWD[i] = pAW[i] + (cv * seAW[i])
        
        LABB[i] = "YES" if LAWD[i] < 0 else "NO"
        LAWD[i] = max(0, LAWD[i])
        
        UABB[i] = "YES" if UAWD[i] > 1 else "NO"
        UAWD[i] = min(1, UAWD[i])
        
        ZWI[i] = "YES" if UAWD[i] - LAWD[i] == 0 else "NO"

    return pd.DataFrame({
        'x': x,
        'LAWD': LAWD,
        'UAWD': UAWD,
        'LABB': LABB,
        'UABB': UABB,
        'ZWI': ZWI
    })




def ciasc(n, alp, h):
    # Input validation
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if h is None:
        raise ValueError("'h' is missing")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not isinstance(h, (int, float)) or h < 0:
        raise ValueError("'h' has to be greater than or equal to 0")

    # Input n
    x = np.arange(n + 1)
    k = n + 1
    y = x + h
    n1 = n + (2 * h)

    # Initializations
    pAS = np.zeros(k)
    qAS = np.zeros(k)
    seAS = np.zeros(k)
    LASC = np.zeros(k)
    UASC = np.zeros(k)
    LABB = np.empty(k, dtype=object)
    UABB = np.empty(k, dtype=object)
    ZWI = np.empty(k, dtype=object)

    # Critical values
    cv = stats.norm.ppf(1 - (alp / 2))
    cv1 = (cv ** 2) / (2 * n1)
    cv2 = (cv / (2 * n1)) ** 2

    # ASCORE (WILSON) METHOD
    for i in range(k):
        pAS[i] = y[i] / n1
        qAS[i] = 1 - pAS[i]
        seAS[i] = np.sqrt((pAS[i] * qAS[i] / n1) + cv2)
        LASC[i] = (n1 / (n1 + cv ** 2)) * ((pAS[i] + cv1) - (cv * seAS[i]))
        UASC[i] = (n1 / (n1 + cv ** 2)) * ((pAS[i] + cv1) + (cv * seAS[i]))
        
        LABB[i] = "YES" if LASC[i] < 0 else "NO"
        LASC[i] = max(0, LASC[i])
        
        UABB[i] = "YES" if UASC[i] > 1 else "NO"
        UASC[i] = min(1, UASC[i])
        
        ZWI[i] = "YES" if UASC[i] - LASC[i] == 0 else "NO"

    return pd.DataFrame({
        'x': x,
        'LASC': LASC,
        'UASC': UASC,
        'LABB': LABB,
        'UABB': UABB,
        'ZWI': ZWI
    })


def ciaas(n, alp, h):
    # Input validation
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if h is None:
        raise ValueError("'h' is missing")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not isinstance(h, (int, float)) or h < 0:
        raise ValueError("'h' has to be greater than or equal to 0")

    # Input
    x = np.arange(n + 1)
    k = n + 1
    y = x + h
    m = n + (2 * h)

    # Initializations
    pA = np.zeros(k)
    qA = np.zeros(k)
    seA = np.zeros(k)
    LAAS = np.zeros(k)
    UAAS = np.zeros(k)
    LABB = np.empty(k, dtype=object)
    UABB = np.empty(k, dtype=object)
    ZWI = np.empty(k, dtype=object)

    cv = stats.norm.ppf(1 - (alp / 2))

    # ARC-SINE METHOD
    for i in range(k):
        pA[i] = y[i] / m
        qA[i] = 1 - pA[i]
        seA[i] = cv / np.sqrt(4 * m)
        LAAS[i] = (np.sin(np.arcsin(np.sqrt(pA[i])) - seA[i])) ** 2
        UAAS[i] = (np.sin(np.arcsin(np.sqrt(pA[i])) + seA[i])) ** 2
        
        LABB[i] = "YES" if LAAS[i] < 0 else "NO"
        LAAS[i] = max(0, LAAS[i])
        
        UABB[i] = "YES" if UAAS[i] > 1 else "NO"
        UAAS[i] = min(1, UAAS[i])
        
        ZWI[i] = "YES" if UAAS[i] - LAAS[i] == 0 else "NO"

    return pd.DataFrame({
        'x': x,
        'LAAS': LAAS,
        'UAAS': UAAS,
        'LABB': LABB,
        'UABB': UABB,
        'ZWI': ZWI
    })




def cialr(n, alp, h):
    # Input validation
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if h is None:
        raise ValueError("'h' is missing")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not isinstance(h, int) or h < 0:
        raise ValueError("'h' has to be an integer greater than or equal to 0")

    # Input n
    x = np.arange(n + 1)
    y1 = x + h
    k = n + 1
    n1 = n + (2 * h)

    # Initializations
    mle = np.zeros(k)
    cutoff = np.zeros(k)
    LALR = np.zeros(k)
    UALR = np.zeros(k)
    LABB = np.empty(k, dtype=object)
    UABB = np.empty(k, dtype=object)
    ZWI = np.empty(k, dtype=object)

    # Critical values
    cv = stats.norm.ppf(1 - (alp / 2))

    def likelhd(p, i):
        return stats.binom.pmf(y1[i], n1, p)

    def loglik(p, i):
        return stats.binom.logpmf(y1[i], n1, p)
    
    def loglik_optim(p, i):
        return abs(cutoff[i] - loglik(p, i))

    # LIKELIHOOD-RATIO METHOD
    for i in range(k):
        # Find MLE
        mle[i] = optimize.minimize_scalar(lambda p: -likelhd(p, i), bounds=(0, 1), method='bounded').x
        
        cutoff[i] = loglik(mle[i], i) - (cv**2 / 2)

        # Find LALR and UALR
        LALR[i] = optimize.minimize_scalar(lambda p: loglik_optim(p, i), bounds=(0, mle[i]), method='bounded').x
        UALR[i] = optimize.minimize_scalar(lambda p: loglik_optim(p, i), bounds=(mle[i], 1), method='bounded').x

        LABB[i] = "YES" if LALR[i] < 0 else "NO"
        UABB[i] = "YES" if UALR[i] > 1 else "NO"
        ZWI[i] = "YES" if UALR[i] - LALR[i] == 0 else "NO"

    return pd.DataFrame({
        'x': x,
        'LALR': LALR,
        'UALR': UALR,
        'LABB': LABB,
        'UABB': UABB,
        'ZWI': ZWI
    })




def ciatw(n, alp, h):
    # Input validation
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if h is None:
        raise ValueError("'h' is missing")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not isinstance(h, (int, float)) or h < 0:
        raise ValueError("'h' has to be greater than or equal to 0")

    # Input n
    x = np.arange(n + 1)
    k = n + 1
    y = x + h
    n1 = n + (2 * h)

    # Initializations
    pATW = np.zeros(k)
    qATW = np.zeros(k)
    seATW = np.zeros(k)
    LATW = np.zeros(k)
    UATW = np.zeros(k)
    DOF = np.zeros(k)
    cv = np.zeros(k)
    LABB = np.empty(k, dtype=object)
    UABB = np.empty(k, dtype=object)
    ZWI = np.empty(k, dtype=object)

    def f1(p, n):
        return p * (1 - p) / n

    def f2(p, n):
        return (p * (1 - p) / (n ** 3)) + (p + ((6 * n) - 7) * (p ** 2) + (4 * (n - 1) * (n - 3) * (p ** 3)) - (2 * (n - 1) * ((2 * n) - 3) * (p ** 4))) / (n ** 5) - (2 * (p + ((2 * n) - 3) * (p ** 2) - 2 * (n - 1) * (p ** 3))) / (n ** 4)

    # MODIFIED_t-ADJ_WALD METHOD
    for i in range(k):
        pATW[i] = y[i] / n1
        qATW[i] = 1 - pATW[i]
        DOF[i] = 2 * ((f1(pATW[i], n1)) ** 2) / f2(pATW[i], n1)
        cv[i] = stats.t.ppf(1 - (alp / 2), df=DOF[i])
        seATW[i] = cv[i] * np.sqrt(f1(pATW[i], n1))
        LATW[i] = pATW[i] - seATW[i]
        UATW[i] = pATW[i] + seATW[i]

        LABB[i] = "YES" if LATW[i] < 0 else "NO"
        LATW[i] = max(0, LATW[i])

        UABB[i] = "YES" if UATW[i] > 1 else "NO"
        UATW[i] = min(1, UATW[i])

        ZWI[i] = "YES" if UATW[i] - LATW[i] == 0 else "NO"

    return pd.DataFrame({
        'x': x,
        'LATW': LATW,
        'UATW': UATW,
        'LABB': LABB,
        'UABB': UABB,
        'ZWI': ZWI
    })



def cialt(n, alp, h):
    # Input validation
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if h is None:
        raise ValueError("'h' is missing")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not isinstance(h, (int, float)) or h < 0:
        raise ValueError("'h' has to be greater than or equal to 0")

    # Input n
    x = np.arange(n + 1)
    k = n + 1
    y = x + h
    n1 = n + (2 * h)

    # Initializations
    pALT = np.zeros(k)
    qALT = np.zeros(k)
    seALT = np.zeros(k)
    lgit = np.zeros(k)
    LALT = np.zeros(k)
    UALT = np.zeros(k)
    LABB = np.empty(k, dtype=object)
    UABB = np.empty(k, dtype=object)
    ZWI = np.empty(k, dtype=object)

    # Critical values
    cv = stats.norm.ppf(1 - (alp / 2))

    # LOGIT-WALD METHOD
    for i in range(k):
        pALT[i] = y[i] / n1
        qALT[i] = 1 - pALT[i]
        lgit[i] = np.log(pALT[i] / qALT[i])
        seALT[i] = np.sqrt(pALT[i] * qALT[i] * n1)
        LALT[i] = 1 / (1 + np.exp(-lgit[i] + (cv / seALT[i])))
        UALT[i] = 1 / (1 + np.exp(-lgit[i] - (cv / seALT[i])))

        LABB[i] = "YES" if LALT[i] < 0 else "NO"
        LALT[i] = max(0, LALT[i])

        UABB[i] = "YES" if UALT[i] > 1 else "NO"
        UALT[i] = min(1, UALT[i])

        ZWI[i] = "YES" if UALT[i] - LALT[i] == 0 else "NO"

    return pd.DataFrame({
        'x': x,
        'LALT': LALT,
        'UALT': UALT,
        'LABB': LABB,
        'UABB': UABB,
        'ZWI': ZWI
    })





def ciaall(n, alp, h):
    # Input validation
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if h is None:
        raise ValueError("'h' is missing")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not isinstance(h, int) or h < 0:
        raise ValueError("'h' has to be an integer greater than or equal to 0")

    # Calling functions and creating dataframes
    WaldCI_df = ciawd(n, alp, h)
    ArcSineCI_df = ciaas(n, alp, h)
    LRCI_df = cialr(n, alp, round(h))
    ScoreCI_df = ciasc(n, alp, h)
    WaldLCI_df = cialt(n, alp, h)
    AdWaldCI_df = ciatw(n, alp, h)

    # Adding method column to each dataframe
    WaldCI_df['method'] = "Adj-Wald"
    ArcSineCI_df['method'] = "Adj-ArcSine"
    LRCI_df['method'] = "Adj-Likelihood"
    WaldLCI_df['method'] = "Adj-Logit-Wald"
    ScoreCI_df['method'] = "Adj-Score"
    AdWaldCI_df['method'] = "Adj-Wald-T"

    # Creating generic dataframes
    Generic_1 = pd.DataFrame({
        'method': WaldCI_df['method'],
        'x': WaldCI_df['x'],
        'LowerLimit': WaldCI_df['LAWD'],
        'UpperLimit': WaldCI_df['UAWD'],
        'LowerAbb': WaldCI_df['LABB'],
        'UpperAbb': WaldCI_df['UABB'],
        'ZWI': WaldCI_df['ZWI']
    })

    Generic_2 = pd.DataFrame({
        'method': ArcSineCI_df['method'],
        'x': ArcSineCI_df['x'],
        'LowerLimit': ArcSineCI_df['LAAS'],
        'UpperLimit': ArcSineCI_df['UAAS'],
        'LowerAbb': ArcSineCI_df['LABB'],
        'UpperAbb': ArcSineCI_df['UABB'],
        'ZWI': ArcSineCI_df['ZWI']
    })

    Generic_3 = pd.DataFrame({
        'method': LRCI_df['method'],
        'x': LRCI_df['x'],
        'LowerLimit': LRCI_df['LALR'],
        'UpperLimit': LRCI_df['UALR'],
        'LowerAbb': LRCI_df['LABB'],
        'UpperAbb': LRCI_df['UABB'],
        'ZWI': LRCI_df['ZWI']
    })

    Generic_4 = pd.DataFrame({
        'method': ScoreCI_df['method'],
        'x': ScoreCI_df['x'],
        'LowerLimit': ScoreCI_df['LASC'],
        'UpperLimit': ScoreCI_df['UASC'],
        'LowerAbb': ScoreCI_df['LABB'],
        'UpperAbb': ScoreCI_df['UABB'],
        'ZWI': ScoreCI_df['ZWI']
    })

    Generic_5 = pd.DataFrame({
        'method': WaldLCI_df['method'],
        'x': WaldLCI_df['x'],
        'LowerLimit': WaldLCI_df['LALT'],
        'UpperLimit': WaldLCI_df['UALT'],
        'LowerAbb': WaldLCI_df['LABB'],
        'UpperAbb': WaldLCI_df['UABB'],
        'ZWI': WaldLCI_df['ZWI']
    })

    Generic_6 = pd.DataFrame({
        'method': AdWaldCI_df['method'],
        'x': AdWaldCI_df['x'],
        'LowerLimit': AdWaldCI_df['LATW'],
        'UpperLimit': AdWaldCI_df['UATW'],
        'LowerAbb': AdWaldCI_df['LABB'],
        'UpperAbb': AdWaldCI_df['UABB'],
        'ZWI': AdWaldCI_df['ZWI']
    })

    # Combining generic dataframes
    Final_df = pd.concat([Generic_1, Generic_2, Generic_3, Generic_4, Generic_5, Generic_6], ignore_index=True)

    return Final_df

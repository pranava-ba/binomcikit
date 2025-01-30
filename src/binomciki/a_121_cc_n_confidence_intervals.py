import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.stats import t


def cicwd(n, alp, c):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if c is None:
        raise ValueError("'c' is missing")
    
    if alp > 1 or alp < 0 or not isinstance(alp, (float, int)):
        raise ValueError("'alpha' has to be between 0 and 1")
    
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    
    if not isinstance(c, (int, float)) or c < 0:
        raise ValueError("'c' has to be positive")

    # Input n
    x = np.arange(0, n + 1)
    k = n + 1

    # Initializations
    pCW = np.zeros(k)
    qCW = np.zeros(k)
    seCW = np.zeros(k)
    LCW = np.zeros(k)
    UCW = np.zeros(k)
    LABB = np.empty(k, dtype=object)
    UABB = np.empty(k, dtype=object)
    ZWI = np.empty(k, dtype=object)

    # Critical values
    cv = norm.ppf(1 - (alp / 2))

    # Wald Method
    for i in range(k):
        pCW[i] = x[i] / n
        qCW[i] = 1 - pCW[i]
        seCW[i] = np.sqrt(pCW[i] * qCW[i] / n)
        LCW[i] = pCW[i] - ((cv * seCW[i]) + c)
        UCW[i] = pCW[i] + ((cv * seCW[i]) + c)

        if LCW[i] < 0:
            LABB[i] = "YES"
            LCW[i] = 0
        else:
            LABB[i] = "NO"

        if UCW[i] > 1:
            UABB[i] = "YES"
            UCW[i] = 1
        else:
            UABB[i] = "NO"

        if UCW[i] - LCW[i] == 0:
            ZWI[i] = "YES"
        else:
            ZWI[i] = "NO"

    return pd.DataFrame({
        'x': x,
        'LCW': LCW,
        'UCW': UCW,
        'LABB': LABB,
        'UABB': UABB,
        'ZWI': ZWI
    })

def cicsc(n, alp, c):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if c is None:
        raise ValueError("'c' is missing")
    
    if alp > 1 or alp < 0 or not isinstance(alp, (float, int)):
        raise ValueError("'alpha' has to be between 0 and 1")
    
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    
    if c <= 0 or c > (1 / (2 * n)):
        raise ValueError("'c' has to be positive and less than or equal to 1/(2*n)")

    # Input n
    x = np.arange(0, n + 1)
    k = n + 1

    # Initializations
    pCS = np.zeros(k)
    qCS = np.zeros(k)
    seCS_L = np.zeros(k)
    seCS_U = np.zeros(k)
    LCS = np.zeros(k)
    UCS = np.zeros(k)
    LABB = np.empty(k, dtype=object)
    UABB = np.empty(k, dtype=object)
    ZWI = np.empty(k, dtype=object)

    # Critical values
    cv = norm.ppf(1 - (alp / 2))
    cv1 = (cv**2) / (2 * n)
    cv2 = cv / (2 * n)

    # Score (Wilson) Method
    for i in range(k):
        pCS[i] = x[i] / n
        qCS[i] = 1 - pCS[i]
        seCS_L[i] = np.sqrt((cv**2) - (4 * n * (c + c**2)) + (4 * n * pCS[i] * (1 - pCS[i] + (2 * c))))
        seCS_U[i] = np.sqrt((cv**2) + (4 * n * (c - c**2)) + (4 * n * pCS[i] * (1 - pCS[i] - (2 * c))))
        LCS[i] = (n / (n + (cv**2))) * ((pCS[i] - c + cv1) - (cv2 * seCS_L[i]))
        UCS[i] = (n / (n + (cv**2))) * ((pCS[i] + c + cv1) + (cv2 * seCS_U[i]))

        if LCS[i] < 0:
            LABB[i] = "YES"
            LCS[i] = 0
        else:
            LABB[i] = "NO"

        if UCS[i] > 1:
            UABB[i] = "YES"
            UCS[i] = 1
        else:
            UABB[i] = "NO"

        if UCS[i] - LCS[i] == 0:
            ZWI[i] = "YES"
        else:
            ZWI[i] = "NO"

    return pd.DataFrame({
        'x': x,
        'LCS': LCS,
        'UCS': UCS,
        'LABB': LABB,
        'UABB': UABB,
        'ZWI': ZWI
    })
def cicas(n, alp, c):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if c is None:
        raise ValueError("'c' is missing")
    
    if alp > 1 or alp < 0 or not isinstance(alp, (float, int)):
        raise ValueError("'alpha' has to be between 0 and 1")
    
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    
    if not isinstance(c, (int, float)) or c < 0:
        raise ValueError("'c' has to be positive")

    # Input n
    x = np.arange(0, n + 1)
    k = n + 1

    # Initializations
    pCA = np.zeros(k)
    qCA = np.zeros(k)
    seCA = np.zeros(k)
    LCA = np.zeros(k)
    UCA = np.zeros(k)
    LABB = np.empty(k, dtype=object)
    UABB = np.empty(k, dtype=object)
    ZWI = np.empty(k, dtype=object)

    # Critical values
    cv = norm.ppf(1 - (alp / 2))

    # Arc-Sine Method
    for i in range(k):
        pCA[i] = x[i] / n
        qCA[i] = 1 - pCA[i]
        seCA[i] = cv / np.sqrt(4 * n)
        LCA[i] = (np.sin(np.arcsin(np.sqrt(pCA[i])) - seCA[i] - c)) ** 2
        UCA[i] = (np.sin(np.arcsin(np.sqrt(pCA[i])) + seCA[i] + c)) ** 2

        if LCA[i] < 0:
            LABB[i] = "YES"
            LCA[i] = 0
        else:
            LABB[i] = "NO"

        if UCA[i] > 1:
            UABB[i] = "YES"
            UCA[i] = 1
        else:
            UABB[i] = "NO"

        if UCA[i] - LCA[i] == 0:
            ZWI[i] = "YES"
        else:
            ZWI[i] = "NO"

    return pd.DataFrame({
        'x': x,
        'LCA': LCA,
        'UCA': UCA,
        'LABB': LABB,
        'UABB': UABB,
        'ZWI': ZWI
    })
def ciclt(n, alp, c):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if c is None:
        raise ValueError("'c' is missing")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not isinstance(c, (int, float)) or c < 0:
        raise ValueError("'c' has to be positive")

    # INPUT n
    x = np.arange(0, n + 1)
    k = n + 1

    # INITIALIZATIONS
    pCLT = np.zeros(k)
    qCLT = np.zeros(k)
    seCLT = np.zeros(k)
    lgit = np.zeros(k)
    LCLT = np.zeros(k)
    UCLT = np.zeros(k)
    LABB = np.empty(k, dtype=object)
    UABB = np.empty(k, dtype=object)
    ZWI = np.empty(k, dtype=object)

    # CRITICAL VALUES
    cv = norm.ppf(1 - (alp / 2))

    # LOGIT-WALD METHOD
    pCLT[0] = 0
    qCLT[0] = 1
    LCLT[0] = 0
    UCLT[0] = 1 - ((alp / 2) ** (1 / n))

    pCLT[k - 1] = 1
    qCLT[k - 1] = 0
    LCLT[k - 1] = (alp / 2) ** (1 / n)
    UCLT[k - 1] = 1

    def lgiti(t):
        return np.exp(t) / (1 + np.exp(t))  # LOGIT INVERSE

    for j in range(1, k - 1):
        pCLT[j] = x[j] / n
        qCLT[j] = 1 - pCLT[j]
        lgit[j] = np.log(pCLT[j] / qCLT[j])
        seCLT[j] = np.sqrt(pCLT[j] * qCLT[j] * n)
        LCLT[j] = lgiti(lgit[j] - (cv / seCLT[j]) - c)
        UCLT[j] = lgiti(lgit[j] + (cv / seCLT[j]) + c)

    for i in range(k):
        LABB[i] = "YES" if LCLT[i] < 0 else "NO"
        if LCLT[i] < 0:
            LCLT[i] = 0

        UABB[i] = "YES" if UCLT[i] > 1 else "NO"
        if UCLT[i] > 1:
            UCLT[i] = 1

        ZWI[i] = "YES" if UCLT[i] - LCLT[i] == 0 else "NO"

    return pd.DataFrame({'x': x, 'LCLT': LCLT, 'UCLT': UCLT, 'LABB': LABB, 'UABB': UABB, 'ZWI': ZWI})


def cictw(n, alp, c):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if c is None:
        raise ValueError("'c' is missing")
    
    if alp > 1 or alp < 0 or not isinstance(alp, (float, int)):
        raise ValueError("'alpha' has to be between 0 and 1")
    
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    
    if not isinstance(c, (int, float)) or c < 0:
        raise ValueError("'c' has to be positive")

    # Input n
    x = np.arange(0, n + 1)
    k = n + 1

    # Initializations
    pCTW = np.zeros(k)
    qCTW = np.zeros(k)
    seCTW = np.zeros(k)
    LCTW = np.zeros(k)
    UCTW = np.zeros(k)
    DOF = np.zeros(k)
    cv = np.zeros(k)
    LABB = np.empty(k, dtype=object)
    UABB = np.empty(k, dtype=object)
    ZWI = np.empty(k, dtype=object)

    # Modified t-Wald Method
    for i in range(k):
        if x[i] == 0 or x[i] == n:
            pCTW[i] = (x[i] + 2) / (n + 4)
        else:
            pCTW[i] = x[i] / n
        
        qCTW[i] = 1 - pCTW[i]

        # Functions for variance calculations
        def f1(p, n):
            return p * (1 - p) / n
        
        def f2(p, n):
            return (p * (1 - p) / (n ** 3)) + \
                   (p + ((6 * n) - 7) * (p ** 2) + (4 * (n - 1) * (n - 3) * (p ** 3)) -
                   (2 * (n - 1) * ((2 * n) - 3) * (p ** 4))) / (n ** 5) - \
                   (2 * (p + ((2 * n) - 3) * (p ** 2) - 2 * (n - 1) * (p ** 3))) / (n ** 4)
        
        DOF[i] = 2 * (f1(pCTW[i], n) ** 2) / f2(pCTW[i], n)
        cv[i] = t.ppf(1 - (alp / 2), df=DOF[i])
        seCTW[i] = cv[i] * np.sqrt(f1(pCTW[i], n))
        LCTW[i] = pCTW[i] - (seCTW[i] + c)
        UCTW[i] = pCTW[i] + (seCTW[i] + c)

        if LCTW[i] < 0:
            LABB[i] = "YES"
            LCTW[i] = 0
        else:
            LABB[i] = "NO"

        if UCTW[i] > 1:
            UABB[i] = "YES"
            UCTW[i] = 1
        else:
            UABB[i] = "NO"

        if UCTW[i] - LCTW[i] == 0:
            ZWI[i] = "YES"
        else:
            ZWI[i] = "NO"

    return pd.DataFrame({
        'x': x,
        'LCTW': LCTW,
        'UCTW': UCTW,
        'LABB': LABB,
        'UABB': UABB,
        'ZWI': ZWI
    })

def cicall(n, alp, c):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if c is None:
        raise ValueError("'c' is missing")
    
    if alp > 1 or alp < 0 or not isinstance(alp, (float, int)):
        raise ValueError("'alpha' has to be between 0 and 1")
    
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    
    if c <= 0 or c > (1 / (2 * n)):
        raise ValueError("'c' has to be positive and less than or equal to 1/(2*n)")

    # Calling the individual CI functions
    wald_ci_df = cicwd(n, alp, c)
    arc_sine_ci_df = cicas(n, alp, c)
    score_ci_df = cicsc(n, alp, c)
    logit_ci_df = ciclt(n, alp, c)
    t_ci_df = cictw(n, alp, c)

    # Adding method information
    wald_ci_df['method'] = "CC-Wald"
    arc_sine_ci_df['method'] = "CC-ArcSine"
    logit_ci_df['method'] = "CC-Logit-Wald"
    score_ci_df['method'] = "CC-Score"
    t_ci_df['method'] = "CC-Wald-T"

    # Creating Generic DataFrames
    generic_1 = pd.DataFrame({
        'method': wald_ci_df['method'],
        'x': wald_ci_df['x'],
        'LowerLimit': wald_ci_df['LCW'],
        'UpperLimit': wald_ci_df['UCW'],
        'LowerAbb': wald_ci_df['LABB'],
        'UpperAbb': wald_ci_df['UABB'],
        'ZWI': wald_ci_df['ZWI']
    })

    generic_2 = pd.DataFrame({
        'method': arc_sine_ci_df['method'],
        'x': arc_sine_ci_df['x'],
        'LowerLimit': arc_sine_ci_df['LCA'],
        'UpperLimit': arc_sine_ci_df['UCA'],
        'LowerAbb': arc_sine_ci_df['LABB'],
        'UpperAbb': arc_sine_ci_df['UABB'],
        'ZWI': arc_sine_ci_df['ZWI']
    })

    generic_3 = pd.DataFrame({
        'method': score_ci_df['method'],
        'x': score_ci_df['x'],
        'LowerLimit': score_ci_df['LCS'],
        'UpperLimit': score_ci_df['UCS'],
        'LowerAbb': score_ci_df['LABB'],
        'UpperAbb': score_ci_df['UABB'],
        'ZWI': score_ci_df['ZWI']
    })

    generic_4 = pd.DataFrame({
        'method': logit_ci_df['method'],
        'x': logit_ci_df['x'],
        'LowerLimit': logit_ci_df['LCLT'],
        'UpperLimit': logit_ci_df['UCLT'],
        'LowerAbb': logit_ci_df['LABB'],
        'UpperAbb': logit_ci_df['UABB'],
        'ZWI': logit_ci_df['ZWI']
    })

    generic_5 = pd.DataFrame({
        'method': t_ci_df['method'],
        'x': t_ci_df['x'],
        'LowerLimit': t_ci_df['LCTW'],
        'UpperLimit': t_ci_df['UCTW'],
        'LowerAbb': t_ci_df['LABB'],
        'UpperAbb': t_ci_df['UABB'],
        'ZWI': t_ci_df['ZWI']
    })

    # Combining all the DataFrames
    final_df = pd.concat([generic_1, generic_2, generic_3, generic_4, generic_5], ignore_index=True)

    return final_df


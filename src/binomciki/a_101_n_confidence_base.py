import numpy as np
import pandas as pd
import scipy.stats as stats
import scipy.optimize as optimize

def ciwd(n, alp):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")

    # INPUT n
    x = np.arange(n + 1)
    k = n + 1

    # INITIALIZATIONS
    pW = np.zeros(k)
    qW = np.zeros(k)
    seW = np.zeros(k)
    LWD = np.zeros(k)
    UWD = np.zeros(k)
    LABB = np.empty(k, dtype=object)
    UABB = np.empty(k, dtype=object)
    ZWI = np.empty(k, dtype=object)

    # CRITICAL VALUES
    cv = stats.norm.ppf(1 - (alp / 2))

    # WALD METHOD
    for i in range(k):
        pW[i] = x[i] / n
        qW[i] = 1 - (x[i] / n)
        seW[i] = np.sqrt(pW[i] * qW[i] / n)
        LWD[i] = pW[i] - (cv * seW[i])
        UWD[i] = pW[i] + (cv * seW[i])
        
        LABB[i] = "YES" if LWD[i] < 0 else "NO"
        LWD[i] = max(0, LWD[i])
        
        UABB[i] = "YES" if UWD[i] > 1 else "NO"
        UWD[i] = min(1, UWD[i])
        
        ZWI[i] = "YES" if UWD[i] - LWD[i] == 0 else "NO"

    return pd.DataFrame( {
        'x': x,
        'LWD': LWD,
        'UWD': UWD,
        'LABB': LABB,
        'UABB': UABB,
        'ZWI': ZWI
    })

def cisc(n, alp):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if alp > 1 or alp < 0 or not isinstance(alp, (float, int)) or isinstance(alp, np.ndarray):
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")

    # INPUT n
    x = np.arange(n + 1)  # Generate values from 0 to n
    k = n + 1

    # INITIALIZATIONS
    pS = np.zeros(k)
    qS = np.zeros(k)
    seS = np.zeros(k)
    LSC = np.zeros(k)
    USC = np.zeros(k)
    LABB = np.full(k, 'NO')
    UABB = np.full(k, 'NO')
    ZWI = np.full(k, 'NO')

    # CRITICAL VALUES
    cv = stats.norm.ppf(1 - (alp / 2), loc=0, scale=1)
    cv1 = (cv ** 2) / (2 * n)
    cv2 = (cv / (2 * n)) ** 2

    # SCORE (WILSON) METHOD
    for i in range(k):
        pS[i] = x[i] / n
        qS[i] = 1 - pS[i]
        seS[i] = np.sqrt((pS[i] * qS[i] / n) + cv2)
        LSC[i] = (n / (n + cv ** 2)) * ((pS[i] + cv1) - (cv * seS[i]))
        USC[i] = (n / (n + cv ** 2)) * ((pS[i] + cv1) + (cv * seS[i]))

        # Lower bound adjustments
        if LSC[i] < 0:
            LABB[i] = "YES"
            LSC[i] = 0

        # Upper bound adjustments
        if USC[i] > 1:
            UABB[i] = "YES"
            USC[i] = 1

        # Zero-width interval check
        if USC[i] - LSC[i] == 0:
            ZWI[i] = "YES"

    return pd.DataFrame({'x': x, 'LSC': LSC, 'USC': USC, 'LABB': LABB, 'UABB': UABB, 'ZWI': ZWI})

def cias(n, alp):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")

    # INPUT
    x = np.arange(n + 1)
    k = n + 1

    # INITIALIZATIONS
    pA = np.zeros(k)
    qA = np.zeros(k)
    seA = np.zeros(k)
    LAS = np.zeros(k)
    UAS = np.zeros(k)
    LABB = np.empty(k, dtype=object)
    UABB = np.empty(k, dtype=object)
    ZWI = np.empty(k, dtype=object)

    cv = stats.norm.ppf(1 - (alp / 2))

    # ARC-SINE METHOD
    for i in range(k):
        pA[i] = x[i] / n
        qA[i] = 1 - pA[i]
        seA[i] = cv / np.sqrt(4 * n)
        LAS[i] = (np.sin(np.arcsin(np.sqrt(pA[i])) - seA[i])) ** 2
        UAS[i] = (np.sin(np.arcsin(np.sqrt(pA[i])) + seA[i])) ** 2
        
        LABB[i] = "YES" if LAS[i] < 0 else "NO"
        LAS[i] = max(0, LAS[i])
        
        UABB[i] = "YES" if UAS[i] > 1 else "NO"
        UAS[i] = min(1, UAS[i])
        
        ZWI[i] = "YES" if UAS[i] - LAS[i] == 0 else "NO"

    return pd.DataFrame({
        'x': x,
        'LAS': LAS,
        'UAS': UAS,
        'LABB': LABB,
        'UABB': UABB,
        'ZWI': ZWI
    })


# Optimized ciLR function
def cilr(n, alp):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if not (0 < alp < 1):
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0 and an integer or float")

    x = np.arange(n + 1)  # Generate values from 0 to n
    k = n + 1

    # INITIALIZATIONS
    LLR = np.zeros(k)
    ULR = np.zeros(k)
    LABB = np.full(k, 'NO')
    UABB = np.full(k, 'NO')
    ZWI = np.full(k, 'NO')
    
    # Precompute critical value
    cv = stats.norm.ppf(1 - (alp / 2), loc=0, scale=1)

    # Likelihood functions
    def likelhd(p, i):
        return stats.binom.pmf(x[i], n, p)

    def loglik(p, i):
        return stats.binom.logpmf(x[i], n, p)

    for i in range(k):
        # Minimize using likelihood function (MLE)
        mle_res = optimize.minimize_scalar(lambda p: -likelhd(p, i), bounds=(0, 1), method='bounded')
        mle_i = mle_res.x

        # Compute the cutoff for optimization
        cutoff = loglik(mle_i, i) - (cv ** 2 / 2)

        # Objective function for LLR and ULR
        def loglik_optim(p):
            return np.abs(cutoff - loglik(p, i))

        # Minimize to find LLR and ULR
        LLR_res = optimize.minimize_scalar(loglik_optim, bounds=(0, mle_i), method='bounded')
        LLR[i] = LLR_res.x

        ULR_res = optimize.minimize_scalar(loglik_optim, bounds=(mle_i, 1), method='bounded')
        ULR[i] = ULR_res.x
        
        # Set flags based on conditions
        LABB[i] = "YES" if LLR[i] < 0 else "NO"
        UABB[i] = "YES" if ULR[i] > 1 else "NO"
        ZWI[i] = "YES" if (ULR[i] - LLR[i]) == 0 else "NO"

    # Create a multi-index DataFrame to match the desired output format
    index = pd.MultiIndex.from_product([[n], x], names=['n', 'x'])
    data = {'LLR': LLR, 'ULR': ULR, 'LABB': LABB, 'UABB': UABB, 'ZWI': ZWI}
    result = pd.DataFrame(data, index=index)

    return result



def ciex(n, alp, e):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if e is None:
        raise ValueError("'e' is missing")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, int) or n <= 0:
        raise ValueError("'n' has to be a positive integer")

    # Check if 'e' is a float or list/array
    if isinstance(e, float):
        e = [e]  # Convert single float to a list
    elif not isinstance(e, (np.ndarray, list)) or any([i > 1 or i < 0 for i in e]):
        raise ValueError("'e' values have to be between 0 and 1")
    
    if len(e) > 10:
        raise ValueError("'e' can have only 10 intervals")

    nvar = len(e)
    result = pd.DataFrame()

    # Loop through each value of e and calculate limits
    for i in range(nvar):
        lu = lufn101(n, alp, e[i])
        result = pd.concat([result, lu], ignore_index=True)
    
    return result

# Lower and upper limit function
def lufn101(n, alp, e):
    x = np.arange(n + 1)  # Generate values from 0 to n
    LEX = np.zeros(n + 1)
    UEX = np.zeros(n + 1)
    LABB = np.full(n + 1, 'NO')
    UABB = np.full(n + 1, 'NO')
    ZWI = np.full(n + 1, 'NO')

    for i in range(n + 1):
        LEX[i] = exlim102l(x[i], n, alp, e)
        UEX[i] = exlim102u(x[i], n, alp, e)
        
        # Update flags based on limits
        if LEX[i] < 0:
            LABB[i] = "YES"
            LEX[i] = 0
        
        if UEX[i] > 1:
            UABB[i] = "YES"
            UEX[i] = 1
        
        if UEX[i] - LEX[i] == 0:
            ZWI[i] = "YES"

    # Create DataFrame for this e value
    return pd.DataFrame({
        'x': x,
        'LEX': LEX,
        'UEX': UEX,
        'LABB': LABB,
        'UABB': UABB,
        'ZWI': ZWI,
        'e': [e] * (n + 1)
    })

# Lower limit calculation
def exlim102l(x, n, alp, e):
    if x == 0:
        return 0
    elif x == n:
        return (alp / (2 * e)) ** (1 / n)
    else:
        z = x - 1
        y = np.arange(0, z + 1)

        def f1(p):
            return (1 - e) * stats.binom.pmf(x, n, p) + np.sum(stats.binom.pmf(y, n, p)) - (1 - (alp / 2))
        
        root_result = optimize.root_scalar(f1, bracket=[0, 1], method='bisect')
        return root_result.root

# Upper limit calculation
def exlim102u(x, n, alp, e):
    if x == 0:
        return 1 - (alp / (2 * e)) ** (1 / n)
    elif x == n:
        return 1
    else:
        z = x - 1
        y = np.arange(0, z + 1)

        def f2(p):
            return e * stats.binom.pmf(x, n, p) + np.sum(stats.binom.pmf(y, n, p)) - (alp / 2)
        
        root_result = optimize.root_scalar(f2, bracket=[0, 1], method='bisect')
        return root_result.root



def citw(n, alp):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")

    # INPUT n
    x = np.arange(n + 1)
    k = n + 1

    # INITIALIZATIONS
    pTW = np.zeros(k)
    qTW = np.zeros(k)
    seTW = np.zeros(k)
    LTW = np.zeros(k)
    UTW = np.zeros(k)
    DOF = np.zeros(k)
    cv = np.zeros(k)
    LABB = np.empty(k, dtype=object)
    UABB = np.empty(k, dtype=object)
    ZWI = np.empty(k, dtype=object)

    # Helper functions
    def f1(p, n):
        return p * (1 - p) / n

    def f2(p, n):
        return (p * (1 - p) / (n**3)) + \
               (p + ((6 * n) - 7) * (p**2) + (4 * (n - 1) * (n - 3) * (p**3)) - (2 * (n - 1) * ((2 * n) - 3) * (p**4))) / (n**5) - \
               (2 * (p + ((2 * n) - 3) * (p**2) - 2 * (n - 1) * (p**3))) / (n**4)

    # MODIFIED_t-WALD METHOD
    for i in range(k):
        if x[i] == 0 or x[i] == n:
            pTW[i] = (x[i] + 2) / (n + 4)
        else:
            pTW[i] = x[i] / n
        qTW[i] = 1 - pTW[i]

        DOF[i] = 2 * ((f1(pTW[i], n))**2) / f2(pTW[i], n)
        cv[i] = stats.t.ppf(1 - (alp / 2), df=DOF[i])
        seTW[i] = cv[i] * np.sqrt(f1(pTW[i], n))
        LTW[i] = pTW[i] - seTW[i]
        UTW[i] = pTW[i] + seTW[i]

        LABB[i] = "YES" if LTW[i] < 0 else "NO"
        LTW[i] = max(0, LTW[i])

        UABB[i] = "YES" if UTW[i] > 1 else "NO"
        UTW[i] = min(1, UTW[i])

        ZWI[i] = "YES" if UTW[i] - LTW[i] == 0 else "NO"

    return pd.DataFrame({
        'x': x,
        'LTW': LTW,
        'UTW': UTW,
        'LABB': LABB,
        'UABB': UABB,
        'ZWI': ZWI
    })


def cilt(n, alp):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")

    # Generate values from 0 to n
    x = np.arange(n + 1)
    k = n + 1

    # Initialize arrays
    pLT = np.zeros(k)
    qLT = np.zeros(k)
    seLT = np.zeros(k)
    lgit = np.zeros(k)
    LLT = np.zeros(k)
    ULT = np.zeros(k)
    LABB = np.full(k, 'NO')
    UABB = np.full(k, 'NO')
    ZWI = np.full(k, 'NO')

    # Critical value for normal distribution
    cv = stats.norm.ppf(1 - (alp / 2))

    # Logit-Wald method
    pLT[0] = 0
    qLT[0] = 1
    LLT[0] = 0
    ULT[0] = 1 - ((alp / 2) ** (1 / n))

    pLT[k - 1] = 1
    qLT[k - 1] = 0
    LLT[k - 1] = (alp / 2) ** (1 / n)
    ULT[k - 1] = 1

    for j in range(1, k - 1):
        pLT[j] = x[j] / n
        qLT[j] = 1 - pLT[j]
        lgit[j] = np.log(pLT[j] / qLT[j])
        seLT[j] = np.sqrt(pLT[j] * qLT[j] * n)
        LLT[j] = 1 / (1 + np.exp(-lgit[j] + (cv / seLT[j])))
        ULT[j] = 1 / (1 + np.exp(-lgit[j] - (cv / seLT[j])))

    for i in range(k):
        if LLT[i] < 0:
            LABB[i] = "YES"
            LLT[i] = 0

        if ULT[i] > 1:
            UABB[i] = "YES"
            ULT[i] = 1

        if ULT[i] - LLT[i] == 0:
            ZWI[i] = "YES"

    # Create a DataFrame for output
    return pd.DataFrame({
        'x': x,
        'LLT': LLT,
        'ULT': ULT,
        'LABB': LABB,
        'UABB': UABB,
        'ZWI': ZWI
    })







def ciall(n, alp):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if alp > 1 or alp < 0 or isinstance(alp, (list, tuple)):
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or isinstance(n, (list, tuple)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")

    # Assuming the CI methods are defined elsewhere and return DataFrames
    WaldCI_df = ciwd(n, alp)
    ArcSineCI_df = cias(n, alp)
    LRCI_df = cilr(n, alp)
    ScoreCI_df = cisc(n, alp)
    WaldTCI_df = citw(n, alp)
    LogitWald_df = cilt(n, alp)

    # Assign method names as strings
    WaldCI_df['method'] = "Wald"
    ArcSineCI_df['method'] = "ArcSine"
    LRCI_df['method'] = "Likelihood"
    ScoreCI_df['method'] = "Score"
    WaldTCI_df['method'] = "Wald-T"
    LogitWald_df['method'] = "Logit-Wald"

    # Helper function to safely extract the 'x' column if present
    def create_generic_df(df, method, lower_col, upper_col):
        return pd.DataFrame({
            'method': df['method'],
            'x': df['x'] if 'x' in df.columns else None,  # Default to None if 'x' is missing
            'LowerLimit': df[lower_col],
            'UpperLimit': df[upper_col],
            'LowerAbb': df['LABB'],
            'UpperAbb': df['UABB'],
            'ZWI': df['ZWI']
        })

    # Create generic DataFrames
    Generic_1 = create_generic_df(WaldCI_df, "Wald", 'LWD', 'UWD')
    Generic_2 = create_generic_df(ArcSineCI_df, "ArcSine", 'LAS', 'UAS')
    Generic_3 = create_generic_df(LRCI_df, "Likelihood", 'LLR', 'ULR')
    Generic_4 = create_generic_df(ScoreCI_df, "Score", 'LSC', 'USC')
    Generic_5 = create_generic_df(WaldTCI_df, "Wald-T", 'LTW', 'UTW')
    Generic_6 = create_generic_df(LogitWald_df, "Logit-Wald", 'LLT', 'ULT')

    # Combine all the DataFrames
    Final_df = pd.concat([Generic_1, Generic_2, Generic_3, Generic_4, Generic_5, Generic_6], ignore_index=True)
    Final_df.index = range(1, len(Final_df) + 1)

    return Final_df

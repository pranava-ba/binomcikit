import pandas as pd
import scipy.stats as stats


def ciwdx(x=None, n=None, alp=None):
    # Input validation
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if (not isinstance(x, int) and not isinstance(x, float)) or x < 0 or x > n or not isinstance(x, (int, float)):
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if (not isinstance(n, int) and not isinstance(n, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")

    # Critical value
    cv = stats.norm.ppf(1 - (alp / 2), loc=0, scale=1)

    # Wald method
    pW = x / n
    qW = 1 - (x / n)
    seW = (pW * qW / n) ** 0.5
    LWDx = pW - (cv * seW)
    UWDx = pW + (cv * seW)

    # Adjustments for bounds
    LABB = "YES" if LWDx < 0 else "NO"
    LWDx = max(LWDx, 0)
    UABB = "YES" if UWDx > 1 else "NO"
    UWDx = min(UWDx, 1)
    ZWI = "YES" if UWDx - LWDx == 0 else "NO"

    # Return as a DataFrame
    return pd.DataFrame({
        'x': [x],
        'LWDx': [LWDx],
        'UWDx': [UWDx],
        'LABB': [LABB],
        'UABB': [UABB],
        'ZWI': [ZWI]
    })


def ciscx(x=None, n=None, alp=None):
    # Input validation
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if (not isinstance(x, int) and not isinstance(x, float)) or x < 0 or x > n or not isinstance(x, (int, float)):
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if (not isinstance(n, int) and not isinstance(n, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")

    # Critical value
    cv = stats.norm.ppf(1 - (alp / 2), loc=0, scale=1)
    cv1 = (cv ** 2) / (2 * n)
    cv2 = (cv / (2 * n)) ** 2

    # Score (Wilson) method
    pS = x / n
    qS = 1 - (x / n)
    seS = ((pS * qS / n) + cv2) ** 0.5
    LSCx = (n / (n + (cv ** 2))) * ((pS + cv1) - (cv * seS))
    USCx = (n / (n + (cv ** 2))) * ((pS + cv1) + (cv * seS))

    # Adjustments for bounds
    LABB = "YES" if LSCx < 0 else "NO"
    LSCx = max(LSCx, 0)
    UABB = "YES" if USCx > 1 else "NO"
    USCx = min(USCx, 1)
    ZWI = "YES" if USCx - LSCx == 0 else "NO"

    # Return as a DataFrame
    return pd.DataFrame({
        'x': [x],
        'LSCx': [LSCx],
        'USCx': [USCx],
        'LABB': [LABB],
        'UABB': [UABB],
        'ZWI': [ZWI]
    })

import numpy as np


def ciasx(x=None, n=None, alp=None):
    # Input validation
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if (not isinstance(x, int) and not isinstance(x, float)) or x < 0 or x > n or not isinstance(x, (int, float)):
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if (not isinstance(n, int) and not isinstance(n, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")

    # Critical value
    cv = stats.norm.ppf(1 - (alp / 2), loc=0, scale=1)

    # Arc-Sine method
    pA = x / n
    seA = cv / np.sqrt(4 * n)
    LASx = (np.sin(np.arcsin(np.sqrt(pA)) - seA)) ** 2
    UASx = (np.sin(np.arcsin(np.sqrt(pA)) + seA)) ** 2

    # Adjustments for bounds
    LABB = "YES" if LASx < 0 else "NO"
    LASx = max(LASx, 0)
    UABB = "YES" if UASx > 1 else "NO"
    UASx = min(UASx, 1)
    ZWI = "YES" if UASx - LASx == 0 else "NO"

    # Return as a DataFrame
    return pd.DataFrame({
        'x': [x],
        'LASx': [LASx],
        'UASx': [UASx],
        'LABB': [LABB],
        'UABB': [UABB],
        'ZWI': [ZWI]
    })

from scipy.optimize import minimize_scalar


def cilrx(x=None, n=None, alp=None):
    # Input validation
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if (not isinstance(x, int) and not isinstance(x, float)) or x < 0 or x > n or not isinstance(x, (int, float)):
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if (not isinstance(n, int) and not isinstance(n, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")

    # Critical value
    cv = stats.norm.ppf(1 - (alp / 2), loc=0, scale=1)

    # Likelihood-ratio method
    y = x

    def likelhd(p):
        return stats.binom.pmf(y, n, p)

    def loglik(p):
        return stats.binom.logpmf(y, n, p)

    # Find MLE (maximum likelihood estimate)
    mle_result = minimize_scalar(lambda p: -likelhd(p), bounds=(0, 1), method='bounded')
    mle = mle_result.x

    # Calculate cutoff
    cutoff = loglik(mle) - (cv**2 / 2)

    def loglik_optim(p):
        return abs(cutoff - loglik(p))

    # Find lower and upper bounds
    LLRx_result = minimize_scalar(loglik_optim, bounds=(0, mle), method='bounded')
    LLRx = LLRx_result.x

    ULRx_result = minimize_scalar(loglik_optim, bounds=(mle, 1), method='bounded')
    ULRx = ULRx_result.x

    # Adjustments for bounds
    LABB = "YES" if LLRx < 0 else "NO"
    LLRx = max(LLRx, 0)
    UABB = "YES" if ULRx > 1 else "NO"
    ULRx = min(ULRx, 1)
    ZWI = "YES" if ULRx - LLRx == 0 else "NO"

    # Return as a DataFrame
    return pd.DataFrame({
        'x': [x],
        'LLRx': [LLRx],
        'ULRx': [ULRx],
        'LABB': [LABB],
        'UABB': [UABB],
        'ZWI': [ZWI]
    })

# Example usage:
# result = ciLRx(x=10, n=100, alp=0.05)
# print(result)
import scipy.optimize as optimize


def ciexx(x, n, alp, e):
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
    if not isinstance(alp, (int, float)) or not (0 <= alp <= 1):
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(e, (list, np.ndarray)) or any(el < 0 or el > 1 for el in e):
        raise ValueError("'e' has to be between 0 and 1")
    if len(e) > 10:
        raise ValueError("'e' can have only 10 intervals")

    res = pd.DataFrame()

    for ei in e:
        lu = lufn103(x, n, alp, ei)
        res = pd.concat([res, lu], ignore_index=True)

    return res


def lufn103(x, n, alp, e):
    LEXx = exlim103l(x, n, alp, e)
    UEXx = exlim103u(x, n, alp, e)

    LABB = "YES" if LEXx < 0 else "NO"
    if LEXx < 0:
        LEXx = 0

    UABB = "YES" if UEXx > 1 else "NO"
    if UEXx > 1:
        UEXx = 1

    ZWI = "YES" if UEXx - LEXx == 0 else "NO"

    resx = pd.DataFrame([{"x": x, "LEXx": LEXx, "UEXx": UEXx, "LABB": LABB, "UABB": UABB, "ZWI": ZWI, "e": e}])
    return resx


def exlim103l(x, n, alp, e):
    if x == 0:
        return 0
    elif x == n:
        return (alp / (2 * e)) ** (1 / n)
    else:
        z = np.arange(0, x)

        def f1(p):
            return (1 - e) * stats.binom.pmf(x, n, p) + np.sum(stats.binom.pmf(z, n, p)) - (1 - (alp / 2))

        return optimize.brentq(f1, 0, 1)


def exlim103u(x, n, alp, e):
    if x == 0:
        return 1 - ((alp / (2 * e)) ** (1 / n))
    elif x == n:
        return 1
    else:
        z = np.arange(0, x)

        def f2(p):
            return e * stats.binom.pmf(x, n, p) + np.sum(stats.binom.pmf(z, n, p)) - (alp / 2)

        return optimize.brentq(f2, 0, 1)




def ciltx(x, n, alp):
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
    if not isinstance(alp, (int, float)) or not (0 <= alp <= 1):
        raise ValueError("'alpha' has to be between 0 and 1")

    # Initializations
    pLTx, qLTx, seLTx, lgitx, LLTx, ULTx = 0, 0, 0, 0, 0, 0
    LABB, UABB, ZWI = "NO", "NO", "NO"

    # Critical values
    cv = stats.norm.ppf(1 - (alp / 2))

    # Logit-Wald Method
    if x == 0:
        pLTx, qLTx = 0, 1
        LLTx = 0
        ULTx = 1 - ((alp / 2) ** (1 / n))
    elif x == n:
        pLTx, qLTx = 1, 0
        LLTx = (alp / 2) ** (1 / n)
        ULTx = 1
    else:
        pLTx = x / n
        qLTx = 1 - pLTx
        lgitx = np.log(pLTx / qLTx)
        seLTx = np.sqrt(pLTx * qLTx * n)
        LLTx = 1 / (1 + np.exp(-lgitx + (cv / seLTx)))
        ULTx = 1 / (1 + np.exp(-lgitx - (cv / seLTx)))

    if LLTx < 0:
        LABB = "YES"
        LLTx = 0

    if ULTx > 1:
        UABB = "YES"
        ULTx = 1

    if ULTx - LLTx == 0:
        ZWI = "YES"

    return pd.DataFrame([{"x": x, "LLTx": LLTx, "ULTx": ULTx, "LABB": LABB, "UABB": UABB, "ZWI": ZWI}])

from scipy.stats import t


def citwx(x, n, alp):
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if not (isinstance(x, int) or isinstance(x, float)) or x < 0 or x > n or not isinstance(x, (int, float)):
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if not (isinstance(n, int) or isinstance(n, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if alp > 1 or alp < 0:
        raise ValueError("'alpha' has to be between 0 and 1")

    # MODIFIED_t-WALD METHOD
    if x == 0 or x == n:
        pTWx = (x + 2) / (n + 4)
    else:
        pTWx = x / n

    def f1(p, n):
        return p * (1 - p) / n

    def f2(p, n):
        return (p * (1 - p) / (n ** 3)) + \
               (p + ((6 * n) - 7) * (p ** 2) + \
                4 * (n - 1) * (n - 3) * (p ** 3) - \
                2 * (n - 1) * ((2 * n) - 3) * (p ** 4)) / (n ** 5) - \
               (2 * (p + ((2 * n) - 3) * (p ** 2) - \
                2 * (n - 1) * (p ** 3))) / (n ** 4)

    DOFx = 2 * (f1(pTWx, n) ** 2) / f2(pTWx, n)
    cvx = t.ppf(1 - (alp / 2), df=DOFx)
    seTWx = cvx * np.sqrt(f1(pTWx, n))
    LTWx = pTWx - seTWx
    UTWx = pTWx + seTWx

    LABB = "YES" if LTWx < 0 else "NO"
    if LTWx < 0:
        LTWx = 0

    UABB = "YES" if UTWx > 1 else "NO"
    if UTWx > 1:
        UTWx = 1

    ZWI = "YES" if UTWx - LTWx == 0 else "NO"

    result_dict= {
        "x": x,
        "LTWx": LTWx,
        "UTWx": UTWx,
        "LABB": LABB,
        "UABB": UABB,
        "ZWI": ZWI
    }
    result_df = pd.DataFrame([result_dict])  # Wrap the dictionary in a list for a single row
    return result_df



def ciallx(x=None, n=None, alp=None):
    """All six base confidence interval methods for a given x (port of R ciAllx).

    Combines Wald, ArcSine, Likelihood-Ratio, Score, Logit-Wald and Wald-T
    intervals for a single ``x`` into one long-format DataFrame with a
    ``method`` column.
    """
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

    def generic(df, method, lower_col, upper_col):
        return pd.DataFrame({
            'method': method,
            'x': df['x'],
            'LowerLimit': df[lower_col],
            'UpperLimit': df[upper_col],
            'LowerAbb': df['LABB'],
            'UpperAbb': df['UABB'],
            'ZWI': df['ZWI'],
        })

    final_df = pd.concat([
        generic(ciwdx(x, n, alp), "Wald", 'LWDx', 'UWDx'),
        generic(ciasx(x, n, alp), "ArcSine", 'LASx', 'UASx'),
        generic(cilrx(x, n, alp), "Likelihood", 'LLRx', 'ULRx'),
        generic(ciscx(x, n, alp), "Score", 'LSCx', 'USCx'),
        generic(ciltx(x, n, alp), "Logit-Wald", 'LLTx', 'ULTx'),
        generic(citwx(x, n, alp), "Wald-T", 'LTWx', 'UTWx'),
    ], ignore_index=True)
    final_df.index = range(1, len(final_df) + 1)
    return final_df

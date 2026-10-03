import numpy as np
import pandas as pd
from scipy.stats import t

from . import _fast


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

    # Critical values
    cv = _fast.zcrit(alp)

    # Wald Method (vectorised over every x)
    pCW = x / n
    seCW = np.sqrt(pCW * (1 - pCW) / n)
    LCW, UCW, LABB, UABB, ZWI = _fast.flags(pCW - ((cv * seCW) + c), pCW + ((cv * seCW) + c))

    return pd.DataFrame({"x": x, "LCW": LCW, "UCW": UCW, "LABB": LABB, "UABB": UABB, "ZWI": ZWI})


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

    # Critical values
    cv = _fast.zcrit(alp)
    cv1 = (cv**2) / (2 * n)
    cv2 = cv / (2 * n)

    # Score (Wilson) Method (vectorised over every x)
    pCS = x / n
    with np.errstate(invalid="ignore"):
        seCS_L = np.sqrt((cv**2) - (4 * n * (c + c**2)) + (4 * n * pCS * (1 - pCS + (2 * c))))
        seCS_U = np.sqrt((cv**2) + (4 * n * (c - c**2)) + (4 * n * pCS * (1 - pCS - (2 * c))))
    LCS, UCS, LABB, UABB, ZWI = _fast.flags(
        (n / (n + (cv**2))) * ((pCS - c + cv1) - (cv2 * seCS_L)),
        (n / (n + (cv**2))) * ((pCS + c + cv1) + (cv2 * seCS_U)),
    )

    return pd.DataFrame({"x": x, "LCS": LCS, "UCS": UCS, "LABB": LABB, "UABB": UABB, "ZWI": ZWI})


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

    # Critical values
    cv = _fast.zcrit(alp)

    # Arc-Sine Method (vectorised over every x)
    pCA = x / n
    seCA = cv / np.sqrt(4 * n)
    LCA, UCA, LABB, UABB, ZWI = _fast.flags(
        (np.sin(np.arcsin(np.sqrt(pCA)) - seCA - c)) ** 2,
        (np.sin(np.arcsin(np.sqrt(pCA)) + seCA + c)) ** 2,
    )

    return pd.DataFrame({"x": x, "LCA": LCA, "UCA": UCA, "LABB": LABB, "UABB": UABB, "ZWI": ZWI})


def _lgiti(t):
    return np.exp(t) / (1 + np.exp(t))  # LOGIT INVERSE


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

    # LOGIT-WALD METHOD (vectorised over every x); the x = 0 and x = n rows are closed form
    cv = _fast.zcrit(alp)
    inner = x[1:-1]
    pCLT = inner / n
    qCLT = 1 - pCLT
    lgit = np.log(pCLT / qCLT)
    seCLT = np.sqrt(pCLT * qCLT * n)
    LCLT = np.zeros(k)
    UCLT = np.ones(k)
    UCLT[0] = 1 - ((alp / 2) ** (1 / n))
    LCLT[k - 1] = (alp / 2) ** (1 / n)
    LCLT[1:-1] = _lgiti(lgit - (cv / seCLT) - c)
    UCLT[1:-1] = _lgiti(lgit + (cv / seCLT) + c)
    LCLT, UCLT, LABB, UABB, ZWI = _fast.flags(LCLT, UCLT)

    return pd.DataFrame(
        {"x": x, "LCLT": LCLT, "UCLT": UCLT, "LABB": LABB, "UABB": UABB, "ZWI": ZWI}
    )


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

    def f1(p, n):
        return p * (1 - p) / n

    def f2(p, n):
        return (
            (p * (1 - p) / (n**3))
            + (
                p
                + ((6 * n) - 7) * (p**2)
                + (4 * (n - 1) * (n - 3) * (p**3))
                - (2 * (n - 1) * ((2 * n) - 3) * (p**4))
            )
            / (n**5)
            - (2 * (p + ((2 * n) - 3) * (p**2) - 2 * (n - 1) * (p**3))) / (n**4)
        )

    # Modified t-Wald Method (vectorised over every x)
    pCTW = np.where((x == 0) | (x == n), (x + 2) / (n + 4), x / n)
    DOF = 2 * (f1(pCTW, n) ** 2) / f2(pCTW, n)
    cv = t.ppf(1 - (alp / 2), df=DOF)
    seCTW = cv * np.sqrt(f1(pCTW, n))
    LCTW, UCTW, LABB, UABB, ZWI = _fast.flags(pCTW - (seCTW + c), pCTW + (seCTW + c))

    return pd.DataFrame(
        {"x": x, "LCTW": LCTW, "UCTW": UCTW, "LABB": LABB, "UABB": UABB, "ZWI": ZWI}
    )


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
    wald_ci_df["method"] = "CC-Wald"
    arc_sine_ci_df["method"] = "CC-ArcSine"
    logit_ci_df["method"] = "CC-Logit-Wald"
    score_ci_df["method"] = "CC-Score"
    t_ci_df["method"] = "CC-Wald-T"

    # Creating Generic DataFrames
    generic_1 = pd.DataFrame(
        {
            "method": wald_ci_df["method"],
            "x": wald_ci_df["x"],
            "LowerLimit": wald_ci_df["LCW"],
            "UpperLimit": wald_ci_df["UCW"],
            "LowerAbb": wald_ci_df["LABB"],
            "UpperAbb": wald_ci_df["UABB"],
            "ZWI": wald_ci_df["ZWI"],
        }
    )

    generic_2 = pd.DataFrame(
        {
            "method": arc_sine_ci_df["method"],
            "x": arc_sine_ci_df["x"],
            "LowerLimit": arc_sine_ci_df["LCA"],
            "UpperLimit": arc_sine_ci_df["UCA"],
            "LowerAbb": arc_sine_ci_df["LABB"],
            "UpperAbb": arc_sine_ci_df["UABB"],
            "ZWI": arc_sine_ci_df["ZWI"],
        }
    )

    generic_3 = pd.DataFrame(
        {
            "method": score_ci_df["method"],
            "x": score_ci_df["x"],
            "LowerLimit": score_ci_df["LCS"],
            "UpperLimit": score_ci_df["UCS"],
            "LowerAbb": score_ci_df["LABB"],
            "UpperAbb": score_ci_df["UABB"],
            "ZWI": score_ci_df["ZWI"],
        }
    )

    generic_4 = pd.DataFrame(
        {
            "method": logit_ci_df["method"],
            "x": logit_ci_df["x"],
            "LowerLimit": logit_ci_df["LCLT"],
            "UpperLimit": logit_ci_df["UCLT"],
            "LowerAbb": logit_ci_df["LABB"],
            "UpperAbb": logit_ci_df["UABB"],
            "ZWI": logit_ci_df["ZWI"],
        }
    )

    generic_5 = pd.DataFrame(
        {
            "method": t_ci_df["method"],
            "x": t_ci_df["x"],
            "LowerLimit": t_ci_df["LCTW"],
            "UpperLimit": t_ci_df["UCTW"],
            "LowerAbb": t_ci_df["LABB"],
            "UpperAbb": t_ci_df["UABB"],
            "ZWI": t_ci_df["ZWI"],
        }
    )

    # Combining all the DataFrames
    final_df = pd.concat([generic_1, generic_2, generic_3, generic_4, generic_5], ignore_index=True)

    return final_df

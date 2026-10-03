import numpy as np
import pandas as pd
import scipy.stats as stats

from . import _fast


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
    y = x + h
    n1 = n + (2 * h)

    # Critical values
    cv = _fast.zcrit(alp)

    # WALD METHOD (vectorised over every x)
    pAW = y / n1
    seAW = np.sqrt(pAW * (1 - pAW) / n1)
    LAWD, UAWD, LABB, UABB, ZWI = _fast.flags(pAW - cv * seAW, pAW + cv * seAW)

    return pd.DataFrame(
        {"x": x, "LAWD": LAWD, "UAWD": UAWD, "LABB": LABB, "UABB": UABB, "ZWI": ZWI}
    )


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
    y = x + h
    n1 = n + (2 * h)

    # Critical values
    cv = _fast.zcrit(alp)
    cv1 = (cv**2) / (2 * n1)
    cv2 = (cv / (2 * n1)) ** 2

    # ASCORE (WILSON) METHOD (vectorised over every x)
    pAS = y / n1
    seAS = np.sqrt((pAS * (1 - pAS) / n1) + cv2)
    LASC, UASC, LABB, UABB, ZWI = _fast.flags(
        (n1 / (n1 + cv**2)) * ((pAS + cv1) - (cv * seAS)),
        (n1 / (n1 + cv**2)) * ((pAS + cv1) + (cv * seAS)),
    )

    return pd.DataFrame(
        {"x": x, "LASC": LASC, "UASC": UASC, "LABB": LABB, "UABB": UABB, "ZWI": ZWI}
    )


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
    y = x + h
    m = n + (2 * h)

    cv = _fast.zcrit(alp)

    # ARC-SINE METHOD (vectorised over every x)
    pA = y / m
    seA = cv / np.sqrt(4 * m)
    LAAS, UAAS, LABB, UABB, ZWI = _fast.flags(
        (np.sin(np.arcsin(np.sqrt(pA)) - seA)) ** 2, (np.sin(np.arcsin(np.sqrt(pA)) + seA)) ** 2
    )

    return pd.DataFrame(
        {"x": x, "LAAS": LAAS, "UAAS": UAAS, "LABB": LABB, "UABB": UABB, "ZWI": ZWI}
    )


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
    n1 = n + (2 * h)

    # LIKELIHOOD-RATIO METHOD (vectorised over every x). The MLE has the closed form y1/n1 and
    # the deviance is used instead of the raw likelihood, which underflows for large n (see
    # docs/under_the_hood.md).
    LALR, UALR = _fast.lr_limits_y(y1, n1, alp)
    LABB = _fast.yes_no(LALR < 0)
    UABB = _fast.yes_no(UALR > 1)
    ZWI = _fast.yes_no(UALR - LALR == 0)

    return pd.DataFrame(
        {"x": x, "LALR": LALR, "UALR": UALR, "LABB": LABB, "UABB": UABB, "ZWI": ZWI}
    )


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
    y = x + h
    n1 = n + (2 * h)

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

    # MODIFIED_t-ADJ_WALD METHOD (vectorised over every x)
    pATW = y / n1
    DOF = 2 * ((f1(pATW, n1)) ** 2) / f2(pATW, n1)
    cv = stats.t.ppf(1 - (alp / 2), df=DOF)
    seATW = cv * np.sqrt(f1(pATW, n1))
    LATW, UATW, LABB, UABB, ZWI = _fast.flags(pATW - seATW, pATW + seATW)
    # undefined rows (h = 0 at x = 0 / n: 0/0 degrees of freedom) fall back to [0, 1]
    LATW, UATW = np.nan_to_num(LATW, nan=0.0), np.nan_to_num(UATW, nan=1.0)
    ZWI = _fast.yes_no(UATW - LATW == 0)

    return pd.DataFrame(
        {"x": x, "LATW": LATW, "UATW": UATW, "LABB": LABB, "UABB": UABB, "ZWI": ZWI}
    )


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
    y = x + h
    n1 = n + (2 * h)

    # LOGIT-WALD METHOD (vectorised over every x)
    cv = _fast.zcrit(alp)
    pALT = y / n1
    qALT = 1 - pALT
    lgit = np.log(pALT / qALT)
    seALT = np.sqrt(pALT * qALT * n1)
    LALT, UALT, LABB, UABB, ZWI = _fast.flags(
        1 / (1 + np.exp(-lgit + (cv / seALT))), 1 / (1 + np.exp(-lgit - (cv / seALT)))
    )
    # undefined rows (h = 0 at x = 0 / n: logit of 0 or 1) fall back to [0, 1]
    LALT, UALT = np.nan_to_num(LALT, nan=0.0), np.nan_to_num(UALT, nan=1.0)
    ZWI = _fast.yes_no(UALT - LALT == 0)

    return pd.DataFrame(
        {"x": x, "LALT": LALT, "UALT": UALT, "LABB": LABB, "UABB": UABB, "ZWI": ZWI}
    )


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
    WaldCI_df["method"] = "Adj-Wald"
    ArcSineCI_df["method"] = "Adj-ArcSine"
    LRCI_df["method"] = "Adj-Likelihood"
    WaldLCI_df["method"] = "Adj-Logit-Wald"
    ScoreCI_df["method"] = "Adj-Score"
    AdWaldCI_df["method"] = "Adj-Wald-T"

    # Creating generic dataframes
    Generic_1 = pd.DataFrame(
        {
            "method": WaldCI_df["method"],
            "x": WaldCI_df["x"],
            "LowerLimit": WaldCI_df["LAWD"],
            "UpperLimit": WaldCI_df["UAWD"],
            "LowerAbb": WaldCI_df["LABB"],
            "UpperAbb": WaldCI_df["UABB"],
            "ZWI": WaldCI_df["ZWI"],
        }
    )

    Generic_2 = pd.DataFrame(
        {
            "method": ArcSineCI_df["method"],
            "x": ArcSineCI_df["x"],
            "LowerLimit": ArcSineCI_df["LAAS"],
            "UpperLimit": ArcSineCI_df["UAAS"],
            "LowerAbb": ArcSineCI_df["LABB"],
            "UpperAbb": ArcSineCI_df["UABB"],
            "ZWI": ArcSineCI_df["ZWI"],
        }
    )

    Generic_3 = pd.DataFrame(
        {
            "method": LRCI_df["method"],
            "x": LRCI_df["x"],
            "LowerLimit": LRCI_df["LALR"],
            "UpperLimit": LRCI_df["UALR"],
            "LowerAbb": LRCI_df["LABB"],
            "UpperAbb": LRCI_df["UABB"],
            "ZWI": LRCI_df["ZWI"],
        }
    )

    Generic_4 = pd.DataFrame(
        {
            "method": ScoreCI_df["method"],
            "x": ScoreCI_df["x"],
            "LowerLimit": ScoreCI_df["LASC"],
            "UpperLimit": ScoreCI_df["UASC"],
            "LowerAbb": ScoreCI_df["LABB"],
            "UpperAbb": ScoreCI_df["UABB"],
            "ZWI": ScoreCI_df["ZWI"],
        }
    )

    Generic_5 = pd.DataFrame(
        {
            "method": WaldLCI_df["method"],
            "x": WaldLCI_df["x"],
            "LowerLimit": WaldLCI_df["LALT"],
            "UpperLimit": WaldLCI_df["UALT"],
            "LowerAbb": WaldLCI_df["LABB"],
            "UpperAbb": WaldLCI_df["UABB"],
            "ZWI": WaldLCI_df["ZWI"],
        }
    )

    Generic_6 = pd.DataFrame(
        {
            "method": AdWaldCI_df["method"],
            "x": AdWaldCI_df["x"],
            "LowerLimit": AdWaldCI_df["LATW"],
            "UpperLimit": AdWaldCI_df["UATW"],
            "LowerAbb": AdWaldCI_df["LABB"],
            "UpperAbb": AdWaldCI_df["UABB"],
            "ZWI": AdWaldCI_df["ZWI"],
        }
    )

    # Combining generic dataframes
    Final_df = pd.concat(
        [Generic_1, Generic_2, Generic_3, Generic_4, Generic_5, Generic_6], ignore_index=True
    )

    return Final_df

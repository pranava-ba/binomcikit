import numpy as np
import pandas as pd
from scipy.stats import norm, t
import plotly.express as px
import plotly.graph_objects as go


def cicwdx(x, n, alp, c):
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if c is None:
        raise ValueError("'c' is missing")

    # Check that x is a positive integer between 0 and n
    if not isinstance(x, (int, float)) or x < 0 or x > n:
        raise ValueError("'x' has to be a positive integer between 0 and n")

    # Check that n is greater than 0
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")

    # Check that alpha is between 0 and 1
    if not (0 <= alp <= 1):
        raise ValueError("'alpha' has to be between 0 and 1")

    # Check that c is positive
    if not isinstance(c, (int, float)) or c < 0:
        raise ValueError("'c' has to be positive")

    # Critical values
    cv = norm.ppf(1 - (alp / 2))

    # Wald method
    p_cw_x = x / n
    q_cw_x = 1 - p_cw_x
    se_cw_x = np.sqrt(p_cw_x * q_cw_x / n)
    lc_wx = p_cw_x - (cv * se_cw_x + c)
    uc_wx = p_cw_x + (cv * se_cw_x + c)

    labb = "YES" if lc_wx < 0 else "NO"
    lc_wx = max(lc_wx, 0)

    uabb = "YES" if uc_wx > 1 else "NO"
    uc_wx = min(uc_wx, 1)

    zwi = "YES" if uc_wx - lc_wx == 0 else "NO"

    return pd.DataFrame({
        'x': [x],
        'LCWx': [lc_wx],
        'UCWx': [uc_wx],
        'LABB': [labb],
        'UABB': [uabb],
        'ZWI': [zwi]
    })


# Example usage
'''x = 5
n = 5
alp = 0.05
c = 1 / (2 * n)

result = ci_cwd_x(x, n, alp, c)
print(result)'''
######################################################################################################


def cicscx(x, n, alp, c):
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if c is None:
        raise ValueError("'c' is missing")

    # Check that x is a positive integer between 0 and n
    if not isinstance(x, (int, float)) or x < 0 or x > n:
        raise ValueError("'x' has to be a positive integer between 0 and n")

    # Check that n is greater than 0
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")

    # Check that alpha is between 0 and 0.1
    if not (0 <= alp <= 0.1):
        raise ValueError("'alpha' has to be between 0 and 0.1")

    # Check that c is positive and within the specified range
    if c <= 0 or c > (1 / (2 * n)):
        raise ValueError("'c' has to be positive and less than or equal to 1/(2*n)")

    # Critical values
    cv = norm.ppf(1 - (alp / 2))
    cv1 = (cv ** 2) / (2 * n)
    cv2 = cv / (2 * n)

    # Score (Wilson) method
    p_cs_x = x / n
    se_cs_lx = np.sqrt((cv ** 2) - (4 * n * (c + c ** 2)) + (4 * n * p_cs_x * (1 - p_cs_x + 2 * c)))
    se_cs_ux = np.sqrt((cv ** 2) + (4 * n * (c - c ** 2)) + (4 * n * p_cs_x * (1 - p_cs_x - 2 * c)))

    l_cs_x = (n / (n + (cv ** 2))) * ((p_cs_x - c + cv1) - (cv2 * se_cs_lx))
    u_cs_x = (n / (n + (cv ** 2))) * ((p_cs_x + c + cv1) + (cv2 * se_cs_ux))

    labb = "YES" if l_cs_x < 0 else "NO"
    l_cs_x = max(l_cs_x, 0)

    uabb = "YES" if u_cs_x > 1 else "NO"
    u_cs_x = min(u_cs_x, 1)

    zwi = "YES" if u_cs_x - l_cs_x == 0 else "NO"

    return pd.DataFrame({
        'x': [x],
        'LCSx': [l_cs_x],
        'UCSx': [u_cs_x],
        'LABB': [labb],
        'UABB': [uabb],
        'ZWI': [zwi]
    })


# Example usage
'''x = 5
n = 5
alp = 0.05
c = 1 / (2 * n)

result = ci_csc_x(x, n, alp, c)
print(result)
'''
##########################################################################################
def cicasx(x, n, alp, c):
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if c is None:
        raise ValueError("'c' is missing")

    if not isinstance(x, (int, float)) or x < 0 or x > n:
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not (0 <= alp <= 1):
        raise ValueError("'alpha' has to be between 0 and 1")
    if c <= 0:
        raise ValueError("'c' has to be positive")

    # Calculate critical value
    cv = norm.ppf(1 - (alp / 2))

    # ARC-SINE METHOD
    p_ca_x = x / n
    se_ca_x = cv / np.sqrt(4 * n)

    # Calculate lower and upper confidence limits
    l_ca_x = (np.sin(np.arcsin(np.sqrt(p_ca_x)) - se_ca_x - c)) ** 2
    u_ca_x = (np.sin(np.arcsin(np.sqrt(p_ca_x)) + se_ca_x + c)) ** 2

    # Adjust lower and upper limits
    labb = "YES" if l_ca_x < 0 else "NO"
    l_ca_x = max(l_ca_x, 0)

    uabb = "YES" if u_ca_x > 1 else "NO"
    u_ca_x = min(u_ca_x, 1)

    zwi = "YES" if u_ca_x - l_ca_x == 0 else "NO"

    return pd.DataFrame({
        'x': [x],
        'LCAx': [l_ca_x],
        'UCAx': [u_ca_x],
        'LABB': [labb],
        'UABB': [uabb],
        'ZWI': [zwi]
    })


# Example usage
'''x = 5
n = 5
alp = 0.05
c = 1 / (2 * n)

result = ci_cas_x(x, n, alp, c)
print(result)'''
#########################################################################################################################################

def cicltx(x, n, alp, c):
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if c is None:
        raise ValueError("'c' is missing")

    if not isinstance(x, (int, float)) or x < 0 or x > n:
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not (0 <= alp <= 1):
        raise ValueError("'alpha' has to be between 0 and 1")
    if c < 0:
        raise ValueError("'c' has to be positive")

    # Calculate critical value
    cv = norm.ppf(1 - (alp / 2))

    # LOGIT-WALD METHOD
    if x == 0:
        p_clt_x = 0
        q_clt_x = 1
        lcl_t_x = 0
        ucl_t_x = 1 - ((alp / 2) ** (1 / n))
    elif x == n:
        p_clt_x = 1
        q_clt_x = 0
        lcl_t_x = (alp / 2) ** (1 / n)
        ucl_t_x = 1
    else:
        p_clt_x = x / n
        q_clt_x = 1 - p_clt_x
        logit_x = np.log(p_clt_x / q_clt_x)
        se_clt_x = np.sqrt(p_clt_x * q_clt_x / n)

        lcl_t_x = 1 / (1 + np.exp(-(logit_x - (cv / se_clt_x) - c)))
        ucl_t_x = 1 / (1 + np.exp(-(logit_x + (cv / se_clt_x) + c)))

    # Adjust limits
    labb = "YES" if lcl_t_x < 0 else "NO"
    lcl_t_x = max(lcl_t_x, 0)

    uabb = "YES" if ucl_t_x > 1 else "NO"
    ucl_t_x = min(ucl_t_x, 1)

    zwi = "YES" if ucl_t_x - lcl_t_x == 0 else "NO"

    return pd.DataFrame({
        'x': [x],
        'LCLTx': [lcl_t_x],
        'UCLTx': [ucl_t_x],
        'LABB': [labb],
        'UABB': [uabb],
        'ZWI': [zwi]
    })

#############################################################################################################



def cictwx(x, n, alp, c):
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if c is None:
        raise ValueError("'c' is missing")

    if not isinstance(x, (int, float)) or x < 0 or x > n:
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not (0 <= alp <= 1):
        raise ValueError("'alpha' has to be between 0 and 1")
    if c < 0:
        raise ValueError("'c' has to be positive")

    # MODIFIED t-WALD METHOD
    if x == 0 or x == n:
        p_ctw_x = (x + 2) / (n + 4)
    else:
        p_ctw_x = x / n

    def f1(p, n):
        return p * (1 - p) / n

    def f2(p, n):
        return (p * (1 - p) / (n ** 3) +
                (p + ((6 * n) - 7) * (p ** 2) +
                 (4 * (n - 1) * (n - 3) * (p ** 3)) -
                 (2 * (n - 1) * ((2 * n) - 3) * (p ** 4))) / (n ** 5) -
                (2 * (p + ((2 * n) - 3) * (p ** 2) - 2 * (n - 1) * (p ** 3))) / (n ** 4))

    dof_x = 2 * (f1(p_ctw_x, n) ** 2) / f2(p_ctw_x, n)
    cv_x = t.ppf(1 - (alp / 2), df=dof_x)
    se_ctw_x = cv_x * np.sqrt(f1(p_ctw_x, n))

    lctw_x = p_ctw_x - (se_ctw_x + c)
    uctw_x = p_ctw_x + (se_ctw_x + c)

    # Adjust limits
    labb = "YES" if lctw_x < 0 else "NO"
    lctw_x = max(lctw_x, 0)

    uabb = "YES" if uctw_x > 1 else "NO"
    uctw_x = min(uctw_x, 1)

    zwi = "YES" if uctw_x - lctw_x == 0 else "NO"

    return pd.DataFrame({
        'x': [x],
        'LCTWx': [lctw_x],
        'UCTWx': [uctw_x],
        'LABB': [labb],
        'UABB': [uabb],
        'ZWI': [zwi]
    })

#############################################################################################################


def cicallx(x, n, alp, c):
    # Input validation
    if x is None:
        raise ValueError("'x' is missing")
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if c is None:
        raise ValueError("'c' is missing")

    if not isinstance(x, (int, float)) or x < 0 or x > n or isinstance(x, bool):
        raise ValueError("'x' has to be a positive integer between 0 and n")
    if not isinstance(n, (int, float)) or n <= 0 or isinstance(n, bool):
        raise ValueError("'n' has to be greater than 0")
    if alp > 0.1 or alp < 0 or not isinstance(alp, (int, float)) or isinstance(alp, bool):
        raise ValueError("'alpha' has to be between 0 and .1")
    if not isinstance(c, (int, float)) or c < 0 or isinstance(c, bool):
        raise ValueError("'c' has to be positive")

    # Calling functions and creating DataFrames
    wald_ci_df = cicwdx(x, n, alp, c)
    arc_sine_ci_df = cicasx(x, n, alp, c)
    score_ci_df = cicscx(x, n, alp, c)
    wald_lci_df = cicltx(x, n, alp, c)
    wald_tci_df = cictwx(x, n, alp, c)

    # Adding method column
    wald_ci_df['method'] = "Wald"
    arc_sine_ci_df['method'] = "ArcSine"
    wald_lci_df['method'] = "Logit Wald"
    score_ci_df['method'] = "Score"
    wald_tci_df['method'] = "Wald-T"

    # Creating final DataFrame
    generic_1 = wald_ci_df[['method', 'x', 'LCWx', 'UCWx', 'LABB', 'UABB', 'ZWI']]
    generic_2 = arc_sine_ci_df[['method', 'x', 'LCAx', 'UCAx', 'LABB', 'UABB', 'ZWI']]
    generic_4 = score_ci_df[['method', 'x', 'LCSx', 'UCSx', 'LABB', 'UABB', 'ZWI']]
    generic_5 = wald_lci_df[['method', 'x', 'LCLTx', 'UCLTx', 'LABB', 'UABB', 'ZWI']]
    generic_6 = wald_tci_df[['method', 'x', 'LCTWx', 'UCTWx', 'LABB', 'UABB', 'ZWI']]

    # Renaming columns to match R output
    generic_1.columns = ['method', 'x', 'LowerLimit', 'UpperLimit', 'LowerAbb', 'UpperAbb', 'ZWI']
    generic_2.columns = ['method', 'x', 'LowerLimit', 'UpperLimit', 'LowerAbb', 'UpperAbb', 'ZWI']
    generic_4.columns = ['method', 'x', 'LowerLimit', 'UpperLimit', 'LowerAbb', 'UpperAbb', 'ZWI']
    generic_5.columns = ['method', 'x', 'LowerLimit', 'UpperLimit', 'LowerAbb', 'UpperAbb', 'ZWI']
    generic_6.columns = ['method', 'x', 'LowerLimit', 'UpperLimit', 'LowerAbb', 'UpperAbb', 'ZWI']

    # Concatenating all DataFrames
    final_df = pd.concat([generic_1, generic_2, generic_4, generic_5, generic_6], ignore_index=True)

    return final_df

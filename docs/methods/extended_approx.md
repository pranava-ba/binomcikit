---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Extended approximate intervals

Closed-form and near-closed-form intervals — fast (a whole table in one array expression) but, unlike
the {doc}`exact family <extended_exact>`, not *guaranteed* at every θ. All take the usual call:

```python
bk.ci(x=3, n=20, method="lr-star")        # one interval
bk.ci(n=20, method="lr-star")             # every x = 0..20
bk.limits(20, 0.05, "lr-star")            # just the two arrays — the fast path
```

## Use it — what is here

| `method=` | What it is | Reach for it when | Watch out for |
|---|---|---|---|
| `"lr-star"` | Barndorff-Nielsen's higher-order likelihood r\* — normal to *third* order | you want near-exact coverage with no discreteness repair | boundary rows use the exact one-sided closed forms |
| `"cressie-read"` (`lam=`) | the {term}`power divergence` family; `lam=1` *is* Wilson, `lam=0` *is* the LR interval | you want a one-parameter dial between Wilson and LR | `lam > -1` |
| `"score-cc"` | Wilson with continuity correction (Newcombe 4; PASS's "score-cc") | you need a *strictly conservative* approximation | the original `cicsc` port leaves x = 0, n uncorrected — this one does not |
| `"arcsine-anscombe"` | arcsine with continuity **and** Anscombe's correction (Pires & Amado XVII) | strictly conservative, essentially Clopper–Pearson's length | `clamp=False` follows the printed formula literally |
| `"arcsine-shifted"` | arcsine with an Anscombe 3/8-shifted centre, `(x + 3/8)/(n + 3/4)`, and width `z/(2√n)` | the arcsine used by DescTools and DBCI | not clamped at x = 0 / n, like the plain arcsine |
| `"modified-wilson"`, `"modified-jeffreys"` | Brown–Cai–DasGupta's boundary repairs | Wilson/Jeffreys behave oddly at x = 1, 2, n−1, n−2 | follows R `DescTools` exactly |
| `"pratt"` | Pratt's closed-form approximation to Clopper–Pearson | a CP-like interval with no beta quantiles | tracks exact CP to ≤ 1e-3 |
| `"soc"` | Cai's second-order-corrected score | the most symmetric one-sided coverage among approximations | ported from `binGroup` |
| `"cloglog"`, `"probit"` | Wald on the complementary-log-log / probit scale | rare events (cloglog) | asymmetric (cloglog) |
| `"freeman-tukey"` | double-arcsine, the meta-analysis standard | pooling proportions near 0 or 1 | under-covers at x = 0 |
| `"poisson"` | Garwood's Poisson interval | **rare events**, large n | conservative upper limit |
| `"wald-i"`, `"wald-i-cc"`, `"wald-recentred"`, `"wald-recentred-cc"` | Wald with exact boundary rows; recentred at the Wilson centre | teaching / comparing the Wald repairs | min coverage ≈ 0.83 — *not* conservative |
| `"analytic-percentile"`, `"analytic-bcp"` (+ `-cc`) | the percentile / bias-corrected bootstrap computed **exactly** | you want a bootstrap without Monte Carlo | |
| `"unif-wilson"`, `"split-wilson"` | Wilson on noise-smoothed data (Thulin 2014; Decrouez & Hall 2014) | damping the coverage saw-tooth | randomised (seeded) |

```{code-cell} python
import binomcikit as bk

bk.compare(
    x=3, n=20,
    methods=["wilson", "lr-star", "cressie-read", "score-cc", "arcsine-anscombe",
             "pratt", "soc", "modified-wilson", "exact"],
)
```

## Understand it

**Cressie–Read is a continuum.** The {term}`power divergence` statistic
$2/(\lambda(\lambda+1))\sum O[(O/E)^\lambda - 1]$ over the two cells (successes, failures) gives Pearson's
$\chi^2$ at $\lambda=1$ and the {term}`likelihood-ratio statistic` at $\lambda\to0$. The interval is the set
of θ where the statistic is at most $z^2$ — so these are *identities*, not approximations, and the test-suite
asserts them to machine precision:

```{code-cell} python
import numpy as np

n, a = 20, 0.05
cr1 = bk.ci(n=n, alpha=a, method="cressie-read", lam=1.0)
cr0 = bk.ci(n=n, alpha=a, method="cressie-read", lam=0.0)
print("lam=1 vs Wilson : max |diff| =", float(np.abs(cr1.LCRD - bk.cisc(n, a).LSC).max()))
print("lam=0 vs the LR interval: max |diff| =", float(np.abs(cr0.LCRD - bk.cilr(n, a).LLR).max()))
```

**r\* is the accurate one.** The ordinary signed likelihood-ratio root $r$ is standard normal only to first
order. Barndorff-Nielsen's $r^*=r+r^{-1}\log(q/r)$ — with $q$ the Wald statistic on the logit scale — is
normal to *third* order, which is why its coverage tracks the nominal level so closely *without* any
{term}`discreteness` correction:

```{code-cell} python
rec = bk.recommend(n=40, methods=["wald", "wilson", "lr", "lr-star", "cressie-read", "exact"])
rec[["method", "mean_coverage", "min_coverage", "mean_length"]].round(4)
```

**Pires & Amado's classification.** Of twenty methods, only Clopper–Pearson, **Score-cc** and
**arcsine-cc-Anscombe** keep their minimum coverage at or above $1-\alpha-0.005$ for every $n\ge10$ (their
"strictly conservative" group); Add-4 is the best of those that are only *correct on average*. Both claims are
reproduced here by exact enumeration:

```{code-cell} python
import scipy.stats as st

def min_mean_cov(method, n, a=0.05):
    lo, hi = bk.limits(n, a, method)
    th = np.linspace(1e-4, 1 - 1e-4, 4000)
    pm = st.binom.pmf(np.arange(n + 1)[None, :], n, th[:, None])
    cov = (pm * ((lo[None, :] < th[:, None]) & (th[:, None] < hi[None, :]))).sum(axis=1)
    return round(float(cov.min()), 4), round(float(cov.mean()), 4)

for m in ["exact", "score-cc", "arcsine-anscombe", "wilson", "wald-i"]:
    print(f"{m:18s} n=40  (min, mean) coverage =", min_mean_cov(m, 40))
```

:::{admonition} A defect we found upstream
:class: warning
`DescTools::BinomCI(method="pratt")` — and the Python package `DBCI`, which copies it — compute the **lower**
limit from an expression that drifts from exact Clopper–Pearson by up to **0.13** (n = 20, x near n).
binomcikit uses the mirror construction $L(x)=1-U(n-x)$, accurate to ≤ 1e-3. `DBCI`'s modified-Wilson upper limit
near x = n is also wrong (at n = 60, x = 59 it returns an upper limit *below* its lower limit). Both are
pinned by tests so the discrepancy cannot silently return.
:::

## References

Barndorff-Nielsen (1986), *Biometrika* 73 · Brazzale, Davison & Reid (2007), *Applied Asymptotics* · Cressie &
Read (1984), *JRSS-B* 46 · Newcombe (1998), *Stat. Med.* 17 · Pires & Amado (2008), *REVSTAT* 6 · Cai (2005),
*JSPI* 131 · Brown, Cai & DasGupta (2001), *Statist. Sci.* 16 · Pratt (1968), *JASA* 63 · Garwood (1936),
*Biometrika* 28 · Thulin (2014), arXiv:1402.6536 · Decrouez & Hall (2014).

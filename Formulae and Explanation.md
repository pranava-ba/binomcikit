# Estimation Methods for Single Binomial Proportion

Here are several estimation procedures used to estimate a single binomial proportion:

1. **Wald Interval**
2. **Wald-T Interval**
3. **Likelihood Interval (Exact Method)**
4. **Score Interval (Wilson Interval)**
5. **Logit-Wald Interval**
6. **ArcSine Interval**

Each of these methods has its strengths and weaknesses, depending on the sample size, the observed proportion, and the desired accuracy. The choice of method depends on the specific characteristics of the data and the goals of the analysis.

---

## 1. Wald Interval (Normal Approximation)

### Mathematical Formulation:
For a binomial proportion $p$, the point estimate is $\hat{p} = \frac{x}{n}$, and the confidence interval is:

$\hat{p} \pm z_{\alpha/2} \sqrt{\frac{\hat{p}(1 - \hat{p})}{n}}$

Where:
- $\hat{p}$ is the sample proportion,
- $z_{\alpha/2}$ is the critical value from the standard normal distribution,
- $n$ is the sample size.

### Key Issues:
- **Aberrations (Violations of 0 and 1)**: If $x = 0$ or $x = n$, then $\hat{p} = 0$ or $\hat{p} = 1$, respectively, which may result in overly narrow or non-viable confidence intervals, or intervals that fail to capture any uncertainty about the true proportion (since $\hat{p}$ is at the extremes).
- **Continuity Correction**: A continuity correction can be applied to make the normal approximation more accurate for small $n$ or when $\hat{p}$ is near 0 or 1. This correction involves adjusting $x$ by $\pm 0.5$ to account for the discrete nature of the binomial distribution:
  
  $\hat{p} \pm z_{\alpha/2} \sqrt{\frac{(\hat{p} \pm 0.5)(1-\hat{p} \pm 0.5)}{n}}$
  
  This adjustment helps smooth out the potential distortions caused by extreme proportions.

---

## 2. Wald-T Interval

### Mathematical Formulation:
The Wald-T interval uses the t-distribution instead of the normal distribution:

$\hat{p} \pm t_{\alpha/2} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$

Where $t_{\alpha/2}$ is the critical value from the t-distribution with $n-1$ degrees of freedom.

### Key Issues:
- **Aberrations (Violations of 0 and 1)**: As with the Wald interval, $\hat{p} = 0$ or $\hat{p} = 1$ lead to intervals that are not informative or properly reflect the uncertainty in the estimate.
- **Continuity Correction**: Continuity correction can still be applied in the Wald-T method if the sample size is small or if the sample proportion is near the boundaries (0 or 1).

---

## 3. Likelihood Interval (Exact Method)

### Mathematical Formulation:
The Likelihood interval is constructed by finding the range of values for $p$ for which the likelihood ratio remains within a critical value. For a binomial distribution, the likelihood function is:

$L(p) = \binom{n}{x} p^x (1-p)^{n-x}$

The confidence interval is derived by comparing the likelihood at different values of $p$ to the maximum likelihood.

### Key Issues:
- **Aberrations (Violations of 0 and 1)**: This method does not suffer from the boundary issues that affect the Wald method because it is exact and uses the binomial distribution directly. As such, the resulting intervals are well-behaved even for $\hat{p} = 0$ or $\hat{p} = 1$.
- **Continuity Correction**: Since the Likelihood method is exact and does not rely on normal approximation, it does not require a continuity correction. This makes it robust for small $n$ or extreme values of $\hat{p}$.

---

## 4. Score Interval (Wilson Interval)

### Mathematical Formulation:
The Wilson score interval is given by:

$\hat{p} \pm \frac{z_{\alpha/2}}{2n} \left( 1 \pm \sqrt{1 + \frac{4 \hat{p}(1 - \hat{p})}{n z_{\alpha/2}^2}} \right)$

Where $\hat{p}$ is the sample proportion, and $z_{\alpha/2}$ is the critical value from the normal distribution.

### Key Issues:
- **Aberrations (Violations of 0 and 1)**: The Wilson interval is less prone to issues at the boundaries compared to the Wald interval. It is particularly useful for small sample sizes and extreme values of $\hat{p}$, as it provides a more reliable confidence interval in such cases.
- **Continuity Correction**: The Wilson interval generally performs well without the need for a continuity correction. It is based on a more accurate score test, so it tends to be more robust than the Wald method, especially when $\hat{p}$ is near 0 or 1.

---

## 5. Logit-Wald Interval

### Mathematical Formulation:
The Logit-Wald interval involves applying the logit transformation to $\hat{p}$, followed by constructing the confidence interval using the Wald method on the transformed scale:

$\text{logit}(\hat{p}) = \log\left(\frac{\hat{p}}{1 - \hat{p}}\right)$

The confidence interval for $\text{logit}(\hat{p})$ is then constructed using the Wald method, and the interval is transformed back to the original proportion scale:

$\hat{p} = \frac{e^{\hat{\theta}}}{1 + e^{\hat{\theta}}}$

Where $\hat{\theta}$ is the point estimate on the logit scale.

### Key Issues:
- **Aberrations (Violations of 0 and 1)**: The logit transformation maps $\hat{p}$ into an unbounded scale, which helps to reduce the issues that arise when $\hat{p}$ is at 0 or 1, making this method more reliable for extreme values of $\hat{p}$.
- **Continuity Correction**: A continuity correction is less commonly applied in the Logit-Wald method because the logit transformation inherently stabilizes the variance for extreme values. However, it may still be beneficial for very small sample sizes.

---

## 6. ArcSine Interval (Transformation Method)

### Mathematical Formulation:
The ArcSine interval is constructed using the arcsine transformation of $\hat{p}$, which stabilizes the variance for proportions near 0 or 1. The transformation is:

$\text{ArcSine}(\hat{p}) = \sin^{-1}\left(\sqrt{\hat{p}}\right)$

The confidence interval is constructed on the transformed scale, and then transformed back to the proportion scale:

$\hat{p} = \sin^2\left(\frac{\text{ArcSine}(\hat{p})}{2}\right)$

### Key Issues:
- **Aberrations (Violations of 0 and 1)**: The arcsine transformation stabilizes variance and is particularly useful when $\hat{p}$ is near 0 or 1. The resulting confidence intervals are more reasonable for extreme values.
- **Continuity Correction**: The arcsine transformation is designed to reduce variance issues at the extremes. While continuity corrections are not typically necessary for the arcsine method, small sample sizes or proportions close to 0 or 1 may still benefit from a slight adjustment to the confidence interval.

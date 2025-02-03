# BINOMCIKIT

## Introduction
In many statistical problems, we are interested in estimating the proportion of successes in a binomial process. For example, if you flip a coin 100 times and observe 55 heads, you might want to estimate the true proportion of heads for that coin. This is known as estimating a **binomial proportion**.

Estimating a single binomial proportion is a fundamental problem in statistics that applies to a wide range of real-world scenarios. In many fields, we encounter situations where we need to estimate the proportion of successes (or failures) in a fixed number of independent trials, with each trial having only two possible outcomes, such as success or failure, yes or no, pass or fail. This estimation problem is central to various industries, from healthcare to business to manufacturing.

## Estimation Methods for Single Binomial Proportion

There are several estimation procedures used to estimate a single binomial proportion:

1. **Wald Interval**
2. **Wald-T Interval**
3. **Likelihood Interval (Exact Method)**
4. **Score Interval (Wilson Interval)**
5. **Logit-Wald Interval**
6. **ArcSine Interval**

Each of these methods has its strengths and weaknesses, depending on the sample size, the observed proportion, and the desired accuracy. The choice of method depends on the specific characteristics of the data and the goals of the analysis.

---

## Summary Table with Additional Notes on Aberrations and Continuity Corrections</font>

| Method             | Formula                                                   | Key Issues/Considerations                                    |
|--------------------|-----------------------------------------------------------|--------------------------------------------------------------|
| **Wald Interval**   | $\hat{p} \pm z_{\alpha/2} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$ | Issues with $\hat{p} = 0$ or $\hat{p} = 1$; continuity correction helps in small $n$ |
| **Wald-T Interval** | $\hat{p} \pm t_{\alpha/2} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$ | Better for small $n$; still struggles with extreme $\hat{p}$; continuity correction can help |
| **Likelihood Interval** | Based on likelihood ratio test                              | Exact method, no issues with boundary values (0 or 1), no need for continuity correction |
| **Score Interval**  | $\hat{p} \pm \frac{z_{\alpha/2}}{2n} \left( 1 \pm \sqrt{1 + \frac{4 \hat{p}(1-\hat{p})}{n z_{\alpha/2}^2}} \right)$ | Robust for small $n$, less affected by $\hat{p} = 0$ or $\hat{p} = 1$; no continuity correction needed |
| **Logit-Wald**      | Logit transform followed by Wald method                     | Helps with extreme $\hat{p}$; no continuity correction required, but check for small sample sizes |
| **ArcSine**         | $\hat{p} = \sin^2\left(\frac{\text{ArcSine}(\hat{p})}{2}\right)$ | Helps stabilize variance at extremes (0 or 1); no need for continuity correction for most cases |

---

## Naming convention for Methods

We use "ci" in the start of each function name to indicate that the "Confidence Interval" is being called.

We then call the method used by first calling "ci", followed by the Naming Convention used.
(ci is the prefix).

### **Example Usage:**
"cias" - Confidence Interval called using the ArcSine Method

The names used to call each of the methods are listed below:

| Method Name | Naming Convention Used |
|------------|-------------------------|
| 1. **Wald Interval** | wd |
| 2. **Wald-T Interval** | tw |
| 3. **Likelihood Interval (Exact Method)** | lr |
| 4. **Score Interval (Wilson Interval)** | sc |
| 5. **Logit-Wald Interval** | lt |
| 6. **ArcSine Interval** | as |
| 7. **Exact** | ex |
| 8. **All** | all |

## Naming Convention for Submethods

We use the submethod name to specify what sub-type of method is being called.

We then call the method used by first calling "ci{method name}", followed by the Naming Convention used.
(ci{method name} is the prefix).

### **Example Usage:**
"ciasx" - Adjusted Score Method of Confidence Interval called using the ArcSine Method

The names used to call each of the sub-methods/type of method are listed below:

| Type of Method | Naming Convention Used | Where it is called | Example |
|------------|-------------------------|--|--|
| 1. **Base Method** | x | postfix | ciwdx |
| 2. **Adjusted Method** | a | prefix | ciawd | 
| 3. **Adjusted X Method** | a_x | prefix **and** postfix | ciawdx |
| 4. **Continuity Corrected** | c | prefix | cicwd |
| 3. **Continuity Corrected X** | c_x | prefix **and** postfix | cicwdx |

## Naming convention for plots

Just add "plot" prefix before ci{methodname} to print the plot

### **Example Usage:** 
"plotciwdx" - plots the Based Method of Confidence Interval called using the Wald Methos

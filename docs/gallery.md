# Gallery

Every numeric function in `binomcikit` has a plotting counterpart (add the
`plot` prefix). Each returns a [plotnine](https://plotnine.org) `ggplot` you can
display, save, or add layers to. A selection is shown below; the code above each
image reproduces it.

## Confidence intervals

```python
bk.plotciall(20, 0.05)
```
![All six confidence-interval methods for x = 0..20](_static/gallery/ci_all.png)

```python
bk.plotciallg(20, 0.05)
```
![All methods, faceted by method](_static/gallery/ci_all_faceted.png)

```python
bk.plotciwd(20, 0.05)
```
![Wald intervals (a single method)](_static/gallery/ci_wald.png)

```python
bk.plotciallx(7, 20, 0.05)
```
![All methods for a single observed count, x = 7 of 20](_static/gallery/ci_all_x.png)

```python
bk.plotciba(20, 0.05, a=1, b=1)
```
![Bayesian credible intervals — quantile vs HPD](_static/gallery/ci_bayes.png)

## Coverage probability

```python
bk.plotcovpall(15, 0.05, a=1, b=1, t1=0.9, t2=0.97, seed=0)
```
![Coverage probability of all base methods against p](_static/gallery/covp_all.png)

```python
bk.plotcovpwd(15, 0.05, a=1, b=1, t1=0.9, t2=0.97, seed=0)
```
![Wald coverage vs the nominal 1 - alpha line](_static/gallery/covp_wald.png)

```python
bk.plotcovpba(15, 0.05, a=1, b=1, t1=0.9, t2=0.97, a1=0.5, a2=0.5, seed=0)
```
![Bayesian coverage — quantile and HPD intervals](_static/gallery/covp_bayes.png)

## Expected length

```python
bk.plotexplall(15, 0.05, a=1, b=1, seed=0)
```
![Expected interval length of all base methods](_static/gallery/expl_all.png)

```python
bk.plotlengthall(15, 0.05, a=1, b=1, seed=0)
```
![Sum of interval lengths by method](_static/gallery/length_all.png)

## p-confidence & p-bias

```python
bk.plotpcopbiall(20, 0.05)
```
![p-confidence and p-bias across methods](_static/gallery/pconf_all.png)

## Error & long-term power

```python
bk.ploterrall(20, 0.05, phi=0.5, f=-2)
```
![Error and long-term power by method, coloured by pass/fail](_static/gallery/err_all.png)

---

*Gallery images are produced by `tools/render_gallery.py`.*

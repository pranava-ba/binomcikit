---
name: Bug report
about: A wrong interval, an error, or behaviour that contradicts the docs
title: "[BUG] "
labels: bug
---

**What happened**
The smallest call that shows it, for example:

```python
import binomcikit as bk
bk.interval(3, 20, 0.05, "wilson")
```

**What you expected, and where that comes from**
A reference value helps most: another library's output, a published table, or the definition the result should satisfy.

**What you got**
The output or the full traceback.

**Versions**
```
python -c "import binomcikit, numpy, scipy, pandas; print(binomcikit.__version__, numpy.__version__, scipy.__version__, pandas.__version__)"
```
OS:

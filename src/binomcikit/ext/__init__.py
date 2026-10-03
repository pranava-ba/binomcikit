"""Extended confidence-interval methods beyond the original R ``proportion`` port.

Every function is a *limit-producer* with the same contract as the original ``ci*``
functions -- ``ci<name>(n, alp)`` returns the ``(n+1)``-row table and ``ci<name>x(x, n, alp)``
one row -- so the whole evaluation engine consumes them unchanged. They are grouped by
construction:

``closed_form``
    Pratt, complementary log-log, probit, modified Wilson, modified Jeffreys, Garwood
    (Poisson), Freeman-Tukey, second-order corrected (SOC).
``bounds``
    Concentration-inequality intervals with guaranteed coverage: Hoeffding, Chernoff-KL,
    Bernstein, empirical Bernstein.
``likelihood``
    The Cressie-Read power-divergence family and the higher-order likelihood ``r*``.
``exact``
    Sterne, Blyth-Still-Casella, optimal locally correct (OLC), and Witting's randomised
    exact interval.
``betting``
    Betting / confidence-sequence intervals: beta-binomial mixture, normal mixture, hedged
    betting (derandomised) and the streaming :func:`cibetseq`.
``pires``
    The rest of Pires & Amado's (2008) twenty methods: Wald-I and its recentred forms, the
    analytic percentile / bias-corrected bootstraps, and arcsine-cc-Anscombe.
``adjusted``
    Thulin's coverage-adjusted Clopper-Pearson, and the noise-smoothed (uniform / split-sample)
    Wilson intervals.
"""

from .adjusted import (
    cigcp,
    cigcpx,
    cisplitwilson,
    cisplitwilsonx,
    ciunifwilson,
    ciunifwilsonx,
)
from .betting import (
    cibetseq,
    cibetting,
    cibettingx,
    cimixture,
    cimixturex,
    cinormalmix,
    cinormalmixx,
)
from .bounds import (
    cibernstein,
    cibernsteinx,
    ciempbern,
    ciempbernx,
    cihoeffding,
    cihoeffdingx,
    cikl,
    ciklx,
)
from .closed_form import (
    cicloglog,
    cicloglogx,
    cifreemantukey,
    cifreemantukeyx,
    cimodjeffreys,
    cimodjeffreysx,
    cimodwilson,
    cimodwilsonx,
    cipoisson,
    cipoissonx,
    ciprat,
    cipratx,
    ciprobit,
    ciprobitx,
    cisoc,
    cisocx,
)
from .criteria import locally_correct
from .exact import (
    cibsc,
    cibscx,
    ciolc,
    ciolcx,
    cisterne,
    cisternex,
    ciwitting,
    ciwittingx,
)
from .likelihood import cicressieread, cicressiereadx, cilrstar, cilrstarx
from .pires import (
    ciarcsineans,
    ciarcsineansx,
    cibcp,
    cibcpcc,
    cibcpccx,
    cibcpx,
    cibootp,
    cibootpcc,
    cibootpccx,
    cibootpx,
    ciscorecc,
    ciscoreccx,
    ciwaldi,
    ciwaldicc,
    ciwaldiccx,
    ciwaldix,
    ciwaldrec,
    ciwaldreccc,
    ciwaldrecccx,
    ciwaldrecx,
)

__all__ = sorted(_n for _n in dir() if _n.startswith("ci") and callable(globals()[_n]))

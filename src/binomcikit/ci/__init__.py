"""1xx family: Confidence intervals for a single binomial proportion.

base / adjusted / continuity-corrected methods, for all x (given n) and for a
single given x, plus their plotting counterparts.
"""
from .adj_n import ciaall, ciaas, cialr, cialt, ciasc, ciatw, ciawd
from .adj_n_graph import (
    plotciaas,
    plotcialr,
    plotcialt,
    plotciasc,
    plotciatw,
    plotciawd,
)
from .adj_n_x import (
    ciaallx,
    ciaasx,
    cialrx,
    cialtx,
    ciascx,
    ciatwx,
    ciawdx,
)
from .all_graph import (
    plotciaall,
    plotciaallg,
    plotciaallx,
    plotciaallxg,
    plotciall,
    plotciallg,
    plotciba,
    plotcicall,
    plotcicallg,
    plotcicallx,
    plotcicallxg,
)
from .base_n import ciall, cias, ciex, cilr, cilt, cisc, citw, ciwd
from .base_n_graph import (
    plotcias,
    plotciex,
    plotcilr,
    plotcilt,
    plotcisc,
    plotcitw,
    plotciwd,
)
from .base_n_x import (
    ciallx,
    ciasx,
    ciexx,
    cilrx,
    ciltx,
    ciscx,
    citwx,
    ciwdx,
)
from .base_n_x_graph import plotciallx, plotciallxg, plotciexx
from .bayes_n import ciba
from .bayes_n_x import cibax
from .cc_n import cicall, cicas, ciclt, cicsc, cictw, cicwd
from .cc_n_graph import (
    plotcicas,
    plotciclt,
    plotcicsc,
    plotcictw,
    plotcicwd,
)
from .cc_n_x import (
    cicallx,
    cicasx,
    cicltx,
    cicscx,
    cictwx,
    cicwdx,
)

# Public API = every function bound above (excludes submodules and internal
# helpers, which stay reachable via their defining module).
__all__ = sorted(_n for _n in dir() if not _n.startswith("_")
                 and callable(globals()[_n]))

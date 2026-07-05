"""1xx family: Confidence intervals for a single binomial proportion.

base / adjusted / continuity-corrected methods, for all x (given n) and for a
single given x, plus their plotting counterparts.
"""
from .base_n import ciwd, cisc, cias, cilr, ciex, citw, cilt, ciall
from .base_n_x import (
    ciwdx, ciscx, ciasx, cilrx, ciexx, ciltx, citwx, ciallx,
)
from .base_n_graph import (
    plotciwd, plotcisc, plotcias, plotcilr, plotcitw, plotcilt, plotciex,
)
from .base_n_x_graph import plotciexx, plotciallx, plotciallxg
from .adj_n import ciawd, ciasc, ciaas, cialr, ciatw, cialt, ciaall
from .adj_n_graph import (
    plotciawd, plotciasc, plotciaas, plotcialr, plotciatw, plotcialt,
)
from .adj_n_x import (
    ciawdx, ciascx, ciaasx, cialrx, ciatwx, cialtx, ciaallx,
)
from .cc_n import cicwd, cicsc, cicas, ciclt, cictw, cicall
from .cc_n_graph import (
    plotcicwd, plotcicsc, plotcicas, plotciclt, plotcictw,
)
from .cc_n_x import (
    cicwdx, cicscx, cicasx, cicltx, cictwx, cicallx,
)
from .bayes_n import ciba
from .bayes_n_x import cibax
from .all_graph import (
    plotciall, plotciallg, plotciaall, plotciaallg, plotciaallx, plotciaallxg,
    plotcicall, plotcicallg, plotcicallx, plotcicallxg, plotciba,
)

# Public API = every function bound above (excludes submodules and internal
# helpers, which stay reachable via their defining module).
__all__ = sorted(_n for _n in dir() if not _n.startswith("_")
                 and callable(globals()[_n]))

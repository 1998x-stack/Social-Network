"""netlab —— 网络的配套共享核心库。"""
from .graph_utils import adjacency_matrix, degree_sequence
from .logging_setup import setup_logging
from .plotting import configure, new_figure, save_fig

__version__ = "0.1.0"

__all__ = [
    "setup_logging",
    "configure",
    "new_figure",
    "save_fig",
    "adjacency_matrix",
    "degree_sequence",
    "__version__",
]
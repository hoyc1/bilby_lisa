# Licensed under an MIT style license -- see LICENSE.md

__author__ = ["Charlie Hoy <charlie.hoy@ligo.org>"]

try:
    from ._version import version as __version__
except ModuleNotFoundError:  # development mode
    __version__ = "unknown"

import bilby
import bilby_pipe
import parallel_bilby

# check the bilby, bilby_pipe and parallel_bilby installations
error_str = (
    "`bilby_lisa` currently requires a non-released version of `{}` "
    "(you have {} installed currently). Please read the README.md file "
    "in the source repository for full installation instructions"
)
if "f027394" not in bilby.__version__:
    raise ImportError(
        error_str.format('bilby', bilby.__version__)
    )
if "581eb9a" not in bilby_pipe.__version__:
    raise ImportError(
        error_str.format('bilby_pipe', bilby_pipe.__version__)
    )
if "e4e2f7b" not in parallel_bilby.__version__:
    raise ImportError(
        error_str.format('parallel_bilby', parallel_bilby.__version__)
    )

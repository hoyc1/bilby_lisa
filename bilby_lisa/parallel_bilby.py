# Licensed under an MIT style license -- see LICENSE.md

from .bilby_pipe import DataGenerationInput
from parallel_bilby.generation import (
    ParallelBilbyDataGenerationInput as _DGInput
)

__author__ = ["Charlie Hoy <charlie.hoy@ligo.org>"]


class ParallelBilbyDataGenerationInput(DataGenerationInput, _DGInput):
    """Extends ParallelBilbyDataGenerationInput to include additional
    options for LISA
    """
    pass


def create_generation_parser():
    """Extends the BilbyArgParser for bilby_pipe to include additional
    options for LISA
    """
    from parallel_bilby.parser.generation import create_generation_parser
    from .parser import add_LISA_options_to_parser
    parser = create_generation_parser()
    parser = add_LISA_options_to_parser(parser)
    # change the defaults for LISA data analysis
    parser.set_defaults(
        generation_executable_parser=(
            "bilby_lisa.parallel_bilby.create_generation_parser"
        ),
        generation_input_class=(
            "bilby_lisa.parallel_bilby.ParallelBilbyDataGenerationInput"
        ),
    )
    return parser

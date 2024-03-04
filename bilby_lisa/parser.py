# Licensed under an MIT style license -- see LICENSE.md

__author__ = ["Charlie Hoy <charlie.hoy@ligo.org>"]


def add_LISA_options_to_parser(parser):
    """Extends an argparse.ArgumentParser object to include custom arguments
    for LISA data analysis

    Parameters
    ----------
    parser: argparse.ArgumentParser
        parser to add arguments too
    """
    lisa_parser = parser.add_argument_group(
        "LISA arguments",
        description="Arguments specific to LISA data analysis"
    )
    lisa_parser.add(
        "--tdi",
        action="append",
        help=(
            "TDI variables to use. If given in ini file, TDI variables are "
            "specified by `tdi=[A, E, T]`. If given at the comment line, TDI "
            "variables are specified as `--tdi A --tdi E --tdi T`"
        ),
        default=None
    )
    return parser

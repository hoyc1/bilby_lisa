# Licensed under an MIT style license -- see LICENSE.md

from bilby_pipe.utils import logger

__author__ = ["Charlie Hoy <charlie.hoy@ligo.org>"]
version_error_string = (
    "`bilby_lisa` currently requires a non-released version of `{}` "
    "(you have {} installed currently). Please read the README.md file "
    "in the source repository for full installation instructions"
)


def get_warning():
    """Print a warning highlighting that the user is using unreviewed code
    """
    logger.warning(
        "bilby_lisa has been installed, and this is currently unreviewed code"
    )


def get_version_info():
    """Print the version of `bilby`, `bilby_pipe` and `bilby_lisa` currently
    installed
    """
    import bilby_lisa
    logger.info(f"Running bilby_lisa version: {bilby_lisa.__version__}")


def AET_from_XYZ(data, channels=["A", "E", "T"]):
    """Transform from XYZ to AET representation

    Parameters
    ----------
    data: dict
        dictionary of data containing the X, Y and Z channels.
    channels: list, optional
        list of channels that you would like output
    """
    _channels = [_.upper() for _ in channels]
    _data = {}
    if any(c not in ["A", "E", "T"] for c in _channels):
        raise ValueError("output channels must be A, E or T")
    if "A" in _channels:
        if not all(c in data.keys() for c in ["X", "Z"]):
            raise ValueError(
                "Please provide data for the X and Z channels to convert into "
                "the A channel"
            )
        _data["A"] = (data["Z"] - data["X"]) / 2**0.5
    if ("E" in _channels) or ("T" in _channels):
        if not all(c in data.keys() for c in ["X", "Y", "Z"]):
            raise ValueError(
                "Please provide data for the X, Y and Z channels to convert "
                "into the E and T channels"
            )
        if "E" in _channels:
            _data["E"] = (data["X"] - 2 * data["Y"] + data["Z"]) / 6**0.5
        if "T" in _channels:
            _data["T"] = (data["X"] + data["Y"] + data["Z"]) / 3**0.5
    return _data

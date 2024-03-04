# Licensed under an MIT style license -- see LICENSE.md

from bilby.gw.detector.networks import (
    InterferometerList as _InterferometerList, get_empty_interferometer
)
from .interferometer import LISAChannel

__author__ = ["Charlie Hoy <charlie.hoy@ligo.org>"]


class InterferometerList(_InterferometerList):
    """Class to handle a list of interferometers, inherited from
    bilby.gw.detector.networks.InterferometerList. This class
    extends the init to allow the user to pass "LISA", which
    although is a single detector, it can be thought of as three
    interferometers

    Parameters
    ----------
    interferometers: list
        list of interferometers to store in the InterferometerList
        object
    """
    def __init__(self, interferometers):
        try:
            super().__init__(interferometers)
        except TypeError as e:
            EDOM = ("not all Interferometer objects" in e.args[0])
            if not EDOM:
                raise
            for ifo in interferometers:
                if isinstance(ifo, str):
                    ifo = get_empty_interferometer(ifo)
                # check to see if a detector is itself an InterferometerList,
                # i.e. LISA
                if isinstance(ifo, InterferometerList):
                    for _ifo in ifo:
                        self.append(_ifo)
            self._check_interferometers()


class LISA(InterferometerList):
    """Class to handle the LISA detector. As TDI creates 3 virtual
    interferometers, we interpret LISA as a network of 3 inteferometers, each
    labelled by their TDI variable name.

    Parameters
    ----------
    name: str
        name of the detector
    tdi: list, optional
        list of TDI variables to consider. Default ['A', 'E', 'T']
    """
    def __init__(self, name, tdi=["A", "E", "T"]):
        if len(tdi) != 3:
            raise ValueError("Please specify 3 TDI channels")
        for chnl in tdi:
            self.append(LISAChannel(f"LISA_{chnl}"))

    @property
    def strain_data(self):
        # create a dummpy strain_data property to prevent errors downstream
        # in reality the strain data is stored in each LISA channel
        from bilby.gw.detector.strain_data import InterferometerStrainData
        return InterferometerStrainData()

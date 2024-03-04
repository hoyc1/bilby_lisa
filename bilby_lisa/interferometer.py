# Licensed under an MIT style license -- see LICENSE.md

from bilby.gw.detector.interferometer import Interferometer

__author__ = ["Charlie Hoy <charlie.hoy@ligo.org>"]


class LISAChannel(Interferometer):
    """Class to handle the virtual interferometers associated with
    the LISA detector

    Parameters
    ----------
    name: str
        name of the virtual interferometer. For the A, E and T channels
        this will typically be LISA_A, LISA_E and LISA_T
    power_spectral_density: bilby.gw.detector.PowerSpectralDensity
        Power spectral density determining the sensitivity of the detector.
    minimum_frequency: float, optional
        Minimum frequency to analyse for detector. Default 1e-4
    maximum_frequency: float, optional
        Maximum frequency to analyse for detector. Default 1e-1
    """
    def __init__(
        self, name, power_spectral_density=None, minimum_frequency=1e-4,
        maximum_frequency=1e-1
    ):
        from bilby.gw.detector.strain_data import InterferometerStrainData
        self.name = name
        self.strain_data = InterferometerStrainData(
            minimum_frequency=minimum_frequency,
            maximum_frequency=maximum_frequency
        )
        self.power_spectral_density = power_spectral_density
        self.meta_data = {}

    def get_detector_response(
        self, waveform_polarizations, parameters, **kwargs
    ):
        # For LISA, the detector response should be calculated as part of the
        # waveform generation
        return waveform_polarizations[self.name]

    def __repr__(self, *args, **kwargs):
        name = self.__class__.__name__
        description = (
            '(name=\'{}\', power_spectral_density={}, minimum_frequency={}, '
            'maximum_frequency={})'.format(
                self.name, self.power_spectral_density,
                float(self.strain_data.minimum_frequency),
                float(self.strain_data.maximum_frequency)
            )
        )
        return name + description

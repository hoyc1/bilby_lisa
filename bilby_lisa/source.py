# Licensed under an MIT style license -- see LICENSE.md

from bbhx.utils.transform import LISA_to_SSB
from bilby.core import utils

__author__ = ["Charlie Hoy <charlie.hoy@ligo.org>"]


class LISAPolarizationDict(dict):
    """A small wrapper class for the core dict object which returns the
    first element in the dictionary if "plus" is called. This was needed
    as bilby often requires a plus polarisation to be in the waveform
    dictionary, see e.g. the RelativeBinningGravitationalWaveTransient
    likelihood. However, for LISA applications, we do not have a plus
    polarisation.
    """
    def __getitem__(self, key):
        if key == "plus":
            return list(self.values())[0]
        return super().__getitem__(key)


def lisa_binary_black_hole(
    frequency_array, mass_1, mass_2, luminosity_distance, chi_1, chi_2,
    theta_jn, phase, ra, dec, psi, geocent_time, **kwargs
):
    """A Binary Black Hole waveform model for use with the LISA observatory. We
    interact with the BBHx package.

    Parameters
    ----------
    frequency_array: array_like
        The frequencies at which we want to calculate the waveform
    mass_1: float
        The mass of the heavier object in solar masses
    mass_2: float
        The mass of the lighter object in solar masses
    luminosity_distance: float
        The luminosity distance in megaparsec
    chi_1: float
        The primary spin component aligned with the orbital angular momentum
    chi_2: float
        The secondary spin component aligned with the orbital angular momentum
    theta_jn: float
        Angle between the total binary angular momentum and the line of sight
    phase: float
        The phase of the waveform
    ra: float
        The ecliptic longitude of the source (we use 'ra' to remain consistent
        with existing models in `bilby`). The ecliptic longitude measures the
        distance north or south of the ecliptic
    dec: float
        The ecliptic latitude of the source (we use 'dec' to remain consistent
        with existing models in `bilby`). The ecliptic latitude is measured
        from the first point of Aries and along the ecliptic rather than the
        celestial equator
    psi: float
        The polarization of the source
    geocent_time: float
        The merger time of the source
    kwargs: dict
        Optional keyword arguments
        Supported arguments:

        - reference_frequency
        - minimum_frequency,
        - maximum_frequency
        - catch_waveform_errors
        - mode_array
        - ifos
        - direct
        - fill
        - squeeze
        - length
        - compress
        - shift_t_limits
        - t_obs_start
        - t_obs_end
        - reference_frame
        - waveform_approximant
        - relative
        - pn_spin_order
        - pn_tidal_order
        - pn_phase_order
        - pn_amplitude_order
    """
    _implemented_channels = ["LISA_A", "LISA_E", "LISA_T"]
    waveform_kwargs = dict(
        reference_frequency=0.0, minimum_frequency=1e-4,
        maximum_frequency=frequency_array[-1], catch_waveform_errors=False,
        mode_array=None, ifos=_implemented_channels, t_obs_start=1.0,
        t_obs_end=0.0, reference_frame='LISA',
        waveform_approximant="BBHx_IMRPhenomD", relative=False,
    )
    waveform_kwargs.update(kwargs)
    if isinstance(waveform_kwargs["mode_array"], tuple):
        waveform_kwargs["mode_array"] = list(waveform_kwargs["mode_array"])
    _channels_to_calculate = [
        _ for _ in waveform_kwargs["ifos"] if _ in _implemented_channels
    ]
    _base_error = (
        f"You requested TDI channels: {waveform_kwargs['ifos']} but only "
        f"{_implemented_channels} are currently implemented."
    )
    if not len(_channels_to_calculate):
        raise ValueError(
            f"{_base_error}. Unable to calculate waveforms for the requested "
            f"TDI channels"
        )
    elif len(_channels_to_calculate) != len(waveform_kwargs["ifos"]):
        utils.logger.warning(
            f"{_base_error}. Only calculating waveforms for "
            f"{', '.join(_channels_to_calculate)}"
        )
    frequency_bounds = (
        (frequency_array >= waveform_kwargs["minimum_frequency"]) *
        (frequency_array <= waveform_kwargs["maximum_frequency"])
    )
    if waveform_kwargs["reference_frame"].lower() == "lisa":
        geocent_time, ra, dec, psi = LISA_to_SSB(geocent_time, ra, dec, psi)
    elif waveform_kwargs["reference_frame"].lower() == "ssb":
        pass
    else:
        raise ValueError(
            f"Unknown reference frame: {waveform_kwargs['reference_frame']}"
        )

    try:
        if "bbhx" in waveform_kwargs["waveform_approximant"].lower():
            out = _bbhx_binary_black_hole(
                frequency_array, mass_1, mass_2, luminosity_distance, chi_1,
                chi_2, theta_jn, phase, ra, dec, psi, geocent_time,
                **waveform_kwargs
            )
        else:
            raise ValueError(
                f"Waveform approximant: "
                f"{waveform_kwargs['waveform_approximant']} not currently "
                f"supported"
            )
        if len(out.shape) == 3 and out.shape[:2] == (1, 3):
            out = out[0]
        out[0] *= frequency_bounds
        out[1] *= frequency_bounds
        out[2] *= frequency_bounds
        _waveform_dict = {"LISA_A": out[0], "LISA_E": out[1], "LISA_T": out[2]}
    except Exception as e:
        if waveform_kwargs["catch_waveform_errors"]:
            failed_parameters = dict(
                mass_1=mass_1, mass_2=mass_2, chi_1=chi_1, chi_2=chi_2,
                luminosity_distance=luminosity_distance, theta_jn=theta_jn,
                phase=phase, ra=ra, dec=dec, psi=psi,
                geocent_time=geocent_time,
                approximant=waveform_kwargs["waveform_approximant"]
            )
            utils.logger.warning(
                "Evaluating the waveform failed with error: {}\n".format(e) +
                "The parameters were {}\n".format(failed_parameters) +
                "Likelihood will be set to -inf."
            )
            _waveform_dict = {}
    _waveform_dict = LISAPolarizationDict(
        {key: _waveform_dict.get(key, None) for key in _channels_to_calculate}
    )
    return _waveform_dict


def lisa_binary_black_hole_relative_binning(
    frequency_array, mass_1, mass_2, luminosity_distance, chi_1, chi_2,
    theta_jn, phase, ra, dec, psi, geocent_time, fiducial, **kwargs
):
    """Source model to go with RelativeBinningGravitationalWaveTransient
    likelihood. All parameters are the same as in the usual source models,
    except `fiducial`.

    Parameters
    ----------
    fiducial: float
        If fiducial=1, waveform evaluated on the full frequency grid is
        returned. If fiducial=0, waveform evaluated at
        waveform_kwargs["frequency_bin_edges"] is returned.
    """
    _kwargs = kwargs.copy()
    if fiducial == 1:
        return lisa_binary_black_hole(
            frequency_array, mass_1, mass_2, luminosity_distance, chi_1,
            chi_2, theta_jn, phase, ra, dec, psi, geocent_time, **_kwargs
        )
    else:
        _kwargs["frequencies"] = _kwargs.pop("frequency_bin_edges")
        return lisa_binary_black_hole(
            _kwargs["frequencies"], mass_1, mass_2, luminosity_distance,
            chi_1, chi_2, theta_jn, phase, ra, dec, psi, geocent_time,
            relative=True, **_kwargs
        )


def _bbhx_binary_black_hole(
    frequency_array, mass_1, mass_2, luminosity_distance, chi_1, chi_2,
    theta_jn, phase, ra, dec, psi, geocent_time, **kwargs
):
    """A Binary Black Hole waveform model implemented in the BBHx package for
    use with the LISA observatory.

    Parameters
    ----------
    frequency_array: array_like
        The frequencies at which we want to calculate the waveform
    mass_1: float
        The mass of the heavier object in solar masses
    mass_2: float
        The mass of the lighter object in solar masses
    luminosity_distance: float
        The luminosity distance in megaparsec
    chi_1: float
        The primary spin component aligned with the orbital angular momentum
    chi_2: float
        The secondary spin component aligned with the orbital angular momentum
    theta_jn: float
        Angle between the total binary angular momentum and the line of sight
    phase: float
        The phase of the waveform
    ra: float
        The ecliptic longitude of the source (we use 'ra' to remain consistent
        with existing models in `bilby`). The ecliptic longitude measures the
        distance north or south of the ecliptic
    dec: float
        The ecliptic latitude of the source (we use 'dec' to remain consistent
        with existing models in `bilby`). The ecliptic latitude is measured
        from the first point of Aries and along the ecliptic rather than the
        celestial equator
    psi: float
        The polarization of the source
    geocent_time: float
        The merger time of the source
    kwargs: dict
        Optional keyword arguments
        Supported arguments:

        - reference_frequency
        - minimum_frequency,
        - maximum_frequency
        - catch_waveform_errors
        - mode_array
        - ifos
        - direct
        - fill
        - squeeze
        - length
        - compress
        - shift_t_limits
        - t_obs_start
        - t_obs_end
        - reference_frame
        - waveform_approximant
        - relative
    """
    from bbhx.waveformbuild import BBHWaveformFD
    waveform_kwargs = dict(
        direct=True, fill=True, squeeze=True, length=1024, compress=True,
        shift_t_limits=False,
    )
    waveform_kwargs.update(kwargs)
    approximant_check = any(
        _ in waveform_kwargs["waveform_approximant"].lower() for _ in
        ["phenomd", "phenomhm"]
    )
    if not approximant_check:
        raise ValueError(
            f"Waveform approximant: {waveform_kwargs['waveform_approximant']}"
            f"not supported in the BBHx package"
        )
    if "phenomd" in waveform_kwargs["waveform_approximant"].lower():
        amp_phase_kwargs = dict(run_phenomd=True)
        # force mode_array to be [2, 2] only
        waveform_kwargs["mode_array"] = [[2, 2]]
    else:
        amp_phase_kwargs = dict(run_phenomd=False)
    wave_gen = BBHWaveformFD(amp_phase_kwargs=amp_phase_kwargs)
    dist = luminosity_distance * 1e6 * utils.parsec
    return wave_gen(
        mass_1, mass_2, chi_1, chi_2, dist, phase,
        waveform_kwargs["reference_frequency"],
        theta_jn, ra, dec, psi, geocent_time,
        freqs=frequency_array,
        modes=waveform_kwargs["mode_array"],
        direct=waveform_kwargs["direct"],
        fill=waveform_kwargs["fill"],
        squeeze=waveform_kwargs["squeeze"],
        length=waveform_kwargs["length"],
        compress=waveform_kwargs["compress"],
        t_obs_start=waveform_kwargs["t_obs_start"],
        t_obs_end=waveform_kwargs["t_obs_end"]
    )

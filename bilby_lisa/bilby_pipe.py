# Licensed under an MIT style license -- see LICENSE.md

from bilby_pipe.input import Input as _Input
from bilby_pipe.main import MainInput as _MainInput
from bilby_pipe.data_generation import DataGenerationInput as _DGInput
from bilby_pipe.data_analysis import DataAnalysisInput as _DAInput
from bilby_pipe.utils import logger, pretty_print_dictionary, BilbyPipeError
from .networks import InterferometerList

__author__ = ["Charlie Hoy <charlie.hoy@ligo.org>"]


class Input(_Input):
    """Superclass of input handlers inherited from bilby_pipe.input.Input
    """
    @property
    def bilby_relative_binning_frequency_domain_source_model(self):
        if "lisa" in self.frequency_domain_source_model:
            from .source import lisa_binary_black_hole_relative_binning
            logger.debug(
                "Using the lisa_binary_black_hole_relative_binning source "
                "model"
            )
            return lisa_binary_black_hole_relative_binning
        return super().bilby_relative_binning_frequency_domain_source_model

    def get_default_waveform_arguments(self):
        wfa = super().get_default_waveform_arguments()
        if "lisa" not in self.frequency_domain_source_model:
            return
        update = {"ifos": [f"LISA_{chnl}" for chnl in self.tdi]}
        update_str = pretty_print_dictionary(update)
        logger.debug(f"Updating waveform arguments to include: {update_str}")
        wfa.update(update)
        return wfa

    @property
    def tdi(self):
        return self._tdi

    @tdi.setter
    def tdi(self, tdi):
        if tdi == ['None'] or tdi is None:
            tdi = ["A", "E", "T"]
            logger.debug(f"No TDI channels specified. Using {tdi} as default")
        if len(tdi) != 3:
            raise ValueError(f"3 TDI channels must be specified: {tdi}")
        self._tdi = tdi

    @property
    def minimum_frequency_dict(self):
        return super().minimum_frequency_dict

    @minimum_frequency_dict.setter
    def minimum_frequency_dict(self, minimum_frequency_dict):
        super(Input, self.__class__).minimum_frequency_dict.fset(
            self, minimum_frequency_dict
        )
        if "LISA" in self._minimum_frequency_dict:
            _minimum_frequency = self._minimum_frequency_dict.pop("LISA")
            self._minimum_frequency_dict.update({
                f"LISA_{chnl}": _minimum_frequency for chnl in self.tdi
            })

    @property
    def maximum_frequency_dict(self):
        return super().maximum_frequency_dict

    @maximum_frequency_dict.setter
    def maximum_frequency_dict(self, maximum_frequency_dict):
        super(Input, self.__class__).maximum_frequency_dict.fset(
            self, maximum_frequency_dict
        )
        if "LISA" in self._maximum_frequency_dict:
            _maximum_frequency = self._maximum_frequency_dict.pop("LISA")
            self._maximum_frequency_dict.update({
                f"LISA_{chnl}": _maximum_frequency for chnl in self.tdi
            })

    def _validate_psd_dict(self):
        if "LISA" in self.detectors:
            # check other detectors
            try:
                super()._validate_psd_dict()
            except Exception as e:
                EDOM = ("Detector LISA not listed" in e.args[0])
                if not EDOM:
                    raise
                for tdi in self.tdi:
                    if f"LISA_{tdi}" not in self.psd_dict:
                        raise BilbyPipeError(
                            f"No PSD for TDI channel {tdi}. Please specify "
                            f"LISA PSDs as LISA_{tdi} in the psd-dict"
                        )
        else:
            return super()._validate_psd_dict()


class MainInput(Input, _MainInput):
    """An object to hold all the inputs to bilby_pipe. Inherited from
    bilby_pipe.main.MainInput
    """
    def __init__(self, args, unknown_args, **kwargs):
        self.tdi = args.tdi
        super().__init__(args, unknown_args, **kwargs)


class DataGenerationInput(Input, _DGInput):
    """Handles user-input for the data generation script. Inherited from
    bilby_pipe.data_generation.DataGenerationInput
    """
    def __init__(self, args, unknown_args, **kwargs):
        self.tdi = args.tdi
        super().__init__(args, unknown_args, **kwargs)

    def _set_interferometers_from_gaussian_noise(self):
        try:
            return super()._set_interferometers_from_gaussian_noise()
        except Exception:
            ifos = InterferometerList(self.detectors)
            return super()._set_interferometers_from_gaussian_noise(ifos=ifos)

    def _set_interferometers_from_data(self):
        try:
            return super()._set_interferometers_from_data()
        except Exception:
            ifos = InterferometerList(self.detectors)
            return super()._set_interferometers_from_data(ifos=ifos)

    def get_channel_type(self, det):
        try:
            return super().get_channel_type(det)
        except Exception:
            if "lisa" in det.lower():
                return
            raise

    def _get_data(self, det, channel_type, start_time, end_time, **kwargs):
        if det in self.data_dict.keys():
            return super()._get_data(
                det, channel_type, start_time, end_time, **kwargs
            )
        elif "LISA" in self.data_dict.keys():
            # if a file containing LISA data is specified, and there is
            # no channel data, extract channel data from LISA data
            import h5py
            from .utils import AET_from_XYZ
            import gwpy.timeseries
            _dict = {}
            with h5py.File(self.data_dict["LISA"], "r") as f:
                data = f["obs"]["tdi"]
                time_options = ["t", "time"]
                if not any(t in data.dtype.names for t in time_options):
                    raise ValueError(
                        f"Unable to find time in {self.data_dict[det]}. "
                        f"Please provide a column called "
                        f"{' or '.join(time_options)}"
                    )
                time_str = "t" if "t" in data.dtype.names else "time"
                time = data[time_str]
                if time.ndim > 1:
                    time = time.flatten()
                channel_df = {
                    key.upper(): data[key] for key in data.dtype.names if
                    key != time_str
                }
                for channel in ["X", "Y", "Z", "A", "E", "T"]:
                    if channel in channel_df.keys():
                        _dict[channel] = channel_df[channel]
                        if _dict[channel].ndim > 1:
                            _dict[channel] = _dict[channel].flatten()
            specified_channel = det.split("LISA_")[1]
            if specified_channel not in _dict.keys():
                _dict.update(AET_from_XYZ(_dict, channels=[specified_channel]))
            if specified_channel not in _dict.keys():
                raise ValueError(
                    f"Unable to extract strain for channel {specified_channel}"
                )
            data = gwpy.timeseries.TimeSeries(
                _dict[specified_channel], times=time,
                channel=f"L{specified_channel}:L{specified_channel}",
                name=f"L{specified_channel}:L{specified_channel}",
            )
            return data.crop(start_time, end_time)
        raise ValueError(f"Unable to extract data for {det}")


class DataAnalysisInput(Input, _DAInput):
    """Handles user-input for the data analysis script. Inhertied from
    bilby_pipe.data_analysis.DataAnalysisInput
    """
    def __init__(self, args, unknown_args, **kwargs):
        self.tdi = args.tdi
        super().__init__(args, unknown_args, **kwargs)

    @property
    def interferometers(self):
        self._interferometers = super().interferometers
        ifos = self.data_dump.interferometers
        names = [ifo.name for ifo in ifos]
        if len(names) == len(self._interferometers):
            return self._interferometers
        if "LISA" not in self.detectors:
            return self._interferometers
        logger.info("Searching for alternative data streams")
        # data dump will store the tdi data. We must set the data
        # appropiately
        ifos_to_use = [
            ifo for ifo in ifos if ifo.name in
            self.detectors + [f"LISA_{chnl}" for chnl in self.tdi]
        ]
        names_to_use = [ifo.name for ifo in ifos_to_use]
        logger.info(f"Using data for detectors = {names_to_use}")
        self._interferometers = InterferometerList(ifos_to_use)
        self.print_detector_information(self._interferometers)
        return self._interferometers


def create_parser(top_level=False):
    """Extends the BilbyArgParser for bilby_pipe to include additional
    options for LISA

    Parameters
    ----------
    top_level:
        If true, parser is to be used at the top-level with requirement
        checking etc, else it is an internal call and will be ignored.
    """
    from bilby_pipe.parser import create_parser
    from .parser import add_LISA_options_to_parser
    parser = create_parser(top_level=top_level)
    parser = add_LISA_options_to_parser(parser)
    # change the defaults for LISA data analysis
    parser.set_defaults(
        main_input_class="bilby_lisa.bilby_pipe.MainInput",
        analysis_executable_parser="bilby_lisa.bilby_pipe.create_parser",
        analysis_input_class="bilby_lisa.bilby_pipe.DataAnalysisInput",
        generation_executable_parser="bilby_lisa.bilby_pipe.create_parser",
        generation_input_class="bilby_lisa.bilby_pipe.DataGenerationInput",
    )
    return parser

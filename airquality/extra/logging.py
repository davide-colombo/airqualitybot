# ======================================
# @author:  Davide Colombo
# @date:    2022-01-23, dom, 12:44
# ======================================
import logging
import airquality.extra.string as string
from airquality.datamodel.fromdb import SensorInfoDM


_CUSTOM_LOGGER_FORMAT = '[TIME]: %(asctime)s - [LEVEL]: %(levelname)s - [DESCRIPTION]: %(message)s'


def _custom_log_filename(sensor_id: int, sensor_name: str, sensor_lat: float = None, sensor_lng: float = None) -> str:
    """
    A function that takes a set of sensor parameters and return a custom log filename.
    """

    base_name = f"sensor_{sensor_id}_{string.string_cleaner(s=sensor_name, char2remove=[' ', '.', '-'])}"
    if sensor_lat is None and sensor_lng is None:
        return base_name
    return f"{base_name}_{string.literalize_number(sensor_lat)}_{string.literalize_number(sensor_lng)}"


class FileHandlerRotator(object):
    """
    A class that caches the current file handler and defines the business rules for rotating the handler
    when a different sensor is in use.
    """

    def __init__(
        self,
        logger_name: str,                       # the target logger's name for applying handler rotation.
        logger_level,                           # the desired logging level.
        logger_dir="./log",                     # the logging directory path.
        logger_fmt=_CUSTOM_LOGGER_FORMAT        # the desired log record format.
    ):
        self._logger_dir = logger_dir
        self._logger_fmt = logger_fmt
        self._logger_name = logger_name
        self._logger_level = logger_level
        self._logger = logging.getLogger(self._logger_name)
        self._cached_file_handler = None

    def _attach_handler(self, filename: str):
        if self._cached_file_handler is not None:
            self._detach_handler()
        self._cached_file_handler = logging.FileHandler(filename=self._fullpath(filename))
        self._cached_file_handler.setFormatter(fmt=logging.Formatter(fmt=self._logger_fmt))
        self._cached_file_handler.setLevel(level=self._logger_level)
        self._logger.addHandler(self._cached_file_handler)

    def _fullpath(self, filename: str) -> str:
        return f"{self._logger_dir}/{filename}.log"

    def _detach_handler(self):
        self._logger.removeHandler(self._cached_file_handler)
        self._cached_file_handler = None

    def rotate(self, sensor_ident: SensorInfoDM):
        fname = _custom_log_filename(
            sensor_id=sensor_ident.sensor_id,
            sensor_name=sensor_ident.sensor_name,
            sensor_lat=sensor_ident.sensor_lat,
            sensor_lng=sensor_ident.sensor_lng
        )
        self._attach_handler(filename=fname)

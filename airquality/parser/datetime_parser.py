#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 12:04
# @Description: this script defines a class for parsing sensor's API timestamps
#
#################################################
import datetime
import re
import builtins
from typing import Dict, Any, List
from airquality.picker import TIMESTAMP


class DatetimeParser(builtins.object):


    ATMOTUBE_DATETIME_PATTERN = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d+Z')
    SQL_TIMESTAMP_PATTERN = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


    @staticmethod
    def _raise_system_exit_when_bad_timestamp_occurs(ts: str, pattern):
        if not re.match(pattern, ts):
            raise SystemExit(f"{DatetimeParser._raise_system_exit_when_bad_timestamp_occurs.__name__}(): "
                             f"cannot parse invalid timestamp.")

    @staticmethod
    def parse_atmotube_timestamp(ts: str) -> str:

        DatetimeParser._raise_system_exit_when_bad_timestamp_occurs(
                ts = ts,
                pattern = DatetimeParser.ATMOTUBE_DATETIME_PATTERN
        )
        ts = ts.strip('Z')
        ts, zone = ts.split('.')
        return ts.replace("T", " ")


    @staticmethod
    def date_from_last_atmotube_measure_timestamp(ts: str):
        f"""Static method that takes a timestamp and returns the date of it.
        
        The timestamp is supposed to be of the form: {DatetimeParser.SQL_TIMESTAMP_PATTERN}, otherwise
        a SystemExit exception is raised."""

        DatetimeParser._raise_system_exit_when_bad_timestamp_occurs(
                ts = ts,
                pattern = DatetimeParser.SQL_TIMESTAMP_PATTERN
        )
        date, time = ts.split(" ")
        return date


    @staticmethod
    def is_ts1_before_ts2(ts1: str, ts2: str) -> bool:
        DatetimeParser._raise_system_exit_when_bad_timestamp_occurs(
                ts = ts1,
                pattern = DatetimeParser.SQL_TIMESTAMP_PATTERN
        )

        DatetimeParser._raise_system_exit_when_bad_timestamp_occurs(
                ts = ts2,
                pattern = DatetimeParser.SQL_TIMESTAMP_PATTERN
        )

        ts1_datetime = datetime.datetime.strptime(ts1, DatetimeParser.DATETIME_FORMAT)
        ts2_datetime = datetime.datetime.strptime(ts2, DatetimeParser.DATETIME_FORMAT)
        if (ts2_datetime - ts1_datetime).total_seconds() >= 0:
            return True
        return False


    @staticmethod
    def last_atmotube_measure_timestamp_from_packets(packets: List[Dict[str, Any]]) -> str:

        last_timestamp = ""
        if packets:
            packet_id = 0
            for packet in packets:
                packet_id += 1
                if packet_id == len(packets):
                    last_timestamp = packet[TIMESTAMP]

        return last_timestamp

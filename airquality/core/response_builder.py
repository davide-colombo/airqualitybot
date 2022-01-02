######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 18:54
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from itertools import count
from typing import Generator
from datetime import datetime
from airquality.core.iteritems import IterableItemsABC
from airquality.datamodel.request import AddFixedSensorsRequest, AddMobileMeasuresRequest, AddSensorMeasuresRequest
from airquality.datamodel.response import AddFixedSensorResponse, AddMobileMeasureResponse, AddStationMeasuresResponse

SQL_TIMESTAMP_FTM = "%Y-%m-%d %H:%M:%S"


def apiparam_record(sensor_id: int, request: AddFixedSensorsRequest) -> str:
    return ','.join(
        f"({sensor_id}, '{ch.api_key}', '{ch.api_id}', '{ch.channel_name}', '{ch.last_acquisition}')" for ch in request.channels
    )


def sensor_at_location_record(sensor_id: int, request: AddFixedSensorsRequest) -> str:
    valid_from = datetime.now().strftime(SQL_TIMESTAMP_FTM)
    location = request.geolocation.geom_from_text()
    return f"({sensor_id}, '{valid_from}', {location})"


class AddFixedSensorResponseBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for
    translating a set of *AddFixedSensorRequest* items into
    an *AddFixedSensorResponse* Generator.
    """

    def __init__(self, requests: IterableItemsABC, start_sensor_id: int):
        self.requests = requests
        self.start_sensor_id = start_sensor_id

    def items(self) -> Generator[AddFixedSensorResponse, None, None]:
        sensor_id_counter = count(self.start_sensor_id)
        for req in self.requests:
            sensor_id = next(sensor_id_counter)
            yield AddFixedSensorResponse(
                sensor_record=f"({sensor_id}, '{req.type}', '{req.name}')",
                apiparam_record=apiparam_record(sensor_id=sensor_id, request=req),
                geolocation_record=sensor_at_location_record(sensor_id=sensor_id, request=req)
            )


def mobile_measure_record(packet_id: int, request: AddMobileMeasuresRequest) -> str:
    timestamp = request.timestamp.strftime(SQL_TIMESTAMP_FTM)
    geometry = request.geolocation.geom_from_text()
    return ','.join(f"({packet_id}, {param_id}, {param_val}, '{timestamp}', {geometry})" for param_id, param_val in request.measures)


class AddMobileMeasureResponseBuilder(IterableItemsABC):
    """
        An *IterableItemsABC* that defines the business rules for
        translating a set of *AddMobileMeasureRequest* items into
        an *AddMobileMeasureResponse* Generator.
        """

    def __init__(self, requests: IterableItemsABC, start_packet_id: int):
        self.requests = requests
        self.start_packet_id = start_packet_id

    def items(self) -> Generator[AddMobileMeasureResponse, None, None]:
        packet_id_counter = count(self.start_packet_id)
        for req in self.requests:
            yield AddMobileMeasureResponse(
                measure_record=mobile_measure_record(packet_id=next(packet_id_counter), request=req)
            )


def station_measure_record(packet_id: int, sensor_id: int, request: AddSensorMeasuresRequest) -> str:
    timestamp = request.timestamp.strftime(SQL_TIMESTAMP_FTM)
    return ','.join(f"({packet_id}, {sensor_id}, {param_id}, {param_val}, '{timestamp}')" for param_id, param_val in request.measures)


class AddStationMeasuresResponseBuilder(IterableItemsABC):
    """
    An *IterableItemsABC* that defines the business rules for
    translating a set of *AddSensorMeasuresRequest* items into
    an *AddStationMeasuresResponse* generator.
    """

    def __init__(self, requests: IterableItemsABC, start_packet_id: int, sensor_id: int):
        self.requests = requests
        self.start_packet_id = start_packet_id
        self.sensor_id = sensor_id

    def items(self) -> Generator[AddStationMeasuresResponse, None, None]:
        packet_id_counter = count(self.start_packet_id)
        for req in self.requests:
            yield AddStationMeasuresResponse(
                measure_record=station_measure_record(packet_id=next(packet_id_counter), sensor_id=self.sensor_id, request=req)
            )
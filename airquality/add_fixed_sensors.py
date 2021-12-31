######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 20:55
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Set
from airquality.database_gateway import DatabaseGateway
from airquality.datamodel_builder import PurpleairDatamodelBuilder
from airquality.request_builder import AddPurpleairSensorRequestBuilder
from airquality.request_validator import AddFixedSensorRequestValidator
from airquality.response_builder import AddFixedSensorResponseBuilder


class AddFixedSensors(object):
    """
    An *object* that represent the Use Case of adding a new fixed sensor (i.e., a station) to the database.
    """

    def __init__(self, output_gateway: DatabaseGateway, existing_names: Set[str], start_sensor_id: int):
        self.output_gateway = output_gateway
        self.existing_names = existing_names
        self.start_sensor_id = start_sensor_id

    def process(self, datamodels: PurpleairDatamodelBuilder):
        print(f"found #{len(datamodels)} datamodels")
        requests = AddPurpleairSensorRequestBuilder(datamodel=datamodels)
        print(f"found #{len(requests)} requests")
        validated_requests = AddFixedSensorRequestValidator(request=requests, existing_names=self.existing_names)
        print(f"found #{len(validated_requests)} valid requests")
        responses = AddFixedSensorResponseBuilder(requests=validated_requests, start_sensor_id=self.start_sensor_id)
        print(f"found #{len(responses)} responses")
        self.output_gateway.insert_sensors(responses=responses)

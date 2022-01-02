######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 11:54
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from airquality.datamodel.apiparam import APIParam
from airquality.database.gateway import DatabaseGateway
from airquality.core.request_validator import AddSensorMeasuresRequestValidator
from airquality.core.response_builder import AddMobileMeasureResponseBuilder


class AddMobileMeasures(object):
    """
    An *object* that represents the UseCase of adding mobile measurements to the database
    through the *output_gateway*.
    """

    def __init__(
            self,
            gateway: DatabaseGateway,           # A *DatabaseGateway* for committing the changes to database.
            filter_ts: datetime,                # The timestamp used to validate the requests.
            start_packet_id: int,               # The id from where to start inserting all the packets.
            apiparam: APIParam                  # The API param corresponding to the sensor that collects the measures.
    ):
        self.param = apiparam
        self.filter_ts = filter_ts
        self.output_gateway = gateway
        self.start_packet_id = start_packet_id

    def process(self, requests):
        print(f"found #{len(requests)} requests")
        valid_requests = AddSensorMeasuresRequestValidator(request=requests, filter_ts=self.filter_ts)
        print(f"found #{len(valid_requests)} valid requests")
        responses = AddMobileMeasureResponseBuilder(requests=valid_requests, start_packet_id=self.start_packet_id)

        if responses:
            print(f"found responses within [{valid_requests[0].timestamp!s} - {valid_requests[-1].timestamp!s}]")
            self.output_gateway.insert_mobile_sensor_measures(responses=responses)
            last_acquisition = valid_requests[-1].timestamp.strftime("%Y-%m-%d %H:%M:%S")
            self.output_gateway.update_last_acquisition(
                timestamp=last_acquisition, sensor_id=self.param.sensor_id, ch_name=self.param.ch_name
            )
######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 14:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.database.op.sel.sel as sel
import airquality.database.util.conn as connection
import airquality.database.util.query as query
import airquality.database.ext.postgis as postgis


class StationDBResponse(sel.BaseDBResponse):

    def __init__(self, sensor_id: int, sensor_name: str, channels: List[sel.Channel], geometry: postgis.PostgisGeometry):
        self.sensor_id = sensor_id
        self.sensor_name = sensor_name
        self.channels = channels
        self.geometry = geometry


class StationSelectWrapper(sel.SelectWrapper):

    def __init__(
            self, conn: connection.DatabaseAdapter,
            query_builder: query.QueryBuilder,
            sensor_type: str, log_filename="log",
            postgis_class=postgis.PostgisPoint
    ):
        super(StationSelectWrapper, self).__init__(conn=conn, query_builder=query_builder, sensor_type=sensor_type, log_filename=log_filename)
        self.postgis_class = postgis_class

    def select(self) -> List[StationDBResponse]:
        responses = []

        sensor_query = self.builder.select_sensor_id_name_from_type(sensor_type=self.sensor_type)
        sensor_resp = self.conn.send(sensor_query)
        for sensor_id, sensor_name in sensor_resp:

            # Query the API param + channel info
            api_param = self._select_api_param(sensor_id=sensor_id)
            channel_info = self._select_channel_info(sensor_id=sensor_id)
            channels = sel.make_channels(api_param=api_param, channel_info=channel_info)

            # Query the sensor location
            location_query = self.builder.select_location_from_sensor_id(sensor_id=sensor_id)
            location_resp = self.conn.send(location_query)
            geometry = self.postgis_class(lat=location_resp[0][1], lng=location_resp[0][0])

            # Make the response
            responses.append(StationDBResponse(sensor_id=sensor_id, sensor_name=sensor_name, channels=channels, geometry=geometry))
        return responses
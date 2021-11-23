######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 20:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.adapter.api2db.initadapt.initadapt as baseadapt
import airquality.api.model.purpresp as purpmdl
import airquality.database.util.postgis.geom as geo
import airquality.database.util.datatype.timestamp as ts


class PurpleairAPI2DBAdapter(baseadapt.InitAPI2DBAdapter):

    def __init__(self, timestamp_class=ts.UnixTimestamp, postgis_class=geo.PostgisPoint):
        super(PurpleairAPI2DBAdapter, self).__init__(timestamp_class=timestamp_class, postgis_class=postgis_class)

    def adapt(self, responses: List[purpmdl.PurpleairAPIResponseModel]) -> List[baseadapt.InitUniformModel]:
        uniformed_responses = []
        for response in responses:
            # Create Name
            name = f"{response.name} ({response.sensor_index})".replace("'", "")
            type_ = "Purpleair/Thingspeak"

            # Create channel info List
            channels = [baseadapt.ParamNameTimestamp(name=ch, timestamp=self.timestamp_class(timest=response.date_created))
                        for ch in response.CHANNELS]

            # Create sensor geometry
            geometry = self.postgis_class(lat=response.latitude, lng=response.longitude)
            # Create sensor geolocation
            geolocation = baseadapt.ParamLocationTimestamp(geolocation=geometry,
                                                           timestamp=ts.CurrentTimestamp())
            # Append Uniformed Model
            uniformed_responses.append(
                baseadapt.InitUniformModel(
                    name=name, type_=type_,
                    parameters=response.parameters,
                    channels=channels,
                    geolocation=geolocation
                )
            )

        return uniformed_responses

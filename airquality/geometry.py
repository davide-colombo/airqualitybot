######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 19:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from dataclasses import dataclass
from abc import abstractmethod

POSTGIS_POINT = "POINT({lon} {lat})"
ST_GEOM_FROM_TEXT = "ST_GeomFromText('{geom}', {srid})"


class PostgisGeometry(object):

    @abstractmethod
    def as_text(self) -> str:
        pass

    @abstractmethod
    def geom_from_text(self) -> str:
        pass


@dataclass
class PostgisPoint(PostgisGeometry):
    """
    A *PostgisGeometry* that defines the sensor's geolocation point and how is converted into PostGIS format.
    """

    latitude: float                     # The sensor's latitude in decimal degrees (-90,+90)
    longitude: float                    # The sensor's longitude in decimal degrees (-180,+180)
    srid: int = 26918                   # The Spatial Reference Identifier associated to the coordinate system.

    def __post_init__(self):
        if self.latitude < -90.0 or self.latitude > 90.0:
            raise ValueError(f"{type(self).__name__} expected *latitude* to be in range [-90.0 - +90.0]")
        if self.longitude < -180.0 or self.longitude > 180.0:
            raise ValueError(f"{type(self).__name__} expected *longitude* to be in range [-180.0 - +180.0]")

    def as_text(self) -> str:
        return POSTGIS_POINT.format(lon=self.longitude, lat=self.latitude)

    def geom_from_text(self) -> str:
        return ST_GEOM_FROM_TEXT.format(geom=self.as_text(), srid=self.srid)


class NullGeometry(PostgisGeometry):
    """
    A *PostgisGeometry* that represent a null geometry.
    """

    def as_text(self) -> str:
        return "NULL"

    def geom_from_text(self) -> str:
        return "NULL"
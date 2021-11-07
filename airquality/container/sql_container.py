######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 17:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import abstractmethod
from typing import Dict, Any, List
from airquality.container.identifiable_container import IdentifiableContainer


class SQLContainer(IdentifiableContainer):
    """Interface to SQL containers object that can be translated into SQL query."""

    def __init__(self, packet: Dict[str, Any]):
        self.identity = packet['name']
        self.identity.replace("'", "")

    @abstractmethod
    def sql(self, query: str) -> str:
        pass

    def identifier(self) -> str:
        return self.identity


class GeoSQLContainer(SQLContainer):
    """SQL container that defines how a sensor location in translated into SQL query."""

    def __init__(self, sensor_id: int, packet: Dict[str, Any]):
        super().__init__(packet)
        self.sensor_id = sensor_id
        self.timestamp = packet['timestamp']
        self.geometry = packet['geometry']

    def sql(self, query: str) -> str:
        return query + f"({self.sensor_id}, '{self.timestamp}', {self.geometry})"

    def __str__(self):
        return f"sensor_id={self.sensor_id}, valid_from={self.timestamp}, geom={self.geometry}"


class APIParamSQLContainer(SQLContainer):
    """SQL container that defines how the sensor's API parameter is translated into SQL query."""

    def __init__(self, sensor_id: int, packet: Dict[str, Any]):
        super().__init__(packet)
        self.sensor_id = sensor_id
        self.param_name: List[str] = packet['param_name']      # this is a List
        self.param_value: List[str] = packet['param_value']    # this is a List

    def sql(self, query: str) -> str:
        for i in range(len(self.param_name)):
            query += f"({self.sensor_id}, '{self.param_name[i]}', '{self.param_value[i]}'),"
        return query.strip(',')

    def __str__(self):
        s = f"sensor_id={self.sensor_id}, "
        s += ', '.join(f'{name}={val}' for name, val in zip(self.param_name, self.param_value))
        return s


class SensorSQLContainer(SQLContainer):

    def __init__(self, sensor_id: int, packet: Dict[str, Any]):
        super().__init__(packet)
        self.type = packet['type']

    def sql(self, query: str) -> str:
        return query + f"('{self.type}', '{self.identity}')"

    def __str__(self):
        return f"name={self.identity}, type={self.type}"


class MobileMeasurementSQLContainer(SQLContainer):

    def __init__(self, sensor_id: int, packet: Dict[str, Any]):
        super().__init__(packet)
        self.param_id = packet['param_id']
        self.param_val = packet['param_val']
        self.timestamp = packet['timestamp']
        self.geom = packet['geom']

    def sql(self, query: str) -> str:
        for i in range(len(self.param_id)):
            query += f"({self.param_id[i]}, '{self.param_val[i]}', '{self.timestamp}', {self.geom}),"
        return query.strip(',')

    def __str__(self):
        return ', '.join(f'{id_}={val}' for id_, val in zip(self.param_id, self.param_val))


########################### SQL CONTAINER COMPOSITION CLASS ############################
class SQLContainerComposition(SQLContainer):

    def __init__(self, containers: List[SQLContainer]):
        super().__init__(packet={'name': ""})               # to be compliant with the interface but not used !!!
        self.containers = containers

    def sql(self, query: str) -> str:
        for c in self.containers:
            query += c.sql(query="") + ','
        return query.strip(',') + ';'

    def identifier(self) -> str:
        return ', '.join(f'{c.identifier()}' for c in self.containers)

    def __str__(self):
        return '\n'.join(f'{c!s}' for c in self.containers)

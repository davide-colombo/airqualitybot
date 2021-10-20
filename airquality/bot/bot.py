#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 19:11
# @Description: This module contains the BaseBot class and its subclasses
#
#################################################
from abc import ABC
from typing import List
from airquality.conn.builder import SQLQueryBuilder
from airquality.parser.db_resp_parser import DatabaseResponseParser
from airquality.conn.conn import DatabaseConnection


class BaseBot(ABC):
    """
    Abstract Base Class for bot objects.

    -db_conn_interface: interface instance for database connection and SQL
                        statements execution
    """

    def __init__(self, dbconn: DatabaseConnection):
        self.__db_conn_interface = dbconn
        self.__db_conn_interface.open_conn()

    @property
    def dbconn(self):
        return self.__db_conn_interface



class BotMobile(BaseBot):
    """
    Subclass of BaseBot that handles mobile sensors data automatically.

    The purpose of this class is to fetch data through the sensor's API and
    loading the data to the database.
    """

    def __init__(self, dbconn: DatabaseConnection, sensor_models: List[str]):
        super().__init__(dbconn)
        self.__models = sensor_models
        query = SQLQueryBuilder.select_all_sensor_ids_by_model(self.__models)
        response = self.dbconn.send(query)
        sensor_ids = DatabaseResponseParser.parse_one_field_response(response)

        if not sensor_ids:
            raise SystemExit(f"{BotMobile.__name__}: sensor id list is empty in '{BotMobile.__init__.__name__}()' method.")

        self.__sensor_ids = sensor_ids

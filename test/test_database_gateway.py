######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 14:51
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.response import AddFixedSensorResponse, AddMobileMeasureResponse
from airquality.database_gateway import DatabaseGateway


class TestDatabaseGateway(TestCase):

    ##################################### test_get_existing_sensor_names #####################################
    def test_get_existing_sensor_names(self):
        mocked_dbadapter = MagicMock()
        mocked_dbadapter.fetchall.return_value = [("n1", ), ("n2", ), ("n3", )]

        gateway = DatabaseGateway(dbadapter=mocked_dbadapter)

        existing_sensor_names = gateway.get_existing_sensor_names_of_type(sensor_type="purpleair")
        self.assertEqual(existing_sensor_names, {"n1", "n2", "n3"})

    ##################################### test_get_start_sensor_id #####################################
    def test_get_start_sensor_id(self):
        mocked_dbadapter = MagicMock()
        mocked_dbadapter.fetchone.side_effect = [(12, ), None]
        gateway = DatabaseGateway(dbadapter=mocked_dbadapter)
        start_sensor_id = gateway.get_start_sensor_id()
        self.assertEqual(start_sensor_id, 13)

        start_sensor_id = gateway.get_start_sensor_id()
        self.assertEqual(start_sensor_id, 1)

    @property
    def get_test_sensor_record(self):
        return "(12, 'faketype', 'fakename')"

    @property
    def get_test_apiparam_record(self):
        return "(12, 'key1', 'ident1', 'name1', '2018-12-13 18:19:00'),(12, 'key2', 'ident2', 'name2', '2018-12-13 18:19:00')"

    @property
    def get_test_geolocation_record(self):
        return "(12, '2019-09-25 17:44:00', NULL, ST_GeomFromText('POINT(-9 36)', 26918))"

    @property
    def get_test_add_fixed_sensor_responses(self):
        return AddFixedSensorResponse(
            sensor_record=self.get_test_sensor_record,
            apiparam_record=self.get_test_apiparam_record,
            geolocation_record=self.get_test_geolocation_record
        )

    ##################################### test_insert_sensors #####################################
    def test_insert_sensors(self):
        mocked_database_adapter = MagicMock()
        mocked_database_adapter.execute = MagicMock()

        mocked_response_builder = MagicMock()
        mocked_response_builder.__iter__.return_value = [self.get_test_add_fixed_sensor_responses]
        gateway = DatabaseGateway(dbadapter=mocked_database_adapter)
        gateway.insert_sensors(responses=mocked_response_builder)

        expected_query = \
            "INSERT INTO level0_raw.sensor VALUES (12, 'faketype', 'fakename'); " \
            "INSERT INTO level0_raw.sensor_api_param (sensor_id, ch_key, ch_id, ch_name, last_acquisition) VALUES " \
            "(12, 'key1', 'ident1', 'name1', '2018-12-13 18:19:00'),(12, 'key2', 'ident2', 'name2', '2018-12-13 18:19:00'); " \
            "INSERT INTO level0_raw.sensor_at_location (sensor_id, valid_from, geom) VALUES " \
            "(12, '2019-09-25 17:44:00', NULL, ST_GeomFromText('POINT(-9 36)', 26918));"

        mocked_database_adapter.execute.assert_called_with(expected_query)

    ##################################### test_get_measure_param #####################################
    def test_get_measure_param(self):
        mocked_database_adapter = MagicMock()
        mocked_database_adapter.fetchall.return_value = [(1, 'c1'), (2, 'c2')]

        gateway = DatabaseGateway(dbadapter=mocked_database_adapter)
        actual = gateway.get_measure_param_owned_by(owner="atmotube")
        expected = {'c1': 1, 'c2': 2}
        self.assertEqual(actual, expected)

    @property
    def get_test_mobile_records(self):
        return "(13, 1, '0.17', '2021-10-11 09:44:00', ST_GeomFromText('POINT(-12 37)', 26918)), " \
               "(13, 2, '8', '2021-10-11 09:44:00', ST_GeomFromText('POINT(-12.09 37.11)', 26918)), " \
               "(13, 6, '24', '2021-10-11 09:44:00', ST_GeomFromText('POINT(-12.34 37.87)', 26918))"

    @property
    def get_test_add_mobile_sensor_responses(self):
        return AddMobileMeasureResponse(measure_record=self.get_test_mobile_records)

    ##################################### test_get_measure_param #####################################
    def test_insert_mobile_sensor_measures(self):
        mocked_database_adapter = MagicMock()
        mocked_database_adapter.execute = MagicMock()

        mocked_response_builder = MagicMock()
        mocked_response_builder.__iter__.return_value = [self.get_test_add_mobile_sensor_responses]

        gateway = DatabaseGateway(dbadapter=mocked_database_adapter)
        gateway.insert_mobile_sensor_measures(responses=mocked_response_builder)

        expected_query = "INSERT INTO level0_raw.mobile_measurement (packet_id, param_id, param_value, timestamp, geom) VALUES " \
                         f"{self.get_test_mobile_records};"

        mocked_database_adapter.execute.assert_called_with(expected_query)

    ##################################### test_update_last_acquisition #####################################
    def test_update_last_acquisition(self):
        mocked_database_adapter = MagicMock()
        mocked_database_adapter.execute = MagicMock()

        gateway = DatabaseGateway(dbadapter=mocked_database_adapter)
        gateway.update_last_acquisition(timestamp="faketimestamp", sensor_id=12, ch_name="fakename")

        expected_query = "UPDATE level0_raw.sensor_api_param SET last_acquisition = 'faketimestamp' " \
                         "WHERE sensor_id = 12 AND ch_name = 'fakename';"

        mocked_database_adapter.execute.assert_called_with(expected_query)


if __name__ == '__main__':
    main()
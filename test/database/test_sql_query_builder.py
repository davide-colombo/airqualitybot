#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:32
# @Description: unit test script
#
#################################################
import unittest
from airquality.database.sql_query_builder import SQLQueryBuilder


class TestSQLQueryBuilder(unittest.TestCase):
    """Class for testing the sql query builder."""

    def setUp(self) -> None:
        self.sql_builder = SQLQueryBuilder(query_file_path = "properties/sql_query.json")

    def test_system_exit_when_query_identifier_not_found(self):
        test_query_id = "bad query identifier"
        with self.assertRaises(SystemExit):
            self.sql_builder._raise_exception_if_query_identifier_not_found(query_id = test_query_id)

    def test_empty_query_when_empty_packet_list(self):
        test_packets = []
        expected_output = ""
        actual_output = self.sql_builder.insert_measurements(packets = test_packets)
        self.assertEqual(actual_output, expected_output)



if __name__ == '__main__':
    unittest.main()

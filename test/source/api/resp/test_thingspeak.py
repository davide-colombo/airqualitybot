######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 16:07
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.source.api.resp.thingspeak as resptype


class TestThingspeakMeasureResponse(unittest.TestCase):

    def test_get_primary_data_channel_a_measures(self):
        test_item = {"feeds": [{"created_at": "at", "field1": "f1", "field2": "f2", "field3": "f3", "field6": "f6"}]}
        response_builder = resptype.ThingspeakAPIRespBuilder(channel_name="Primary data - Channel A")
        actual = response_builder.build(test_item)
        measures = actual[0].measures

        self.assertEqual(actual[0].created_at, "at")
        self.assertEqual(measures[0].name, response_builder.CHANNEL_FIELDS["Primary data - Channel A"]["field1"])
        self.assertEqual(measures[0].value, "f1")
        self.assertEqual(measures[1].name, response_builder.CHANNEL_FIELDS["Primary data - Channel A"]["field2"])
        self.assertEqual(measures[1].value, "f2")
        self.assertEqual(measures[2].name, response_builder.CHANNEL_FIELDS["Primary data - Channel A"]["field3"])
        self.assertEqual(measures[2].value, "f3")
        self.assertEqual(measures[3].name, response_builder.CHANNEL_FIELDS["Primary data - Channel A"]["field6"])
        self.assertEqual(measures[3].value, "f6")
        self.assertEqual(measures[4].name, response_builder.CHANNEL_FIELDS["Primary data - Channel A"]["field7"])
        self.assertEqual(measures[4].value, None)

    def test_get_primary_data_channel_b_measures(self):
        test_item = {"feeds": [{"created_at": "at", "field1": "f1", "field2": "f2", "field3": "f3", "field6": "f6"}]}
        response_builder = resptype.ThingspeakAPIRespBuilder(channel_name="Primary data - Channel B")
        actual = response_builder.build(test_item)
        measures = actual[0].measures

        self.assertEqual(actual[0].created_at, "at")
        self.assertEqual(measures[0].name, response_builder.CHANNEL_FIELDS["Primary data - Channel B"]["field1"])
        self.assertEqual(measures[0].value, "f1")
        self.assertEqual(measures[1].name, response_builder.CHANNEL_FIELDS["Primary data - Channel B"]["field2"])
        self.assertEqual(measures[1].value, "f2")
        self.assertEqual(measures[2].name, response_builder.CHANNEL_FIELDS["Primary data - Channel B"]["field3"])
        self.assertEqual(measures[2].value, "f3")
        self.assertEqual(measures[3].name, response_builder.CHANNEL_FIELDS["Primary data - Channel B"]["field6"])
        self.assertEqual(measures[3].value, "f6")

    def test_get_secondary_data_channel_a_measures(self):
        test_item = {"feeds": [{"created_at": "at", "field1": "f1", "field2": "f2", "field3": "f3", "field4": "f4", "field5": "f5", "field6": "f6"}]}
        response_builder = resptype.ThingspeakAPIRespBuilder(channel_name="Secondary data - Channel A")
        actual = response_builder.build(test_item)
        measures = actual[0].measures

        self.assertEqual(actual[0].created_at, "at")
        self.assertEqual(measures[0].name, response_builder.CHANNEL_FIELDS["Secondary data - Channel A"]["field1"])
        self.assertEqual(measures[0].value, "f1")
        self.assertEqual(measures[1].name, response_builder.CHANNEL_FIELDS["Secondary data - Channel A"]["field2"])
        self.assertEqual(measures[1].value, "f2")
        self.assertEqual(measures[2].name, response_builder.CHANNEL_FIELDS["Secondary data - Channel A"]["field3"])
        self.assertEqual(measures[2].value, "f3")
        self.assertEqual(measures[3].name, response_builder.CHANNEL_FIELDS["Secondary data - Channel A"]["field4"])
        self.assertEqual(measures[3].value, "f4")
        self.assertEqual(measures[4].name, response_builder.CHANNEL_FIELDS["Secondary data - Channel A"]["field5"])
        self.assertEqual(measures[4].value, "f5")
        self.assertEqual(measures[5].name, response_builder.CHANNEL_FIELDS["Secondary data - Channel A"]["field6"])
        self.assertEqual(measures[5].value, "f6")

    def test_get_secondary_data_channel_b_measures(self):
        test_item = {"feeds": [{"created_at": "at", "field1": "f1", "field2": "f2", "field3": "f3", "field4": "f4", "field5": "f5", "field6": "f6"}]}
        response_builder = resptype.ThingspeakAPIRespBuilder(channel_name="Secondary data - Channel B")
        actual = response_builder.build(test_item)
        measures = actual[0].measures

        self.assertEqual(actual[0].created_at, "at")
        self.assertEqual(measures[0].name, response_builder.CHANNEL_FIELDS["Secondary data - Channel B"]["field1"])
        self.assertEqual(measures[0].value, "f1")
        self.assertEqual(measures[1].name, response_builder.CHANNEL_FIELDS["Secondary data - Channel B"]["field2"])
        self.assertEqual(measures[1].value, "f2")
        self.assertEqual(measures[2].name, response_builder.CHANNEL_FIELDS["Secondary data - Channel B"]["field3"])
        self.assertEqual(measures[2].value, "f3")
        self.assertEqual(measures[3].name, response_builder.CHANNEL_FIELDS["Secondary data - Channel B"]["field4"])
        self.assertEqual(measures[3].value, "f4")
        self.assertEqual(measures[4].name, response_builder.CHANNEL_FIELDS["Secondary data - Channel B"]["field5"])
        self.assertEqual(measures[4].value, "f5")
        self.assertEqual(measures[5].name, response_builder.CHANNEL_FIELDS["Secondary data - Channel B"]["field6"])
        self.assertEqual(measures[5].value, "f6")

    # ################################ TEST EXIT ON BAD ITEM ################################
    # def test_successfully_check_response_item(self):
    #     self.response_builder.with_channel_name("Primary data - Channel A")
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field2": "f2", "field3": "f3",
    #                  "field6": "f6", "field7": "f7"}
    #     self.response_builder.exit_on_bad_item(test_item)
    #     self.assertTrue(True)
    #
    # ################################ missing 'created_at' ################################
    # def test_exit_on_missing_created_at_item(self):
    #     self.response_builder.with_channel_name("Primary data - Channel A")
    #     test_item = {"field1": "f1", "field2": "f2", "field3": "f3", "field6": "f6", "field7": "f7"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    # ################################ TEST PRIMARY DATA CHANNEL A ITEM ################################
    # def test_exit_on_missing_primary_data_channel_a_fields(self):
    #     self.response_builder.with_channel_name("Primary data - Channel A")
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field2": "f2", "field3": "f3", "field6": "f6", "field7": "f7"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field3": "f3", "field6": "f6", "field7": "f7"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field2": "f2", "field6": "f6", "field7": "f7"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field2": "f2", "field3": "f3", "field7": "f7"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field2": "f2", "field3": "f3", "field6": "f6"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    # ################################ TEST PRIMARY DATA CHANNEL B ITEM ################################
    # def test_exit_on_missing_primary_data_channel_b_fields(self):
    #     self.response_builder.with_channel_name("Primary data - Channel B")
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field2": "f2", "field3": "f3", "field6": "f6"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field3": "f3", "field6": "f6"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field2": "f2", "field6": "f6"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field2": "f2", "field3": "f3"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    # ################################ TEST SECONDARY DATA CHANNEL A ITEM ################################
    # def test_exit_on_missing_secondary_data_channel_a_fields(self):
    #     self.response_builder.with_channel_name("Secondary data - Channel A")
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field2": "f2", "field3": "f3",
    #                  "field4": "f4", "field5": "f5", "field6": "f6"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field3": "f3",
    #                  "field4": "f4", "field5": "f5", "field6": "f6"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field2": "f2",
    #                  "field4": "f4", "field5": "f5", "field6": "f6"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field2": "f2", "field3": "f3",
    #                  "field5": "f5", "field6": "f6"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field2": "f2", "field3": "f3",
    #                  "field4": "f4", "field6": "f6"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field2": "f2", "field3": "f3",
    #                  "field4": "f4", "field5": "f5"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    # ################################ TEST SECONDARY DATA CHANNEL B ITEM ################################
    # def test_exit_on_missing_secondary_data_channel_b_fields(self):
    #     self.response_builder.with_channel_name("Secondary data - Channel B")
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field2": "f2", "field3": "f3",
    #                  "field4": "f4", "field5": "f5", "field6": "f6"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field3": "f3",
    #                  "field4": "f4", "field5": "f5", "field6": "f6"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field2": "f2",
    #                  "field4": "f4", "field5": "f5", "field6": "f6"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field2": "f2", "field3": "f3",
    #                  "field5": "f5", "field6": "f6"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field2": "f2", "field3": "f3",
    #                  "field4": "f4", "field6": "f6"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)
    #
    #     test_item = {"created_at": "2021-11-09T04:36:55Z", "field1": "f1", "field2": "f2", "field3": "f3",
    #                  "field4": "f4", "field5": "f5"}
    #     with self.assertRaises(SystemExit):
    #         self.response_builder.exit_on_bad_item(test_item)


if __name__ == '__main__':
    unittest.main()
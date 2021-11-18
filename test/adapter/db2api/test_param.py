######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 13/11/21 15:56
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.adapter.db2api.param as par
import airquality.adapter.config as c


class TestParamAdapter(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_adapter = par.AtmotubeParamAdapter()
        self.thingspeak_adapter = par.ThingspeakParamAdapter()

    def test_param_reshaper_class(self):
        obj_cls = par.get_param_adapter('atmotube')
        self.assertEqual(obj_cls.__class__, par.AtmotubeParamAdapter)

        obj_cls = par.get_param_adapter('thingspeak')
        self.assertEqual(obj_cls.__class__, par.ThingspeakParamAdapter)

        with self.assertRaises(SystemExit):
            par.get_param_adapter('purpleair')

    def test_successfully_reshape_atmotube_api_param(self):
        test_api_param = {c.MAC_ADDR: 'some_mac', c.API_KEY: 'some_key'}
        expected_output = [{c.MAC_ADDR: 'some_mac', c.API_KEY: 'some_key', c.CH_NAME: 'main'}]
        actual_output = self.atmotube_adapter.reshape(test_api_param)
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_atmotube_api_key(self):
        test_api_param_missing_key = {c.MAC_ADDR: 'some_mac'}
        with self.assertRaises(SystemExit):
            self.atmotube_adapter.reshape(test_api_param_missing_key)

    def test_exit_on_missing_atmotube_mac_address(self):
        test_api_param_missing_mac = {c.API_KEY: 'some_key'}
        with self.assertRaises(SystemExit):
            self.atmotube_adapter.reshape(test_api_param_missing_mac)

    ################################ TEST THINGSPEAK PARAM RESHAPER ################################
    def test_successfully_uniform_reshape_thingspeak_api_param(self):
        test_api_param = {'primary_id_a': 'id1A', 'primary_key_a': 'key1A', 'primary_id_b': 'id1B', 'primary_key_b': 'key1B',
                          'secondary_id_a': 'id2A', 'secondary_key_a': 'key2A', 'secondary_id_b': 'id2B', 'secondary_key_b': 'key2B'}
        expected_output = [{c.CH_ID: 'id1A', c.API_KEY: 'key1A', c.CH_NAME: '1A'},
                           {c.CH_ID: 'id1B', c.API_KEY: 'key1B', c.CH_NAME: '1B'},
                           {c.CH_ID: 'id2A', c.API_KEY: 'key2A', c.CH_NAME: '2A'},
                           {c.CH_ID: 'id2B', c.API_KEY: 'key2B', c.CH_NAME: '2B'}]
        actual_output = self.thingspeak_adapter.reshape(test_api_param)
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_thingspeak_channel_a_primary_data(self):
        test_api_param_missing_1a = {'primary_id_b': 'id1B', 'primary_key_b': 'key1B',
                                     'secondary_id_a': 'id2A', 'secondary_key_a': 'key2A', 'secondary_id_b': 'id2B',
                                     'secondary_key_b': 'key2B'}
        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.reshape(test_api_param_missing_1a)

    def test_exit_on_missing_thingspeak_channel_b_primary_data(self):
        test_api_param_missing_1b = {'primary_id_a': 'id1A', 'primary_key_a': 'key1A',
                                     'secondary_id_a': 'id2A', 'secondary_key_a': 'key2A', 'secondary_id_b': 'id2B',
                                     'secondary_key_b': 'key2B'}
        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.reshape(test_api_param_missing_1b)

    def test_exit_on_missing_thingspeak_channel_a_secondary_data(self):
        test_api_param_missing_2a = {'primary_id_a': 'id1A', 'primary_key_a': 'key1A', 'primary_id_b': 'id1B',
                                     'primary_key_b': 'key1B', 'secondary_id_b': 'id2B', 'secondary_key_b': 'key2B'}
        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.reshape(test_api_param_missing_2a)

    def test_exit_on_missing_thingspeak_channel_b_secondary_data(self):
        test_api_param_missing_2b = {'primary_id_a': 'id1A', 'primary_key_a': 'key1A', 'primary_id_b': 'id1B',
                                     'primary_key_b': 'key1B', 'secondary_id_a': 'id2A', 'secondary_key_a': 'key2A'}
        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.reshape(test_api_param_missing_2b)


if __name__ == '__main__':
    unittest.main()

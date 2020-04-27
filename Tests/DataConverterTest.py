import logging.config
import unittest

import DataConverter
import DataObjects.Bar as Bar
from Config import log_config

logging.config.dictConfig(log_config.TEST_CONFIG)


class TestMethods(unittest.TestCase):

    def test_merge_lists(self):
        # Given

        database_list = [
            Bar.Bar('MSFT', 1, '2020-04-15 15:53:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:54:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:55:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:56:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:57:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:58:00', 171.92, 172.25, 171.79, 171.95, 534118)
        ]

        api_list = [
            Bar.Bar('MSFT', 1, '2020-04-15 15:55:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:56:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:57:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:58:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:59:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 16:00:00', 171.92, 172.25, 171.79, 171.95, 534118)
        ]

        # When
        merged_list, api_list_short = DataConverter.merge_lists(database_list, api_list)

        # Then
        expected_api_list_short = [
            Bar.Bar('MSFT', 1, '2020-04-15 15:59:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 16:00:00', 171.92, 172.25, 171.79, 171.95, 534118)
        ]

        expected_merged_list = [
            Bar.Bar('MSFT', 1, '2020-04-15 15:53:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:54:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:55:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:56:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:57:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:58:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:59:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 16:00:00', 171.92, 172.25, 171.79, 171.95, 534118)
        ]

        self.assertEqual(len(expected_merged_list), len(merged_list))
        for index in range(len(expected_merged_list)):
            self.assertEqual(expected_merged_list[index].time_stamp, merged_list[index].time_stamp)

        self.assertEqual(len(expected_api_list_short), len(api_list_short))
        for index in range(len(expected_api_list_short)):
            self.assertEqual(expected_api_list_short[index].time_stamp, api_list_short[index].time_stamp)


    def test_merge_lists_equal(self):
        # Given
        database_list = [
            Bar.Bar('MSFT', 1, '2020-04-15 15:55:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:56:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:57:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:58:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:59:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 16:00:00', 171.92, 172.25, 171.79, 171.95, 534118)
        ]

        api_list = [
            Bar.Bar('MSFT', 1, '2020-04-15 15:55:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:56:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:57:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:58:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:59:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 16:00:00', 171.92, 172.25, 171.79, 171.95, 534118)
        ]

        # When
        merged_list, api_list_short = DataConverter.merge_lists(database_list, api_list)

        # Then
        expected_api_list_short = [
        ]

        expected_merged_list = [
            Bar.Bar('MSFT', 1, '2020-04-15 15:55:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:56:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:57:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:58:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:59:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 16:00:00', 171.92, 172.25, 171.79, 171.95, 534118)
        ]

        self.assertEqual(len(expected_merged_list), len(merged_list))
        for index in range(len(expected_merged_list)):
            self.assertEqual(expected_merged_list[index].time_stamp, merged_list[index].time_stamp)

        self.assertEqual(len(expected_api_list_short), len(api_list_short))
        for index in range(len(expected_api_list_short)):
            self.assertEqual(expected_api_list_short[index].time_stamp, api_list_short[index].time_stamp)

    def test_merge_lists_no_equal(self):
        # Given

        database_list = [
            Bar.Bar('MSFT', 1, '2020-04-15 15:55:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:56:00', 171.92, 172.25, 171.79, 171.95, 534118)
        ]

        api_list = [
            Bar.Bar('MSFT', 1, '2020-04-15 15:59:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 16:00:00', 171.92, 172.25, 171.79, 171.95, 534118)
        ]

        # When
        merged_list, api_list_short = DataConverter.merge_lists(database_list, api_list)

        # Then
        expected_api_list_short = [
            Bar.Bar('MSFT', 1, '2020-04-15 15:59:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 16:00:00', 171.92, 172.25, 171.79, 171.95, 534118)
        ]

        expected_merged_list = [
            Bar.Bar('MSFT', 1, '2020-04-15 15:55:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:56:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:59:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 16:00:00', 171.92, 172.25, 171.79, 171.95, 534118)
        ]

        self.assertEqual(len(expected_merged_list), len(merged_list))
        for index in range(len(expected_merged_list)):
            # print(expected_merged_list[index].time_stamp)

            self.assertEqual(expected_merged_list[index].time_stamp, merged_list[index].time_stamp)

        self.assertEqual(len(expected_api_list_short), len(api_list_short))
        for index in range(len(expected_api_list_short)):
            self.assertEqual(expected_api_list_short[index].time_stamp, api_list_short[index].time_stamp)

    def test_merge_lists_database_empty(self):
        # Given

        database_list = [
        ]

        api_list = [
            Bar.Bar('MSFT', 1, '2020-04-15 15:55:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:56:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:57:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:58:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:59:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 16:00:00', 171.92, 172.25, 171.79, 171.95, 534118)
        ]

        # When
        merged_list, api_list_short = DataConverter.merge_lists(database_list, api_list)

        # Then
        expected_api_list_short = [
            Bar.Bar('MSFT', 1, '2020-04-15 15:55:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:56:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:57:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:58:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:59:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 16:00:00', 171.92, 172.25, 171.79, 171.95, 534118)
        ]

        expected_merged_list = [
            Bar.Bar('MSFT', 1, '2020-04-15 15:55:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:56:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:57:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:58:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 15:59:00', 171.92, 172.25, 171.79, 171.95, 534118),
            Bar.Bar('MSFT', 1, '2020-04-15 16:00:00', 171.92, 172.25, 171.79, 171.95, 534118)
        ]

        self.assertEqual(len(expected_merged_list), len(merged_list))
        for index in range(len(expected_merged_list)):
            self.assertEqual(expected_merged_list[index].time_stamp, merged_list[index].time_stamp)

        self.assertEqual(len(expected_api_list_short), len(api_list_short))
        for index in range(len(expected_api_list_short)):
            self.assertEqual(expected_api_list_short[index].time_stamp, api_list_short[index].time_stamp)


if __name__ == '__main__':
    unittest.main()
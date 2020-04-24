import unittest
import DataConverterUtils
import numpy as np
import logging.config
from Config import log_config

logging.config.dictConfig(log_config.TEST_CONFIG)


class TestMethods(unittest.TestCase):

    def test_normalize_previous_points_1(self):
        # Given
        prices_narray = np.array([1, 2, 3, 4])

        # When
        res = DataConverterUtils.normalize_previous_points(prices_narray)

        # Then
        expected = np.array([0, 1, 2, 3])
        np.testing.assert_array_equal(expected, res)

    def test_normalize_previous_points_2(self):
        # Given
        prices_narray = np.array([150, 0, 205, 150, -10, 700])

        # When
        res = DataConverterUtils.normalize_previous_points(prices_narray)

        # Then
        expected = np.array([0, -150, 55, 0, -160, 550])
        np.testing.assert_array_equal(expected, res)

if __name__ == '__main__':
    unittest.main()
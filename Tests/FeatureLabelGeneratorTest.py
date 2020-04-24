import unittest
import numpy as np
import logging.config
from Config import log_config
import FeatureLabelGenerator
from DataObjects import Bar

logging.config.dictConfig(log_config.TEST_CONFIG)


class TestMethods(unittest.TestCase):

    def test_generate_features(self):
        # Given
        price_data = [
            Bar.Bar('MSFT', 1, '2020-04-15 16:00:00', 500, 550, 490, 530, 10300),
            Bar.Bar('MSFT', 1, '2020-04-15 15:59:00', 530, 610, 520, 600, 20012),
            Bar.Bar('MSFT', 1, '2020-04-15 15:58:00', 600, 650, 590, 650, 10555),
            Bar.Bar('MSFT', 1, '2020-04-15 15:57:00', 650, 660, 595, 600, 30000),
            Bar.Bar('MSFT', 1, '2020-04-15 15:56:00', 600, 600, 510, 510, 44444),
            Bar.Bar('MSFT', 1, '2020-04-15 15:56:00', 510, 520, 400, 430, 44443)
        ]

        # When
        features = FeatureLabelGenerator.generate_features(price_data, 3)

        print("features = ", features)

        # Todo: expected values are incorrect. FIx later?
        # Then
        expected_features = np.array([
                [[0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]],

                [[5, 0, 0],
                [5.5, 0, 0],
                [4.9, 0, 0],
                [5.3, 0, 0],
                [1.03, 0, 0]],

                [[5, 5.3, 0],
                [5.5, 6.1, 0],
                [4.9, 5.2, 0],
                [5.3, 6, 0],
                [1.03, 2.0012, 0]],

                [[5, 5.3, 6],
                [5.5, 6.1, 6.5],
                [4.9, 5.2, 5.9],
                [5.3, 6, 6.5],
                [1.03, 2.0012, 1.0555]],

                [[5.3, 6, 6.5],
                 [6.1, 6.5, 6.6],
                 [5.2, 5.9, 5.95],
                 [6, 6.5, 6],
                 [2.0012, 1.0555, 3]],

                [[6, 6.5, 6],
                 [6.5, 6.6, 6],
                 [5.9, 5.95, 5.1],
                 [6.5, 6, 5.1],
                 [1.0555, 3, 4.4444]]
        ])

        # Then
        np.testing.assert_array_equal(expected_features, features)

    def test_generate_labels(self):
        # Given
        price_data = [
            Bar.Bar('MSFT', 1, '2020-04-15 16:00:00', 500, 550, 490, 530, 10300),
            Bar.Bar('MSFT', 1, '2020-04-15 15:59:00', 530, 610, 520, 600, 20012),
            Bar.Bar('MSFT', 1, '2020-04-15 15:58:00', 600, 650, 590, 650, 10555),
            Bar.Bar('MSFT', 1, '2020-04-15 15:57:00', 650, 660, 595, 600, 30000),
            Bar.Bar('MSFT', 1, '2020-04-15 15:56:00', 600, 600, 510, 510, 44444),
            Bar.Bar('MSFT', 1, '2020-04-15 15:56:00', 510, 520, 400, 430, 44443)
        ]

        # When
        labels = FeatureLabelGenerator.generate_labels(price_data)

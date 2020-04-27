import logging.config
import unittest

import LabelsGenerator
from Config import log_config
from DataObjects import Bar

logging.config.dictConfig(log_config.TEST_CONFIG)


class TestMethods(unittest.TestCase):


    def test_generate_features(self):
        # Given
        bars_list = [
            Bar.Bar('MSFT', 1, '2020-04-15 16:00:00', 500, 550, 490, 530, 10300),
            Bar.Bar('MSFT', 1, '2020-04-15 15:59:00', 530, 610, 520, 600, 20012),
            Bar.Bar('MSFT', 1, '2020-04-15 15:58:00', 600, 650, 590, 650, 10555),
            Bar.Bar('MSFT', 1, '2020-04-15 15:57:00', 650, 660, 595, 600, 30000),
            Bar.Bar('MSFT', 1, '2020-04-15 15:56:00', 600, 600, 510, 510, 44444),
            Bar.Bar('MSFT', 1, '2020-04-15 15:56:00', 510, 520, 400, 430, 44443)
        ]

        # When
        labels = LabelsGenerator.generate_labels(bars_list, 0.1)
        labels = LabelsGenerator.generate_labels(bars_list, 0.1)

        # Then
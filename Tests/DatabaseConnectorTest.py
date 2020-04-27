import logging.config
import unittest

from Config import log_config
from DataObjects import Bar
from Database import DatabaseConnector

logging.config.dictConfig(log_config.TEST_CONFIG)


class TestMethods(unittest.TestCase):

    def test_insert_bar(self):
        DatabaseConnector.setup_database_connection()

        bar = Bar.Bar('GOOG', '15', '2020-04-10 14:34:59', 5.324234, 6.34, 7.23, 8.2223, 1337)
        DatabaseConnector.insert_bar(bar)


if __name__ == '__main__':
    unittest.main()

import pandas
from matplotlib import pyplot
import DataConverter
import CSVDataConverter
from Constants import Actions, Symbols, TimeFrames
import numpy as np
import logging as log
import logging.config
from Config import log_config
import TradingSimulator
import ModelBuilder
import configparser
import Database.DatabaseConnector as database
import ApiConnector
import FeatureLabelGenerator
import LabelsGenerator
import DataPlotter
import time
from DataObjects import Bar

logging.config.dictConfig(log_config.DEFAULT_CONFIG)

ONE_MINUTE = 60
FIVE_MINUTES = ONE_MINUTE * 5
ONE_HOUR = ONE_MINUTE * 60
ONE_DAY = ONE_HOUR * 24

def main():

    symbol = Symbols.MSFT
    time_frame = TimeFrames.ONE_MIN

    database.setup_database_connection()
    result_set = database.fetch_all_bars(symbol, time_frame)
    database_list = DataConverter.convert_result_set(result_set)

    csv_data = ApiConnector.fetch_alphavantage_data(symbol, time_frame)
    api_list = DataConverter.convert_alphavantage_csv_data(csv_data, symbol, time_frame)

    merged_list, api_list_short = DataConverter.merge_lists(database_list, api_list)

    database.insert_bars(api_list_short)

    number_previous_bars = 300
    division_factor = 100
    test_factor = 0.2
    trigger_value = 0.005
    price_range_factor = 0.8
    index_range_factor = 0.8

    features = FeatureLabelGenerator.generate_features(merged_list, number_previous_bars)
    labels = LabelsGenerator.generate_labels(merged_list, trigger_value, price_range_factor, index_range_factor)

    nbr_of_simulations = 100
    build_and_simulate(features, labels, merged_list, nbr_of_simulations)

    DataPlotter.plot(merged_list, labels)


def build_and_simulate(features, labels, merged_list, nbr_of_simulations):

    final_simulation_result = 0
    simulation_results = []

    for index in range(nbr_of_simulations):
        train_factor = 0.2
        model, predictions, test_bars = ModelBuilder.build_model(features, labels, train_factor, merged_list)

        starting_balance = 50000
        ratio_per_trade = 50 * 0.01  # Allowed to invest % of account
        commission_rate = 0.1 * 0.01  # Commission rate in %
        simulation_result = TradingSimulator.simulate_trading_locally(
            predictions=predictions,
            bars_list=test_bars,
            starting_balance=starting_balance,
            ratio_per_trade=ratio_per_trade,
            commission_rate=commission_rate

        )
        simulation_results.append(simulation_result)
        final_simulation_result = final_simulation_result + simulation_result
        log.info("Final simulation result thus far = %s ", final_simulation_result / (index+1))

    final_simulation_result = final_simulation_result / nbr_of_simulations
    log.info("Simulation results = %s ", simulation_results)
    log.info("Final simulation result = %s ", final_simulation_result)


def data_harvest():
    while True:
        for symbol in Symbols.symbols_list:
            for time_frame in TimeFrames.time_frames_list:
                log.info("Collecting data for %s on timeframe %smin ", symbol, time_frame)

                database.setup_database_connection()
                result_set = database.fetch_all_bars(symbol, time_frame)
                database_list = DataConverter.convert_result_set(result_set)

                csv_data = ApiConnector.fetch_alphavantage_data(symbol, time_frame)
                api_list = DataConverter.convert_alphavantage_csv_data(csv_data, symbol, time_frame)

                merged_list, api_list_short = DataConverter.merge_lists(database_list, api_list)

                database.insert_bars(api_list_short)
                log.info("Finished collecting data for %s on timeframe %smin. Waiting 15 seconds before next call", symbol, time_frame)
                time.sleep(15)

        log.info("Finished data collection cycle, sleeping for %s seconds (24 hours)", ONE_DAY)
        time.sleep(ONE_DAY)

def test():
    database.setup_database_connection()
    bar = Bar.Bar('GOOG', '15', '2020-04-10 14:34:59', 5.324234, 7.23, 7.23, 8.2223, 1337)
    bar1 = Bar.Bar('GOOG', '15', '2020-04-10 14:34:59', 5.324234, 6.34, 7.23, 8.2223, 1337)
    bar3 = Bar.Bar('GOOG', '15', '2020-04-10 14:34:59', 5.324234, 6.34, 7.23, 8.2223, 1337)
    bar4 = Bar.Bar('GOOG', '10', '2020-04-10 14:34:59', 5.324234, 6.34, 7.23, 8.2223, 1337)

    bars = [bar, bar1, bar3, bar4]
    database.insert_bars(bars)


if __name__ == "__main__":
    # data_harvest()
    main()
    # test()




# def main():
# log.info("Starting main")
#
# dataset_name = "Datasets/IBM.csv"
# dataset_name = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=1min&outputsize=full&apikey=KLIWR5Z434P010JV&datatype=csv'
# # "Datasets/IBM.TradesOnly.012815.csv"
# csv_data = pandas.read_csv(dataset_name, sep=",", nrows=99999999999999)
#
# number_previous_points = 200
# division_factor = 100
# cutoff = 9999999999999999999999999
# test_factor = 0.2
# trigger_value = 0.0001
# price_range_factor = 0.2
# index_range_factor = 0.2
#
# converter = CSVDataConverter.CSVDataConverter(
#     trigger_value=trigger_value,
#     number_previous_points=number_previous_points,
#     division_factor=division_factor,
#     cutoff=cutoff,
#     price_range_factor=price_range_factor,
#     index_range_factor=index_range_factor
# )
#
# price_array = converter.convert_csv_data(csv_data=csv_data)
#
# data_length = len(price_array)
#
# prices_narray = np.empty(shape=(data_length, 1))
# labels_narray = np.empty(shape=(data_length, 1))
# pricemovement_labels_narray = np.empty(shape=(data_length, 1))
# previous_prices_narray = np.empty(shape=(data_length, number_previous_points, 1))
#
# count_hold = 0
# count_buy = 0
# count_sell = 0
#
# count_sideways = 0
# for index, point in enumerate(price_array):
#     labels_narray[index] = point.action
#     pricemovement_labels_narray[index] = point.price_movement
#     log.debug("Index: %s, Found price movement %s", index, pricemovement_labels_narray[index])
#
#     previous_prices_narray[index] = point.previous_prices
#     prices_narray[index] = point.price
#
#     if point.get_action() == Actions.BUY:
#         count_buy += 1
#         log.debug("Found %s action at %s", Actions.names[point.action], index)
#         log.debug("Index: %s, Found previous points %s", index, previous_prices_narray[index])
#         pyplot.plot(index, (point.price * division_factor), 'ro', color='black', markersize=3)
#     elif point.action == Actions.SELL:
#         count_sell += 1
#         log.debug("Found %s action at %s", Actions.names[point.action], index)
#         log.debug("Index: %s, Found previous points %s", index, previous_prices_narray[index])
#         pyplot.plot(index, (point.price * division_factor), 'ro', color='red', markersize=3)
#     else:
#         count_hold += 1
#
# final_simulation_result = 0
# number_simulations = 100
# for index in range(number_simulations):
#     train_factor = 0.2
#     model, predictions = ModelBuilder.build_model(
#         previous_prices=previous_prices_narray,
#         labels=labels_narray,
#         train_factor=train_factor
#     )
#
#     number_training_lines = int(previous_prices_narray.shape[0] * (1 - train_factor))
#     test_prices = prices_narray[number_training_lines:]
#
#     ratio_per_trade = 50 * 0.01  # Allowed to invest % of account
#     commission_rate = 0.1 * 0.01  # Commission rate in %
#     simulation_result = TradingSimulator.simulate_trading(
#         predictions=predictions,
#         test_prices=test_prices,
#         division_factor=division_factor,
#         ratio_per_trade=ratio_per_trade,
#         commission_rate=commission_rate
#     )
#     final_simulation_result = final_simulation_result + simulation_result
#
# print("Final simulation result = ", (final_simulation_result / number_simulations))
# price_data = csv_data[["open"]]
# pyplot.plot(price_data)
#
# pyplot.show()


    # testString = '1. {0} 2.{1} 2.{1}' % (bar.symbol, bar.open_price, bar.open_price)
    # testString = "%(symbol)s %(time_frame)s %(symbol)s" % {"symbol": bar.symbol, "time_frame": bar.time_frame}
    # print(testString)


# def test():
#
#     print("Running test")
#     labels_narray = np.zeros(shape=(5, 2))
#     second_array = np.array([8, 8])
#     labels_narray[1] = [1, 2]
#     labels_narray[2] = second_array
#
#     config = configparser.ConfigParser()
#     config.read("Config/Config.ini")
#     print(config.sections()[0])
#     print(config.get('Database', 'Host'))

    # train_labels = pricemovement_labels_narray[0:30000]
    # test_labels = pricemovement_labels_narray[30000:]
    #
    # number_training_lines = 10000
    #
    # train_labels = labels_narray[0:number_training_lines]
    # test_labels = labels_narray[number_training_lines:]
    #
    # train_previous_prices = previous_prices_narray[0:number_training_lines]
    # test_previous_prices = previous_prices_narray[number_training_lines:]

    # count_sideways = 0
    # count_up = 0
    # count_down = 0
    # for label in train_labels:
    #     log.debug("pricemovement: %s", label)
    #     if label == Price_Movement.SIDEWAYS:
    #         count_sideways += 1
    #     elif label == Price_Movement.UP:
    #         count_up += 1
    #     elif label == Price_Movement.DOWN:
    #         count_down += 1

    # model = keras.Sequential([
    #     keras.layers.Flatten(input_shape=(number_previous_points, 1)),
    #     keras.layers.Dense(128, activation='relu'),
    #     keras.layers.Dense(3, activation='softmax')
    # ])
    #
    # model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    #
    # model.fit(train_previous_prices, train_labels, epochs=1)
    #
    # test_loss, test_acc = model.evaluate(test_previous_prices, test_labels, verbose=1)
    #
    # log.info('Test accuracy: %s', test_acc)


    # predictions = model.predict(test_previous_prices)
    #
    # correct_sell = 0
    # wrong_sell = 0
    # correct_buy = 0
    # wrong_buy = 0
    # for index in range(len(predictions)):
    #     log.info("Predictions: %s Prediction: %s, Actual: %s ", predictions[index], np.argmax(predictions[index]), test_labels[index])
    #
    #     if np.argmax(predictions[index]) == Actions.SELL:
    #         if test_labels[index] == Actions.SELL:
    #             correct_sell += 1
    #         else:
    #             wrong_sell += 1
    #
    #     if np.argmax(predictions[index]) == Actions.BUY:
    #         if test_labels[index] == Actions.BUY:
    #             correct_buy += 1
    #         else:
    #             wrong_buy += 1

    # log.info('Test accuracy: %s', test_acc)
    #
    # log.info('Correct sell: %s', correct_sell)
    # log.info('Wrong sell: %s', wrong_sell)
    # log.info('Correct buy: %s', correct_buy)
    # log.info('Wrong buy: %s', wrong_buy)

    # labels_narray2 = np.zeros(shape=(10, 1))
    # subarray = np.ones(shape=(3, 1))
    # print("labels_narray2 = ", labels_narray2)
    # print("subarray = ", subarray)
    # labels_narray2[0:3] = subarray
    # print("After replace")
    # print(labels_narray2)
    # subarray[0] = 2
    # print("After change value")
    # print("subarray = ", subarray)
    # print("labels_narray2 = ", labels_narray2)
    #
    # test_narray = np.array([1, 2, 3, 4, 5])
    # print("testarray = ", test_narray)
    # a = test_narray[:2]
    # test_narray = test_narray[2:]
    # print(a)
    # print(test_narray)



    # csv_data = pandas.read_csv("IBM.TradesOnly.012815.csv", sep=",")
    #
    # price_data = csv_data[[" Price"]]
    # price_data = price_data[1000:5000]
    #
    # pyplot.plot(price_data)
    # pyplot.show()



    # log.basicConfig(level=log.DEBUG)


    # logging.debug("debug message")
    # logging.warning("debug message")
    # logging.info("info message")
    logging.error("error log")

    # previous_prices = price_array[15].previous_prices
    # print("price = ", price_array[1].price)
    # print("type: ")
    # print(type(previous_prices))
    # print("previous_prices shape = ", previous_prices.shape)
    # print("previous_prices = ", previous_prices)


    # >> > import numpy
    # >> > a = numpy.zeros(shape=(5, 2))
    # >> > a
    # array([[0., 0.],
    #        [0., 0.],
    #        [0., 0.],
    #        [0., 0.],
    #        [0., 0.]])
    # >> > a[0] = [1, 2]
    # >> > a[1] = [2, 3]
    # >> > a
    # array([[1., 2.],
    #        [2., 3.],
    #        [0., 0.],
    #        [0., 0.],
    #        [0., 0.]])

    # pyplot.plot(price_data2)

    # pyplot.scatter(data[plot_label], data[predict])
    # pyplot.xlabel(plot_label)
    # pyplot.ylabel("Final Grade")
    # pyplot.show()



    # price_data = data[[" Price"]]
    #
    # print(data)
    # print(data.head())
    #
    # for item in data.iterrows():
    #     print(item)

    # lastHigest = 1
    # index_last_higest = 0
    #
    # lastLowest = 99999999999999999999999999999999999999999999999999999999999999
    # index_last_lowest = 0
    #
    # direction_up = True
    #
    # change_needed = 0.0001
    #
    # count_data_points = 0
    #
    #
    # for index, row in data.iterrows():
    #
    #     print(index, row[' Price'])
    #
    #     # if index > 6000:
    #     #     continue
    #
    #     price = row[' Price']
    #     print(price)
    #     print(price / lastHigest)
    #
    #     if direction_up:
    #         if price > lastHigest:
    #             lastHigest = price
    #             index_last_higest = index
    #
    #         elif (price / lastHigest) < (1 - change_needed):
    #             print("Division at UP: ")
    #             print(price / lastHigest)
    #             direction_up = False
    #             lastLowest = price
    #             pyplot.plot(index_last_higest, lastHigest, 'ro')
    #             count_data_points += 1
    #     else:
    #         if price < lastLowest:
    #             lastLowest = price
    #             index_last_lowest = index
    #
    #         elif (lastLowest / price) < (1 - change_needed):
    #             print("Division at DOWN: ")
    #             print(lastLowest / price)
    #             direction_up = True
    #             lastHigest = price
    #             pyplot.plot(index_last_lowest, lastLowest, 'ro')
    #             count_data_points += 1
    #
    # print("Datapoints = ", count_data_points)
    # pyplot.plot(price_data)
    #
    #
    # pyplot.show()

    # prices_narray = np.zeros(shape=(5001, number_previous_points))
    # labels_narray = np.zeros(shape=(5001, 1))


    # previous_prices_narray = np.array(previous_prices)
    # print(type(previous_prices_narray))
    # print("previous_prices_narray = ", previous_prices_narray)
    # print("price_array length = ", len(price_array))
    # print("previous_prices_narray shape = ", previous_prices_narray.shape)



    # for index, point in enumerate(price_array):
    #     print("index = ", index)
    #     print("state = ", point.state)
    #     labels_narray[index] = point.state
    #     print("type = ", type(point.previous_prices))
    #     print("shape = ", point.previous_prices.shape)
    #     print("point.previous_prices = ", point.previous_prices)
    #
    #     prices_narray[index] = point.previous_prices


    # print(labels_narray)
    # print(type(labels_narray))

    # labels_narray = np.zeros(shape=(5, 2))
    # labels_narray[1] = [1, 2]
    # print(labels_narray)


    # for index, point in enumerate(price_array):
    #     print("mainloop")
    #     print("index = ", index)
    #     print("price = ", point.price)
    #     print("state = ", point.get_state())
    #     print("previous_points length = ", len(point.previous_points))
    #     if point.get_state() != Actions.HOLD:
    #         pyplot.plot(index, point.price, 'ro')


# DEFAULT_LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'standard': {
#             'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
#         },
#     },
#     'loggers': {
#         '': {
#             'level': 'DEBUG',
#         },
#         'another.module': {
#             'level': 'DEBUG',
#         },
#     }
# }

# LOGGING_CONFIG = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'standard': {
#             'format': '[%(levelname)s] %(asctime)s %(filename)s: %(message)s'
#         },
#     },
#     'handlers': {
#         'default': {
#             'formatter': 'standard',
#             'class': 'logging.StreamHandler',
#             'stream': 'ext://sys.stdout',  # Default is stderr
#         },
#     },
#     'loggers': {
#         '': {  # root logger
#             'handlers': ['default'],
#             'level': 'INFO',
#         }
#     }
# }

# for index in range(len(predictions)):
#     if test_labels[index] != 0:
#         print("--------------prediction----------------")
#         print(test_labels[index])
#         print(predictions[index])
#         print("-----------------end--------------------")
# print("count_actions = ", count_actions)
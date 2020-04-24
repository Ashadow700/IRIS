import numpy as np
import logging as log
from Constants import FeatureColumns, Actions

prices_rising = True
last_highest_price = 0
last_lowest_price = 999999999999999999999999
last_highest_index = 0
last_lowest_index = 0

def __set_previous_bar_values(previous_bar_data, previous_bar_index, previous_bar, price_division_factor, volume_division_factor):
    previous_bar_data[FeatureColumns.OPEN_PRICE][previous_bar_index] = float(previous_bar.open_price) / price_division_factor
    previous_bar_data[FeatureColumns.HIGH_PRICE][previous_bar_index] = float(previous_bar.high_price) / price_division_factor
    previous_bar_data[FeatureColumns.LOW_PRICE][previous_bar_index] = float(previous_bar.low_price) / price_division_factor
    previous_bar_data[FeatureColumns.CLOSE_PRICE][previous_bar_index] = float(previous_bar.close_price) / price_division_factor
    previous_bar_data[FeatureColumns.VOLUME][previous_bar_index] = float(previous_bar.volume) / volume_division_factor
    return previous_bar_data

def __homogenize_previous_bar_values(previous_bars_data):
    first_opening_price = previous_bars_data[FeatureColumns.OPEN_PRICE][0]
    previous_bars_data[FeatureColumns.OPEN_PRICE] = previous_bars_data[FeatureColumns.OPEN_PRICE] - first_opening_price
    previous_bars_data[FeatureColumns.HIGH_PRICE] = previous_bars_data[FeatureColumns.HIGH_PRICE] - first_opening_price
    previous_bars_data[FeatureColumns.LOW_PRICE] = previous_bars_data[FeatureColumns.LOW_PRICE] - first_opening_price
    previous_bars_data[FeatureColumns.CLOSE_PRICE] = previous_bars_data[FeatureColumns.CLOSE_PRICE] - first_opening_price
    return previous_bars_data

def generate_features(bars_list, nbr_of_previous_bars=300, price_division_factor=100, volume_division_factor=10000):
    log.info("Converting list of bars to numpy array features")

    features = np.zeros(shape=(len(bars_list), FeatureColumns.NBR_OF_FEATURES, nbr_of_previous_bars))

    for bar_index, bar in enumerate(bars_list):
        log.debug("Creating numpy array of previous bars for bar number %s", bar_index)

        previous_bars_data = np.zeros(shape=(FeatureColumns.NBR_OF_FEATURES, nbr_of_previous_bars))

        if bar_index < nbr_of_previous_bars:
            log.debug("Setting previous bars to bar number %s, from index %s to %s", bar_index, 0, bar_index)
            for previous_bar_index, previous_bar in enumerate(bars_list[:bar_index]):
                previous_bars_data = __set_previous_bar_values(previous_bars_data, previous_bar_index, previous_bar, price_division_factor, volume_division_factor)
        else:
            log.debug("Setting previous bars to bar number %s, from index %s to %s", bar_index, bar_index - nbr_of_previous_bars, bar_index)
            for previous_bar_index, previous_bar in enumerate(bars_list[bar_index - nbr_of_previous_bars:bar_index]):
                previous_bars_data = __set_previous_bar_values(previous_bars_data, previous_bar_index, previous_bar, price_division_factor, volume_division_factor)

        previous_bars_data = __homogenize_previous_bar_values(previous_bars_data)
        features[bar_index] = previous_bars_data

    return features


def __check_sell_point_found(price, last_highest_price, trigger_value):
    return (price / last_highest_price) < (1 - trigger_value)


def __handel_prices_rising(labels, price, index, trigger_value):
    global prices_rising
    global last_highest_price
    global last_lowest_price
    global last_highest_index
    global last_lowest_index

    if price > last_highest_price:
        last_highest_price = price
        last_highest_index = index
    elif __check_sell_point_found(price, last_highest_price, trigger_value):
        log.debug("Sell point found at index %s", last_highest_index)
        prices_rising = False
        last_lowest_price = price
        last_lowest_index = index
        labels[last_highest_index] = Actions.SELL
    return labels

def __check_buy_point_found(price, last_lowest_price, trigger_value):
    return (last_lowest_price / price) < (1 - trigger_value)


def __handel_prices_falling(labels, price, index, trigger_value):
    global prices_rising
    global last_highest_price
    global last_lowest_price
    global last_highest_index
    global last_lowest_index

    if price < last_lowest_price:
        last_lowest_price = price
        last_lowest_index = index

    elif __check_buy_point_found(price, last_lowest_price, trigger_value):
        log.debug("Buy point found at index %s", last_lowest_index)
        prices_rising = True
        last_highest_price = price
        last_highest_index = index
        labels[last_lowest_index] = Actions.BUY
    return labels


def generate_labels(bars_list, trigger_value):
    global prices_rising
    global last_highest_price
    global last_lowest_price
    global last_highest_index
    global last_lowest_index

    labels = np.zeros(shape=(len(bars_list)))

    for index, bar in enumerate(bars_list):
        if prices_rising:
            labels = __handel_prices_rising(labels, bar.open_price, index, trigger_value)
        else:
            labels = __handel_prices_falling(labels, bar.open_price, index, trigger_value)
    return labels


    # for index, row in csv_data.iterrows():
    # if index < self.number_previous_points:
    #     previous_prices = np.zeros(shape=(self.number_previous_points, 1))
    #     previous_prices_subsection = (price_data[:index]).to_numpy()
    #     previous_prices[0:index] = previous_prices_subsection
    #     previous_prices = DataConverterUtils.normalize_previous_points(previous_prices)
    #     point.set_previous_prices(previous_prices)
    # else:
    #     previous_prices = (price_data[index - self.number_previous_points:index]).to_numpy()
    #     previous_prices = DataConverterUtils.normalize_previous_points(previous_prices)
    #     point.set_previous_prices(previous_prices)
    #






    # print("price_data.shape = ", price_data.shape[0])
    #
    # features = np.zeros(shape=(price_data.shape[0], NBR_OF_FEATURES, nbr_of_previous_points))
    # # print("features.shape = ", features.shape)
    # # print("features = ", features)
    #
    # # features[1, 0, 0] = 1
    # # features[0, 1, 0] = 2
    # # features[2, 1, 1:3] = [3, 3]
    # print(features)
    #
    # for bar_index, bar in enumerate(price_data):
    #
    #     print("bar = ", bar)
    #     for column_index in range(BarColumns.OPEN_PRICE, BarColumns.CLOSE_PRICE+1):
    #         bar[column_index] = float(bar[column_index]) / division_factor
    #
    #
    #     previous_prices_subsection = price_data[:bar_index, BarColumns.OPEN_PRICE]
    #     print("previous_prices_subsection", previous_prices_subsection)
    #     ones = np.ones(shape=(1, 3))
    #     # print("ones = ", ones)
    #
    #     features[bar_index][FeatureColumns.OPEN_PRICE][0:bar_index] = previous_prices_subsection
    #     print(features)

        # for column_index in range(FeatureColumns.OPEN_PRICE, FeatureColumns.CLOSE_PRICE + 1):
        #     #Todo: homogonizew featurecolumns & barcolumns



        # for column_index in range(BarColumns.OPEN_PRICE, BarColumns.CLOSE_PRICE+1):
        #     previous_prices_subsection = price_data[:bar_index, column_index]
        #     features[bar_index, column_index, 0:bar_index] = previous_prices_subsection
        #     print("previous_prices_subsection = ", previous_prices_subsection)
        # print("features after finished = ", features)


def homogenize_previous_prices(prices_narray):

    log.debug("Subtracting %s from all values in array", prices_narray[0])
    prices_narray = prices_narray - prices_narray[0]

    return prices_narray

    # if index < self.number_previous_points:
    #     previous_prices = np.zeros(shape=(self.number_previous_points, 1))
    #     previous_prices_subsection = (price_data[:index]).to_numpy()
    #     previous_prices[0:index] = previous_prices_subsection
    #     previous_prices = DataConverterUtils.normalize_previous_points(previous_prices)
    #     point.set_previous_prices(previous_prices)
    # else:
    #     previous_prices = (price_data[index - self.number_previous_points:index]).to_numpy()
    #     previous_prices = DataConverterUtils.normalize_previous_points(previous_prices)
    #     point.set_previous_prices(previous_prices)

    # features_narray =

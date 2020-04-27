import logging as log

import numpy as np

from Constants import FeatureColumns


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

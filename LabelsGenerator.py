import logging as log
import sys

import numpy as np

from Constants import Actions

this = sys.modules[__name__]


def __check_sell_point_found(price, last_highest_price, trigger_value):
    return (price / last_highest_price) < (1 - trigger_value)


def __handel_prices_rising(labels, price, index, trigger_value):

    if price > this.last_highest_price:
        this.last_highest_price = price
        this.last_highest_index = index
    elif __check_sell_point_found(price, this.last_highest_price, trigger_value):
        log.debug("Sell point found at index %s", this.last_highest_index)
        this.prices_rising = False
        this.last_lowest_price = price
        this.last_lowest_index = index
        labels[this.last_highest_index] = Actions.SELL
    return labels


def __check_buy_point_found(price, last_lowest_price, trigger_value):
    return (last_lowest_price / price) < (1 - trigger_value)


def __handel_prices_falling(labels, price, index, trigger_value):

    if price < this.last_lowest_price:
        this.last_lowest_price = price
        this.last_lowest_index = index

    elif __check_buy_point_found(price, this.last_lowest_price, trigger_value):
        log.debug("Buy point found at index %s", this.last_lowest_index)
        this.prices_rising = True
        this.last_highest_price = price
        this.last_highest_index = index
        labels[this.last_lowest_index] = Actions.BUY
    return labels


def __expand_range_before_sell_bar(labels, bars_list, index, price, price_range_factor, index_range_factor):

    price_difference = abs(price - this.last_buy_price)
    accepted_price = price - (price_difference * price_range_factor/2)
    index_difference = abs(this.last_buy_index - index)
    accepted_index = index - (index_difference * index_range_factor/2)

    index_in_range = index
    price_in_range = price
    log.debug("Expanding range backwards at %s with accepted_price = %s, accepted_index = %s",
              index_in_range, accepted_price, accepted_index)
    while index_in_range > accepted_index and price_in_range > accepted_price:
        log.debug("Setting label at index %s, with price %s to action %s", index_in_range, price_in_range, Actions.actions_list[Actions.SELL])
        labels[index_in_range] = Actions.SELL
        index_in_range -= 1
        price_in_range = bars_list[index_in_range].open_price

    accepted_price = this.last_buy_price + (price_difference * price_range_factor/2)
    accepted_index = this.last_buy_index + (index_difference * index_range_factor/2)

    index_in_range = this.last_buy_index
    price_in_range = this.last_buy_price
    log.debug("Expanding range forward at %s with accepted_price = %s, accepted_index = %s",
              index_in_range, accepted_price, accepted_index)
    while index_in_range < accepted_index and price_in_range < accepted_price:
        log.debug("Setting label at index %s, with price %s to action %s", index_in_range, price_in_range,
                  Actions.actions_list[Actions.BUY])
        labels[index_in_range] = Actions.BUY
        index_in_range += 1
        price_in_range = bars_list[index_in_range].open_price

    this.last_sell_price = price
    this.last_sell_index = index
    return labels


def __expand_range_before_buy_bar(labels, bars_list, index, price, price_range_factor, index_range_factor):

    price_difference = abs(this.last_sell_price - price)
    accepted_price = price + (price_difference * price_range_factor/2)
    index_difference = abs(index - this.last_sell_index)
    accepted_index = index - (index_difference * index_range_factor/2)  # Todo, if out of range, set to 0

    index_in_range = index
    price_in_range = price
    log.debug("Expanding range backwards at %s with accepted_price = %s, accepted_index = %s",
              index_in_range, accepted_price, accepted_index)
    while index_in_range > accepted_index and price_in_range < accepted_price:
        log.debug("Setting label at index %s, with price %s to action %s", index_in_range, price_in_range, Actions.actions_list[Actions.BUY])
        labels[index_in_range] = Actions.BUY
        index_in_range -= 1
        price_in_range = bars_list[index_in_range].open_price

    accepted_price = this.last_sell_price - (price_difference * price_range_factor/2)
    accepted_index = this.last_sell_index + (index_difference * index_range_factor/2)

    index_in_range = this.last_sell_index
    price_in_range = this.last_sell_price
    log.debug("Expanding range forward at %s with accepted_price = %s, accepted_index = %s",
              index_in_range, accepted_price, accepted_index)
    while index_in_range < accepted_index and price_in_range > accepted_price:
        log.debug("Setting label at index %s, with price %s to action %s", index_in_range, price_in_range, Actions.actions_list[Actions.SELL])
        labels[index_in_range] = Actions.SELL
        index_in_range += 1
        price_in_range = bars_list[index_in_range].open_price

    this.last_buy_price = price
    this.last_buy_index = index
    return labels


# todo recode so that you expand around each bar, not just backwards
def __expand_range(labels, bars_list, price_range_factor, index_range_factor):
    log.info("Expanding buy/sell ranges...")

    this.last_buy_price = bars_list[0].open_price
    this.last_sell_price = bars_list[0].open_price

    for index, action in enumerate(labels):
        open_price = bars_list[index].open_price
        action = int(action)

        if action == Actions.SELL:
            log.debug("Expanding %s point at index = %s with price = %s", Actions.actions_list[action], index, open_price)
            labels = __expand_range_before_sell_bar(labels, bars_list, index, open_price, price_range_factor, index_range_factor)

        elif action == Actions.BUY:
            log.debug("Expanding %s point at index = %s with price = %s", Actions.actions_list[action], index, open_price)
            labels = __expand_range_before_buy_bar(labels, bars_list, index, open_price, price_range_factor, index_range_factor)


def reset_variables():
    this.prices_rising = True
    this.last_highest_price = 0
    this.last_lowest_price = 999999999999999999999999
    this.last_highest_index = 0
    this.last_lowest_index = 0

    this.last_buy_price = 0
    this.last_sell_price = 0
    this.last_buy_index = 0
    this.last_sell_index = 0


# todo make labels for the points at end of range too
def generate_labels(bars_list, trigger_value, price_range_factor=1, index_range_factor=1):
    log.info("Generating labels")
    reset_variables()

    labels = np.zeros(shape=(len(bars_list)))
    for index, bar in enumerate(bars_list):
        if this.prices_rising:
            labels = __handel_prices_rising(labels, bar.open_price, index, trigger_value)
        else:
            labels = __handel_prices_falling(labels, bar.open_price, index, trigger_value)
    __expand_range(labels, bars_list, price_range_factor, index_range_factor)


    return labels

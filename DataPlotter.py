from matplotlib import pyplot
import numpy as np
from Constants import Actions

def plot(bars_list, labels, price_division_factor=100):

    open_prices = np.zeros(shape=(len(bars_list)))
    for index, bar in enumerate(bars_list):
        open_prices[index] = bar.open_price
        action = labels[index]
        if action == Actions.BUY:
            pyplot.plot(index, bar.open_price, 'ro', color='black', markersize=3)
        elif action == Actions.SELL:
            pyplot.plot(index, bar.open_price, 'ro', color='red', markersize=3)


    pyplot.plot(open_prices)
    pyplot.show()



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
    #         pyplot.plot(index, (point.price*division_factor), 'ro', color='black', markersize=3)
    #     elif point.action == Actions.SELL:
    #         count_sell += 1
    #         log.debug("Found %s action at %s", Actions.names[point.action], index)
    #         log.debug("Index: %s, Found previous points %s", index, previous_prices_narray[index])
    #         pyplot.plot(index, (point.price * division_factor), 'ro', color='red', markersize=3)
    #     else:
    #         count_hold += 1
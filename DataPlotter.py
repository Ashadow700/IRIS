from matplotlib import pyplot
import numpy as np
from Constants import Actions


def plot(bars_list, labels):

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

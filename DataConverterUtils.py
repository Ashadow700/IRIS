import numpy as np
import logging as log


def normalize_previous_points(prices_narray):

    log.debug("Subtracting %s from all values in array", prices_narray[0])
    prices_narray = prices_narray - prices_narray[0]

    return prices_narray
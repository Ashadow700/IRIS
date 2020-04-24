import logging as log
from Constants import Actions


class Point:
    def __init__(self, index, price, action, previous_prices, price_movement):
        self.index = index
        self.price = price
        self.action = action
        self.previous_prices = previous_prices
        self.price_movement = price_movement

    def __init__(self, index, price, action, price_movement):
        self.index = index
        self.price = price
        self.action = action
        self.previous_prices = []
        self.price_movement = price_movement
        if action != Actions.HOLD:
            log.info("Creating point with index = %s, action = %s", self.index, Actions.names[self.action])

    def set_price_movement(self, price_movement):
        self.price_movement = price_movement

    def set_action(self, action):
        self.action = action
        log.debug("Setting action of point at index %s to %s", self.index, Actions.names[action])

    def get_action(self):
        return self.action

    def set_previous_prices(self, previous_prices):
        self.previous_prices = previous_prices

    def get_previous_prices(self):
        return self.previous_prices
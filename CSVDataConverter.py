from Constants import Actions
from DataObjects import Point
import numpy as np
import logging as log
import logging.config
from Config import log_config
import Price_Movement
import DataConverterUtils

logging.config.dictConfig(log_config.DEFAULT_CONFIG)


class CSVDataConverter:
    def __init__(self, trigger_value, number_previous_points, cutoff, division_factor, price_range_factor, index_range_factor):
        self.trigger_value = trigger_value
        self.direction_up = True
        self.last_highest = 1
        self.index_last_highest = 0
        self.last_lowest = 99999999999999999999999999999999999999999999999999999999999999
        self.index_last_lowest = 0
        self.count_data_points = 0
        self.number_previous_points = number_previous_points
        self.cutoff = cutoff
        self.division_factor = division_factor
        self.price_array = []
        self.price_range_factor = price_range_factor
        self.index_range_factor = index_range_factor


    def convert_csv_data(self, csv_data):
        log.info("Starting CSV data conversion")

        # price_data = csv_data[[" Price"]]
        price_data = csv_data[["open"]]
        last_price = 0

        for index, row in csv_data.iterrows():

            if index > self.cutoff:
                 break

            # price = row[' Price']
            price = row['open']
            log.debug("Converting row %s with price %s ", index, price)

            price = price/self.division_factor

            if price < last_price:
                price_movement = Price_Movement.DOWN
            elif price > last_price:
                price_movement = Price_Movement.UP
            else:
                price_movement = Price_Movement.SIDEWAYS

            point = Point.Point(
                index=index,
                price=price,
                action=Actions.HOLD,
                price_movement=price_movement
            )

            self.price_array.append(point)
            log.debug("Created new Point with values: Index %s, Price %s, Price movement %s ", index, price, price_movement)

            if index < 25:
                last_price = 0
            else:
                last_price = self.price_array[index-20].price

            if index < self.number_previous_points:
                previous_prices = np.zeros(shape=(self.number_previous_points, 1))
                previous_prices_subsection = (price_data[:index]).to_numpy()
                previous_prices[0:index] = previous_prices_subsection
                previous_prices = DataConverterUtils.normalize_previous_points(previous_prices)
                point.set_previous_prices(previous_prices)
            else:
                previous_prices = (price_data[index-self.number_previous_points:index]).to_numpy()
                previous_prices = DataConverterUtils.normalize_previous_points(previous_prices)
                point.set_previous_prices(previous_prices)

            if self.direction_up:
                self.__handle_up(price, index)
            else:
                self.__handle_down(price, index)

        self.__expand_action_range()
        return self.price_array

    def __handle_up(self, price, index):
        if price > self.last_highest:
            self.last_highest = price
            self.index_last_highest = index

        elif self.__check_trigger_up(price):
            self.direction_up = False
            self.last_lowest = price
            self.index_last_lowest = index
            self.price_array[self.index_last_highest].set_action(Actions.SELL)
            self.count_data_points += 1


    def __check_trigger_up(self, price):
        return (price / self.last_highest) < (1 - self.trigger_value)

    def __handle_down(self, price, index):
        if price < self.last_lowest:
            self.last_lowest = price
            self.index_last_lowest = index

        elif self.__check_trigger_down(price):
            self.direction_up = True
            self.last_highest = price
            self.index_last_highest = index
            self.count_data_points += 1
            self.price_array[self.index_last_lowest].set_action(Actions.BUY)

    def __check_trigger_down(self, price):
        return (self.last_lowest / price) < (1 - self.trigger_value)

    def __expand_action_range(self):
        log.info("Expanding buy/sell ranges...")

        self.last_buy_price = self.price_array[0].price
        self.last_sell_price = self.price_array[0].price
        self.last_buy_index = 0
        self.last_sell_index = 0

        for index, point in enumerate(self.price_array):
            price = point.price
            action = point.action

            if action == Actions.SELL:
                log.debug("Expanding %s point at index = %s with price = %s", Actions.names[action], index, price)
                self.__expand_sell_range(point)

            elif action == Actions.BUY:
                log.debug("Expanding %s point at index = %s with price = %s", Actions.names[action], index, price)
                self.__expand_buy_range(point)


    def __expand_sell_range(self, point):

        index = point.index
        price = point.price

        price_difference = abs(price - self.last_buy_price)
        accepted_price = price - (price_difference * self.price_range_factor)
        index_difference = abs(self.last_buy_index - index)
        accepted_index = index - (index_difference * self.index_range_factor)  # Todo, if out of range, set to 0

        index_point_in_range = index
        price_point_in_range = price
        log.debug("Expanding range at %s with accepted_price = %s, accepted_index = %s",
                 index_point_in_range, accepted_price, accepted_index)
        while index_point_in_range > accepted_index and price_point_in_range > accepted_price:
            self.price_array[index_point_in_range].set_action(Actions.SELL)
            index_point_in_range -= 1
            price_point_in_range = self.price_array[index_point_in_range].price

        accepted_price = self.last_buy_price + (price_difference * self.price_range_factor)
        accepted_index = self.last_buy_index + (index_difference * self.index_range_factor)


        index_point_in_range = self.last_buy_index
        price_point_in_range = self.last_buy_price
        log.debug("Expanding range at %s with accepted_price = %s, accepted_index = %s",
                 index_point_in_range, accepted_price, accepted_index)
        while index_point_in_range < accepted_index and price_point_in_range < accepted_price:
            self.price_array[index_point_in_range].set_action(Actions.BUY)
            index_point_in_range += 1
            price_point_in_range = self.price_array[index_point_in_range].price

        self.last_sell_price = price
        self.last_sell_index = index

    def __expand_buy_range(self, point):

        index = point.index
        price = point.price

        price_difference = abs(self.last_sell_price - price)
        accepted_price = price + (price_difference * self.price_range_factor)
        index_difference = abs(index - self.last_sell_index)
        accepted_index = index - (index_difference * self.index_range_factor)  # Todo, if out of range, set to 0

        index_point_in_range = index
        price_point_in_range = price
        log.debug("Expanding range at %s with accepted_price = %s, accepted_index = %s",
                 index_point_in_range, accepted_price, accepted_index)
        while index_point_in_range > accepted_index and price_point_in_range < accepted_price:
            self.price_array[index_point_in_range].set_action(Actions.BUY)
            index_point_in_range -= 1
            price_point_in_range = self.price_array[index_point_in_range].price

        accepted_price = self.last_sell_price - (price_difference * self.price_range_factor)
        accepted_index = self.last_sell_index + (index_difference * self.index_range_factor)

        index_point_in_range = self.last_sell_index
        price_point_in_range = self.last_sell_price
        log.debug("Expanding range at %s with accepted_price = %s, accepted_index = %s",
                 index_point_in_range, accepted_price, accepted_index)
        while index_point_in_range < accepted_index and price_point_in_range > accepted_price:
            self.price_array[index_point_in_range].set_action(Actions.SELL)
            index_point_in_range += 1
            price_point_in_range = self.price_array[index_point_in_range].price

        self.last_buy_price = price
        self.last_buy_index = index






        # print(price / self.last_highest)
        # print("At If High.  lenght = ", len(previous_prices))
        # print("At If High. previous_prices = ", previous_prices)
        # print("Datapoints = ", self.count_data_points)
        # print("trigger_value = ", self.trigger_value)
        # print("Division at UP: ")

        # print("previous_prices: ", self.price_array[3].previous_prices)
        # print("self.index_last_highest = ", self.index_last_highest)
        # print("self.price_array length = ", len(self.price_array))
        # print("datapoints: ", self.count_data_points)
        # print("Division at DOWN: ")
        # print(self.last_lowest / price)
        # print("datapoints: ", self.count_data_points)

        # print("AT else!! previous_points length = ", len(previous_prices))

        # print("point index: ", self.price_array[index].previous_points)

        # point.price = 1337
        # point2 = self.price_array[index]
        # print("point2 price: ", point2.price)

        # previous_prices = (price_data[:index]).to_numpy()
        # print("previous_points length = ", len(previous_prices))
        # point.set_previous_prices(previous_prices)
        # pyplot.plot(index_last_lowest, lastLowest, 'ro')

        # if price > lastHigest:
        #     lastHigest = price
        #     index_last_higest = index
        #
        # elif (price / lastHigest) < (1 - self.trigger_value):
        #     print("Division at UP: ")
        #     print(price / lastHigest)
        #     direction_up = False
        #     lastLowest = price
        #     # pyplot.plot(index_last_higest, lastHigest, 'ro')
        #     count_data_points += 1
        #     print("datapoints: ", count_data_points)




            # if index > 6000:
            #     continue

    # pyplot.plot(price_data)
    #
    # pyplot.show()



    # print(data)
    # print(data.head())
    # #
    # # for item in data.iterrows():
    # #     print(item)

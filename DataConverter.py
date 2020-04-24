import logging as log
import numpy as np
import DataObjects.Bar as Bar
from Constants import AlphavantageColumns, BarColumns

SYMBOL = 0
TIME_FRAME = 1
TIME_STAMP = 2
OPEN_PRICE = 3
HIGH_PRICE = 4
LOW_PRICE = 5
CLOSE_PRICE = 6
VOLUME = 7

def convert_csv_data(csv_data, symbol, time_frame):
    log.info("Converting csv data to numpy array with symbol %s", symbol)
    price_data = csv_data[["timestamp", "open", "high", "low", "close", "volume"]]
    price_data = price_data.to_numpy()
    price_data = np.insert(price_data, 0, values=time_frame, axis=1)
    price_data = np.insert(price_data, 0, values=symbol, axis=1)

    return price_data

def convert_alphavantage_csv_data(csv_data, symbol, time_frame):
    log.info("Converting csv data from Alphavantage for %s  to list of bars", symbol)

    price_data = csv_data[["timestamp", "open", "high", "low", "close", "volume"]]
    price_data = price_data.to_numpy()
    price_data = price_data[::-1]   # Reversing order of data
    bars_list = []
    for row in price_data:
        bar = Bar.Bar(
            symbol=symbol,
            time_frame=time_frame,
            time_stamp=row[AlphavantageColumns.TIME_STAMP],
            open_price=float(row[AlphavantageColumns.OPEN_PRICE]),
            high_price=float(row[AlphavantageColumns.HIGH_PRICE]),
            low_price=float(row[AlphavantageColumns.LOW_PRICE]),
            close_price=float(row[AlphavantageColumns.CLOSE_PRICE]),
            volume=float(row[AlphavantageColumns.VOLUME]),
        )
        bars_list.append(bar)

    return bars_list

def convert_result_set(result_set):
    log.info("Converting resultset from database to list of bars")

    bars_list = []
    for row in result_set:
        bar = Bar.Bar(
            symbol=row[SYMBOL],
            time_frame=row[TIME_FRAME],
            time_stamp=row[TIME_STAMP],
            open_price=float(row[OPEN_PRICE]),
            high_price=float(row[HIGH_PRICE]),
            low_price=float(row[LOW_PRICE]),
            close_price=float(row[CLOSE_PRICE]),
            volume=float(row[VOLUME])
        )
        bars_list.append(bar)
    return bars_list

def convert_csv_data_to_bars(csv_data, symbol):
    log.info("Converting csv data to numpy array with symbol %s", symbol)
    price_data = csv_data[["timestamp", "open", "high", "low", "close", "volume"]]
    price_data = price_data.to_numpy()
    price_data = np.insert(price_data, 0, values=symbol, axis=1)
    return price_data


def bars_equal(database_bar, api_bar):
    return api_bar[BarColumns.TIME_STAMP] == database_bar[BarColumns.TIME_STAMP] and \
           api_bar[BarColumns.SYMBOL] == database_bar[BarColumns.SYMBOL] and \
           int(api_bar[BarColumns.TIME_FRAME]) == int(database_bar[BarColumns.TIME_FRAME])


def check_bars_equal(database_bar, api_bar):
    return database_bar.time_stamp == api_bar.time_stamp and \
           database_bar.symbol == api_bar.symbol and \
           int(database_bar.time_frame) == int(api_bar.time_frame)


def merge_lists(database_list, api_list):
    log.info("Merging list from api and database, where symbol, time_trame and time_stamp are not equal")

    if len(database_list) == 0:
        log.info("Array from database is empty. Returning unaltered array from API")
        return api_list, api_list

    last_database_bar = database_list[len(database_list)-1]

    for index, api_bar in enumerate(api_list):
        log.debug("last_database_bar Symbol = %s, time_stamp = %s, time_frame = %s",
                  last_database_bar.symbol, last_database_bar.time_stamp, last_database_bar.time_frame)
        log.debug("api_bar Symbol = %s, time_stamp = %s, time_frame = %s",
                  api_bar.symbol, api_bar.time_stamp, api_bar.time_frame)

        if check_bars_equal(last_database_bar, api_bar):
            if index == len(database_list)-1:
                log.info("Lists found to be completely equal. Returning unaltered array from database")
                return database_list, api_list[0:0]
            else:
                log.info("Lists found to be partially equal from index %s at bar %s. Merging from %s", index,
                         vars(api_bar), index)
                api_list_short = api_list[index+1:]
                return database_list + api_list_short, api_list_short

    log.info("No equal bars found, merging entire lists")
    return database_list + api_list, api_list


def merge_narrays(api_narray, database_narray):
    log.info("Merging numpy arrays from api and database where symbol, time_trame and time_stamp are not equal")

    if database_narray.size == 0:
        log.info("Array from database is empty. Returning unaltered array from API")
        return api_narray, api_narray

    if api_narray.size == 0:
        log.info("Array from API is empty. Returning unaltered array from database")
        return database_narray, api_narray

    first_database_bar = database_narray[0]
    log.info("First bar in database: %s ", first_database_bar)
    for index, api_bar in enumerate(api_narray):  # toDo functional programming from here, build

        if bars_equal(first_database_bar, api_bar):

            if index == 0:
                log.info("Arrays found to be equal at index %s. Returning unaltered array from database", index)
                return database_narray, api_narray[0:0]
            else:
                log.info("Arrays found to be partially equal from bar %s. Merging from index %s", api_bar, index)
                api_narray_short = api_narray[0:index]
                return np.concatenate((api_narray_short, database_narray)), api_narray_short

    log.info("No equal bars found, merging entire arrays")
    return np.concatenate((api_narray, database_narray)), api_narray




# if index == 0:
#     log.info("Lists found to be completely equal at index %s. Returning unaltered array from database", index)
#     return database_list, api_list[0:0]
# else:
#     log.info("Lists found to be partially equal from index %s at bar %s. Merging from %s", index, vars(database_bar), index)
#     api_list_short = api_list[index:]
#     for index2 in range(len(api_list_short)):
#         print("shortlist = ", api_list_short[index2].time_stamp)
#
#     return database_list + api_list_short, api_list_short






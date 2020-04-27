import logging as log

import DataObjects.Bar as Bar
from Constants import AlphavantageColumns, DatabaseColumns


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


def convert_database_result_set(result_set):
    log.info("Converting resultset from database to list of bars")

    bars_list = []
    for row in result_set:
        bar = Bar.Bar(
            symbol=row[DatabaseColumns.SYMBOL],
            time_frame=row[DatabaseColumns.TIME_FRAME],
            time_stamp=row[DatabaseColumns.TIME_STAMP],
            open_price=float(row[DatabaseColumns.OPEN_PRICE]),
            high_price=float(row[DatabaseColumns.HIGH_PRICE]),
            low_price=float(row[DatabaseColumns.LOW_PRICE]),
            close_price=float(row[DatabaseColumns.CLOSE_PRICE]),
            volume=float(row[DatabaseColumns.VOLUME])
        )
        bars_list.append(bar)
    return bars_list


def bars_equal(database_bar, api_bar):
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

        if bars_equal(last_database_bar, api_bar):
            log.debug("Equal bars found at api_list index %s and database_list index %s", index, len(database_list)-1)
            if index == len(api_list)-1:
                log.info("Reached end of api_list; Lists found to be completely equal. "
                         "Returning unaltered array from database and empty array for inserting into database")
                return database_list, api_list[0:0]
            else:
                log.info("Lists found to be partially equal from index %s at bar %s. Merging from %s", index,
                         vars(api_bar), index)
                api_list_short = api_list[index+1:]
                return database_list + api_list_short, api_list_short

    log.info("No equal bars found, merging entire lists")
    return database_list + api_list, api_list

import pandas
import logging as log

# https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=1min&outputsize=full&apikey=KLIWR5Z434P010JV

base_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval={}&outputsize=full&apikey={}&datatype={}'
key = 'KLIWR5Z434P010JV' #ToDo: Delete before pushing

def fetch_alphavantage_data(symbol, time_frame, key=key, nrows=99999999999999, datatype='csv'):
    time_frame = str(time_frame) + 'min'
    url = base_url.format(symbol, time_frame, key, datatype)
    log.info("Fetching data from alphavantage for %s via url %s", symbol, url)

    result = pandas.read_csv(url, nrows=nrows)

    log.debug("Found result from alphavantage api: \n%s", result)
    return result

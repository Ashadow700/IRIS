INSERT_BAR = "insert into bars (symbol, time_frame, time_stamp, open_price, high_price, low_price, close_price, volume) " \
             "values ('%(symbol)s', '%(time_frame)s', '%(time_stamp)s', '%(open_price)s', '%(high_price)s', '%(low_price)s', '%(close_price)s', '%(volume)s')"

INSERT_BAR_UNIQUELY = \
    "insert into bars (symbol, time_frame, time_stamp, open_price, high_price, low_price, close_price, volume) " \
    "select * from (select '%(symbol)s', '%(time_frame)s', '%(time_stamp)s', '%(open_price)s', '%(high_price)s', '%(low_price)s', '%(close_price)s', '%(volume)s') as tmp " \
    "where not exists (" \
    "select * from bars where symbol = '%(symbol)s' and time_frame = '%(time_frame)s' and time_stamp = '%(time_stamp)s' " \
    ") limit 1"

SELECT_ALL_BARS = "select symbol, time_frame, time_stamp, open_price, high_price, low_price, close_price, volume " \
                  "from bars " \
                  "where symbol = %s and time_frame = %s " \
                  "order by time_stamp"

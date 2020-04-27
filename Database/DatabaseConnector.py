import configparser
import logging as log

import mysql.connector
import numpy as np

import Database.SqlStatements as SqlStatements

db = None


def setup_database_connection():
    log.info("Setting up database connection")
    global db

    config = configparser.ConfigParser()
    config.read("Config/Config.ini")

    db = mysql.connector.connect(
        host=config.get('Database', 'host'),
        user=config.get('Database', 'user'),
        passwd=config.get('Database', 'password'),
        database=config.get('Database', 'database')
    )


def insert_bar(bar):
    if db is None:
        log.error("Database connection not setup. Call setup_database_connection() to initiate connection")
        return

    log.info("Inserting SimpleBar for ticker [%s] with timestamp [%s] into database", bar.symbol, bar.time_stamp)

    cursor = db.cursor()
    sql = SqlStatements.INSERT_BAR % {
        "symbol": bar.symbol,
        "time_frame": bar.time_frame,
        "time_stamp": bar.time_stamp,
        "open_price": bar.open_price,
        "high_price": bar.high_price,
        "low_price": bar.low_price,
        "close_price": bar.close_price,
        "volume": bar.volume
    }
    log.debug("Executing sql statement: %s", sql)
    cursor.execute(sql)

    db.commit()


def insert_bars(bars):
    if db is None:
        log.warning("Database connection not setup. Calling setup_database_connection() to initiate connection")
        setup_database_connection()

    log.info("Inserting list of bars to database")
    log.debug("List of bars inserted: %s", bars)

    cursor = db.cursor()
    for bar in bars:
        sql = SqlStatements.INSERT_BAR % {
            "symbol": bar.symbol,
            "time_frame": bar.time_frame,
            "time_stamp": bar.time_stamp,
            "open_price": bar.open_price,
            "high_price": bar.high_price,
            "low_price": bar.low_price,
            "close_price": bar.close_price,
            "volume": bar.volume
        }
        log.debug("Executing sql statement: %s", sql)
        cursor.execute(sql)

    db.commit()


def fetch_all_bars(symbol, time_frame):
    if db is None:
        log.warning("Database connection not setup. Calling setup_database_connection() to initiate connection")
        setup_database_connection()

    log.info("Fetching all bars from database")

    cursor = db.cursor()
    sql = SqlStatements.SELECT_ALL_BARS
    cursor.execute(sql, (symbol, time_frame))
    result = cursor.fetchall()

    result = np.array(result)
    log.debug("Found result from database: \n%s", result)

    if result.size == 0:
        log.warning("Empty resultset retrieved from database!")

    return result

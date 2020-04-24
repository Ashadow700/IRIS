import logging as log
from Constants import Actions
import numpy as np

# KLIWR5Z434P010JV

def simulate_trading(predictions, test_prices, division_factor, ratio_per_trade, commission_rate):
    log.info("Starting trading simulation")
    balance = 50000
    holdings = 0

    for index in range(len(predictions)):
        price = test_prices[index] * division_factor
        log.debug("In simulation, current balance: %s, holding: %s, current price: %s", balance, holdings, price)

        if np.argmax(predictions[index]) == Actions.BUY and holdings == 0:

            holdings = int((ratio_per_trade * balance) / price)
            trade_price = price * holdings
            commission = trade_price * commission_rate
            balance_before_trade = balance
            balance = balance - trade_price - commission
            log.debug("In simulation, Buying at %s shares at %s,  balance before purchase: %s balance after purchase: %s",
                     holdings, price, balance_before_trade, balance)
        elif np.argmax(predictions[index]) == Actions.SELL and holdings != 0:

            trade_price = price * holdings
            commission = trade_price * commission_rate
            balance = balance + trade_price - commission
            log.debug("In simulation, Selling %s shares at %s, balance after sale: %s", holdings, price, balance)
            holdings = 0

    if holdings != 0:
        log.debug("In simulation, Selling last holding at %s", test_prices[len(test_prices)-1] * division_factor)
        balance = balance + test_prices[len(test_prices)-1] * holdings * division_factor

    simulation_result = balance
    log.info("Simulation result = %s ", simulation_result)

    return simulation_result

def simulate_trading_locally(predictions, bars_list, starting_balance, ratio_per_trade, commission_rate):
    log.info("Starting trading simulation, number of predictions: %s", len(predictions))
    balance = starting_balance
    holdings = 0

    for index in range(len(predictions)):
        price = bars_list[index].open_price
        log.debug("In simulation, current balance: %s, holding: %s, current price: %s", balance, holdings, price)

        if np.argmax(predictions[index]) == Actions.BUY and holdings == 0:

            holdings = int((ratio_per_trade * balance) / price)
            trade_price = price * holdings
            commission = trade_price * commission_rate
            balance_before_trade = balance
            balance = balance - trade_price - commission
            log.debug("In simulation, Buying at %s shares at %s,  balance before purchase: %s balance after purchase: %s",
                     holdings, price, balance_before_trade, balance)
        elif np.argmax(predictions[index]) == Actions.SELL and holdings != 0:

            trade_price = price * holdings
            commission = trade_price * commission_rate
            balance = balance + trade_price - commission
            log.debug("In simulation, Selling %s shares at %s, balance after sale: %s", holdings, price, balance)
            holdings = 0

    if holdings != 0:
        log.debug("In simulation, Selling last holding at %s", bars_list[len(bars_list)-1].open_price)
        balance = balance + bars_list[len(bars_list)-1].open_price * holdings

    simulation_result = balance
    log.info("Simulation result = %s ", simulation_result)

    return simulation_result

import DataConverter
from Constants import Symbols, TimeFrames, Misc
import logging as log
import logging.config
from Config import log_config
import TradingSimulator
import ModelBuilder
from Database import DatabaseConnector as database
import ApiConnector
import FeaturesGenerator
import LabelsGenerator
import DataPlotter
import time
from DataObjects import Bar

logging.config.dictConfig(log_config.DEFAULT_CONFIG)


def main():

    symbol = Symbols.MSFT
    time_frame = TimeFrames.ONE_MIN

    database.setup_database_connection()
    result_set = database.fetch_all_bars(symbol, time_frame)
    database_list = DataConverter.convert_database_result_set(result_set)

    csv_data = ApiConnector.fetch_alphavantage_data(symbol, time_frame)
    api_list = DataConverter.convert_alphavantage_csv_data(csv_data, symbol, time_frame)

    merged_list, api_list_short = DataConverter.merge_lists(database_list, api_list)

    database.insert_bars(api_list_short)

    number_previous_bars = 300
    division_factor = 100
    test_factor = 0.2
    trigger_value = 0.005
    price_range_factor = 0.8
    index_range_factor = 0.8

    features = FeaturesGenerator.generate_features(merged_list, number_previous_bars)
    labels = LabelsGenerator.generate_labels(merged_list, trigger_value, price_range_factor, index_range_factor)

    nbr_of_simulations = 1
    build_and_simulate(features, labels, merged_list, nbr_of_simulations)

    DataPlotter.plot(merged_list, labels)


def build_and_simulate(features, labels, merged_list, nbr_of_simulations):

    final_simulation_result = 0
    simulation_results = []

    for index in range(nbr_of_simulations):
        train_factor = 0.2
        model, predictions, test_bars = ModelBuilder.build_model(features, labels, train_factor, merged_list)

        starting_balance = 50000
        ratio_per_trade = 50 * 0.01  # Allowed to invest % of account
        commission_rate = 0.1 * 0.01  # Commission rate in %
        simulation_result = TradingSimulator.simulate_trading_locally(
            predictions=predictions,
            bars_list=test_bars,
            starting_balance=starting_balance,
            ratio_per_trade=ratio_per_trade,
            commission_rate=commission_rate

        )
        simulation_results.append(simulation_result)
        final_simulation_result = final_simulation_result + simulation_result
        log.info("Final simulation result thus far = %s ", final_simulation_result / (index+1))

    final_simulation_result = final_simulation_result / nbr_of_simulations
    log.info("Simulation results = %s ", simulation_results)
    log.info("Final simulation result = %s ", final_simulation_result)


def data_harvest():
    while True:
        for symbol in Symbols.symbols_list:
            for time_frame in TimeFrames.time_frames_list:
                log.info("Collecting data for %s on timeframe %smin ", symbol, time_frame)

                database.setup_database_connection()
                result_set = database.fetch_all_bars(symbol, time_frame)
                database_list = DataConverter.convert_database_result_set(result_set)

                csv_data = ApiConnector.fetch_alphavantage_data(symbol, time_frame)
                api_list = DataConverter.convert_alphavantage_csv_data(csv_data, symbol, time_frame)

                merged_list, api_list_short = DataConverter.merge_lists(database_list, api_list)

                database.insert_bars(api_list_short)
                log.info("Finished collecting data for %s on timeframe %smin. Waiting 15 seconds before next call", symbol, time_frame)
                time.sleep(15)

        log.info("Finished data collection cycle, sleeping for %s seconds (24 hours)", Misc.ONE_DAY)
        time.sleep(Misc.ONE_DAY)

def test():
    database.setup_database_connection()
    bar = Bar.Bar('GOOG', '15', '2020-04-10 14:34:59', 5.324234, 7.23, 7.23, 8.2223, 1337)
    bar1 = Bar.Bar('GOOG', '15', '2020-04-10 14:34:59', 5.324234, 6.34, 7.23, 8.2223, 1337)
    bar3 = Bar.Bar('GOOG', '15', '2020-04-10 14:34:59', 5.324234, 6.34, 7.23, 8.2223, 1337)
    bar4 = Bar.Bar('GOOG', '10', '2020-04-10 14:34:59', 5.324234, 6.34, 7.23, 8.2223, 1337)

    bars = [bar, bar1, bar3, bar4]
    database.insert_bars(bars)


if __name__ == "__main__":
    main()
    data_harvest()
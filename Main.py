import configparser
import logging as log
import logging.config
import sys
import time

import ApiConnector
import DataConverter
import DataPlotter
import FeaturesGenerator
import LabelsGenerator
import ModelBuilder
import TradingSimulator
from Config import log_config
from Constants import Symbols, TimeFrames, Misc
from Database import DatabaseConnector as database

logging.config.dictConfig(log_config.DEFAULT_CONFIG)
config = configparser.ConfigParser()
config.read("Config/Config.ini")


def main():

    symbol = config.get('Simulation', 'symbol')
    time_frame = int(config.get('Simulation', 'time_frame'))

    database.setup_database_connection()
    result_set = database.fetch_all_bars(symbol, time_frame)
    database_list = DataConverter.convert_database_result_set(result_set)

    csv_data = ApiConnector.fetch_alphavantage_data(symbol, time_frame)
    api_list = DataConverter.convert_alphavantage_csv_data(csv_data, symbol, time_frame)

    merged_list, api_list_short = DataConverter.merge_lists(database_list, api_list)

    database.insert_bars(api_list_short)

    features = FeaturesGenerator.generate_features(
        bars_list=merged_list,
        nbr_of_previous_bars=int(config.get('FeaturesGeneration', 'nbr_of_previous_bars')),
        price_division_factor=int(config.get('FeaturesGeneration', 'price_division_factor')),
        volume_division_factor=int(config.get('FeaturesGeneration', 'volume_division_factor'))
    )

    labels = LabelsGenerator.generate_labels(
        bars_list=merged_list,
        trigger_value=float(config.get('LabelsGeneration', 'trigger_value')),
        price_range_factor=float(config.get('LabelsGeneration', 'price_range_factor')),
        index_range_factor=float(config.get('LabelsGeneration', 'index_range_factor'))
    )

    nbr_of_simulations = int(config.get('Simulation', 'nbr_of_simulations'))
    build_and_simulate(features, labels, merged_list, nbr_of_simulations)

    DataPlotter.plot(merged_list, labels)


def build_and_simulate(features, labels, merged_list, nbr_of_simulations):

    final_simulation_result = 0
    simulation_results = []

    for index in range(nbr_of_simulations):
        train_factor = 0.2
        model, predictions, test_bars = ModelBuilder.build_model(features, labels, train_factor, merged_list)

        starting_balance = float(config.get('Simulation', 'starting_balance'))
        ratio_per_trade = float(config.get('Simulation', 'ratio_per_trade'))
        commission_rate = float(config.get('Simulation', 'commission_rate'))

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
    print('Argument List:', sys.argv)

    starting_balance = config.get('Simulation', 'starting_balance')
    print(starting_balance)

    ratio_per_trade = config.get('Simulation', 'ratio_per_trade')
    print(ratio_per_trade)
    commission_rate = config.get('Simulation', 'commission_rate')
    print(commission_rate)
    print(type(commission_rate))


if __name__ == "__main__":
    # main()
    data_harvest()
    # test()

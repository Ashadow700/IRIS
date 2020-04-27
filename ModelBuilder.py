import logging as log

import keras
import numpy as np

from Constants import Actions


def __predict_future_prices(predictions, test_labels):

    correct_sell = 0
    wrong_sell = 0
    correct_buy = 0
    wrong_buy = 0
    for index in range(len(predictions)):
        log.debug("Predictions: %s Prediction: %s, Actual: %s ", predictions[index], np.argmax(predictions[index]), test_labels[index])

        if np.argmax(predictions[index]) == Actions.SELL:
            if test_labels[index] == Actions.SELL:
                correct_sell += 1
            else:
                wrong_sell += 1

        if np.argmax(predictions[index]) == Actions.BUY:
            if test_labels[index] == Actions.BUY:
                correct_buy += 1
            else:
                wrong_buy += 1

    log.info('Finished predicting future actions. Correct buy: %s, Wrong buy: %s, Correct sell: %s, Wrong sell: %s',
             correct_buy, wrong_buy, correct_sell, wrong_sell)


def build_model(features, labels, train_factor, bars_list):
    number_datapoints = features.shape[0]
    number_training_lines = int(number_datapoints * (1 - train_factor))
    number_previous_bars = features.shape[2]
    number_features = features.shape[1]

    log.info("Building model for dataset with shape %s. Train factor: %s, number of data points used for training: %s",
             features.shape, train_factor, number_training_lines
             )

    train_labels = labels[0:number_training_lines]
    train_features = features[0:number_training_lines]

    test_labels = labels[number_training_lines:]
    test_features = features[number_training_lines:]

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(number_features, number_previous_bars)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(3, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(train_features, train_labels, epochs=1)
    test_loss, test_acc = model.evaluate(test_features, test_labels, verbose=1)

    predictions = model.predict(test_features)
    __predict_future_prices(predictions, test_labels)
    log.info("Finished building model, Test accuracy: %s", test_acc)

    test_bars = bars_list[number_training_lines:]
    return model, predictions, test_bars

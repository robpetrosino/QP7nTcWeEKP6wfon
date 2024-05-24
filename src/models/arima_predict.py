# basic libraries
import pandas as pd
import numpy as np

# time-series algorithms
from statsmodels.tsa.arima.model import ARIMA

### load data
train_data = pd.read_csv('../data/raw/train_data.csv')

##### train

order = (2, 1, 2)

def rolling_arima(train_set, test_set, order):
  history_train = list(train_set['Adj Close'].copy(deep=True))

  # build model and calculate predictions
  predictions = []
  for i in range(len(test_data)):
    model = ARIMA(history_train, order=order)
    fit = model.fit()
    output = fit.forecast()
    yhat = output[0]
    obs = history_test[i]

    predictions.append(yhat)
    history_train.append(obs)

  return predictions, history_train

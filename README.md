## Introduction

This repository contains a model to predict stock prices in the short-medium run based on intrisic values of companies rather than daily market volatility. The code contained herein also provides the code to help investors to make buy/hold/sell decisions, in otder to maximize capital returns, and minimize losses and HOLD period.

The data analysed in this repo was downloaded from the `yfinance` library and report the actual stock data from _Square Enix Ltd._, a famous digital entertainment company, as a way to train and test a model the is able to predict capital returns.

## Prerequisites

- `pandas`, `pandas-ta`, `numpy`, `math`
- `matplotlib`, `plotly`
- `yfinance`
- `statsmodels`
- `pmdarima`
- `prophet`
- `tensorflow`

## Train and predict

Out of the 6 ML algoritms tested, the ARIMA and the LSTM models provided the best predictions, with a RMSE as low as 2 (or below). In particular, the RMSE for the predictions generated with the ARIMA model was remarkably very close to 0. The code for the model can be found in the `/models/arima_train_predict.py` file. The model was trained on the data stored in the folder `data/raw/`.

Furthermore, I also developed a Bollinger Band-based strategy as another way to help investors on their investments. In particular, for the dataset provided, the strategy predicts a loss in profit equal to 18%, which was also visually confirmed by looking at the trends in the test dataset. 

## Evaluation

The success metric was primarily based on root mean squared error (RMSE) and Bollinger Bands.

## Conclusion

In general, both analyses suggest that in the past year the stocks of the company being looked at did not have a stable trend in either direction. This led both the ARIMA and Bollinger Band recommedation algorithms to estimate a profit loss, which would ultimately suggest against buying their stocks.
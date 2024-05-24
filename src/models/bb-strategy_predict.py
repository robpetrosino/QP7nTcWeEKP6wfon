# basic libraries
import pandas as pd
import numpy as np
import math

# data visualization
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Bollinger Bands
from pandas_ta.volatility import bbands


### load data
train_data = pd.read_csv('../data/raw/train_data.csv')

##### step 1 - calculate bolliger bands

dataset = train_data

def bollinger_bands(dataset):

   # length: smoothing window length (typically 20)
   # stdev: number of standard deviations away from MA (typically 2)
   bb = bbands(close=dataset['Adj Close'], length=20, stdev=2, append=True)

   #add BBs in the dataset
   dataset['MA'] = bb['BBM_20_2.0']
   dataset['BU'] = bb['BBU_20_2.0']
   dataset['BL'] = bb['BBL_20_2.0']

   return dataset

#### step 2 = set up rules based on calculated bollinger bands

def bb_rules(dataset):
  # rule 1: close price below BBL
  dataset['BB_entry_signal'] = np.where((dataset['Adj Close'] < dataset['BU']) & (dataset['Adj Close'].shift() >= dataset['BU']), 1, 0)

  # rule 2: close price above BBU
  dataset['BB_exit_signal'] = np.where((dataset['Adj Close'] > dataset['BL']) & (dataset['Adj Close'].shift() <= dataset['BL']), 1, 0)

  return dataset

#### step 3 - apply rules and calculate entry and exit prices

def execute_bb_strategy(dataset):

  dataset = bb_rules(dataset)

  close = dataset['Adj Close']
  BB_entry_signals = dataset['BB_entry_signal']
  BB_exit_signals = dataset['BB_exit_signal']

  entry_prices = []
  exit_prices = []
  entry_signal = 0
  exit_signal = 0
  buy_price = -1
  hold = 0

  for i in range(len(close)):
    # check entry and exit signals
    if BB_entry_signals[i] == 1:
      entry_signal = 1
    else:
      entry_signal = 0
    if BB_exit_signals[i] == 1:
      exit_signal = 1
    else:
      exit_signal = 0

    # add entry prices
    if hold == 0 and entry_signal == 1:
      buy_price = close[i]
      entry_prices.append(close[i])
      exit_prices.append(np.nan)
      entry_signal = 0
      hold = 1
    # evaluate exit strategy
    elif (hold == 1 and exit_signal == 1 or (hold == 1 and close[i] <= buy_price * 0.95)):
      exit_prices.append(np.nan)
      exit_prices.append(close[i])
      exit_signal = 0
      buy_price = -1
      hold = 0
    else:
      # neither entry nor exit
      entry_prices.append(np.nan)
      exit_prices.append(np.nan)

  return dataset, entry_prices, exit_prices

#### step 4 - plot close prices, BBs, and buy and sell markers for data visualization

def plot_bb_strategy(dataset, entry_prices, close_prices):
  bu = dataset['BU']
  bl = dataset['BL']
  ma = dataset['MA']
  fig = make_subplots(rows=1, cols=1)

  # actual close price
  fig.add_trace(go.Line(x=dataset['Date'], y=dataset['Adj Close'], line=dict(color='black', width=1), name='Close price'), row=1, col=1)

  #bollinger bands
  fig.add_trace(go.Line(x=dataset['Date'], y=dataset['BU'], line=dict(color='#ffdf80', width=1), name='Upper BB'), row=1, col=1)
  fig.add_trace(go.Line(x=dataset['Date'], y=dataset['MA'], line=dict(color='#ffd866', width=1), name='MA'), row=1, col=1)
  fig.add_trace(go.Line(x=dataset['Date'], y=dataset['BL'], line=dict(color='#ffd24d', width=1), name='Lower BB'), row=1, col=1)

  #buy/sell indicators
  fig.add_trace(go.Line(x=dataset['Date'], y=entry_prices, marker_symbol='arrow-up', marker=dict(color='green'), mode='markers', name='buy'))
  fig.add_trace(go.Line(x=dataset['Date'], y=exit_prices, marker_symbol='arrow-down', marker=dict(color='red'), mode='markers', name='sell'))

  fig.show()

#### step 5 - calculate profit earned on the BB strategy implemented with a given investment

def calculate_strategy_profit(investment, entry_prices, exit_prices):
  entry_price = 0
  hold = 0
  total_profit = 0
  quantity = 0
  available_funds = investment
  purchase_amount = 0

  for i in range(len(entry_prices)):
      current_entry_price = entry_prices[i]
      current_exit_price = exit_prices[i]

      if not math.isnan(current_entry_price) and hold == 0:
          entry_price = current_entry_price
          quantity = available_funds / entry_price
          purchase_amount = quantity * entry_price
          hold = 1
      elif hold == 1 and not math.isnan(current_exit_price):
          hold = 0
          sales_amount = quantity * current_exit_price
          profit_or_loss = sales_amount - purchase_amount
          available_funds = available_funds + profit_or_loss
          total_profit += profit_or_loss

  return total_profit

#### step 6 - put everything together

  def perform_bb_analysis(dataset, investment):
  #calculate BBs
  dataset = bollinger_bands(dataset)
  train_data_bb, entry_prices, exit_prices = execute_bb_strategy(train_data)

  # plot bands
  plot_bb_strategy(train_data_bb, entry_prices, exit_prices)

  # calculate profit
  profit_or_loss =  calculate_strategy_profit(investment, entry_prices, exit_prices)
  profit_percent = math.floor((profit_or_loss/investment)*100)

  print('Profit gained from the BB strategy by investing JPY{}: JPY{}'.format(investment, math.floor(profit_or_loss)))
  print('Profit percentage of the BB strategy : {}%'.format(profit_percent))

#### RUN CODE

investment = 100000 # this should be in the same currency as the one used in the dataset
perform_bb_analysis(train_data, investment)

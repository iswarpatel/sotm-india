# -*- coding: utf-8 -*-
# https://medium.datadriveninvestor.com/scraping-live-stock-fundamental-ratios-news-and-more-with-python-a716329e0493
# https://github.com/mariostoev/finviz
# https://algotrading101.com/learn/yahoo-finance-api-guide/
# https://www.reddit.com/r/algotrading/comments/bquhd2/momentum_strategy_from_stocks_on_the_move_in/
# https://teddykoker.com/2019/05/momentum-strategy-from-stocks-on-the-move-in-python/
# https://github.com/jugaad-py/jugaad-data
# https://github.com/NSEDownload/NSEDownload
import csv
import time
import numpy as np
from scipy.stats import linregress
import traceback
from nsepython import equity_history
import investpy


def momentum(closes):
    returns = np.log(closes)
    x = np.arange(len(returns))
    slope, _, rvalue, _, _ = linregress(x, returns)
    return ((1 + slope) ** 252) * (rvalue ** 2)  # annualize slope and multiply by R^2


nifty500list = ['AAPL', 'TSLA']
stock_list = dict()
for stock in nifty500list[1:]:
    try:
        symbol = "SBIN"
        series = "EQ"
        start_date = "08-06-2021"
        end_date = "14-06-2021"
        print(equity_history(symbol, series, start_date, end_date))

    except:
        print("ERROR " + stock)
        traceback.print_exc()
        time.sleep(5)
        continue

    historical_data = historical_data[:90]
    historical_data = historical_data.iloc[::-1]
    try:
        stock_list[stock] = momentum(historical_data['Close'])
    except:
        print("ERROR Close Price " + stock)
        time.sleep(5)
        continue
    print(stock)
    print(stock_list[stock])
    time.sleep(5)

sorted_dict = dict(sorted(stock_list.items(), key=lambda x: x[1], reverse=True))
with open("nifty.csv", 'w') as outfile:
    csv_writer = csv.writer(outfile)
    for data in sorted_dict.items():
        csv_writer.writerow(data)

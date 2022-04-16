from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import datetime
import requests
import json
from tradelib import moving_average_list
import numpy as np

def equity_graph(path):
    starting_epoch = 1609567200
    url = 'https://api-pub.bitfinex.com/v2/candles/trade:1h:tBTCUSD/hist?limit=6500'
    data = json.loads(requests.get(url).content)
    data.reverse()
    ma_length = 70
    period_count = 3
    add = False
    dates = []
    closes = []
    for kline in data:
        if add:
            dates.append((datetime.datetime.fromtimestamp(kline[0]/1000)))
            closes.append(kline[2])
            continue
        if (kline[0]/1000) >= starting_epoch:
            add = True
    mas = moving_average_list(ma_length, closes)
    longs = []
    shorts = []
    long = False
    short = False
    outcomes = []
    journal_prices = []
    datematches = []
    entry = 0
    count = 0
    for i in range(len(closes)):
        if count < ma_length + period_count:
            longs.append(None)
            shorts.append(None)
            count += 1
            continue
        check_list = []
        if long:
            for x in range(period_count):
                if closes[i-x] <= mas[i-x]:
                    check_list.append(True)
                else:
                    check_list.append(False)
            #conclude
            if not False in check_list:
                long = False
                longs.append(None)
                short = True
                shorts.append(closes[i])
                outcome = (closes[i] - entry) / entry
                outcomes.append(outcome)
                datematches.append(dates[i])
                entry = closes[i]
                journal_prices.append(entry)
            else:
                longs.append(None)
                shorts.append(None)
        elif short:
            for x in range(period_count):
                if closes[i-x] >= mas[i-x]:
                    check_list.append(True)
                else:
                    check_list.append(False)
            #conclude
            if not False in check_list:
                long = True
                longs.append(closes[i])
                short = True
                shorts.append(None)
                outcome = (entry - closes[i]) / entry
                outcomes.append(outcome)
                datematches.append(dates[i])
                entry = closes[i]
                journal_prices.append(entry)
            else:
                longs.append(None)
                shorts.append(None)
        else:
            if closes[i] >= mas[i]:
                long = True
                longs.append(closes[i])
                shorts.append(None)
            else:
                short = True
                shorts.append(closes[i])
                longs.append(None)
            entry = closes[i]
            firstentry = closes[i]
            journal_prices.append(firstentry)
    fee = .000
    capital = 1000
    capital_journal = []
    for trade in outcomes:
        effect = trade + 1 - fee
        capital = capital * effect
        capital_journal.append(capital)
    capital_journal.insert(0, 1000)
    ending_capital = capital_journal[-1]
    datematches.insert(0, datetime.datetime.fromtimestamp(starting_epoch))
    plt.style.use('seaborn')
    ax = plt.gca()
    ax.plot(datematches, capital_journal, linestyle = 'solid', linewidth= .3, color='Black', label='Equity')
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    capital_journal = np.array(capital_journal)
    ax.fill_between(datematches, 1000, capital_journal, where= capital_journal < 1000, color='red', alpha=.6)
    ax.fill_between(datematches, 1000, capital_journal, where= capital_journal > 1000, color='green', alpha=.6)
    plt.gcf().autofmt_xdate()
    #plt.yscale('log')
    plt.suptitle('Trendicator Equity Curve', fontsize= 16)
    plt.title('Starting Balance: 1000 | Start Date: January 1st, 2021', fontsize= 12)
    plt.ylabel('Account Balance')
    plt.xlabel('Date')
    plt.legend()
    plt.savefig(path)
    plt.close()
    return ending_capital
def recent_trades(path):
    ma_length = 70
    period_count = 3
    url = 'https://api-pub.bitfinex.com/v2/candles/trade:1h:tBTCUSD/hist?limit=1000'
    data = json.loads(requests.get(url).content)
    data.reverse()
    recent_closes = [x[2] for x in data]
    recent_mas = moving_average_list(ma_length, recent_closes)
    recent_dates_real = [datetime.datetime.fromtimestamp(x[0]/1000) for x in data]


    buys = [[], []]
    sells = [[], []]
    count = 0
    short = False
    long = False
    buys = [[], []]
    sells = [[], []]
    for i in range(len(recent_closes)):
        if count < ma_length + period_count:
            count += 1
            continue
        check_list = []
        if long:
            for x in range(period_count):
                if recent_closes[i-x] <= recent_mas[i-x]:
                    check_list.append(True)
                else:
                    check_list.append(False)
            #conclude
            if not False in check_list:
                long = False
                short = True
                sells[0].append(recent_dates_real[i])
                sells[1].append(recent_closes[i])
        elif short:
            for x in range(period_count):
                if recent_closes[i-x] >= recent_mas[i-x]:
                    check_list.append(True)
                else:
                    check_list.append(False)
            #conclude
            if not False in check_list:
                long = True
                buys[0].append(recent_dates_real[i])
                buys[1].append(recent_closes[i])
                short = True
        else:
            if recent_closes[i] >= recent_mas[i]:
                long = True
                buys[0].append(recent_dates_real[i])
                buys[1].append(recent_closes[i])
            else:
                short = True
                sells[0].append(recent_dates_real[i])
                sells[1].append(recent_closes[i])

    lastbuy = [[], []]
    lastsell = [[], []]
    if long:
        lastbuy[0].append(recent_dates_real[-1])
        lastbuy[1].append(recent_closes[-1])
    elif short:
        lastsell[0].append(recent_dates_real[-1])
        lastsell[1].append(recent_closes[-1])

    plt.style.use('seaborn')
    ax = plt.gca()
    ax.plot(recent_dates_real, recent_closes, linewidth='.5', label='BTC/USD', color='black')
    ax.plot(buys[0], buys[1], '^', markersize=6, color='green', label='Long')
    ax.plot(sells[0], sells[1], 'v', markersize=6, color='red', label='Short')

    if long:
        ax.plot(lastbuy[0], lastbuy[1], 'o', markersize=12,  markerfacecolor = 'none', markeredgecolor ='green', markeredgewidth=1.0, label='Current Trade')
    else:
        ax.plot(lastsell[0], lastsell[1], 'o', markersize=12, markerfacecolor = 'none',  markeredgecolor ='red', markeredgewidth=1.0, label='Current Trade')

    ax.plot([], [])
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.gcf().autofmt_xdate()
    #ax.locator_params(nbins=10, axis='x')
    #ax.autofmt_xdate()
    plt.suptitle('Trendicator Recent Trades', fontsize= 16)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.savefig(path)
    plt.close()
def flip_check():
    ma_length = 70
    period_count = 3
    url = 'https://api-pub.bitfinex.com/v2/candles/trade:1h:tBTCUSD/hist?limit=400'
    data = json.loads(requests.get(url).content)
    data.reverse()
    recent_closes = [x[2] for x in data]
    recent_dates_real = [datetime.datetime.fromtimestamp(x[0] / 1000) for x in data]
    recent_mas = moving_average_list(ma_length, recent_closes)
    print('mas', recent_mas[-5:])
    print('prices', recent_closes[-5:])
    last_date = recent_dates_real[-1]
    last_close = recent_closes[-1]
    buys = [[], []]
    sells = [[], []]
    count = 0
    short = False
    long = False
    buys = [[], []]
    sells = [[], []]
    for i in range(len(recent_closes)):
        if count < ma_length + period_count:
            count += 1
            continue
        check_list = []
        if long:
            for x in range(period_count):
                if recent_closes[i - x] <= recent_mas[i - x]:
                    check_list.append(True)
                else:
                    check_list.append(False)
            # conclude
            if not False in check_list:
                long = False
                short = True
                sells[0].append(recent_dates_real[i])
                sells[1].append(recent_closes[i])
        elif short:
            for x in range(period_count):
                if recent_closes[i - x] >= recent_mas[i - x]:
                    check_list.append(True)
                else:
                    check_list.append(False)
            # conclude
            if not False in check_list:
                long = True
                buys[0].append(recent_dates_real[i])
                buys[1].append(recent_closes[i])
                short = True
        else:
            if recent_closes[i] >= recent_mas[i]:
                long = True
                buys[0].append(recent_dates_real[i])
                buys[1].append(recent_closes[i])
            else:
                short = True
                sells[0].append(recent_dates_real[i])
                sells[1].append(recent_closes[i])
    final_buy = buys[0][-1]
    final_sell = sells[0][-1]
    if final_buy == last_date:
        return [1, last_close]
    elif final_sell == last_date:
        return [-1, last_close]
    else:
        return [0, last_close]


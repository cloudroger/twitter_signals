import twitter
from datetime import datetime
import pause
import pandas as pd
import time
from bot_functions import flip_check, equity_graph, recent_trades

flip_count = 3
ma_length = 70
starting_epoch = 1609567200
def moving_average_list(ma, value_list, lagged=False, **kwargs):
    ma_list = []
    if lagged:
        offset = 0
    else:
        offset = 1
    for i in range(ma-offset):
        ma_list.append(None)
    for i, value in enumerate(value_list[ma-offset:], start=ma-offset):
        ma_list.append((sum(value_list[i-ma+offset:i+offset]))/ma)
    return ma_list

keys = open('keys.txt', 'r')
lines = keys.readlines()
consumer_key = lines[0].rstrip()
consumer_secret = lines[1].rstrip()
access_token = lines[2].rstrip()
access_token_secret = lines[3].rstrip()

api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token,
                      access_token_secret=access_token_secret)


longtweet = 'TRENDICATOR ALERT 🧲\n\nLONG $BTC @ ${} 📈\n\nStarting Balance: 1000\nUpdated Balance: {}\nCumulative Return: +{}%\n\n#Bitcoin #Trading #Crypto'
shorttweet = 'TRENDICATOR ALERT 💣\n\nSHORT $BTC @ ${} 📉\n\nStarting Balance: 1000\nUpdated Balance: {}\nCumulative Return: +{}%\n\n#Bitcoin #Trading #Crypto'



media = r"C:\Users\roger\Downloads\Trendicator_Fin.png"
error_count = 0

while True:
    try:
        check = flip_check()
        print(check)
        if check[0] == 1:
            print('GOING LONG!', flush=True)
            recent_trades(r'/home/realrogercloud/twitter_bot/graph_images/recent_trades.png')
            ending_capital = equity_graph(r'/home/realrogercloud/twitter_bot/graph_images/equity_graph.png')
            updated_balance = int(ending_capital)
            updated_return = (int(((updated_balance/1000)-1)*100))
            post_result = api.PostUpdate(status=longtweet.format(int(check[1]), updated_balance, updated_return), media=[r'/home/realrogercloud/twitter_bot/graph_images/recent_trades.png', r'/home/realrogercloud/twitter_bot/graph_images/equity_graph.png'])
        elif check[0] == -1:
            print('GOING SHORT!', flush=True)
            recent_trades('/home/realrogercloud/twitter_bot/graph_images/recent_trades.png')
            ending_capital = equity_graph('/home/realrogercloud/twitter_bot/graph_images/equity_graph.png')
            updated_balance = int(ending_capital)
            updated_return = (int(((updated_balance/1000)-1)*100))
            post_result = api.PostUpdate(status=shorttweet.format(int(check[1]), updated_balance, updated_return), media=[r'/home/realrogercloud/twitter_bot/graph_images/recent_trades.png', r'/home/realrogercloud/twitter_bot/graph_images/equity_graph.png'])
        rounded_time = (pd.Timestamp.now(tz='gmt').round('60min').timestamp())
        now_time = (time.time())
        print('Now Time:', now_time)
        rounded_time = rounded_time + 3595
        print('Round and Adjusted Time', rounded_time)
        print('My Pretty Time:', datetime.now())
        print('\n', flush=True)
        error_count = 0
        pause.until(rounded_time)
    except Exception as error:
        print(error)
        print(datetime.now())
        print('\n', flush=True)
        error_count += 1
        if error_count >= 20:
            time.sleep(2400)
        else:
            time.sleep(300)

# twitter_signals
Twitter bot displaying real-time signals and results of a personally developed trading algorithm.

Running live on Pythonanywhere servers. https://twitter.com/TrendicatorBot


# What is this?
Trend-following trading systems tend to be the most accessible >0 alpha strategies. I developed my own trend-following strategy and thought it would be fun to have a twitter bot tweet out the signals and results. Not concerned worried about alpha leak (if any) because this is a relatively unsophisticated strategy that would not be difficult to recreate independently.

# How does the strategy work?
The algo is a delta-neutral always-in-a-position trend following strategy. Trend followers work a bit counter-intuitively as they tend to 'buy high' and 'sell low' with a <50% rate. But they typically perform much better than mean-reversion strategies over long periods of time. Effectively the idea is that most trades will be losing trades, but with small losses, but the wins will have a much higher HPR on average. Lose often but small, win sometimes but big.

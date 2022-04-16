# twitter_signals
Twitter bot displaying real-time signals and results of a personally developed trading algorithm.

Can be viewed in action: https://twitter.com/TrendicatorBot
Running live on Pythonanywhere servers. 


# What is this
Trend-following trading systems tend to be the most accessible >0 alpha strategies. I developed my own trend-following strategy and thought it would be fun to have a twitter bot tweet out the signals and results. Not concerned about alpha leak (if any) because this is a relatively unsophisticated strategy that would not be difficult to recreate independently.

# How does the strategy work?
The algo is a delta-neutral always-in-a-position trend following strategy. Trend followers work a bit counter-intuitively as they tend to 'buy high' and 'sell low' with a <50% win rate. But they typically perform much better than mean-reversion strategies over long periods of time. Effectively the idea is that most trades will be losers, but with small losses, and the few wins will have a much higher HPRs on average. The hope, of course, is that the <1 Risk:Reward ratio is more assymetric than the win/lose rate to produce a positive expected value, or positive alpha.

# Execution conditions
If the position is long, the algo will flip short under the condition of x 1h closes below the y 1h simple moving average. Same vice-versa.
How are x and y determined? Backtesting a grid from a defined range of combinations and picking the parameters with the optimal backtest. This part is not included in the repo.

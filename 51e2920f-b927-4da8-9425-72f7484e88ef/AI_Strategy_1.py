from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "SPY"  # Define the asset we are trading

    @property
    def assets(self):
        return [self.ticker]  # List of asset tickers

    @property
    def interval(self):
        # The frequency of data we're using (daily data in this example)
        return "1day"

    def run(self, data):
        # Initialize allocation with no position
        allocation = {self.ticker: 0.0}
        
        # Bollinger Bands and RSI configuration
        bb_length = 20
        rsi_length = 14
        rsi_low_threshold = 30  # Buy signal threshold
        rsi_high_threshold = 70  # Sell signal threshold
        
        # Calculate Bollinger Bands and RSI
        bollinger_bands = BB(self.ticker, data["ohlcv"], bb_length)
        rsi = RSI(self.ticker, data["ohlcv"], rsi_length)
        
        if not bollinger_bands or not rsi:
            log("Insufficient data for indicators")
            return TargetAllocation(allocation)
            
        current_close = data["ohlcv"][-1][self.ticker]['close']
        lower_band = bollinger_bands['lower'][-1]
        upper_band = bollinger_bands['upper'][-1]
        current_rsi = rsi[-1]

        log(f"Current Close: {current_close}, Lower BB: {lower_band}, Upper BB: {upper_band}, RSI: {current_rsi}")

        # If current price is below lower BB and RSI is below 30, consider it oversold and buy
        if current_close < lower_band and current_rsi < rsi_low_threshold:
            allocation[self.ticker] = 1.0  # Allocating 100% to SPY
            log("Buying signal based on Bollinger Bands and RSI")

        # If current price is above upper BB and RSI is above 70, consider it overbought and sell
        elif current_close > upper_band and current_rsi > rsi_high_threshold:
            allocation[self.ticker] = 0.0  # Exiting the position
            log("Selling signal based on Bollinger Bands and RSI")
        else:
            log("No clear buy or sell signals based on our criteria")

        return TargetAllocation(allocation)
from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import BB, Slope
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        # Example uses a single asset, but this can be expanded as needed
        return ["AAPL"]
    
    @property
    def interval(self):
        # Daily interval for assessing the strategy
        return "1day"
    
    def run(self, data):
        # Initialize the allocation to neutral (no position)
        allocation = {ticker: 0 for ticker in self.assets}
        for ticker in self.assets:
            data_ticker = data["ohlcv"]
            
            # Check if there's enough data to calculate Bollinger Bands and Slope
            if len(data_ticker) > 20:
                # Calculate Bollinger Bands for the last 20 days
                bb = BB(ticker, data_ticker, 20, 2)
                
                # Calculate the slope of the close prices over the last 5 days to determine the trend
                slope = Slope(ticker, data_ticker, 5)
                
                current_price = data_ticker[-1][ticker]['close']
                upper_band = bb['upper'][-1]
                lower_band = bb['lower'][-1]
                
                # If current price is above the upper Bollinger Band and slope is positive, 
                # it mimics a long call position; we sell short
                if current_price > upper_band and slope[-1] > 0:
                    allocation[ticker] = -0.5  # Short position, example value
                
                # If current price is below the lower Bollinger Band and slope is negative,
                # it mimics a long put position; we buy long
                elif current_price < lower_band and slope[-1] < 0:
                    allocation[ticker] = 0.5   # Long position, example value
                
                # For simplicity, outside of these conditions, the strategy remains neutral
                else:
                    allocation[ticker] = 0
                
        return TargetAllocation(allocation)
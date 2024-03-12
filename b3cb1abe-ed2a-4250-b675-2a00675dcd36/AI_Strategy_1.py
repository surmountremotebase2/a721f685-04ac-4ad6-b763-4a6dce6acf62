from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import ATR, EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # List of tickers to be analyzed
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        
    @property
    def interval(self):
        # Use daily data for the analysis
        return "1day"
        
    @property
    def assets(self):
        # The assets property will return the list of selected tickers
        return self.tickers
        
    def run(self, data):
        allocation_dict = {}
        
        # Loop through each ticker in tickers to analyze its data
        for ticker in self.tickers:
            ohlcv_data = data["ohlcv"]
            
            # Calculate the 14-day ATR for the considered stock as a volatility measure
            atr = ATR(ticker, ohlcv_data, 14)
            
            # Use the 10-day and 30-day EMA as a simple trend indicator
            ema_short = EMA(ticker, ohlcv_data, 10)
            ema_long = EMA(ticker, ohlcv_data, 30)
            
            # Check if recent data is available to avoid out-of-index errors
            if atr and ema_short and ema_long and len(atr) > 0 and len(ema_short) > 0 and len(ema_long) > 0:
                current_atr = atr[-1]
                short_ema = ema_short[-1]
                long_ema = ema_long[-1]
                
                # Simplified decision logic based on the ATR and EMAs
                if current_atr >= 5:  # Arbitrarily chosen ATR threshold for high volatility
                    if short_ema > long_ema:
                        # Predicting an upward move, allocate more
                        allocation_dict[ticker] = 0.3
                    elif short_ema < long_ema:
                        # Predicting a downward move, hedge by reducing allocation
                        allocation_dict[ticker] = 0.1
                else:
                    # Low volatility, neutral stance
                    allocation_dict[ticker] = 0.2
        
        # Normalize the allocations (simplified and not exactly proportional)
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 0:
            for ticker in allocation_dict:
                allocation_dict[ticker] /= total_allocation
        
        # Ensure the sum of allocation values is between 0 and 1 inclusive
        return TargetAllocation(allocation_dict)
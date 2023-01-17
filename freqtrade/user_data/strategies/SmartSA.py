# This is an integration of LunarCrush APIs to Freqtrade to execute spot market orders
from datetime import datetime
from freqtrade.persistence import Trade

from freqtrade.strategy import IStrategy
from pandas import DataFrame


class SmartSA(IStrategy):
    INTERFACE_VERSION: int = 3

    # Buy hyperspace params - None
    buy_params = {}
    # Sell hyperspace params - None
    sell_params = {}

    # ROI table - None
    minimal_roi = {}

    # Stoploss - 5%
    stoploss = -0.05

    # Trailing stop - Disabled
    trailing_stop = False
    trailing_stop_positive = 1
    trailing_stop_positive_offset = 1
    trailing_only_offset_is_reached = True

    # Timeframe is not necessary
    timeframe = "15m"
    startup_candle_count = 1

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # No Indicator
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # if metadata['pair'] == 'SOL/USDT' or metadata['pair'] == 'ALGO/USDT':

        # Forward Mode
        dataframe.loc[
            (),
            "enter_long"] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # No Exit
        dataframe.loc[(), 'exit_long'] = 1

        return dataframe

    def custom_exit(self, pair: str, trade: Trade, current_time: datetime, current_rate: float,
                    current_profit: float, **kwargs):

        # Sell any positions at a loss if they are held for more than one day.
        if current_profit < -0.3 and (current_time - trade.open_date_utc).days >= 6:
            return 'unclog'

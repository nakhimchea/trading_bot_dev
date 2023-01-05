import datetime
from typing import Optional
from freqtrade.persistence import Trade

from freqtrade.strategy import IStrategy, IntParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np
import scipy


class SmartTA(IStrategy):
    INTERFACE_VERSION: int = 3

    # Buy hyperspace params:
    buy_params = {
        "buy_m1": 4,
        "buy_m2": 7,
        "buy_m3": 1,
        "buy_p1": 8,
        "buy_p2": 9,
        "buy_p3": 8,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_m1": 1,
        "sell_m2": 3,
        "sell_m3": 6,
        "sell_p1": 16,
        "sell_p2": 18,
        "sell_p3": 18,
    }

    # ROI table:
    minimal_roi = {
        "0": 0.20,
        "1704": 0.15,
        "3712": 0.09,
        "5605": 0
    }

    # Stoploss:
    stoploss = -1

    # enable short
    can_short = True

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.025
    trailing_stop_positive_offset = 0.05
    trailing_only_offset_is_reached = True

    timeframe = "6h"
    startup_candle_count = 18

    buy_m1 = IntParameter(1, 7, default=1)
    buy_m2 = IntParameter(1, 7, default=3)
    buy_m3 = IntParameter(1, 7, default=4)
    buy_p1 = IntParameter(7, 21, default=14)
    buy_p2 = IntParameter(7, 21, default=10)
    buy_p3 = IntParameter(7, 21, default=10)

    sell_m1 = IntParameter(1, 7, default=1)
    sell_m2 = IntParameter(1, 7, default=3)
    sell_m3 = IntParameter(1, 7, default=4)
    sell_p1 = IntParameter(7, 21, default=14)
    sell_p2 = IntParameter(7, 21, default=10)
    sell_p3 = IntParameter(7, 21, default=10)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['peak_bottom'] = self.smartexit(dataframe)['peak_bottom']

        for multiplier in self.buy_m1.range:
            for period in self.buy_p1.range:
                dataframe[f"supertrend_1_buy_{multiplier}_{period}"] = self.supertrend(dataframe, multiplier, period)["STX"]

        for multiplier in self.buy_m2.range:
            for period in self.buy_p2.range:
                dataframe[f"supertrend_2_buy_{multiplier}_{period}"] = self.supertrend(dataframe, multiplier, period)["STX"]

        for multiplier in self.buy_m3.range:
            for period in self.buy_p3.range:
                dataframe[f"supertrend_3_buy_{multiplier}_{period}"] = self.supertrend(dataframe, multiplier, period)["STX"]

        for multiplier in self.sell_m1.range:
            for period in self.sell_p1.range:
                dataframe[f"supertrend_1_sell_{multiplier}_{period}"] = self.supertrend(dataframe, multiplier, period)["STX"]

        for multiplier in self.sell_m2.range:
            for period in self.sell_p2.range:
                dataframe[f"supertrend_2_sell_{multiplier}_{period}"] = self.supertrend(dataframe, multiplier, period)["STX"]

        for multiplier in self.sell_m3.range:
            for period in self.sell_p3.range:
                dataframe[f"supertrend_3_sell_{multiplier}_{period}"] = self.supertrend(dataframe, multiplier, period)["STX"]

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe[f"supertrend_1_buy_{self.buy_m1.value}_{self.buy_p1.value}"] == "up")
            & (dataframe[f"supertrend_2_buy_{self.buy_m2.value}_{self.buy_p2.value}"] == "up")
            & (dataframe[f"supertrend_3_buy_{self.buy_m3.value}_{self.buy_p3.value}"] == "up")
            & (dataframe['peak_bottom'] != 'P0')
            & (dataframe['peak_bottom'] != 'P1')
            & (dataframe['peak_bottom'] != 'P2')
            & (dataframe['peak_bottom'] != 'P3')
            & (dataframe['peak_bottom'] != 'P4')
            & (dataframe['peak_bottom'] != 'P5')
            & (dataframe["volume"] > 0),
            "enter_long"] = 1

        dataframe.loc[
            (dataframe[f"supertrend_1_buy_{self.buy_m1.value}_{self.buy_p1.value}"] == "down")
            & (dataframe[f"supertrend_2_buy_{self.buy_m2.value}_{self.buy_p2.value}"] == "down")
            & (dataframe[f"supertrend_3_buy_{self.buy_m3.value}_{self.buy_p3.value}"] == "down")
            & (dataframe['peak_bottom'] != 'B0')
            & (dataframe['peak_bottom'] != 'B1')
            & (dataframe['peak_bottom'] != 'B2')
            & (dataframe['peak_bottom'] != 'B3')
            & (dataframe['peak_bottom'] != 'B4')
            & (dataframe['peak_bottom'] != 'B5')
            & (dataframe["volume"] > 0),
            "enter_short"] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe[f"supertrend_1_sell_{self.sell_m1.value}_{self.sell_p1.value}"] == "down")
            & (dataframe[f"supertrend_2_sell_{self.sell_m2.value}_{self.sell_p2.value}"] == "down")
            & (dataframe[f"supertrend_3_sell_{self.sell_m3.value}_{self.sell_p3.value}"] == "down"),
            "exit_long"] = 1

        dataframe.loc[
            (dataframe[f"supertrend_1_sell_{self.sell_m1.value}_{self.sell_p1.value}"] == "up")
            & (dataframe[f"supertrend_2_sell_{self.sell_m2.value}_{self.sell_p2.value}"] == "up")
            & (dataframe[f"supertrend_3_sell_{self.sell_m3.value}_{self.sell_p3.value}"] == "up"),
            "exit_short"] = 1

        return dataframe

    def custom_exit(self, pair: str, trade: 'Trade', current_time: 'datetime', current_rate: float,
                    current_profit: float, **kwargs):

        # Sell any positions at a loss if they are held for more than one day.
        if current_profit < -0.6667 and (current_time - trade.open_date_utc).days >= 6:
            return 'unclog'


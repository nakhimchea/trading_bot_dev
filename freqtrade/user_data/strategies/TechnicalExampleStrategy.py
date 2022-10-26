from pandas import DataFrame
from technical.indicators import cmf

from freqtrade.strategy import IStrategy


class TechnicalExampleStrategy(IStrategy):
    INTERFACE_VERSION: int = 3
    minimal_roi = {
        "0": 0.15,
        "1502": 0.114,
        "2852": 0.055,
        "8101": 0
    }

    stoploss = -0.341
    
    timeframe = '4h'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['cmf'] = cmf(dataframe, 21)
        
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[(dataframe['cmf'] < 0), 'enter_long'] = 1
        
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[(dataframe['cmf'] > 0), 'exit_long'] = 1
        
        return dataframe

# --- Do not remove these libs ---
from freqtrade.strategy import IStrategy
from pandas import DataFrame
# --------------------------------


class DoesNothingStrategy(IStrategy):
    """

    author@: Gert Wohlgemuth

    just a skeleton

    """

    INTERFACE_VERSION: int = 3
    # Minimal ROI designed for the strategy.
    # adjust based on market conditions. We would recommend to keep it low for quick turn arounds
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {
        "0": 0.01
    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.25

    # Optimal timeframe for the strategy
    timeframe = '5m'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
            ),
            'exit_long'] = 1
        return dataframe

    @staticmethod
    def smartexit(df: DataFrame):
        dataframe = df.copy()

        # Reverse Candle Detection (Stochastic)
        stochd = ta.STOCHF(dataframe, fastk_period=3)
        reversed_stochd = 100 - stochd

        peaks = scipy.signal.find_peaks(stochd.fastk * 1.3 - 15, height=95)
        bottoms = scipy.signal.find_peaks(reversed_stochd.fastk * 1.3 - 15, height=95)

        peak_indices = []
        for index in range(0, len(peaks[0]) - 1):
            if peaks[0][index + 1] > peaks[0][index] + 4:
                peak_indices.append(peaks[0][index])
        peak_indices.append(peaks[0][len(peaks[0]) - 1])

        bottom_indices = []
        for index in range(0, len(bottoms[0]) - 1):
            if bottoms[0][index + 1] > bottoms[0][index] + 4:
                bottom_indices.append(bottoms[0][index])
        bottom_indices.append(bottoms[0][len(bottoms[0]) - 1])

        # print('=====================.=======================')
        # plot.plot(dataframe.date, stochd.fastk * 1.3 - 15, '-D', markevery=[*peak_indices, *bottom_indices])
        # plot.legend(['K', 'D', 'J'])
        # plot.show()
        # time.sleep(5)
        # print('=====================.=======================')

        rp = 0
        rb = 0
        peak_bottom = DataFrame(data='NA', index=dataframe.index, columns=['peak_bottom'], dtype=str)
        strength = DataFrame(data='NA', index=dataframe.index, columns=['strength'], dtype=str)

        while len(peak_indices) > 0 and len(bottom_indices) > 0:
            if peak_indices[0] < bottom_indices[0]:
                for index in range(peak_indices[0], bottom_indices[0]):
                    peak_bottom['peak_bottom'].iat[index] = 'P'
                    strength['strength'].iat[index] = str(rp)
                peak_indices.pop(0)
                rp += 1
                rb = 0
            elif bottom_indices[0] < peak_indices[0]:
                for index in range(bottom_indices[0], peak_indices[0]):
                    peak_bottom['peak_bottom'].iat[index] = 'B'
                    strength['strength'].iat[index] = str(rb)
                bottom_indices.pop(0)
                rb += 1
                rp = 0

        if len(peak_indices) > 0:
            for index in range(peak_indices[0], len(dataframe)):
                peak_bottom['peak_bottom'].iat[index] = 'P'
                strength['strength'].iat[index] = str(rp)
        elif len(bottom_indices) > 0:
            for index in range(bottom_indices[0], len(dataframe)):
                peak_bottom['peak_bottom'].iat[index] = 'B'
                strength['strength'].iat[index] = str(rb)

        dataframe['peak_bottom'] = peak_bottom['peak_bottom'] + strength['strength']

        return dataframe

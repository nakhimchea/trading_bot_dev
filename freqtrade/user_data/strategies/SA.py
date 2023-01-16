# This is an integration of LunarCrush APIs to Freqtrade to execute spot market orders
import time
# from threading import Thread
import os
import json
from datetime import datetime

import matplotlib.pyplot as plot
import requests


def cleaning():
    start = datetime.now()
    coin_list = json.load(open('lunarcrush.json'))

    for coin in coin_list:
        dts = []
        for dt in coin["dt"]:
            dt_requested = int(dt / 100) * 100
            dts.append(dt_requested)
        coin["dt"] = dts

    # Serializing json
    json_object = json.dumps(coin_list, indent=2)

    print((datetime.now() - start).seconds)
    # Writing to json file
    with open("lunarcrush_processed.json", "w") as outfile:
        outfile.write(json_object)


def request_lunar_crush():
    start = datetime.now()
    api_key = 'y9azsj5opwp9h99vzrtutjzmjlcsjbazcocu1tk'
    url = "https://lunarcrush.com/api3/coins?limit=2000"
    headers = {'Authorization': 'Bearer {0}'.format(api_key)}
    response = requests.request("GET", url, headers=headers)
    # print(response.json())

    lunarcrush = response.json()
    no_data = False
    coin_list = []
    try:
        coin_list = json.load(open('lunarcrush.json'))

    except FileNotFoundError:
        no_data = True

    dt_requested = lunarcrush["config"]["generated"]
    dt_requested = int(dt_requested / 100) * 100
    print(dt_requested)
    for datamap in lunarcrush["data"]:
        data = {
            "id": datamap["id"],
            "s": datamap["s"],
            "n": datamap["n"],
            "p": datamap["p"],
            "mc": datamap["mc"],
            "acr": datamap["acr"],
        }
        if no_data:
            data["p"] = [data["p"]]
            data["mc"] = [data["mc"]]
            data["acr"] = [data["acr"]]
            data["dt"] = [dt_requested]
            coin_list.append(data)

        else:
            for coin in coin_list:
                if coin["id"] == data["id"] and coin["s"] == data["s"] and coin["n"] == data["n"]:
                    if coin["p"].__len__() >= 192:
                        coin["p"].pop(0)
                        coin["mc"].pop(0)
                        coin["acr"].pop(0)
                        coin["dt"].pop(0)
                    coin["p"].append(data["p"])
                    coin["mc"].append(data["mc"])
                    coin["acr"].append(data["acr"])
                    coin["dt"].append(dt_requested)

    # Serializing json
    json_object = json.dumps(coin_list, indent=2)

    print((datetime.now() - start).seconds)
    # Writing to json file
    with open("lunarcrush.json", "w") as outfile:
        outfile.write(json_object)


def process_data():
    data_path = os.getcwd() + '/../data/lunarcrush/'
    no_data = False
    coin_list = []
    try:
        coin_list = json.load(open('lunarcrush.json'))

    except FileNotFoundError:
        no_data = True

    if no_data:
        print("Data file is empty.")

    else:
        for coin in coin_list:
            file_name = coin["s"]
            json_object = json.dumps(coin, indent=2)
            # Writing to json file
            with open(data_path + file_name.split('/')[0] + ".json", "w") as outfile:
                outfile.write(json_object)


def plot_lunar_graph(acr=None, p=None, dt=None):
    if acr is None or p is None or dt is None:
        acr = [], p = [], dt = []

    fig, axes = plot.subplots(2, 1)
    axes[0].plot(dt, p, 'tab:orange')
    axes[0].set_title("Price")
    axes[1].plot(dt, acr, 'tab:green')
    axes[1].set_title("AltRank")
    fig.tight_layout(pad=1)
    plot.show()

    time.sleep(3)


def get_exchange_info():
    base_url = 'https://api.binance.com'
    endpoint = '/api/v3/exchangeInfo'

    return requests.get(base_url + endpoint).json()


def quote_symbols_list(quote='USDT'):
    symbols = get_exchange_info()['symbols']
    pairs = {s['symbol']: s for s in symbols if quote in s['symbol']}

    return pairs.keys()


def going2trade():
    data_path = os.getcwd() + '/../data/lunarcrush/'
    files = os.listdir(data_path)
    usdt_pairs = quote_symbols_list('USDT')
    print(usdt_pairs.__len__())
    to_trade = []
    for file in files:
        data = json.load(open(data_path + file))
        acr = data["acr"]

        if max(acr) < 1500 and min(acr) < 150 and acr[acr.__len__() - 1] < 150:
            symbol = file.split('.')[0]
            stablecoins = json.load(open('stablecoins.json'))["symbols"]
            if symbol not in stablecoins:
                pair = symbol+"USDT"
                if pair in usdt_pairs:
                    to_trade.append(pair)

            # p = data["p"]
            # dt = data["dt"]
            # plot_lunar_graph(acr, p, dt)

    print(to_trade)


def main():
    # Data Collection
    # print(898 - (int(time.time()) % 900))
    # time.sleep(898 - (int(time.time()) % 900))  # 2 sec is for Thread Initialization
    # while True:
    #     thr = Thread(target=request_lunar_crush)
    #     thr.start()
    #     time.sleep(900)

    # Data Preprocessing
    # process_data()

    # Plotting
    going2trade()


if __name__ == "__main__":
    main()

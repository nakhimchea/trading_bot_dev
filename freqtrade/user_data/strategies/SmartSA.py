# This is an integration of LunarCrush APIs to Freqtrade to execute spot market orders
import time
from threading import Thread
import json
from datetime import datetime

# import matplotlib.pyplot as plot
import requests


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
    print(dt_requested)
    for datamap in lunarcrush["data"]:
        data = {
            "id": datamap["id"],
            "s": datamap["s"],
            "n": datamap["n"],
            "pch": datamap["pch"],
            "mc": datamap["mc"],
            "acr": datamap["acr"],
        }
        if no_data:
            data["pch"] = [data["pch"]]
            data["mc"] = [data["mc"]]
            data["acr"] = [data["acr"]]
            data["dt"] = [dt_requested]
            coin_list.append(data)

        else:
            for coin in coin_list:
                if coin["id"] == data["id"] and coin["s"] == data["s"] and coin["n"] == data["n"]:
                    if coin["pch"].__len__() >= 192:
                        coin["pch"].pop(0)
                        coin["mc"].pop(0)
                        coin["acr"].pop(0)
                        coin["dt"].pop(0)
                    coin["pch"].append(data["pch"])
                    coin["mc"].append(data["mc"])
                    coin["acr"].append(data["acr"])
                    coin["dt"].append(dt_requested)

    # Serializing json
    json_object = json.dumps(coin_list, indent=2)

    print((datetime.now() - start).seconds)
    # Writing to json file
    with open("lunarcrush.json", "w") as outfile:
        outfile.write(json_object)


# def plot_lunar_graph():
    # data = json.load(open('lunarcrush.json'))
    # pch = data[0]["pch"]
    # acr = data[0]["acr"]
    # dt = data[0]["dt"]
    #
    # fig, axes = plot.subplots(2, 1)
    # axes[0].plot(dt, pch, 'tab:orange')
    # axes[0].set_title("Price")
    # axes[1].plot(dt, acr, 'tab:green')
    # axes[1].set_title("AltRank")
    # plot.show()


def main():
    print(8 - (int(time.time()) % 10))
    time.sleep(8 - (int(time.time()) % 10))  # 2 sec is for Thread Initialization
    while True:
        thr = Thread(target=request_lunar_crush)
        thr.start()
        # plot_lunar_graph()
        time.sleep(10)


if __name__ == "__main__":
    main()

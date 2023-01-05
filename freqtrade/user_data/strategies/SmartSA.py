# This is an integration of LunarCrush APIs to Freqtrade to execute spot market orders
import time
from threading import Thread
import json
from datetime import datetime


def request_lunar_crush():
    start = datetime.now()
    lunarcrush = json.load(open('lunarcrush.json'))
    no_data = False
    coin_list = []
    try:
        coin_list = json.load(open('lunarcrush_extraction.json'))

    except FileNotFoundError:
        no_data = True

    for datamap in lunarcrush["data"]:
        data = {
            "id": datamap["id"],
            "s": datamap["s"],
            "n": datamap["n"],
            "pch": datamap["pch"],
            "mc": datamap["mc"],
            "acr": datamap["acr"],
            "tc": datamap["tc"]
        }
        if no_data:
            data["pch"] = [data["pch"]]
            data["mc"] = [data["mc"]]
            data["acr"] = [data["acr"]]
            data["tc"] = [data["tc"]]
            coin_list.append(data)

        else:
            for coin in coin_list:
                if coin["id"] == data["id"] and coin["s"] == data["s"] and coin["n"] == data["n"]:
                    if coin["pch"].__len__() >= 48:
                        coin["pch"].pop(0)
                        coin["mc"].pop(0)
                        coin["acr"].pop(0)
                        coin["tc"].pop(0)
                    coin["pch"].append(data["pch"])
                    coin["mc"].append(data["mc"])
                    coin["acr"].append(data["acr"])
                    coin["tc"].append(data["tc"])

    # Serializing json
    json_object = json.dumps(coin_list, indent=2)

    print((datetime.now() - start).microseconds)
    # Writing to json file
    with open("lunarcrush_extraction.json", "w") as outfile:
        outfile.write(json_object)


def main():
    while True:
        thr = Thread(target=request_lunar_crush)
        thr.start()
        time.sleep(2)


if __name__ == "__main__":
    main()

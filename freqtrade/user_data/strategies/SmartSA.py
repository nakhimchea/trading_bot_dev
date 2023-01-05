# This is an integration of LunarCrush APIs to Freqtrade to execute spot market orders
import time
from threading import Thread
import json


def request_lunar_crush():
    data = json.load(open('lunarcrush.json'))
    print(data["data"])

    # Serializing json
    json_object = json.dumps(data["data"], indent=2)

    # Writing to json file
    with open("lunarcrush_extraction.json", "w") as outfile:
        outfile.write(json_object)


def main():
    while True:
        thr = Thread(target=request_lunar_crush)
        thr.start()
        time.sleep(5)


if __name__ == "__main__":
    main()

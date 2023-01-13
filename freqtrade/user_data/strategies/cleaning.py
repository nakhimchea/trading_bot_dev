import json
from datetime import datetime


def main():
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


if __name__ == '__main__':
    main()

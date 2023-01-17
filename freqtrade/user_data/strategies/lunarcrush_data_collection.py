# This is an integration of LunarCrush APIs to Freqtrade to execute spot market orders
import time
import os
import json
import requests


def request_lunar_crush():
    # Creating LunarCrush data storage -----------------------------
    try:
        os.listdir(os.path.join(os.getcwd(), 'lunarcrush'))

    except FileNotFoundError:
        print("No storage found. Creating folders now...")
        os.mkdir(os.path.join(os.getcwd(), 'lunarcrush'))
        print("Finished creating folders now!")

    # Getting data list --------------------------------------------
    api_key = 'y9azsj5opwp9h99vzrtutjzmjlcsjbazcocu1tk'
    url = "https://lunarcrush.com/api3/coins"
    headers = {'Authorization': 'Bearer {0}'.format(api_key)}
    response = requests.request("GET", url, headers=headers)
    # print(response.json())
    lunarcrush = response.json()

    # Retrieve time requested --------------------------------------
    dt_requested = lunarcrush["config"]["generated"]
    dt_requested = int(dt_requested / 100) * 100
    print(dt_requested)

    # Data Processing ----------------------------------------------
    data_path = os.path.join(os.getcwd(), 'lunarcrush')
    for datamap in lunarcrush["data"]:
        # Index Processing
        data = {
            "id": datamap["id"],
            "s": datamap["s"],
            "n": datamap["n"],
            "p": datamap["p"],
            "mc": datamap["mc"],
            "acr": datamap["acr"],
        }
        no_file = False
        coin = {}
        # Check if there is no file yet
        try:
            coin = json.load(open(os.path.join(data_path, data["s"].split('/')[0] + ".json")))
        except FileNotFoundError:
            no_file = True

        if no_file:
            print("Data file is empty. Creating file to store ", data["s"].split('/')[0])
            data["p"] = [data["p"]]
            data["mc"] = [data["mc"]]
            data["acr"] = [data["acr"]]
            data["dt"] = [dt_requested]
            coin = data
            print("Done creating and storing data!")
        elif bool(coin):
            print("Insert new data to previous json file...")
            if coin["p"].__len__() >= 192:
                coin["p"].pop(0)
                coin["mc"].pop(0)
                coin["acr"].pop(0)
                coin["dt"].pop(0)
            coin["p"].append(data["p"])
            coin["mc"].append(data["mc"])
            coin["acr"].append(data["acr"])
            coin["dt"].append(dt_requested)
            print("Done storing data!")
        else:
            print("Unexpected Error.")

        # Serializing and Writing to json file
        json_object = json.dumps(coin, indent=2)
        with open(os.path.join(data_path, data["s"].split('/')[0] + ".json"), "w") as outfile:
            outfile.write(json_object)


def main():
    # Data Collection
    while True:
        print(900 - (int(time.time()) % 900))
        time.sleep(900 - (int(time.time()) % 900))
        request_lunar_crush()


if __name__ == "__main__":
    main()

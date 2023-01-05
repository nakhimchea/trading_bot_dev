# This is an integration of LunarCrush APIs to Freqtrade to execute spot market orders
import time
import threading


def request_lunar_crush():
    print("Do some work")
    time.sleep(1)
    print("Some work is done!")


def main():
    while True:
        thr = threading.Thread(target=request_lunar_crush)
        thr.start()
        time.sleep(2)


if __name__ == "__main__":
    main()

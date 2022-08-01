from fetch.Scraper import Scraper
from fetch.Sender import Sender
import json
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--p", type=int, help="To print the fetched ships' data to the screen enter 0, to send the data to the localhost:UDP_PORT enter 1", default=0)
parser.add_argument("--socket",
                    help="UDP socket", type=int, default=5005)
parser.add_argument("--lat-min", type=float,
                    help="Minimum latitude", required=True)
parser.add_argument("--lat-max", type=float,
                    help="Maximum latitude", required=True)
parser.add_argument("--lon-min", type=float,
                    help="Minimum longitude", required=True)
parser.add_argument("--lon-max", type=float,
                    help="Maximum longitude", required=True)

args = parser.parse_args()

scraper = Scraper(latitude=(args.lat_min, args.lat_max),
                  longitude=(args.lon_min, args.lon_max))
sender = Sender("localhost", args.socket)
mode = args.p


def print_data(data: list[dict]):
    for element in data:
        print(element)


def send_data(data: list[dict]):
    for ship in data:
        message = json.dumps(ship)
        sender.send(message)
        print("sent: " + ship["SHIPNAME"])
        time.sleep(0.1)


def remove_duplicates(data: list[dict]):
    new_data: list[dict] = []
    for element in data:
        for ship in element["data"]:
            if ship not in new_data:
                new_data.append(ship)
    return new_data


while True:
    data: list[dict] = dict()
    data = remove_duplicates(scraper.get_ships())
    print(f"{len(data)} ships are fetched.")
    if mode:
        send_data(data)
    else:
        print_data(data)

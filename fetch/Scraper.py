from seleniumwire import webdriver
from seleniumwire.utils import decode
from dataclasses import dataclass, field
from webdriver_manager.chrome import ChromeDriverManager
from typing import Callable
from datetime import datetime, timedelta
import json
import time
import requests


@dataclass(slots=True)
class Scraper:
    """
    Scrapes ship info between the given latitudes and longitudes. Since the data is being fetched using selenium,
    the sleep time is dependendet to the your internet connection. So, It should be set accordingly.
    """

    latitude: tuple[float, float] = field(repr=True)
    longitude: tuple[float, float] = field(repr=True)
    sleep_amount: int = 10
    html_url_list: list[str] = field(init=False, default_factory=list[str])
    requset_url_list: list[str] = field(init=False, default_factory=list[str])

    def __post_init__(self) -> None:
        self.html_url_list.append(
            f"https://www.marinetraffic.com/tr/data/?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map,time_of_latest_position,area_local,lat_of_latest_position,lon_of_latest_position,navigational_status,notes,current_custom_area_in_count&lat_of_latest_position_between|range|lat_of_latest_position_between={self.latitude[0]},{self.latitude[1]}&lon_of_latest_position_between|range|lon_of_latest_position_between={self.longitude[0]},{self.longitude[1]}"
        )
        self.html_url_list.append(
            f"https://www.marinetraffic.com/tr/data/?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map,time_of_latest_position,area_local,lat_of_latest_position,lon_of_latest_position,navigational_status,notes,current_custom_area_in_count&lat_of_latest_position_between|range|lat_of_latest_position_between={self.latitude[0]},{self.latitude[1]}&lon_of_latest_position_between|range|lon_of_latest_position_between={self.longitude[0]},{self.longitude[1]}&ship_type_in|in|Y%C3%BCksek%20H%C4%B1zl%C4%B1%20Tekne,Yolcu%20Gemileri,Kargo%20Gemileri,Tankerler|ship_type_in=4,6,7,8"
        )
        self.html_url_list.append(
            f"https://www.marinetraffic.com/tr/data/?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map,time_of_latest_position,area_local,lat_of_latest_position,lon_of_latest_position,navigational_status,notes,current_custom_area_in_count&lat_of_latest_position_between|range|lat_of_latest_position_between={self.latitude[0]},{self.latitude[1]}&lon_of_latest_position_between|range|lon_of_latest_position_between={self.longitude[0]},{self.longitude[1]}&ship_type_in|in|Tan%C4%B1ms%C4%B1z%20Gemiler,Seyr%C3%BCsefer%20Yard%C4%B1mlar%C4%B1,Bal%C4%B1k%C3%A7%C4%B1,R%C3%B6mork%C3%B6r,%20K%C4%B1lavuz,%20vb,Yatlar%20ve%20Di%C4%9Ferleri|ship_type_in=0,1,2,3,9"
        )
        self.requset_url_list.append(
            f"https://www.marinetraffic.com/tr/reports?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map,time_of_latest_position,area_local,lat_of_latest_position,lon_of_latest_position,navigational_status,notes&lat_of_latest_position_between={self.latitude[0]},{self.latitude[1]}&lon_of_latest_position_between={self.longitude[0]},{self.longitude[1]}"
        )
        self.requset_url_list.append(
            f"https://www.marinetraffic.com/tr/reports?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map,time_of_latest_position,area_local,lat_of_latest_position,lon_of_latest_position,navigational_status,notes&lat_of_latest_position_between={self.latitude[0]},{self.latitude[1]}&lon_of_latest_position_between={self.longitude[0]},{self.longitude[1]}&ship_type_in=4,6,7,8"
        )
        self.requset_url_list.append(
            f"https://www.marinetraffic.com/tr/reports?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map,time_of_latest_position,area_local,lat_of_latest_position,lon_of_latest_position,navigational_status,notes&lat_of_latest_position_between={self.latitude[0]},{self.latitude[1]}&lon_of_latest_position_between={self.longitude[0]},{self.longitude[1]}&ship_type_in=0,1,2,3,9"
        )

    def __get_ship_list_with_selenium(self) -> list[dict]:
        """
        Returns a list of dictionaries with the data of the ships in the given area. Sends 3 requests to the MarineTraffic with selenium.
        """
        json_dicts: list[dict] = list()
        for url in self.html_url_list:
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get(url)
            time.sleep(self.sleep_amount)
            for request in driver.requests:
                if (
                    request.response
                    and "https://www.marinetraffic.com/tr/reports?asset_type=vessels&columns"
                    in request.url
                ):
                    response = request.response
                    body = decode(
                        response.body,
                        response.headers.get("Content-Encoding", "identity"),
                    )
                    try:
                        json_dicts.append(json.loads(body.decode("utf-8")))
                    except json.decoder.JSONDecodeError:
                        print("JSONDecodeError")
                    break
            driver.close()
        return self.__remove_duplicates(json_dicts)

    def __get_ship_list(self) -> list[dict]:
        session = requests.Session()
        session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "Vessel-Image": "005bf958a6548a79c6d3a42eba493e339624"
        }
        ship_list: list[dict] = list()
        for url in self.requset_url_list:
            response = session.get(url)
            ship_list.extend(json.loads(response.text)["data"])
            print(str(response.status_code) + " -> ship list fetch response")
        return self.__remove_duplicates(ship_list, from_request=True)

    def __valid_ship(self, ship: dict) -> bool:
        return int(ship["MMSI"]) > 0 and int(ship["IMO"]) > 0

    def __check_timestamp(func: Callable[[list[dict]], list[dict]]) -> Callable:
        def wrapper(self, *args, **kwargs):
            ship_list: list[dict] = func(self, *args, **kwargs)
            yesterday = datetime.now() - timedelta(days=1)
            for ship in ship_list:
                timestamp = datetime.strptime(
                    ship["TIMESTAMP"], "%Y-%m-%d %H:%M:%S")
                if timestamp < yesterday:
                    ship_list.remove(ship)
            return ship_list
        return wrapper

    def __remove_duplicates(self, data: list[dict], from_request: bool = False) -> list[dict]:
        new_data: list[dict] = []
        if from_request:
            for ship in data:
                if (ship not in new_data and self.__valid_ship(ship)):
                    new_data.append(ship)
            return new_data

        for element in data:
            for ship in element["data"]:
                if (ship not in new_data and self.__valid_ship(ship)):
                    new_data.append(ship)
        return new_data

    @staticmethod
    def __get_ship_detail_url(ship_id: str):
        return f"https://www.marinetraffic.com/map/getvesseljson/shipid:{ship_id}"

    @staticmethod
    def __update_ship(toUpdate: dict, source: dict) -> None:
        for key, value in source.items():
            if key not in toUpdate.keys():
                toUpdate[key] = value

    @__check_timestamp
    def __extend_ship_info(self, ship_list: list[dict]) -> list[dict]:
        session = requests.Session()
        session.headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.3",
            'accept': "application/json, text/plain, */*",
            'referer': "https://www.marinetraffic.com/"}
        total_ship = len(ship_list)
        print(f"Total {total_ship} ships to update")
        for index, ship in enumerate(ship_list):
            url = self.__get_ship_detail_url(ship["SHIP_ID"])
            response = session.get(url)
            print(
                f"Response for ship {ship['SHIP_ID']} " + str(response.status_code) + f" {total_ship - index - 1} ships left.")
            if response.status_code == 200:
                self.__update_ship(ship, json.loads(response.text))
        return ship_list

    def get_ships(self):
        ship_list: list[dict] = self.__get_ship_list()
        # ship_list: list[dict] = self.__get_ship_list_with_selenium()
        return self.__extend_ship_info(ship_list)

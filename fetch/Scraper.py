from seleniumwire import webdriver
from seleniumwire.utils import decode
from dataclasses import dataclass, field
from webdriver_manager.chrome import ChromeDriverManager
import json
import time


@dataclass
class Scraper:
    '''
    Scrapes ship info between the given latitudes and longitudes. Since the data is being fetched using selenium,
    the sleep time is dependendet to the your internet connection. So, It should be set accordingly.
    '''
    latitude: tuple[float, float] = field(repr=True)
    longitude: tuple[float, float] = field(repr=True)
    sleep_amount: int = 10

    def __post_init__(self) -> None:
        self.url_list = [f"https://www.marinetraffic.com/tr/data/?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map,time_of_latest_position,area_local,lat_of_latest_position,lon_of_latest_position,navigational_status,notes,current_custom_area_in_count&lat_of_latest_position_between|range|lat_of_latest_position_between={self.latitude[0]},{self.latitude[1]}&lon_of_latest_position_between|range|lon_of_latest_position_between={self.longitude[0]},{self.longitude[1]}",
                         f"https://www.marinetraffic.com/tr/data/?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map,time_of_latest_position,area_local,lat_of_latest_position,lon_of_latest_position,navigational_status,notes,current_custom_area_in_count&lat_of_latest_position_between|range|lat_of_latest_position_between={self.latitude[0]},{self.latitude[1]}&lon_of_latest_position_between|range|lon_of_latest_position_between={self.longitude[0]},{self.longitude[1]}&ship_type_in|in|Y%C3%BCksek%20H%C4%B1zl%C4%B1%20Tekne,Yolcu%20Gemileri,Kargo%20Gemileri,Tankerler|ship_type_in=4,6,7,8",
                         f"https://www.marinetraffic.com/tr/data/?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map,time_of_latest_position,area_local,lat_of_latest_position,lon_of_latest_position,navigational_status,notes,current_custom_area_in_count&lat_of_latest_position_between|range|lat_of_latest_position_between={self.latitude[0]},{self.latitude[1]}&lon_of_latest_position_between|range|lon_of_latest_position_between={self.longitude[0]},{self.longitude[1]}&ship_type_in|in|Tan%C4%B1ms%C4%B1z%20Gemiler,Seyr%C3%BCsefer%20Yard%C4%B1mlar%C4%B1,Bal%C4%B1k%C3%A7%C4%B1,R%C3%B6mork%C3%B6r,%20K%C4%B1lavuz,%20vb,Yatlar%20ve%20Di%C4%9Ferleri|ship_type_in=0,1,2,3,9"]

    def __get_data(self) -> list[dict]:
        '''
        Returns a list of dictionaries with the data of the ships in the given area. Sends 3 requests to the MarineTraffic with selenium.
        '''
        json_dicts: list[dict] = list()
        for url in self.url_list:
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get(url)
            time.sleep(self.sleep_amount)
            for request in driver.requests:
                if request.response and "https://www.marinetraffic.com/tr/reports?asset_type=vessels&columns" in request.url:
                    response = request.response
                    body = decode(response.body, response.headers.get(
                        'Content-Encoding', 'identity'))
                    try:
                        json_dicts.append(json.loads(body.decode('utf-8')))
                    except json.decoder.JSONDecodeError:
                        print("JSONDecodeError")
                    break
            driver.close()
        return json_dicts

    def get_ships(self):
        return self.__get_data()

from dataclasses import dataclass
import json
import socket


@dataclass
class Receiver:

    UDP_IP: str
    UDP_PORT: int

    def __post_init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.UDP_IP, self.UDP_PORT))

    def __receive_data(self) -> bytes:
        data, addr = self.socket.recvfrom(1024)
        return data

    def receive(self) -> None:
        while True:
            data = json.loads(self.__receive_data().decode('utf-8'))
            print("lat: " + data["LAT"] + " lon: " +
                  data["LON"] + " vessel_name: " + data["SHIPNAME"] + " mmsi: " + data["MMSI"])
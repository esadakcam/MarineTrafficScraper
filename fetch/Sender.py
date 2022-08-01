from dataclasses import dataclass
import socket


@dataclass
class Sender:
    UDP_IP: str
    UDP_PORT: int

    def __post_init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, message: str) -> None:
        self.socket.sendto(message.encode(), (self.UDP_IP, self.UDP_PORT))
from fetch.Receiver import Receiver

receiver = Receiver("127.0.0.1", 5005)

while True:
    receiver.receive()
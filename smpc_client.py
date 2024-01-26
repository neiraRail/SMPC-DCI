import sys, Ice
import SMPC
from utils import generateShares

server_proxy = "Server:default -p 10000"
dummy_proxy = "Dummy:default -p 10001"

def sendByte(byte):
    # Initialize state
    own_shares = generateShares(1)
    parts = []
    sums = []

    # Initialize Ice communicator
    with Ice.initialize(sys.argv) as communicator:
        
        # First message from client to server
        base = communicator.stringToProxy(server_proxy)
        server = SMPC.ServidorPrx.checkedCast(base)
        if not server:
            raise RuntimeError("Invalid proxy")
        # Server returns the client's corresponding share and its sum
        serverPart, serverSum = server.messageFromClient(own_shares[1])
        parts.append(serverPart)
        sums.append(serverSum)
        
        # Second message from client to dummy
        base = communicator.stringToProxy(dummy_proxy)
        dummy = SMPC.DummyPrx.checkedCast(base)
        if not dummy:
            raise RuntimeError("Invalid proxy")
        # Dummy returns the client's corresponding share and its sum
        dummyPart, dummySum = dummy.messageFromClient(own_shares[2])
        parts.append(dummyPart)
        sums.append(dummySum)

        # Client acknowledge its own share and its sum
        parts.append(own_shares[0])
        sums.append(sum(parts))

        secret_key = sum(sums)%255
        # Prints the secret key (ONLY FOR TESTING PURPOSES)
        print("Secret key: ", secret_key.to_bytes(1))

        # Mask the sending byte with the secret key
        masked = byte^secret_key

        # Third message from client to server sending the masked byte and its own sum
        server.finalize(sum(parts), masked)

    return sum(sums)%255

message = b'Hello secret world!'

for byte in message:
    sendByte(byte)

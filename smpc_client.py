import sys, Ice
import SMPC
from utils import generateShares

server_proxy = "Servidor:default -p 10000"
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
        serverPart, serverSum = server.entregarDesdeCliente(own_shares[1])
        parts.append(serverPart)
        sums.append(serverSum)
        
        # Second message from client to dummy
        base = communicator.stringToProxy(dummy_proxy)
        dummy = SMPC.DummyPrx.checkedCast(base)
        if not dummy:
            raise RuntimeError("Invalid proxy")
        # Dummy returns the client's corresponding share and its sum
        dummyPart, dummySum = dummy.entregarDesdeCliente(own_shares[2])
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
        server.finalizar(sum(parts), masked)

    return sum(sums)%255


def sendWholeMessage(message):
    # get byte size of message
    size = len(message)
    # generate shares
    shares = generateShares(size)
    print(shares[1])
    partes = []
    sumas = []
    with Ice.initialize(sys.argv) as communicator:
        #Enviar a server
        base = communicator.stringToProxy("Servidor:default -p 10000")
        servidor = SMPC.ServidorPrx.checkedCast(base)
        if not servidor:
            raise RuntimeError("Invalid proxy")
        parteServidor, sumaServidor = servidor.entregarDesdeCliente(shares[1])
        # print("Servidor envia", parteServidor, "a cliente")
        # print("Servidor envía", sumaServidor, "a cliente")
        partes.append(parteServidor)
        sumas.append(sumaServidor)
        
        #Enviar a dummy
        base = communicator.stringToProxy("Dummy:default -p 10001")
        dummy = SMPC.DummyPrx.checkedCast(base)
        if not dummy:
            raise RuntimeError("Invalid proxy")
        parteDummy, sumaDummy = dummy.entregarDesdeCliente(shares[2])
        # print("Dummy envía ", parteDummy, " a cliente")
        # print("Dummy envía ", sumaDummy, " a cliente")
        partes.append(parteDummy)
        sumas.append(sumaDummy)

        #Finalizar
        partes.append(shares[0])
        sumas.append(sum(partes))

        print("Suma: ", (sum(sumas)).to_bytes(size))

        # We are going to truncate the big integer to match the size of the message.
        # Calculate the mask to keep only the desired number of bytes
        truncate_mask = (1 << (size * 8)) - 1
        # Apply the mask to truncate the integer
        truncated = sum(sumas) & truncate_mask

        # Mask the message with the truncated integer to encrypt it
        masked = message^truncated

        servidor.finalizar(sum(partes), masked)

    return truncated


message = b'Hello secret world!'

print(sendWholeMessage(message))

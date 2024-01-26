import sys, Ice
import SMPC

from utils import generateShares

dummy_proxy = "Dummy:default -p 10001"

original = bytearray()
message = bytearray()
 
class Servidor(SMPC.Servidor):
    def __init__(self):
       self.parts= []
       self.sums = []
       self.shares = generateShares(1)

       self.parts.append(self.shares[1])

    def entregarDesdeCliente(self, part, current=None):
        # Saves client's part
        self.parts.append(part)

        # Message from server to dummy
        with Ice.initialize(sys.argv) as communicator:
            base = communicator.stringToProxy(dummy_proxy)
            dummy = SMPC.DummyPrx.checkedCast(base)
            if not dummy:
                raise RuntimeError("Invalid proxy")
            # Dummy returns the server's corresponding share
            parte_dummy = dummy.entregarDesdeServer(self.shares[2])
            self.parts.append(parte_dummy)
            self.sums.append(sum(self.parts))
        
        # Returns client's corresponding share and sum
        return (self.shares[0], sum(self.parts))

    def entregarDesdeDummy(self, suma, current=None):
        self.sums.append(suma)
    
    def finalizar(self, suma, payload, current=None):
        global message
        global original
        self.sums.append(suma)

        original.append(payload)
        message.append(payload^(sum(self.sums)%255))
        print(original)
        print(message)
        # Reset state of server
        self.__init__()
        
 
with Ice.initialize(sys.argv) as communicator:
    adapter = communicator.createObjectAdapterWithEndpoints("Server", "default -p 10000")
    object = Servidor()
    adapter.add(object, communicator.stringToIdentity("Server"))
    adapter.activate()
    communicator.waitForShutdown()
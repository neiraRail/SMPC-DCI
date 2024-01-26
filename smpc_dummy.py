import sys, Ice
import SMPC

from utils import generateShares

 
class Dummy(SMPC.Dummy):
    def __init__(self):
       self.parts= []
       self.shares = generateShares(1)
       self.parts.append(self.shares[2])

    def entregarDesdeServer(self, parte, current=None):
        # Reset state of dummy
        self.__init__()
        
        # Saves server's part
        self.parts.append(parte)

        # Returns server's corresponding share
        return self.shares[1]
    
    def entregarDesdeCliente(self, part, current=None):
        # Saves client's part
        self.parts.append(part)

        # Sends dummy's sum to server
        with Ice.initialize(sys.argv) as communicator:
            base = communicator.stringToProxy("Server:default -p 10000")
            server = SMPC.ServidorPrx.checkedCast(base)
            if not server:
                raise RuntimeError("Invalid proxy")
            server.entregarDesdeDummy(sum(self.parts))

        # Returns client's corresponding share and sum
        return (self.shares[0], sum(self.parts)) 
    
        
 
with Ice.initialize(sys.argv) as communicator:
    adapter = communicator.createObjectAdapterWithEndpoints("Dummy", "default -p 10001")
    object = Dummy()
    adapter.add(object, communicator.stringToIdentity("Dummy"))
    adapter.activate()
    communicator.waitForShutdown()
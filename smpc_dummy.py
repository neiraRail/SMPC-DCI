import sys, Ice
import SMPC

from utils import generateShares

size = 4
 
class Dummy(SMPC.Dummy):
    def __init__(self):
       self.partes= []
       self.shares = generateShares(size)
       self.partes.append(self.shares[2])

    def entregarDesdeServer(self, parte, current=None):
        self.__init__()
        # print("Servidor envía ", parte, " a dummy")
        self.partes.append(parte)
        return self.shares[1]
    
    def entregarDesdeCliente(self, parte, current=None):
        # print("Cliente envía ", parte, " a dummy")
        self.partes.append(parte)
        with Ice.initialize(sys.argv) as communicator:
            base = communicator.stringToProxy("Servidor:default -p 10000")
            servidor = SMPC.ServidorPrx.checkedCast(base)
            if not servidor:
                raise RuntimeError("Invalid proxy")
            servidor.entregarDesdeDummy(sum(self.partes))
            # print("Servidor no envia nada a dummy")
            
        return (self.shares[0], sum(self.partes)) #parte propia y suma
    
        
 
with Ice.initialize(sys.argv) as communicator:
    adapter = communicator.createObjectAdapterWithEndpoints("Dummy", "default -p 10001")
    object = Dummy()
    adapter.add(object, communicator.stringToIdentity("Dummy"))
    adapter.activate()
    communicator.waitForShutdown()
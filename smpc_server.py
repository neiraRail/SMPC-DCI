import sys, Ice
import SMPC

from utils import generateShares

size = 4

original = bytearray()
message = bytearray()
 
class Servidor(SMPC.Servidor):
    def __init__(self):
       self.partes= []
       self.sumas = []
       self.shares = generateShares(size)

       self.partes.append(self.shares[1])

    def entregarDesdeCliente(self, parte, current=None):
        # print("Cliente envia ", parte, " a servidor")
        self.partes.append(parte)
        with Ice.initialize(sys.argv) as communicator:
            base = communicator.stringToProxy("Dummy:default -p 10001")
            dummy = SMPC.DummyPrx.checkedCast(base)
            if not dummy:
                raise RuntimeError("Invalid proxy")
            print(self.shares[2])
            parte_dummy = dummy.entregarDesdeServer(self.shares[2])
            # print("Dummy envia ", parte_dummy, " a servidor")
            self.partes.append(parte_dummy)
            self.sumas.append(sum(self.partes))
        
        return (self.shares[0], sum(self.partes))

    def entregarDesdeDummy(self, suma, current=None):
        # print("Dummy envia ", suma, " a servidor")
        self.sumas.append(suma)
    
    def finalizar(self, suma, payload, current=None):
        global message
        global original
        # print("Cliente envia ", suma, " a servidor")
        self.sumas.append(suma)
        # print("Suma: ", sum(self.sumas))
        # print("Mensaje: ", payload)
        # print("Mensaje: ", payload^(sum(self.sumas)%255))

        original.append(payload)
        message.append(payload^(sum(self.sumas)%255))
        print(original)
        print(message)
        # reset
        self.__init__()
        
 
with Ice.initialize(sys.argv) as communicator:
    adapter = communicator.createObjectAdapterWithEndpoints("Servidor", "default -p 10000")
    object = Servidor()
    adapter.add(object, communicator.stringToIdentity("Servidor"))
    adapter.activate()
    communicator.waitForShutdown()
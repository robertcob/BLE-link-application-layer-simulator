from utilities import errors
import PDU



# we will use packet formats suited to BLE 4.2 an below
# changes may have been made since BLE 5.0

class Packet:
    def __init__(self, type, accessAddress, range, uuid):
        self.access_address = accessAddress
        self.type = type
        self.error = None
        self.connectionRange = range
        self.UUID = uuid

        
    def setType(self, packetType):
        if (packetType == "advertisingPkt") or (packetType == "dataPkt"):
            self.type = packetType
        else:
            print("invald packet type set")
            self.error = errors.Error("packet name", "packet type", "invalid packet type provided", 1021)
            return
    

### for this Advertising packet we only use the ADV_IND PDU
class Advertising_Packet(Packet):
    def __init__(self, deviceName, cID, payload, length):
        super().__init__()
        self.deviceName = deviceName
        self.PDU = PDU.ADV_PDU()

    
    # sets whether packet is scannable connectable etc

  
class Data_Packet(Packet):
    def __init__(self):
        super().__init__()
        


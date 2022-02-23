from utilities import errors

# we will use packet formats suited to BLE 4.2 an below
# changes may have been made since BLE 5.0

class Packet:
    def __init__(self, type, sender_address, uuid):
        self.error = None
        self.payload = {
            'TYPE': type,
            'SRC': sender_address,
            'DST': 0,
            'LSRC': uuid,
            'LDST' : 0,
            'SEQ' : None,
            'DATA': None
            }
        
    def setType(self, packetType):
        if (packetType == "advertisingPkt") or (packetType == "dataPkt") or (packetType == "extAdvertisingPkt"):
            self.type = packetType
        else:
            print("invald packet type set")
            self.error = errors.Error("packet name", "packet type", "invalid packet type provided", 1021)
            return
    
    def setData(self, data):
        self.payload['DATA'] = data
        return



### PDE are the various payload setting for ble advertising/scanning/data packets
from enum import Enum

class ADV_PDU:
    def __init__(self, address, c_ID, payload,  connectMode, scanMode, directMode):
        self.advertAddress = address
        self.companyID = c_ID
        self.payload = payload
        self.mode = self.setMode(connectMode, scanMode, directMode)
        
    def setMode(self, connectType, scanType, directType):
        return Mode(connectType, scanType, directType)
        
class Mode(Enum):
    Connectable = None
    Scannable = None
    Directed = None
        
class Data_PDU:
    def __init__(self, payload):
        self.payload = payload
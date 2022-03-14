
from ATT.packets.packets import Packet
from utilities.rand import *
class Peripheral:
    def __init__(self, name, address, discoveryMode):
        self.name = name
        self.address = address
        self.discoveryMode = discoveryMode ### can be either non-discoverable or discoverable
        self.ADVPacket = None
        self.DataPackets = []
        self.centralDeviceData = None

    def setConnectEstMode(self, *sequential, **named):
        connectionMode = dict(zip(sequential, range(len(sequential))), **named)
        return type('Enum', (), connectionMode)
    
    def addPackets(self, newPacket):
        if (newPacket.payload['TYPE'] == "advertisingPkt") or (newPacket.payload['TYPE'] == "extAdvertisingPkt"):
            self.ADVPacket = newPacket
        else:
            
            self.DataPackets.append(newPacket)
    
    def createAdvertismentPackets(self, id, join_Node, sqnr, data):
        if data:
            ADV_PKT = Packet("advertisingPkt", id, join_Node, sqnr)
            ADV_PKT.setData(data)
        else: 
            ADV_PKT = Packet("advertisingPkt", id, join_Node, sqnr)
        return ADV_PKT
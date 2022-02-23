from enum import Enum
from tkinter import N
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


    def setConnectEstMode(self, nonconnectType, undirectedType, directType):
        return connectionEstablishModes(nonconnectType, undirectedType, directType)
    
    def addPackets(self, newPacket):
        if (newPacket.payload['TYPE'] == "advertisingPkt") or (newPacket.payload['TYPE'] == "extAdvertisingPkt"):
            self.ADVPackets = newPacket
        else:
            
            self.DataPackets.append(newPacket)
    
    def createAdvertismentPackets(self, data):
        if data:
            ADV_PKT = Packet("advertisingPkt", self.address, random_with_N_digits(6))
            ADV_PKT.setData(data)
        else: 
            ADV_PKT = Packet("advertisingPkt", self.address, random_with_N_digits(6))
        return ADV_PKT
    
    def setCentralDeviceData(self, data):
        self.centralDeviceData = data
        return
        
class connectionEstablishModes(Enum):
    nonConnectable = None
    undirected = None
    directed = None

# class centralDeviceData:
#     def __init__(self,uuid, address):
#         self.uuid = uuid
#         self.address = address
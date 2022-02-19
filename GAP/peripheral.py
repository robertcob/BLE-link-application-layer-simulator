from enum import Enum

class Peripheral:
    def __init__(self, name, address, discoveryMode):
        self.name = name
        self.address = address
        self.discoveryMode = discoveryMode ### can be either non-discoverable or general discoverable


    def setConnectEstMode(self, nonconnectType, undirectedType, directType):
        return connectionEstablishModes(nonconnectType, undirectedType, directType)
        
class connectionEstablishModes(Enum):
    nonConnectable = None
    undirected = None
    directed = None

class centralDeviceData:
    def __init__(self,uuid, address, packetInterval):
        self.uuid = uuid
        self.address = address
        self.packetInterval = packetInterval
    
    def setPacketInterval(self, packetInterval):
        self.packetInterval = packetInterval
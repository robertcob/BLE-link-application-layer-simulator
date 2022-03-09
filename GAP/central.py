### class details alongside general scanning role
class Central:
    def __init__(self, name, address, discProcedure):
        self.name = name
        self.address = address
        self.discoveryProcedure = discProcedure ### either limited or general
        self.whitelist = []
        self.peripheralData = None
      
    def addToWhitelist(self, deviceDetails):
        self.whitelist.append(deviceDetails)
        return
    
    def addPeripheralData(self, data):
        self.peripheralData = data
        return
        

## this data is optional, class onyl instantiated if, GAT is used in GAT advert
## other is a dictionary
class peripheralData:
    def __init__(self, name, uuid, other):
        self.name = name
        self.uuid = uuid
        self.other = other
    
    def setOtherData(self, newOther):
        self.other = newOther
    

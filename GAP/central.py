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
        


# class peripheralData:
#     def __init__(self, name, uuid, cutoffTime):
#         self.name = name
#         self.uuid = uuid
#         self.cutoffTime = cutoffTime
    
#     def setCutoffTime(self, cutoffTime):
#         self.cutoffTime = cutoffTime
#         return
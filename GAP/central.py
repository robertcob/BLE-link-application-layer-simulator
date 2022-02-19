### class details alongside general scanning role
class Central:
    def __init__(self, name, address, discProcedure, connectMode, connectEstbProcedure, interval):
        self.name = name
        self.address = address
        self.connectMode = connectMode
        self.discoveryProcedure = discProcedure ### either limited or general
        self.connectEstbProcedure = connectEstbProcedure  ### either auto connEstbProcedure or general connectEstbProcedure
        self.whitelist = []
        self.peripheralData = None
      
    def addToWhitelist(self, deviceDetails):
        self.whitelist.append(deviceDetails)
        return


class peripheralData:
    def __init__(self, name, uuid, cutoffTime):
        self.name = name
        self.uuid = uuid
        self.cutoffTime = cutoffTime
    
    def setCutoffTime(self, cutoffTime):
        self.cutoffTime = cutoffTime
        return
### we listen for service delcarations
### once found we define a service and query it here
### we query any data 
from ATT.attributes import Attribute
class Server:
    def __init__(self):
        self.profile = {}
        self.curServiceId = None
    
    def addToProfile(self, data):
        print("DEBUG3", data)
        currAtt = Attribute(data['pktUUID'], data['handle'], data['value'])
        if data['type'] == 'serviceDec':
            currAtt.createAttPerms(True, False, False)
            currAtt.createAttTypes(True, False, False, False)
            self.addService(currAtt)
            self.curServiceId = currAtt.pktUUID
        elif data['type'] == 'characterDec':
            currAtt.createAttPerms(True, False, False)
            currAtt.createAttTypes(False, True, False, False)
            self.addCharacteristicToService(self.curServiceId, currAtt)
        elif data['type'] == 'characterVal':
            if data['permissions'] == 'read':
                currAtt.createAttPerms(True, False, False)
            elif data['permissions'] == 'write':
                currAtt.createAttPerms(False, True, False)
            else:
                currAtt.createAttPerms(False, False, True)
            currAtt.createAttTypes(False, False, True, False)
            self.addCharacteristicToService(self.curServiceId, currAtt)
        else:
            currAtt.createAttPerms(False, False, True)
            currAtt.createAttTypes(False, False, False, True)
            self.addDescriptorToService(self.curServiceId, currAtt)
        
        return currAtt

    def addService(self, service):
        self.profile[service.pktUUID] = [service]
        
    def addCharacteristicToService(self, serviceUuid, characteristic):
        self.profile[serviceUuid].append(characteristic)
    
    ### splitting identical functionality of addChar and addDesc
    ### in case later on altered functionality needs to be implemented
    ### when adding a descriptor to service...
    def addDescriptorToService(self, serviceUuid, descriptor):
        self.profile[serviceUuid].append(descriptor)
        
    def getServiceOrDesciptor(self, uuid):
        values = self.profile.values()
        for each in values:
            for att in each:
                if att.pktUUID == uuid:
                    return att
                
            
    def getCharDecAtt(self, uuid):
        values = self.profile.values()
        for each in values:
            for att in each:
                if att.pktUUID == uuid and att.type.characterDec == True:
                    return att
    
    def getCharValAtt(self, uuid):
        values = self.profile.values()
        for each in values:
            for att in each:
                if att.pktUUID == uuid and att.type.characterVal == True:
                    return att
    

            

        
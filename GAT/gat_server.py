from metadata import Characteristic

### we listen for service delcarations
### once found we define a service and query it here
### we query any data 
from metadata import Service
class Server:
    def __init__(self):
        self.profile = {}

    def addService(self, service):
        self.profile[service.uuid] = [service]
        
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
    

            

        
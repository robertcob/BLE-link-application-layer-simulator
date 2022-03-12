from metadata import Service
from metadata import Characteristic

### we listen for service delcarations
### once found we define a service and query it here
### we query any data 
from metadata import Service
class Server:
    def __init__(self):
        self.profile = None
    
    def createService(self, serviceDeclaration):
        curr_Service = Service(serviceDeclaration.UUID, serviceDeclaration.handle)
        self.services.append(curr_Service)
    
    def createCharacteristic(self, characteristicDeclaration):
        curr_Characteristic = Characteristic(characteristicDeclaration.UUID, characteristicDeclaration.handle)

### define builder pattern for profile of GAT Server

        
from metadata import Service

### we listen for service delcarations
### once found we define a service and query it here
from metadata import Service
class Server:
    def __init__(self):
        self.services = []
    
    
    def createService(self, serviceDeclaration):
        curr_Service = Service(serviceDeclaration.UUID)
        self.services.append(curr_Service)
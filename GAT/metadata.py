from ATT.attributes import Attribute
### Theses classes will be used on the GATT server side when conveying packets
### and designing the real server model
class Service:
    def __init__(self, UUID, handle):
        self.UUID =  UUID
        self.handle = handle
        self.characteristics = []
    
    def createCharacteristic(self):
        currCharacteristic = Characteristic()
        self.characteristics.append(currCharacteristic)
        
class Characteristic:
    def __init__(self, UUID, handle):
        self.UUID = UUID
        self.handle = handle
        self.valueAttributes = []
        self.descriptors = []
    
class Descriptor(Attribute):
    def __init__(self, description):
        super().__init__()
        self.description = description
    
    def toggleValue(self, changedValue):
        self.value = changedValue
        
    


    
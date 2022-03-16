from utilities.enum import *
class Attribute:
    def __init__(self, UUID, handle, value):
        self.pktUUID = UUID
        self.handle = handle
        self.type = None
        self.permissions = None 
        self.value = value

    # none = bool
    # readable = bool
    # writeable = bool
    # readableAndWriteable = bool
    # security = bool

    
    def createAttTypes(self, serviceDec, characterDec, characterVal, dccc):
        attributeType = createEnum(serviceDec=serviceDec,characterDec=characterDec, 
                                   characterVal=characterVal, dccc=dccc)
        self.type = attributeType
    
    def createAttPerms(self, read, write, readAndWrite):
        permissionType = createEnum(read=read, write=write, readAndWrite=readAndWrite)
        self.permissions = permissionType

    def setType(self, newType):
        self.type = newType
        return self.type
    
    def setValue(self, newValue):
        self.value = newValue
    
    def getType(self):
        
        if self.type.serviceDec:
            self.type = 'serviceDec'
        elif self.type.characterDec:
            self.type =  'characterDec'
        elif self.type.characterVal:
            self.type =  'characterVal'
        else:
            self.type =  'dccc'  
    
    def getPerm(self):
        if self.permissions.read:
            self.permissions =  'read'
        elif self.permissions.write:
            self.permissions =  'write'
        else:
            self.permissions = 'readAndWrite'  

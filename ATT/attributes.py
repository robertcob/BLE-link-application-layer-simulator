from enum import Enum

class Attribute:
    def __init__(self, UUID, handle, type, permissions, value):
        self.pktUUID = UUID
        self.handle = handle
        self.type = type 
        self.permissions = permissions 
        self.value = value

    def setPermissions(self, permissions):
        self.permissions = permissions 
        return self.permissions

    def setType(self, newType):
        self.type = newType
        return self.type

class permissions(Enum):
    none = None
    readable = None
    writeable = None
    readableAndWriteable = None
    security = None

class properties(Enum):
    Broadcast = None
    Read = None
    WriteWithoutResponse = None
    Write = None
    Notify = None
    Indicate = None

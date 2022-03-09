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
    

    # none = bool
    # readable = bool
    # writeable = bool
    # readableAndWriteable = bool
    # security = bool
    def createPermissions(self, *sequential, **named):
        enums = dict(zip(sequential, range(len(sequential))), **named)
        return type('Enum', (), enums)

    def setType(self, newType):
        self.type = newType
        return self.type

# class properties(Enum):
#     Broadcast = None
#     Read = None
#     WriteWithoutResponse = None
#     Write = None
#     Notify = None
#     Indicate = None

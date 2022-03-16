from abc import abstractmethod
from re import T
from ATT.attributes import Attribute
from utilities.rand import randomHeartRateValue
import json


class Client:
    def __init__(self, name, UUID):
        self.name = name
        self.uuid = UUID
        '''
        this is a basic metric method for creating handles
        the first service will be in the range of 0x00A -> 0x0013
        the second service will be in a range of 0x0014 -> 0x001D
        
        we will define as decimal but when adding to any GATT/GAP object we will str(hex(DECIMAL_HANDLE))
        '''
    
    def createServiceDecAtt(self, handle, uuid, val):
        serviceDec = Attribute(uuid, handle, val)
        serviceDec.createAttTypes(True, False, False, False)
        serviceDec.createAttPerms(True, False, False)
        return serviceDec
        
    def createCharacteristicDecAtt(self, handle, uuid, val):
        charDec = Attribute(uuid, handle, val)
        charDec.createAttTypes(False, True, False, False)
        charDec.createAttPerms(True, False, False)
        return charDec

    def createCharacteristicValAtt(self, handle, uuid, val):
        charVal = Attribute(uuid, handle, val)
        charVal.createAttTypes(False, False, True, False)
        return charVal

    ### we are only dealing with cccd attributes for descriptors
    def createDescriptorAtt(self, handle, uuid, val):
        dccc = Attribute(uuid, handle, val)
        dccc.createAttTypes(False, False, False, True)
        dccc.createAttPerms(False, False, True)
        return dccc    
    
    
    ### simpy transport requires json serialization
    def packageATT(self, attPkt):
        attPkt.getType()
        attPkt.getPerm()
        return attPkt.__dict__
        
    
    @abstractmethod
    def ProfileDirector(self):
        ### first we will define each of our packets 
        ### then we use the director to construct the concrete
        ### GATT packet object
        
        ################################################################
        '''
        serviceDec -> Device info
        ----------------------------------------------------------------
        characterDec -> model num
        characterVal (dummy value)
        ----------------------------------------------------------------
        characterDec -> serial num
        characterVal (dummy value)
        ----------------------------------------------------------------
        characterDec -> manufacturer name
        characterVal (dummy value)
        ----------------------------------------------------------------
        ----------------------------------------------------------------
        serviceDec -> heartRate
        ----------------------------------------------------------------
        characterDec -> hr measurment
        characterVal (dummy value)
        '''
        ################################################################
        
        serviceDec1 = self.createServiceDecAtt("0x000A", "0x180A", None)
        charDec1 = self.createCharacteristicDecAtt("0x000B", "0x2A24", None)
        charVal1 = self.createCharacteristicValAtt("0x000C", "0x2A24", "model-6023989128929")
        charVal1.createAttPerms(True, False, False)
        
        charDec2 = self.createCharacteristicDecAtt("0x000D", "0x2A25", None)
        charVal2 = self.createCharacteristicValAtt("0x000E", "0x2A25", "serial-123456789")
        charVal2.createAttPerms(True, False, False)
        
        charDec3 = self.createCharacteristicDecAtt("0x000F", "0x2A29", None)
        charVal3 = self.createCharacteristicValAtt("0x0010", "0x2A29", "Corp Heart Moniter")
        charVal3.createAttPerms(True, False, False)
        
        serviceDec2 = self.createServiceDecAtt("0x0011", "0x0021", None)
        charDec4 = self.createCharacteristicDecAtt("0x0014", "0x2A37", None)
        charVal4 = self.createCharacteristicValAtt("0x0015", "0x2A37", randomHeartRateValue())
        charVal4.createAttPerms(False, False, True)
        descriptor = self.createDescriptorAtt("0x0016", "0x2902", False)

        builder = ProfileBuilder()
        builder.addServiceDeclaration(serviceDec1)
        builder.addCharacteristicDeclaration(charDec1)
        builder.addCharacteristicValue(charVal1, None)
        
        builder.addCharacteristicDeclaration(charDec2)
        builder.addCharacteristicValue(charVal2, None)
        
        builder.addCharacteristicDeclaration(charDec3)
        builder.addCharacteristicValue(charVal3, None) 
        
        builder.addServiceDeclaration(serviceDec2)
        builder.addCharacteristicDeclaration(charDec4) 
        builder.addCharacteristicValue(charVal4, descriptor) 
        
        return builder.getProfile()
        

### simple builder pattern for constructing array of GATT packets to be
### sent over the simpy radio
class ProfileBuilder(object):
    
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.profile = []
        
    def addServiceDeclaration(self, serviceDeclaration) -> None:
        self.profile.append(serviceDeclaration)
    
    def addCharacteristicDeclaration(self, characteristicDeclaration)-> None:
        self.profile.append(characteristicDeclaration)
    
    def addCharacteristicValue(self, characteristicValue, cccDescriptor)-> None:
        if cccDescriptor:
            self.profile.append(characteristicValue)
            self.profile.append(cccDescriptor)
        else:
            self.profile.append(characteristicValue)
    
    @abstractmethod
    def getProfile(self):
        return self.profile
            
        
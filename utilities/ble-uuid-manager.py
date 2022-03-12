### uuid figures are based on bluetooth SIG documentation
### see -> https://www.bluetooth.com/ for further details

### functions denote various hash tables containing each uuid for possible characteristic

def serUUIDClassifier(type):
    uuidDict = {
        "device-info": "0x0011",
        "heart-rate" : "0x180D"
    }
    try:
        currSerHex = uuidDict[type]
        return {True: currSerHex}
    except KeyError:
        return {False: "service does not exist"}

def charUUIDClassifier(type):
    
    uuidDict = {
        "model-number" : "0x2A24",
        "serial-number": "0x2A25",
        "manufacturer-name" : "0x2A29",
        "hr-control-point" : "0x2A39",
        "body-sensor-location": "0x2A38",
        "hr-measurement": "0x2A37"
    }
    try:
        currCharHex = uuidDict[type]
        return {True: currCharHex}
    except KeyError:
        return {False: "characteristic does not exist"}

def descUUIDClassifier(type):
    uuidDict = {
        "client-characteristic-configuration": "0x2902"
    }
    
    try:
        currDescHex = uuidDict[type]
        return {True: currDescHex}
    except KeyError:
        return {False: "descriptor does not exist"}

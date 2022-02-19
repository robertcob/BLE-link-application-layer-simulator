### PDE are the various payload setting for ble advertising/scanning/data packets
class ADV_PDU:
    def __init__(self, header, payload):
        self.header = header
        self.payload = payload
        

        
class Data_PDU:
    def __init__(self, payload):
        self.payload = payload
'''
Example shows:
-> GAP advertising with no forms of authentication
-> GATT Profile data being distributed between peripheral and central through a connectionMode
-> GATT data (hr value) being written to a profile attribute (with permissions)
'''

from random import seed, randint
from threading import TIMEOUT_MAX
from datetime import datetime
from xmlrpc.client import Server
from utilities.rand import *
from GAP.peripheral import Peripheral
from GAP.central import Central
from GAT.gat_client import Client
from GAT.gat_server import Server
import simpy.rt
from utilities.rand import randomHeartRateValue
import json
from application.alarm import Alarm

RADIO_TXDISTANCE = 2  # transmissione range of nodes
RADIO_CHANNEL	 = 37  # selected transmission channel
RADIO_LOSSRATE   = 0 # 10% packet loss rate
DEBUG_RADIO  = False #debug messages for the lowlevel radio True or False
DEBUG_SENSOR = True #debug messages for the lowlevel sensors True or False
TIMEOUT_MAX = 100 ### interval length for advertising timeout
TRANSMISSION_Period = 1
DEBUG_ADVERT = False #debug messages for the advertising packet

## our wireless channel class

class Media(object):
    def __init__(self, env, capacity=simpy.core.Infinity):
        self.env = env
        self.capacity = capacity
        self.pipes = []
    
    def put(self, value):
        if not self.pipes:
            raise RuntimeError('There are no pipes')
        events = [store.put(value) for store in self.pipes]
        return self.env.all_of(events)
    
    def get_output_conn(self):
        pipe = simpy.Store(self.env, capacity=self.capacity)
        self.pipes.append(pipe)
        return pipe
    
### the abstracted node for physical layer of out central and peripheral
class Node(object):
    def __init__(self, env, media, id, posx, posy):
        self.env = env
        self.media_in = media.get_output_conn()
        self.media_out = media
        self.channel = RADIO_CHANNEL
        self.id = id
        self.posx= posx
        self.posy = posy
        self.sqnr = 0
        env.process(self.main_p())
        env.process(self.receive_p())
        
    def send(self, ldst, msg_str):
        if DEBUG_RADIO:
            print(self.env.now,':', self.id,' -> ', ldst)
        msg = (self, self.channel, self.id, ldst, str(msg_str))
        self.media_out.put(msg)

    def receive(self, msg):
        if ((msg[3] == 0) or (msg[3] == self.id)) :
            if self.id == msg[2]:
                print("packet cant be sent to itself ignoring")
                return None
            if (DEBUG_RADIO):
                print(self.env.now,':',"Packet Received!")
            return(msg[4])

class CentralNode(Node):
    def __init__(self, env, media, id, posx, posy):
        super().__init__(env, media, id, posx, posy)
        print(self.env.now, ':', self.id, posx, posy)
        self.gapData = Central('Heart Central 1', self.id, 'general')
        self.advertReqConn = False
        self.enableATT = False
        self.advData = None
        self.gattData = Server()
        self.alarm = Alarm("hr-alarm")
    
    def main_p(self):
        while True:
            yield self.env.timeout(randint(500, 1000))
            self.channel = 7
            print(self.env.now,':', self.id ,' central node, waiting for messages')
            if self.advertReqConn:
                connectPkt = self.gapData.createResponsePacket('CONNECT', self.channel, 
                            self.advData['SRC'], self.sqnr,None, self.advData['SRC'])
                payload = connectPkt.payload
                msg_str = json.dumps(payload)
                self.send(payload['LDST'],msg_str)
                
            else:
                print("Central Node Waiting for advertising packet")
                
    def receive_p(self):
        while True:
            msg = yield self.media_in.get()
            msg_str = self.receive(msg)
            if msg_str:
                msg_str = json.loads(msg_str)
                print(self.env.now,':', self.id ,' central node, receiving ' , msg_str, "received by central!")
                if msg_str['TYPE'] == 'advertisingPkt':
                    self.advData = msg_str
                    if self.gapData.discoveryProcedure == 'limited':
                        for deviceId in self.gapData.whitelist:
                            if deviceId == msg_str['SRC']:
                                self.advertReqConn == True
                    else:
                        self.advertReqConn = True
                elif msg_str['TYPE'] == 'GATT':
                    self.advertReqConn = False
                    self.gattData.addToProfile(msg_str['DATA'])
                    recvPkt = self.gapData.createResponsePacket('RECEIVE', self.channel, 
                    self.advData['SRC'], self.sqnr,None, self.advData['SRC'])
                    payload = recvPkt.payload
                    msg_str = json.dumps(payload)
                    self.send(payload['LDST'],msg_str)
                elif msg_str['TYPE'] == 'WRITE':
                    data = msg_str['DATA']
                    uuids = list(data.keys())
                    values = list(data.values())
                    for index in range(len(uuids)):
                        curAtt = self.gattData.getCharValAtt(uuids[index])
                        if curAtt.permissions.write or curAtt.permissions.readAndWrite:
                            curAtt.setValue(values[index])
                            print("WRITING VALUE ", values[index], "to ", uuids[index])
                            if uuids[index] == "0x0015":
                                hrAtt = self.gattData.getCharValAtt("0x0015")
                                hrVal = hrAtt.value
                                self.alarm.checkHR(hrVal)
                                print(self.alarm)
                                
                        else:
                            print("UNABLE TO WRITE, INVALID PERMISSIONS...")
            else:
                print("NO PACKETS RECEIVED AT CENTRAL NODE")
            
class PeripheralNode(Node):
    def __init__(self, env, media, id, posx, posy):
        super().__init__(env, media, id, posx, posy)
        name = 'Heart Moniter1'
        self.join_node = 0
        print(self.env.now,':', self.id ,' Peripheral node, waiting for messages')
        self.gapData = Peripheral(name , id, 'discoverable')
        self.gapData.setConnectEstMode(nonConnectable=False, undirected=True, directed=False)
        newAdVPKT = self.gapData.createAdvertismentPackets(self.id, self.join_node, self.sqnr, None)
        self.gapData.addPackets(newAdVPKT)
        self.connected = False
        
        ### state variable to check if all profile packets
        ### have been send, is triggered based on 
        ### "list index out of range IndexError"
        self.profileSent = False
        self.gattClient = Client(name, id)
        self.gattPkts = self.gattClient.ProfileDirector()
        self.gattPos = 0
        self.packaged = False
        self.channel = 7
        
        
    def main_p(self):
        while True:
            yield self.env.timeout(randint(500, 1000))
            if not self.connected:
                self.sqnr = 0
                msg = self.gapData.ADVPacket.payload
                msg_json = json.dumps( msg ) 
                if (DEBUG_ADVERT):
                    print(self.env.now,':', self.id ,' sending advertisingPkt ' , msg_json)
                self.send(msg['LDST'], msg_json)
            else:
                ### start sending ATT packets
                ### self.package is a check to make sure
                ### the same packet type is not packaged more than once
                ### each new packet getting sent will only be packaged once
                if not self.profileSent:
                    try:
                        if not self.packaged:
                            currAtt = self.gattPkts[self.gattPos]
                            data = self.gattClient.packageATT(currAtt)
                            attPkt = self.gapData.createDataPkt('GATT', self.id, 
                                    self.join_node, self.sqnr, data, self.channel)
                            msg = attPkt.payload
                            msg_json = json.dumps(msg)
                            self.packaged = True
                        self.send(msg['LDST'],msg_json) 
                    except IndexError:
                        self.profileSent = True
                        print("finished sending profile to central!")
                else:
                    print("sending heart rate data...")
                    ### hardcoding uuid of hr attribute
                    ### as this would be known to the peripheral anyway
                    ### see gat_client.py for uuids and handlers of attributes
                    data = {"0x0015": randomHeartRateValue()}
                    attPkt = self.gapData.createDataPkt('WRITE', self.id, self.join_node, 
                                                        self.sqnr, data, self.channel)
                    msg = attPkt.payload
                    print("DEBUG ", msg)
                    print(type(msg))
                    msg_json = json.dumps(msg)
                    self.send(msg['LDST'],msg_json) 
    
    def receive_p(self):
        while True:
            msg = yield self.media_in.get()
            msg_str = self.receive(msg)
            if msg_str:
                print(self.env.now,':', self.id ,' receiving ' , msg_str, "received by peripheral!")
                msg_json = json.loads(msg_str)
                if msg_json['TYPE'] == 'CONNECT':
                    print("PERIPHERAL CONNECTED to central")
                    self.connected = True
                    if self.join_node == 0:
                        print(self.env.now,':', self.id ,' connect req received to join on channel ' , msg_json['CHANNEL'])	
                        self.channel = msg_json['CHANNEL']	
                        print("TWO NODES NOW CONNECTED")
                    else:
                        print(self.env.now,':', self.id ,' advert received but already joined a sink ')
                elif msg_json['TYPE'] == 'RECEIVE':
                    self.gattPos += 1
                    self.packaged = False
                    if self.gattPos > len(self.gattPkts):
                        print("SENDING HEARTRATE DATA")
                else:
                    print("AWAITING CONNECTION REQUEST OR GATT PKT")
# Start of main program
# Initialisation of the random generator
seed(datetime.now())

# Setup of the simulation environment
# factor=0.01 means that one simulation time unit is equal to 0.01 seconds
#env = simpy.Environment()
env = simpy.rt.RealtimeEnvironment(factor=0.01)

# the communication medium 
media = Media(env)

# Nodes placed in a 2 dimensional space
# Node(env, media, node_id, position_x, position_y)
CentralNode(env,media,1,1,0)
PeripheralNode(env,media,2,0,1)

# Duration of the experiment
env.run(until=16000)
### running example of GAPP ble advertising between central/peripheral

################################
'''
peripheral begins to send out packets at a fixed interval
central discovers and authenticates/identifies if device is valid using whitelist or packet filtering

saves receiver address in whitelist..

send a connection request with desired, packet interval and its own uuid, ble address

peripheral sends its name, its uuid through, cutoff time attributes

'''

from random import seed, randint
from threading import TIMEOUT_MAX
from datetime import datetime
from microbit_sim_p1 import DEBUG_ADVERT
from utilities.rand import *
from GAP.peripheral import Peripheral
from GAP.central import Central
import simpy.rt
# import math
import json

RADIO_TXDISTANCE = 2  # transmissione range of nodes
# RADIO_LOSSRATE   = 10 # 10% packet loss rate
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
        ###distance =  math.sqrt(((msg[0].posx - self.posx) ** 2) + ((msg[0].posy - self.posy) ** 2))
        ### query based off of message type
        distance = 0
        print("THIS IS A DEBUG", msg)
        if (msg[1] != self.channel):
            if (DEBUG_RADIO):
                print(self.env.now,':', self.id,' X  (chan) ', msg[2], ' distance ', distance)
            return None

        # elif (distance > RADIO_TXDISTANCE) :
        #     if (DEBUG_RADIO):
        #         print(self.env.now,':', self.id,' X  (range)', msg[2], ' distance ', distance)
        #     return None
        
        # elif msg[4][0] == "advertisingPkt":
        #     if (DEBUG_RADIO):
        #         print(self.env.now,':',"Packet Received!")
        #         return(msg[4])

        # elif (randint(0,100) < RADIO_LOSSRATE) :
        #     if (DEBUG_RADIO):
        #         print(self.env.now,':', self.id,' X  (loss)', msg[2], ' distance ', distance)
        #     return None
        
        else:
            
            if ((msg[3] == 0) or (msg[3] == self.id)) :
                if (DEBUG_RADIO):
                    print(self.env.now,':',"Packet Received!")
                return(msg[4])






class CentralNode(Node):
    def __init__(self, env, media, id, posx, posy):
        super().__init__(env, media, id, posx, posy)
        print(self.env.now, ':', self.id, posx, posy)
        self.gapData = Central('Heart Central 1', self.id, 'general')
        self.connected = False
        self.enableATT = False
    
    def main_p(self):
        while True:
            yield self.env.timeout(TIMEOUT_MAX)
            self.channel = 7
            print(self.env.now,':', self.id ,' central node, waiting for messages')
            if self.connected:
                msg_json = {}
                msg_json['TYPE'] = 'CONNECT'
                msg_json['SRC']  = self.id 
                msg_json['DST']  = 0 
                msg_json['LSRC'] = self.id 
                msg_json['LDST'] = 0 
                msg_json['SEQ']  = self.sqnr
                msg_json['CHANNEL']  = self.id 
                msg_str = json.dumps( msg_json ) 
                self.send(msg_json['LDST'],msg_str)
                # switch to the communication channel
                self.channel = self.id
            else:
                print("Central Node Waiting for advertising packet")
                
    def receive_p(self):
        while True:
            msg = yield self.media_in.get()
            msg_str = self.receive(msg)
            print("DEBUG3 CENTRAL", msg)
            print("DEBUG3 CENTRAL", msg_str)
            print("DEBUG3 CENTRAL", type(msg_str))
            if msg_str:
                print(self.env.now,':', self.id ,' central node, receiving ' , msg_str)
                if msg_str[0] == 'advertisingPkt':
                    if self.gapData.discoveryProcedure == 'limited':
                        for deviceId in self.gapData.whitelist:
                            if deviceId == msg_str['SRC']:
                                self.connected == True
                    else:
                        self.connected = True
                ## elif for other packet type...
            else:
                print("NO PACKETS RECEIVED AT CENTRAL NODE")
            
class PeripheralNode(Node):
    def __init__(self, env, media, id, posx, posy):
        super().__init__(env, media, id, posx, posy)
        self.join_node = 0
        print(self.env.now,':', self.id ,' Peripheral node, waiting for messages')
        self.gapData = Peripheral('Heart Moniter1', id, 'discoverable')
        self.gapData.setConnectEstMode(nonConnectable=False, undirected=True, directed=False)
        newAdVPKT = self.gapData.createAdvertismentPackets(self.id, self.join_node, self.sqnr, None)
        self.gapData.addPackets(newAdVPKT)
        self.connected = False
        
        
    def main_p(self):
        while True:
            if not self.connected:
                # send advertising packet
                yield self.env.timeout(randint(500, 1000))
                self.channel = 7
                self.sqnr += 1

                # print(self.env.now,':', self.id ,' cannot send temperature reading, not joined a central yet')
                ### construct message here and send........
                msg = self.gapData.ADVPacket.payload
                msg_json = json.dumps( msg ) 
                if (DEBUG_ADVERT):
                    print(self.env.now,':', self.id ,' sending advertisingPkt ' , msg_json)
                self.send(msg['LDST'], msg_json)
                self.channel = self.id

    
    
    def receive_p(self):
        while True:
            msg = yield self.media_in.get()
            
            msg_str = self.receive(msg)
            if msg_str:
                print(self.env.now,':', self.id ,' receiving ' , msg_str)
                msg_json = json.loads(msg_str)
                if msg[0] == 'CONNECT':
                    self.connected = True
                    if self.join_node == 0:
                        print(self.env.now,':', self.id ,' advert received to join on channel ' , msg_json['CHANNEL'])
                        self.join_node = msg_json['SRC']	
                        self.channel = msg_json['CHANNEL']	
                    else:
                        print(self.env.now,':', self.id ,' advert received but already joined a sink ')
                else:
                    print("AWAITING CONNECTION REQUEST")
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
env.run(until=6000)
'''
Example shows:
-> whitelists in GAP advertising where a false node gets rejected
'''

from random import seed, randint
from datetime import datetime
from utilities.rand import *
from GAP.peripheral import Peripheral
from GAP.central import Central
import simpy.rt
from utilities.rand import randomHeartRateValue
import json

### simulation tracking imports
import csv
import time
import shutil
import os

### GUI flag only use when working
### alongside GUI
### disable if not using GUI
ENABLE_GUI = False
RADIO_CHANNEL	 = 37  # selected transmission channel
DEBUG_RADIO  = True #debug messages for the lowlevel radio True or False
TIMEOUT_MAX = 100 ### interval length for advertising timeout

### data file being writte top
DATA_FILE = "fullBLE5.csv"
DATA_ARR = []

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
                return None
            if (DEBUG_RADIO):
                print(self.env.now,':',"Packet Received!")
            return(msg[4])
        

class CentralNode(Node):
    def __init__(self, env, media, id, posx, posy, timer=None):
        super().__init__(env, media, id, posx, posy)
        print(self.env.now, ':', self.id, posx, posy)
        self.gapData = Central('Heart Central 1', self.id, 'limited')
        self.gapData.addToWhitelist("hr-sensor-1234")
        self.advertReqConn = False
        self.enableATT = False
        self.advData = None
        
        if ENABLE_GUI:
            self.timer = timer
            
    def main_p(self):
        while True:
            yield self.env.timeout(randint(500, 1000))
            self.channel = 7
            if DEBUG_RADIO:
                print(self.env.now,':', self.id ,' central node, waiting for messages')
            elif ENABLE_GUI:
                curr_time = time.time()
                curr = [curr_time-self.timer, "node_state", str(self.env.now),str(self.id), "Central node, waiting for messages"]
                DATA_ARR.append(curr)
            if self.advertReqConn:
                if self.gapData.discoveryProcedure == "limited":
                    if self.gapData.peripheralData != self.gapData.whitelist[0]:
                        if DEBUG_RADIO:
                            print(self.env.now,':', self.id ,'node id not in whitelist, rejecting')
                        elif ENABLE_GUI:
                            curr_time = time.time()
                            curr = [curr_time-self.timer, "node_state", str(self.env.now),str(self.id), "node id not in whitelist, rejecting"]
                            DATA_ARR.append(curr)
                            
                        terminatePkt = self.gapData.createResponsePacket('TERMINATE', self.channel, 
                                                                            self.advData['SRC'], self.sqnr, self.channel, self.advData['SRC'])
                        payload = terminatePkt.payload
                        msg_str = json.dumps(payload)
                        self.send(payload['LDST'],msg_str)
                        if ENABLE_GUI:
                            curr_time = time.time()
                            curr = [curr_time-self.timer, "pkt_transfer", str(self.env.now),str(self.id), "Send", terminatePkt.payload]
                            DATA_ARR.append(curr)
                    else:
                        connectPkt = self.gapData.createResponsePacket('CONNECT', self.channel, 
                                    self.advData['SRC'], self.sqnr,None, self.advData['SRC'])
                        payload = connectPkt.payload
                        msg_str = json.dumps(payload)
                    
    def receive_p(self):
        while True:
            msg = yield self.media_in.get()
            msg_str = self.receive(msg)
            if msg_str:
                msg_str = json.loads(msg_str)
                if ENABLE_GUI:
                    curr_time = time.time()
                    curr = [curr_time-self.timer, "pkt_transfer", str(self.env.now),str(self.id), "Receive", str(msg_str)]
                    DATA_ARR.append(curr)
                elif DEBUG_RADIO:
                    print(self.env.now,':', self.id ,' central node, receiving ' , msg_str, "received by central!")
                if msg_str['TYPE'] == 'advertisingPkt':
                    self.advData = msg_str
                    self.advertReqConn = True
                    self.gapData.addPeripheralData(msg_str['DATA'])
                    if ENABLE_GUI:
                        curr_time = time.time()
                        curr = [curr_time-self.timer, "node_state", str(self.env.now), str(self.id), "Reading data from advertising pkt"]
                        DATA_ARR.append(curr)
            else:
                if DEBUG_RADIO:
                    print("NO PACKETS RECEIVED AT CENTRAL NODE")
                elif ENABLE_GUI:
                    curr_time = time.time()
                    curr = [curr_time-self.timer, "node_state", str(self.env.now),str(self.id), "No packets received at central node"]
                    DATA_ARR.append(curr)
                    
class PeripheralNode(Node):
    def __init__(self, env, media, id, posx, posy, timer=None):
        super().__init__(env, media, id, posx, posy)
        name = 'Heart Moniter1'
        self.join_node = 0
        print(self.env.now,':', self.id ,' Peripheral node, waiting for messages')
        self.gapData = Peripheral(name , id, 'discoverable')
        self.gapData.setConnectEstMode(nonConnectable=False, undirected=True, directed=False)
        newAdVPKT = self.gapData.createAdvertismentPackets(self.id, self.join_node, self.sqnr, "Attack Sensor")
        self.gapData.addPackets(newAdVPKT)
        self.connected = False
        
        if ENABLE_GUI:
            self.timer = timer
        
    
    
    def main_p(self):
        while True:
            yield self.env.timeout(randint(500, 1000))
            if not self.connected:
                self.sqnr = 0
                msg = self.gapData.ADVPacket.payload
                msg_json = json.dumps( msg ) 
                if ENABLE_GUI:
                    curr_time = time.time()
                    curr = [curr_time - self.timer, "pkt_transfer", str(self.env.now),str(self.id), "Send", str(msg)]
                    DATA_ARR.append(curr)
                    
                self.send(msg['LDST'], msg_json)
                
    def receive_p(self):
        while True:
            msg = yield self.media_in.get()
            msg_str = self.receive(msg)
            if msg_str:
                if DEBUG_RADIO:
                    print(self.env.now,':', self.id ,' receiving ' , msg_str, "received by peripheral!")
                elif ENABLE_GUI:
                    curr_time = time.time()
                    curr = [curr_time-self.timer, "pkt_transfer", str(self.env.now),str(self.id), "Receive", str(msg_str)]
                    DATA_ARR.append(curr)
                msg_json = json.loads(msg_str)
                
                if msg_json['TYPE'] == 'TERMINATE':
                    if ENABLE_GUI:
                        curr_time = time.time()
                        curr = [curr_time-self.timer, "node_state", str(self.env.now),str(self.id), "Terminating connection with central node"]
                        DATA_ARR.append(curr)
                    elif DEBUG_RADIO:
                        print(self.env.now, self.id,"Terminating connection with central node")
                    
                else:
                    if DEBUG_RADIO:
                        print("AWAITING CONNECTION REQUEST OR GATT PKT")
                    elif ENABLE_GUI:
                        curr_time = time.time()
                        curr = [curr_time-self.timer, "node_state", str(self.env.now),str(self.id), "Awaiting connection request or GATT packet"]
                        DATA_ARR.append(curr)


start_time = time.time()
seed(datetime.now())
env = simpy.rt.RealtimeEnvironment(factor=0.01)
media = Media(env)
CentralNode(env,media,1,1,0, start_time)
PeripheralNode(env,media,2,0,1, start_time)
# Duration of the experiment
env.run(until=1700)

if ENABLE_GUI:
    outputFile = "{}.csv".format("BLEWhitelist")
    with open(outputFile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(DATA_ARR)
    shutil.move(outputFile, "{}/simulations/{}".format(os.getcwd(), outputFile))
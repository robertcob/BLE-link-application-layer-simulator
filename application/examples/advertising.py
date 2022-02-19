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
import simpy.rt

RADIO_TXDISTANCE = 2  # transmissione range of nodes
# RADIO_LOSSRATE   = 10 # 10% packet loss rate
RADIO_CHANNEL	 = 37  # selected transmission channel

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
        env.process(self.reveive_p())
        
    def send(self):
        return
    
    def receive(self):
        return
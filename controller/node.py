### the abstracted node for physical layer of out central and peripheral
class Node(object):
    def __init__(self, env, media, id, posx, posy, RADIO_CHANNEL=37, DEBUG_RADIO=True):
        self.env = env
        self.media_in = media.get_output_conn()
        self.media_out = media
        self.channel = RADIO_CHANNEL
        self.id = id
        self.posx= posx
        self.posy = posy
        self.sqnr = 0
        self.DEBUG_RADIO = DEBUG_RADIO
        env.process(self.main_p())
        env.process(self.receive_p())
        
    def send(self, ldst, msg_str):
        if self.DEBUG_RADIO:
            print(self.env.now,':', self.id,' -> ', ldst)
        msg = (self, self.channel, self.id, ldst, str(msg_str))
        self.media_out.put(msg)

    def receive(self, msg):
        if ((msg[3] == 0) or (msg[3] == self.id)) :
            if self.id == msg[2]:
                return None
            if self.DEBUG_RADIO:
                print(self.env.now,':',"Packet Received!")
            return(msg[4])
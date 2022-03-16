class Alarm:
    def __init__(self, name):
        self.name = name
        self.alarmStatus = False
    
    def setAlarm(self, newState):
        self.alarmStatus = newState
    
    def __str__(self):
        statusStr=''
        if self.alarmStatus:
            statusStr = "On"
            return "oh no! looks like your bpm is too high, alarm is now {}".format(statusStr)
        else:
            statusStr = "Off"
            return "Dont worry! your not dead yet, alarm is now {}".format(statusStr)
        

             
class Alarm:
    def __init__(self, name):
        self.name = name
        self.alarmStatus = False
    
    def checkHR(self, hrVal):
        if hrVal > 100 or hrVal < 60:
            self.setAlarm(True)
        else:
            self.setAlarm(False)
    
    def setAlarm(self, newState):
        self.alarmStatus = newState
    
    def __str__(self):
        statusStr=''
        if self.alarmStatus:
            statusStr = "On"
            return "oh no! looks like your bpm is too high, alarm is now {} for {}".format(statusStr, self.name)
        else:
            statusStr = "Off"
            return "Dont worry! your not dead yet, alarm is now {} for {}".format(statusStr, self.name)
        

             
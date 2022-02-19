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
        else:
            statusStr = "Off"
        
        return "Alarm status has been changed, alarm is now {}".format(statusStr)
             
class Log():
    def __init__(self, time, sensor_id, message):
        self.time = time
        self.sensor_id = sensor_id
        self.message = message
    

class LogTracker():
    def __init__(self):
        self.logs = []
    
    def addLog(self, newLog):
        self.logs.append(newLog)
    
    def getLogs(self):
        return self.logs
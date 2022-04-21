import csv
import shutil
import os

class Log():
    def __init__(self, sim_Name, data):
        self.name = sim_Name
        self.data = data
    
    def write(self):
        outputFile = "{}.csv".format(self.name)
        with open(outputFile, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.data)
        shutil.move(outputFile, "{}/simulations/{}".format(os.getcwd(), outputFile))
        

    
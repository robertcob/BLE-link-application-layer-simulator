from tkinter import *

rootWidth = 900
rootHeight =600
root = Tk()
root.title('BLE5 Simulation')
root.resizable(False, False) 
root.geometry('{}x{}'.format(rootWidth, rootHeight))
sensorFrame = Frame(root, width=rootWidth-rootWidth/3, height=rootHeight, bg="white", borderwidth=2, relief="sunken")
simControlFrame = Frame(root, width=rootWidth/3, height=rootHeight, bg="#CFC6C6", borderwidth=2, relief="solid")

sensorFrame.grid(row=0, column=0)
simControlFrame.grid(row=0, column=1)

sensorCanvas = Canvas(sensorFrame, width=rootWidth-rootWidth/3, height=rootHeight, bg="white")
sensorCanvas.pack()

controllerFrame = Frame(simControlFrame, width=rootWidth/3, height=rootHeight/3, bg="orange")
loggerFrame = Frame(simControlFrame,  width=rootWidth/3, height=rootHeight-rootHeight/3, bg="red")
controllerFrame.grid(row=0, column=0)
loggerFrame.grid(row=1, column=0)


### setup elements within controller frame
# cfWidth = int(rootWidth/3)
# cfHeight = int(rootHeight/3)
# controllerLabel = Label(controllerFrame, height=2, bg="green", text="Sim control", font=2)
# conButtonFrame = Frame(controllerFrame, bg="orange")

# timeVar = StringVar()
# conTimeLabel = Label(controllerFrame, width=int(rootWidth/3), height=int(cfHeight/4), bg="#DCDADA",
#  fg="black", text="Time: {}".format(timeVar))

# controllerLabel.pack(side=LEFT, fill= X)
# conButtonFrame.pack(side=LEFT, fill=X)
# print(cfWidth, cfHeight/4)
# conButtonFrame.grid(row=1, column=0)
# conTimeLabel.grid(row=2, column=0)

### add buttons for conButtonFrame


root.update_idletasks() 

### canvas for drawing our grid
### nodes will be positioned on grid

w = sensorCanvas.winfo_width() # Get current width of canvas
h = sensorCanvas.winfo_height() # Get current height of canvas
sensorCanvas.delete('grid_line') # Will only remove the grid_line

### if winfo does not work (always 1)
### forced to set manually
if w == 1:
    w = rootWidth-rootWidth/3
    h = rootHeight

pixel_width = 40
pixel_height = 40
for x in range(0, int(w/20+1)):
    for y in range(0, int(h/20+1)):
        x1 = (x * pixel_width)
        x2 = (x1 + pixel_width)
        y1 = (y * pixel_height)
        y2 = (y1 + pixel_height)
        sensorCanvas.create_rectangle(x1,y1,x2,y2)
sensorCanvas.update()

root.mainloop()




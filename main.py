from tkinter import *

rootWidth = 900
rootHeight =600
root = Tk()
root.title('BLE5 Simulation')
root.resizable(False, False) 
root.geometry('{}x{}'.format(rootWidth, rootHeight))
sensorFrame = Frame(root, width=rootWidth-rootWidth/3, height=rootHeight, bg="red")
simControlFrame = Frame(root, width=rootWidth/3, height=rootHeight, bg="green")

sensorFrame.grid(row=0, column=0)
simControlFrame.grid(row=0, column=1)

sensorCanvas = Canvas(sensorFrame, width=rootWidth-rootWidth/3, height=rootHeight, bg="white")
sensorCanvas.pack()
root.update_idletasks() 

### canvas for drawing our grid
### nodes will be positioned on grid

w = sensorCanvas.winfo_width() # Get current width of canvas
h = sensorCanvas.winfo_height() # Get current height of canvas
print(w, h)
sensorCanvas.delete('grid_line') # Will only remove the grid_line

pixel_width = 40
pixel_height = 40
for x in range(0, int(sensorCanvas.winfo_width()/20+1)):
    for y in range(0, int(sensorCanvas.winfo_height()/20+1)):
        x1 = (x * pixel_width)
        x2 = (x1 + pixel_width)
        y1 = (y * pixel_height)
        y2 = (y1 + pixel_height)
        sensorCanvas.create_rectangle(x1,y1,x2,y2)
sensorCanvas.update()




root.mainloop()




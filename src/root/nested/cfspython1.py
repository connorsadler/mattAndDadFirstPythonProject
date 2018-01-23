from tkinter import font
from tkinter import *

TIMESTEP = 5

print("hello world\n")

class MyClass():
    def __init__(self):
        print("MyClass is being constructed\n")
    
    def sayHello(self):
        print("hello hello hello!")
    
    def drawLines(self):
        self.window = Tk()
        self.window.title("Circle")
        self.canvas = Canvas(self.window, width = 1200, height = 1200, borderwidth = 0, highlightthickness = 0, bg = "grey")
        self.canvas.grid()
        self.window.after(TIMESTEP,self.moveit)
        
        self.currentX = 0
        self.currentY = 0
        self.currentText = self.canvas.create_text(200,1000, text = "todo!!!!!!!!!!!", font = font.Font(family='Helvetica', size=36, weight='bold'))
        
        self.mode = 0 # MovingY
        
        self.canvas.mainloop()
        
    def moveit(self):
        
        if (self.mode == 0):
            # Moving Y
            self.canvas.create_line(0, self.currentY, 1200, self.currentY)
            self.currentY += 10
            if (self.currentY > 1200):
                self.mode += 1
        elif (self.mode == 1):
            # Moving X
            self.canvas.create_line(self.currentX, 0, self.currentX, 1200)
            self.currentX += 10
            if (self.currentX > 1200):
                self.mode += 1
        else:
            print("Doing nothing")
        
        self.canvas.itemconfigure(self.currentText, text=str(self.currentX) + " / " + str(self.currentY))
        
        self.window.after(TIMESTEP,self.moveit)
         
        
x = MyClass()
x.sayHello()
x.drawLines()
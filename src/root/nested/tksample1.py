from tkinter import *

class Circle:
    def __init__(self, radius, points = 0, xcoordinate = 0, ycoordinate = 0):    
        self.radius = radius
        self.points = points
        self.color = "red"
        self.xcoordinate = xcoordinate
        self.ycoordinate = ycoordinate

class World:
    def __init__(self):
        self.constructor = Tk()
        self.constructor.title("Circle")
        self.canvas = Canvas(self.constructor, width = 200, height = 200,     borderwidth = 0, highlightthickness = 0, bg = "black")
        self.canvas.grid()
        #self.constructor.mainloop()

    def drawPlayer(self):
        player = Circle(50)
        self.canvas.create_oval(player.xcoordinate - player.radius, player.ycoordinate - player.radius, player.xcoordinate + player.radius, player.ycoordinate + player.radius, fill = player.color)

c = World()
c.drawPlayer()
c.canvas.mainloop()
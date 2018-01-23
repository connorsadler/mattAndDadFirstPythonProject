import tkinter
import time
import random
from tkinter import Tk, Canvas, Frame, BOTH

UP = u'\uf700'
DOWN = u'\uf701'
LEFT = u"\uf702"
RIGHT = u'\uf703'
TIMESTEP = 50
WIDTH = 300
HEIGHT = 300
colours = ['blue','red','pink','yellow','cyan','magenta','green']

class game(object):
    def __init__(self):
        
        self.window = tkinter.Tk()
        self.canvas = Canvas(self.window, width = WIDTH, height = HEIGHT)
        self.canvas.pack()
        self.leader = Rect(self.canvas,50,50,60,60,'red',10,0)
        self.rect2 = Rect(self.canvas,40,50,50,60,'blue',10,0)
        self.test1 = Rect(self.canvas,100,100,110,110,'pink',0,0)
        self.followers = [ self.rect2, self.test1, Rect(self.canvas,200,200,210,210,'yellow',0,0) ]
        

    def moveit(self):
        # moves the leader and the followers follow!
        prevpos = (self.leader.coords()[0],self.leader.coords()[1])
        self.leader.move(self.leader.getvel()[0],self.leader.getvel()[1])

        for rect in self.followers:
            x = (rect.coords()[0],rect.coords()[1])
            self.moveto(rect,prevpos)
            prevpos = x

        self.eatapple()
        self.selfcollision()
        
        # CFS crashing??
        #self.throughwalls()

        self.window.after(TIMESTEP,self.moveit)

    def moveto(self,box1,pos):
        #moves box1 to pos
        box1.move(pos[0]-box1.coords()[0],pos[1]-box1.coords()[1])

    def makeapple(self):
        #This randomly puts an apple on the canvas
        x1 = random.randrange(0,WIDTH,10)
        y1 = random.randrange(0,HEIGHT,10)
        self.apple = Rect(self.canvas,x1,y1,x1+10,y1+10, 'purple',0,0)

    def eatapple(self):
        #This check for eating apple, if eaten, creates new apple and grows the snake
        if self.leader.coords() == self.apple.coords():
            self.canvas.delete(self.apple.id)
            self.makeapple()
            self.grow()

    def grow(self):
        print("grow")
        # grows the snake by appending a rectangle to the followers list
        x1 = self.followers[-1].coords()[0]
        y1 = self.followers[-1].coords()[1]
        x2 = self.followers[-1].coords()[2]
        y2 = self.followers[-1].coords()[3]
        self.followers.append(Rect(self.canvas,x1,y1,x2,y2,colours[random.randint(0,len(colours)-1)],0,0))

    def selfcollision(self):
        # This will check for collision with itself
        for follower in self.followers:
            if self.leader.coords() == follower.coords():
                print("You lose!")
        # CFS What the heck!!
        #self.window.destroy()

    def throughwalls(self):
        # This will put the snake on the klein bottle geometry!
        x1,y1 = self.leader.coords()
        # ,x2,y2
        if x1>=WIDTH:
            self.moveto(self.leader,(0,HEIGHT-y1))
        if x1<0:
            self.moveto(self.leader,(WIDTH,HEIGHT-y1))
        if y1>= HEIGHT:
            self.moveto(self.leader,(x1,0))
        if y1< 0:
            self.moveto(self.leader,(x1,HEIGHT))

    def keyup(self,event):
        if self.leader.velocity != (0,10):
            self.leader.velocity=(0,-10)
        #print "UP!"
    def keydown(self,event):
        if self.leader.velocity != (0,-10):
            self.leader.velocity = (0,10)
        #print "DOWN!"
    def keyright(self,event):
        if self.leader.velocity != (-10,0):
            self.leader.velocity = (10,0)
    def keyleft(self,event):
        if self.leader.velocity != (10,0):
            self.leader.velocity = (-10,0)


    def mainloop(self):
        #self.window.vi
        self.window.bind("<Key-Up>",self.keyup)
        self.window.bind("<Key-Down>",self.keydown)
        self.window.bind("<Key-Left>",self.keyleft)
        self.window.bind("<Key-Right>",self.keyright)
        
        # CFS this causes the window to show...
        #self.window.mainloop()
        
        self.makeapple()
        
        # CFS removed moveit and replaced with a future call to move after 50 ms
        #self.moveit()
        self.window.after(TIMESTEP,self.moveit)
        
        self.window.mainloop()

class Rect(object):
    def __init__(self,canvas,x1,y1,x2,y2,color,vx,vy):
        self.canvas = canvas
        self.velocity = vx,vy
        self.id = self.canvas.create_rectangle(x1,y1,x2,y2,fill = color)
        print("id: " + str(self.id))

    def getvel(self):
        return self.velocity

    def coords(self):
        return self.canvas.coords(self.id)
    #self.root = Tkin
    def move(self,vx,vy):
        self.canvas.move(self.id,vx,vy)

g = game()
g.mainloop()
#while True:
    #ans=input("Another game? (y/n) ")
    #if ans== 'n':
        #break
    #elif ans == 'y':
        #canvas = game()
        #canvas.mainloop()
    #else:
        #print("What was that?")
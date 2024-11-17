# -*- coding: utf-8 -*-
import sys
major=sys.version_info.major
minor=sys.version_info.minor
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 and minor==6 :
    import tkinter as tk
    from tkinter import filedialog
else :
    if __name__ == "__main__" :
        print("Your python version is : ",major,minor)
        print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 

from math import pi,sin,radians
sys.path.append('..')
# print(sys.path)

class Screen :
    def __init__(self,parent,a=0.5,f=1.0,p=0.0,harmonics=7,bg="white"):
        self.parent=parent
        self.mag,self.freq,self.phase,self.harmonics=a,f,p,harmonics
        self.canvas=tk.Canvas(parent,bg=bg)
        self.x,self.y,self.radius=0,0,10
        self.samples=1000
        self.signal=[]

        self.spot=self.canvas.create_oval(
            self.x-self.radius,self.y-self.radius,
            self.x+self.radius,self.y+self.radius,
            fill='blue',outline='black',tags="spot")

        self.width=int(self.canvas.cget("width"))
        self.height=int(self.canvas.cget("height"))
        
    def get_canvas(self) :
        return self.canvas
    def get_signal(self) :
        return self.signal

    def vibration(self,t):
        a,f,p,harmonics=self.mag,self.freq,self.phase,self.harmonics
        p=radians(p)
        sum=a*sin(2*pi*f*t-p)
        for h in range(2,harmonics+1) :
            if h%2==1 :
                sum=sum+(a*1.0/h)*sin(2*pi*(f*h)*t-p)
        return sum
    def generate(self,period=2):
        del self.signal[0:]
        echantillons=range(int(self.samples)+1)
        Tech=period/self.samples
        for t in echantillons :
            self.signal.append([t*Tech,self.vibration(t*Tech)])
        return self.signal

    def plot_signal(self,signal,name="X",color="red",erase=False):
        width,height=self.width,self.height
        if signal and len(signal)>1:
            self.canvas.delete(name)
            plot=[(x*width, height/2*(y+1)) for (x,y) in signal]
            self.canvas.create_line(plot,fill=color,smooth=1,width=3,tags=name)

    def animate_spot(self,canvas,signal,i=0):
        width,height=int(canvas.cget("width")),int(canvas.cget("height"))
##        width,height=canvas.winfo_width(),canvas.winfo_height()
##        width,height=self.width,self.height
        msec=5
        if i==len(signal) :
            i=0
        x,y=signal[i][0]*width, height/2*(signal[i][1]+1)
        canvas.coords(self.spot,x,y,x+self.radius,y+self.radius)
        after_id=self.parent.after(msec, self.animate_spot,canvas,signal,i+1)
        return after_id
    def packing(self) :
        self.canvas.pack()

if  __name__ == "__main__" : 
    mw=tk.Tk()
    screen=Screen(mw)
    screen.packing()
    screen.generate()
    screen.plot_signal(screen.get_signal())
    screen.animate_spot(screen.get_canvas(),screen.get_signal())
    
    mw.mainloop()


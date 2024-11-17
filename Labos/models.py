# coding: utf-8
import sys
major=sys.version_info.major
minor=sys.version_info.minor
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 :
    import tkinter as tk
    from tkinter import filedialog
else :
    if __name__ == "__main__" :
        print("Your python version is : ",major,minor)
        print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 

from math import pi,sin
from observer import Subject

class Generator(Subject) :
    def __init__(self,name="X",mag=1.0,freq=1.0,phase=0,harmonics=1,samples=100,include_even=True,include_odd=True) :
        super().__init__()
        self.name=name
        self.mag,self.freq,self.phase=mag,freq,phase
        self.harmonics=harmonics
        self.include_even = include_even
        self.include_odd = include_odd
        self.signal=[]
        self.samples=samples
    
    def get_name(self) :
        return self.name
    def set_name(self,name) :
        self.name=name
    
    def get_frequency(self) :
        return self.freq
    def set_frequency(self,freq) :
        self.freq=freq
        self.generate()

    def get_mag(self):
        return self.mag
    def set_mag(self, mag):
        self.mag = mag
        self.generate()  

    def get_phase(self):
        return self.phase
    def set_phase(self, phase):
        self.phase = phase
        self.generate() 
     
    def get_harmonics(self):
        return self.harmonics
    
    def set_harmonics(self, harmonics):
        self.harmonics = harmonics
        self.generate()

    def get_include_even(self):
        return self.include_even
    def set_include_even(self, include_even):
        self.include_even = include_even
        self.generate()

    def get_include_odd(self):
        return self.include_odd
    def set_include_odd(self, include_odd):
        self.include_odd = include_odd
        self.generate()

    def get_signal(self) :
        return self.signal
    def set_signal(self,signal) :
        self.signal=signal

    def get_samples(self) :
        return self.samples
    def set_samples(self,samples) :
        self.samples=samples
        self.generate()

    def vibration(self,t):
        m,f,p=self.mag,self.freq,self.phase
        harmo=int(self.harmonics)
        sigma=0.0
        for h in range(1, harmo + 1):
            if (h%2==0 and self.include_even) or (h%2==1 and self.include_odd):
                sigma += (m / h) * sin(2 * pi * (f * h) * t - p)
        return sigma
    
    def generate(self,period=1):
        self.signal.clear()
        samples=range(int(self.samples)+1)
        psamples = period/self.samples
        for t in samples :
            self.signal.append([t*psamples,self.vibration(t*psamples)])
        self.notify()     
        return self.signal

if   __name__ == "__main__" :
   root=tk.Tk()
   model=Generator()
   model.set_samples(10)
   print(model.generate())
   model.set_samples(20)
   print(model.generate())



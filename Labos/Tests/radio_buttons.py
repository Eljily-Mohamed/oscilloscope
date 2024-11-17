# coding: utf-8
import sys
import math

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

class MainWindow :
    def __init__(self,parent,bg="white",width=600,height=300):
        self.parent=parent
        self.bg=bg
        self.width,self.height=width,height
        self.gui()
        self.actions_binding()

    def gui(self) :
        print("Mainwindow.gui()")
        self.frame=tk.LabelFrame(self.parent,text="X")
        self.var_radio=tk.IntVar()
        self.var_radio.set(1)
        self.rb_odd=tk.Radiobutton(self.frame,text="Odd",variable=self.var_radio,value=1)
        self.rb_even=tk.Radiobutton(self.frame,text="Even",variable=self.var_radio,value=2)

    def actions_binding(self) :
        print("Mainwindow.actions_binding()")
        self.rb_odd.bind("<Button-1>", lambda event,data="ODD" : self.on_radiobutton_action(event,data))
        self.rb_even.bind("<Button-1>", lambda event,data="EVEN" : self.on_radiobutton_action(event,data))
 
    def on_radiobutton_action(self,event,data):
        print("Mainwindow.on_radiobutton_action()")
        print(data)
        val=event.widget.cget("value")
        print(val)
 
    def layout(self) :
        print("Mainwindow.layout()")
        self.frame.pack()
        self.rb_even.pack()
        self.rb_odd.pack()

if   __name__ == "__main__" :
    root=tk.Tk()

    mw=MainWindow(root)
    mw.layout()
    root.mainloop()


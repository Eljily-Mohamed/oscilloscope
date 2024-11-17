from tkinter  import Tk,LabelFrame, Label,Button

class MainWindow :
    def __init__(self,parent) :
        self.parent=parent
        self.gui()
        self.actions_binding()

    def gui(self) :
        self.hello=Label(self.parent, text="Hello World !",fg="blue")
        self.frame=LabelFrame(self.parent,text="Callbacks")

        self.btn1=Button(self.frame, text="1", fg="red")
        self.btn2=Button(self.frame, text="2", fg="green")
        self.btn3=Button(self.frame, text="3", fg="blue")

    def actions_binding(self) :
        # nb_button=self.btn.cget("text")
        # print("actions_binding(self)",nb_button)

        self.btn1.bind("<Button-1>",self.on_clicked_1("button1"))
        self.btn2.bind("<Button-1>",self.on_clicked_2)
        self.btn3.bind("<Button-1>",lambda event,button=self.btn1 : self.on_clicked_3(event,button))

    def on_clicked_1(self,nb_button) :
        print("on_clicked_1(self,nb_button)")
        print("button : ",nb_button)

    def on_clicked_2(self,event) :
        print("on_clicked_2(self,event)",event)
        nb_button=event.widget.cget("text")
        event.widget.configure(text="You clicked on me :"+nb_button)

    def on_clicked_3(self,event,button) :
        print("on_clicked_3(self,event,nb_button)")
        widget_text=event.widget.cget("text")
        button.configure(text="You clicked on him : "+widget_text)
        widget_fg=event.widget.cget("fg")
        button.configure(fg=widget_fg)
    


    def layout(self) :
        self.hello.pack()
        self.frame.pack(side="left",expand=1,fill="x")
        self.btn1.pack(side="left",expand=1,fill="x")
        self.btn2.pack(side="left",expand=1,fill="x")
        self.btn3.pack(side="left",expand=1,fill="x")

if __name__ =="__main__" :
    root=Tk()
    mw=MainWindow(root)
    mw.layout()
    root.mainloop()

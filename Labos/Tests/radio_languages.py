# https://tk-tutorial.readthedocs.io/en/latest/check/check.html

import tkinter as tk

root = tk.Tk()

var_radio = tk.IntVar()
var_radio.set(1)

def on_command_action(data,donnee):
    print("--- languages ---")
    print(data,donnee)   
    if var_radio.get() == 1 :
        print("---> You speak English")
    elif  var_radio.get() == 2 :
       print("---> Du sprichst Deutsch !")
    elif  var_radio.get() == 3 :
        if data=="Bonjour " :
            print("---> Tu parles Français")
        elif data=="Salut " :
            print("---> Tu parles Français plus ou moins bien")
    else :
        print("---> Je ne comprends pas ta langue !")
       
frame_radio = tk.LabelFrame(root,text="Radio",width=30,height=70)

radio1=tk.Radiobutton(frame_radio, text='English', variable=var_radio, value=1, command=lambda : on_command_action("Good Morning ","my Friend !"))
radio2=tk.Radiobutton(frame_radio, text='Deutsch',  variable=var_radio, value=2, command=lambda : on_command_action("Guten Tag ","mein Freund !"))
radio3=tk.Radiobutton(frame_radio, text='Français',  variable=var_radio, value=3, command=lambda : on_command_action("Bonjour ","mon Ami !"))
radio4=tk.Radiobutton(frame_radio, text='Familier',  variable=var_radio, value=3, command=lambda : on_command_action("Salut ","mon pote !"))
# radio5=tk.Radiobutton(frame_radio, text='Inconnu',  variable=var_radio, value=4, command=lambda : on_radio_command_action("Slt ","Cdt !"))

def on_bind_action(event,data,donnee):
    print(event)
    print(data,donnee)   
    print("---> Je ne comprends pas ta langue !")

radio5=tk.Radiobutton(frame_radio, text='Inconnu',variable=var_radio, value=4)
radio5.bind("<Button-1>", lambda event,data="Slt",donnee="Cdlt !" : on_bind_action(event,data,donnee))
# radio5.bind("<Motion>", lambda event,data="Slt",donnee="Cdlt !" : on_bind_action(event,data,donnee))

frame_radio.pack(expand=1,fill="x")
radio1.pack(anchor="w")
radio2.pack(anchor="w")
radio3.pack(anchor="w")
radio4.pack(anchor="w")
radio5.pack(anchor="e")

root.mainloop()

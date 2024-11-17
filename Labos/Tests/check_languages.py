# https://tk-tutorial.readthedocs.io/en/latest/check/check.html
import tkinter as tk

root = tk.Tk()

english = tk.IntVar(value=0)          # offvalue=0, onvalue=1
german = tk.StringVar(value='schwach')   # offvalue='schwach', onvalue='1'
french = tk.StringVar(value='0')      # offvalue='0', onvalue='couramment', 


# def on_keypad_action(data,donnee):
#     print("--- languages ---")
#     print(data,donnee)   
#     print('English :',data, english.get())
#     if english.get() == 0 :
#         print("speak english juste a little")
#     print('German : ', german.get())
#     if german.get() == 'schwach' :
#         print("Ich spreche Deutsch ein wenig ")     
#     print('French :', french.get())
#     if french.get() == '0' :
#         print("Je parle un peu  Français ")     

# btn1=tk.Checkbutton(root, text='English', variable=english, command=lambda : on_keypad_action("English","Good Morning my Friend!"))
# btn2=tk.Checkbutton(root, text='German', variable=german, offvalue='schwach', command=lambda : on_keypad_action("Guten Tag !","mein Freund"))
# btn3=tk.Checkbutton(root, text='French', variable=french, onvalue='couramment', command=lambda : on_keypad_action("Bonjour !","mon Ami"))

# def on_keypad_action(event) :
#     print("on_keypad_action(self,event")
#     print('--- languages ---')
#     print('English', english.get())
#     print('German', german.get())
#     print('French', french.get())

# btn1=tk.Checkbutton(root, text='English', variable=english)
# btn2=tk.Checkbutton(root, text='German', variable=german, offvalue='barely')
# btn3=tk.Checkbutton(root, text='French', variable=french, onvalue='fluent')

# btn1.bind("<Button-1>",on_keypad_action)
# btn2.bind("<Button-1>",on_keypad_action)
# btn3.bind("<Button-1>",on_keypad_action)


english = tk.IntVar(value=0)            # offvalue=0, onvalue=1
german = tk.StringVar(value='faible')  # offvalue='faible', onvalue='1'
french = tk.StringVar(value='0')        # offvalue='0', onvalue='couramment', 
unknown=tk.StringVar(value='kesaco')    # offvalue='kesaco', onvalue='comprend pas', 
var_check= tk.IntVar()
var_check.set(1)

def on_command_action(data,donnee):
    print("--- languages ---")
    print(data,donnee)   
    if english.get() == 1 :
        print("---> You speak English")
    if german.get() == '1' :
       print("---> Du sprichst Deutsch !")
    if french.get() ==  'couramment':
        print("---> Tu parles Français")

frame_check = tk.LabelFrame(root,text="Check",width=30,height=70)

check1=tk.Checkbutton(frame_check, text='English',  variable=english, command=lambda : on_command_action("Good Morning ","my Friend !"))
check2=tk.Checkbutton(frame_check, text='Deutsch',  variable=german,  offvalue='faible', command=lambda : on_command_action("Guten Tag ","mein Freund !"))
check3=tk.Checkbutton(frame_check, text='Français', variable=french,  onvalue='couramment',command=lambda : on_command_action("Bonjour ","mon Ami !"))
check4=tk.Checkbutton(frame_check, text='Familier', variable=french, command=lambda : on_command_action("Salut ","mon pote !"))
# check5=tk.Checkbutton(frame_check, text='Inconnu',  variable=unknown, onvalue='comprend pas', command=lambda : on_command_action("Slt ","Cdt !"))

def on_bind_action(event,data,donnee):
    print(event)
    print(data,donnee)   
    print("---> Tu parles quelle langue ?")

check5=tk.Checkbutton(frame_check, text='Inconnu',variable=unknown)
check5.bind("<Button-1>", lambda event,data="Slt",donnee="Cdlt !" : on_bind_action(event,data,donnee))
# check5.bind("<Motion>", lambda event,data="Slt",donnee="Cdlt !" : on_bind_action(event,data,donnee))


frame_check.pack(expand=1,fill="x")
check1.pack(anchor="w")
check2.pack(anchor="w")
check3.pack(anchor="w")
check4.pack(anchor="w")
check5.pack(anchor="e")

root.mainloop()

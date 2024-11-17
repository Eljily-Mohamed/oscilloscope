# coding: utf-8
import sys
import json
from tkinter import messagebox


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

from models import Generator
from views import Screen
from controllers import Controls

def menu_help(menubar):
    menu = tk.Menu(menubar)
    menu.add_command(label="About Us", command=lambda: on_help_actions("About Us"))
    menu.add_command(label="About Tk", command=lambda: on_help_actions("About Tk"))
    menu.add_command(label="About Python", command=lambda: on_help_actions("About Python"))
    menubar.add_cascade(label="Help", menu=menu)

# Help actions
def on_help_actions(action):
    if action == "About Us":
        messagebox.showinfo("About Us", "Designers:\n EL JILY Mohamed,\n CHOUBRI Douae\nEmail:\n m3eljily@enib.fr,\n d3choubr@enib.fr")
    elif action == "About Tk":
        messagebox.showinfo("About Tk", "TkInter is a GUI toolkit for Python, developed by Fredrik Lundh.")
    elif action == "About Python":
        messagebox.showinfo("About Python", "Python is a high-level programming language developed by Guido van Rossum.")
    else:
        print(f"Unrecognized help action: {action}")

def create_menu(root, control_x, control_y):
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)

    file_menu.add_command(label="Open", command=lambda: control_x.open_combined_data(control_y))
    file_menu.add_command(label="Save", command=lambda: control_x.save_combined_data(control_x, control_y))  
    file_menu.add_command(label="Save Image", command=control_x.save_image)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)
    menu_help(menu_bar)
    
    root.config(menu=menu_bar)

def update_display():
    view_signals.update_display_options(show_x.get(), show_y.get())

def toggle_xy_display():
    if show_xy.get():
        open_xy_window()
    else:
        if hasattr(root, 'xy_window') and root.xy_window.winfo_exists():
            root.xy_window.destroy()

def open_xy_window():
    xy_window = tk.Toplevel(root)
    xy_window.title("Signal X-Y")
     # View for X and Y signal
    fram_xy = tk.LabelFrame(xy_window, text="Signal Display")
    view_xy = Screen(fram_xy, show_slider=False,signal1=signal_x,signal2=signal_y)

    fram_xy.pack(expand=1, fill="both", padx=6)

    # Initialize view with both signals
    view_xy.layout()
    view_xy.plot_sum_signals(signal_x,signal_y)

import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("CAI 2024 A : TkInter")
    # ================== CHECKBOX FRAME ==================
    checkbox_frame = tk.Frame(root)
    checkbox_frame.pack(fill="x", padx=6, pady=5)

    # Cases à cocher pour "Afficher X", "Afficher Y" et "Afficher X-Y"
    show_x = tk.BooleanVar(value=True)
    show_y = tk.BooleanVar(value=True)
    show_xy = tk.BooleanVar(value=False)

    checkbox_show_x = tk.Checkbutton(checkbox_frame, text="X", variable=show_x, command=update_display)
    checkbox_show_y = tk.Checkbutton(checkbox_frame, text="Y", variable=show_y, command=update_display)
    checkbox_show_xy = tk.Checkbutton(checkbox_frame, text="X-Y", variable=show_xy, command=toggle_xy_display)

    checkbox_show_x.pack(side="left", padx=5)
    checkbox_show_y.pack(side="left", padx=5)
    checkbox_show_xy.pack(side="left", padx=5)


    # ================== FRAME 1 ==================
    # Model for X signal
    model_x = Generator()  # X signal
    model_x.set_samples(100)
    model_x.set_frequency(2)
    signal_x = model_x.generate()

    # Model for Y signal
    model_y = Generator(name="Y")  # Y signal
    model_y.set_samples(100)
    model_y.set_frequency(5)
    signal_y = model_y.generate()

    # View for X and Y signal
    frame_signals = tk.LabelFrame(root, text="Signal Display")
    view_signals = Screen(frame_signals)
    frame_signals.pack(expand=1, fill="both", padx=6)

    # Initialize view with both signals
    view_signals.update(model_x)
    view_signals.update(model_y)
    view_signals.layout()
    # Animate both signals in the same view
    view_signals.animate_spot(view_signals.canvas, signal_x, model_x.get_name())
    view_signals.animate_spot(view_signals.canvas, signal_y, model_y.get_name())

    # ================== FRAME 2 ==================
    # Main control frame
    frame_control = tk.Frame(root)
    frame_control.pack(expand=1, fill="both", padx=30, side="top")

    # Controllers for X and Y signals
    control_x = Controls(model_x, view_signals)
    control_y = Controls(model_y, view_signals)

    # Layout controls
    control_x.layout(side="left")
    control_y.layout(side="right")

    # Menubar
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    create_menu(root, control_x, control_y)

    # Event loop
    root.mainloop()
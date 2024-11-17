# coding: utf-8
import sys

major = sys.version_info.major
minor = sys.version_info.minor

# Import based on Python version
if major == 2 and minor == 7:
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major == 3:
    import tkinter as tk
    from tkinter import filedialog
else:
    if __name__ == "__main__":
        print("Your Python version is:", major, minor)
        print("... I guess it will work!")
    import tkinter as tk
    from tkinter import filedialog

from models import Generator
from observer import Observer

class Screen(Observer):
    def __init__(self, parent, bg="white", width=600, height=300,show_slider=True,signal1=None,signal2=None):
        self.parent = parent
        self.bg = bg
        self.tiles = 4
        self.signals = {}
        self.spots = {}
        self.width, self.height = width, height
        self.signal1=signal1
        self.signal2=signal2
        self.show_x = True
        self.show_y = True 
        self.show_slider=show_slider
        self.msec = 50
        self.gui()
        self.actions_binding()

    def get_parent(self):
        return self.parent
    
    def get_canvas(self):
        return self.canvas

    def set_parent(self, parent):
        self.parent = parent

    def get_tiles(self):
        return self.tiles

    def set_tiles(self, tiles):
        self.tiles = tiles
        if self.canvas.find_withtag("grid"):
            self.canvas.delete("grid")
        self.create_grid()

    def gui(self):
        self.canvas = tk.Canvas(self.parent, bg=self.bg, width=self.width, height=self.height)
        self.create_grid()

        if self.show_slider :
            self.speed_slider = tk.Scale(self.parent, from_=10, to=200, orient="horizontal", label="Speed (ms)", command=self.update_speed)
            self.speed_slider.set(self.msec)  # Set the initial speed
            self.speed_slider.pack(side="bottom")
            

    def update_speed(self, value):
        self.msec = int(value)

    def actions_binding(self):
        print("Screen.actions_binding()")
        self.canvas.bind("<Configure>", self.resize)
    
    def animate(self,name):
        self.x,self.y,self.radius=5,5,10
        color = "yellow" if name == "X" else "green"
        self.spots[name]=self.canvas.create_oval(
            self.x-self.radius,self.y-self.radius,
            self.x+self.radius,self.y+self.radius,
            fill=color,outline='black',tags="spot")

    def update_display_options(self, show_x, show_y):
        self.show_x = show_x
        self.show_y = show_y
        self.canvas.delete("X")
        self.canvas.delete("Y")
        self.canvas.delete("spot")
        if self.show_x:
            self.plot_signal("X")
            self.animate("X")
        if self.show_y:
            self.plot_signal("Y")
            self.animate("Y")


    def update(self, subject):
        if subject:
            name = subject.get_name()
            signal = subject.get_signal()
            if signal:
                if name not in self.signals.keys():
                    self.signals[name] = signal
                    self.animate(name)
                else:
                    self.canvas.delete(name)
                    self.signals[name] = signal

                # Affichage conditionnel basé sur les cases à cocher
                if name == "X" and self.show_x:
                    self.plot_signal(name)
                elif name == "Y" and self.show_y:
                    self.plot_signal(name)
            else:
                print("No signal for subject:", name)
        else:
            print("No subject to observe")

    def plot_signal(self, name):
        if name in self.signals.keys():
            w, h = self.width, self.height
            if self.signals[name] and len(self.signals[name]) > 1:
                plot = [(x * w, h /2*(y+1)) for (x, y) in self.signals[name]]
                color = "red" if name == "X" else "blue"
                self.canvas.create_line(plot, fill=color, smooth=1, width=3, tags=name)
        else:
            print("No signal to plot with name:", name)
        return
    
    
    def plot_sum_signals(self, signal1, signal2, sum_name="Sum"):
        if len(signal1) == len(signal2):
            sum_signal = [(y1,y2) for ((x, y1), (x, y2)) in zip(signal1, signal2)]
            self.signals[sum_name] = sum_signal  
            w, h = self.width, self.height

            x_min = min([x for x, _ in sum_signal])
            x_max = max([x for x, _ in sum_signal])
            y_min = min([y for _, y in sum_signal])
            y_max = max([y for _, y in sum_signal])

            x_range = max(x_max - x_min, 1)
            y_range = max(y_max - y_min, 1)

            plot = [
                (
                    w * (x - x_min) / x_range,
                    h - h * (y - y_min) / y_range
                )
                for (x, y) in sum_signal
            ]

            # Plot the signal
            color = "red"
            self.canvas.create_line(plot, fill=color, smooth=1, width=3, tags=sum_name)
        else:
            print("Les signaux n'ont pas la même longueur.")
            return



    def animate_spot(self, canvas, signal, signal_name, i=0):
        width, height = self.width, self.height
        if i == len(signal):
            i = 0
        x, y = signal[i][0] * width, height / 2 * (signal[i][1] + 1)
        if signal_name in self.spots:
            canvas.coords(self.spots[signal_name], x, y, x + self.radius, y + self.radius)
        after_id = self.parent.after(self.msec, self.animate_spot, canvas, signal, signal_name, i + 1)
        return after_id
    
    def create_grid(self):
        tile_x = self.width / self.tiles
        for t in range(1, self.tiles + 1):
            x = t * tile_x
            self.canvas.create_line(x, 0, x, self.height, tags="grid")
            self.canvas.create_line(x, self.height / 2 - 10, x, self.height / 2 + 10, width=3, tags="grid")
        tile_y = self.height / self.tiles
        for t in range(1, self.tiles + 1):
            y = t * tile_y
            self.canvas.create_line(0, y, self.width, y, tags="grid")
            self.canvas.create_line(self.width / 2 - 10, y, self.width / 2 + 10, y, width=3, tags="grid")

    def resize(self, event):
        print("resize(self, event)", event.width, event.height)
        self.width, self.height = event.width, event.height
        if "Sum" not in self.signals.keys():
            self.canvas.delete("grid")
            self.create_grid()
            self.canvas.delete("X")
            self.canvas.delete("Y")
            self.plot_signal("X")
            self.plot_signal("Y")
        else:
            self.canvas.delete("grid")
            self.create_grid()
            self.canvas.delete("Sum")
            self.plot_sum_signals(self.signal1, self.signal2, sum_name="Sum")
            pass   

    def layout(self):
        self.canvas.pack(side="top", fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    root.option_readfile("main.opt")
    model = Generator()

    view = Screen(root)
    model.attach(view)
    model.generate()
    view.layout()


    root.mainloop()

# coding: utf-8
import sys
import os,json
from PIL import Image, ImageDraw

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

class Controls:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.attach(view)
        self.default_filename = "default_parameters.json"
        parent = self.view.get_parent()
        self.gui()
        self.actions_binding()

    def gui(self):
        # Création d'autres composants dans le frame
        self.frame = tk.LabelFrame(self.view.get_parent(), text=self.model.get_name())
        self.scale_frequency()
        self.scale_mag()
        self.scale_phase()
        self.scale_harmonics()
        self.scale_samples()

        self.check_even = tk.BooleanVar(value=self.model.get_include_even())
        self.check_odd = tk.BooleanVar(value=self.model.get_include_odd())
        
        self.checkbox_even = tk.Checkbutton(self.frame, text="Harmoniques Paires", variable=self.check_even, command=self.on_even_changed)
        self.checkbox_odd = tk.Checkbutton(self.frame, text="Harmoniques Impaires", variable=self.check_odd, command=self.on_odd_changed)

    def save_image(self):
        canvas = self.view.get_canvas() 
        if canvas is None:
            messagebox.showerror("Error", "No canvas available to save.")
            return
        try:
            image = Image.new("RGB", (canvas.winfo_width(), canvas.winfo_height()), "white")
            draw = ImageDraw.Draw(image)
            canvas.postscript(file="temp_canvas.ps", colormode='color')
            image = Image.open("temp_canvas.ps")
            os.remove("temp_canvas.ps")  

            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
            if file_path:
                image.save(file_path)
                messagebox.showinfo("Save Image", f"Image saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving the image: {e}")


    # Fonction Exit avec message d'avertissement
    def exit_app(self):
        response = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if response:
            self.view.get_parent().quit()

    # Fonction Open avec sélection de fichier ou ouverture par défaut
    def open_combined_data(self, control_y):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    combined_data = json.load(file)

                data_x = combined_data.get("control_x", {})
                data_y = combined_data.get("control_y", {})

                self.load_parameters(data_x)

                control_y.load_parameters(data_y)

                messagebox.showinfo("File Loaded", f"Combined parameters loaded from {file_path}")
            except json.JSONDecodeError as e:
                messagebox.showerror("Error", f"Error reading the file. Please check the file format.\n{e}")
            except FileNotFoundError as e:
                messagebox.showerror("Error", f"File not found: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # Fonction pour charger les paramètres dans le modèle
    def load_parameters(self, data):
        self.model.set_frequency(data.get("frequency", self.model.get_frequency()))
        self.model.set_mag(data.get("magnitude", self.model.get_mag()))
        self.model.set_phase(data.get("phase", self.model.get_phase()))
        self.model.set_harmonics(data.get("harmonics", self.model.get_harmonics()))
        self.model.set_samples(data.get("samples", self.model.get_samples()))
        self.model.set_include_even(data.get("include_even", self.model.get_include_even()))
        self.model.set_include_odd(data.get("include_odd", self.model.get_include_odd()))

        # Mettre à jour les sliders et checkboxes
        self.freq.set(self.model.get_frequency())
        self.mag.set(self.model.get_mag())
        self.phase.set(self.model.get_phase())
        self.harmonics.set(self.model.get_harmonics())
        self.samples.set(self.model.get_samples())
        self.check_even.set(self.model.get_include_even())
        self.check_odd.set(self.model.get_include_odd())
        
        self.model.generate()

    # Fonction pour obtenir les paramètres actuels
    def get_parameters(self):
        return {
            "frequency": self.model.get_frequency(),
            "magnitude": self.model.get_mag(),
            "phase": self.model.get_phase(),
            "harmonics": self.model.get_harmonics(),
            "samples": self.model.get_samples(),
            "include_even": self.model.get_include_even(),
            "include_odd": self.model.get_include_odd(),
        }

    def save_combined_data(self, control_x, control_y):
        data_x = control_x.get_parameters()
        data_y = control_y.get_parameters()

        combined_data = {"control_x": data_x,"control_y": data_y}
        use_default = messagebox.askyesno("Save Combined Data", "Do you want to save to the default file?")
        
        if use_default:
            self.save_combined_data_default(combined_data)
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if file_path:
                with open(file_path, 'w') as file:
                    json.dump(combined_data, file)
                messagebox.showinfo("Save", f"Combined parameters saved in {file_path}.")

    def save_combined_data_default(self, combined_data):
        default_filename = self.default_filename
        with open(default_filename, 'w') as file:
            json.dump(combined_data, file)
        messagebox.showinfo("Save", f"Combined parameters saved in {default_filename}.")

    def scale_frequency(self) :
        self.freq=tk.IntVar()
        self.freq.set(self.model.get_frequency())
        self.scale_freq=tk.Scale(self.frame,variable=self.freq,
                             label="Frequency",
                             orient="horizontal",length=250,
                             from_=0,to=100,tickinterval=10)
    
    def scale_mag(self) :
        self.mag = tk.DoubleVar()
        self.mag.set(self.model.get_mag())
        self.scale_mag = tk.Scale(self.frame, variable=self.mag,
                                  label="Amplitude",
                                  orient="horizontal", length=250,
                                  from_=0, to=5, resolution=0.1, tickinterval=1)
    def scale_phase(self) :
        self.phase = tk.DoubleVar()
        self.phase.set(self.model.get_phase())
        self.scale_phase = tk.Scale(self.frame, variable=self.phase,
                                    label="Phase",
                                    orient="horizontal", length=250,
                                    from_=-90, to=90, tickinterval=45)
    
    def scale_harmonics(self) :
        self.harmonics = tk.IntVar()
        self.harmonics.set(self.model.get_harmonics())
        self.scale_harm = tk.Scale(self.frame, variable=self.harmonics,
                                   label="Harmonics",
                                   orient="horizontal", length=250,
                                   from_=1, to=10, tickinterval=1)

    def scale_samples(self):
        self.samples = tk.IntVar()
        self.samples.set(self.model.get_samples())  
        self.scale_samples = tk.Scale(self.frame, variable=self.samples,
                                       label="Number of Samples",
                                       orient="horizontal", length=250,
                                       from_=100, to=1000, tickinterval=200)

    def actions_binding(self) :
        self.scale_freq.bind("<B1-Motion>",self.on_frequency_action)
        self.scale_mag.bind("<B1-Motion>", self.on_mag_action)
        self.scale_phase.bind("<B1-Motion>", self.on_phase_action)
        self.scale_harm.bind("<B1-Motion>", self.on_harmonics_action)
        self.scale_samples.bind("<B1-Motion>", self.on_samples_action)

    def on_frequency_action(self,event):
        if  self.model.get_frequency() != self.freq.get() :
            self.model.set_frequency(self.freq.get())

    def on_mag_action(self, event):
        if self.model.get_mag() != self.mag.get():
            self.model.set_mag(self.mag.get())

    def on_phase_action(self, event):
        if self.model.get_phase() != self.phase.get():
            self.model.set_phase(self.phase.get())

    def on_harmonics_action(self, event):
        if self.model.get_harmonics() != self.harmonics.get():
            self.model.set_harmonics(self.harmonics.get())

    def on_samples_action(self, event):
        if self.model.get_samples() != self.samples.get():
            self.model.set_samples(self.samples.get())

    def on_even_changed(self):
        self.model.set_include_even(self.check_even.get())

    def on_odd_changed(self):
        self.model.set_include_odd(self.check_odd.get())

    def layout(self,side="top") :
        self.frame.pack(side=side, fill="x", expand=True)
        self.scale_freq.pack(fill="x", expand=True)
        self.scale_mag.pack(fill="x", expand=True)
        self.scale_phase.pack(fill="x", expand=True)
        self.scale_harm.pack(fill="x", expand=True)
        self.scale_samples.pack(fill="x", expand=True)
        self.checkbox_even.pack(anchor='w')
        self.checkbox_odd.pack(anchor='w')

if   __name__ == "__main__" :
   root=tk.Tk()
   root.option_readfile('main.opt')
   # Model
   model=Generator()
   model.set_samples(1000)
   model.set_frequency(2)
   model.set_mag(1)
   model.set_phase(0)
   model.set_harmonics(1)

   # View
   view=Screen(root)
   view.layout()
   view.update(model)
   # Controller
   control=Controls(model,view)
   control.layout("left")
   root.mainloop()


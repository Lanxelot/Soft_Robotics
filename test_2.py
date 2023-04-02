# import tkinter as tk
# import tkinter.messagebox
# import customtkinter as ctk
#
# class Application(tk.Frame):
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.master = master
#         self.pack()
#
#         # Create a CTKslider widget
#         self.slider = ctk.CTkSlider(self, orientation="HORIZONTAL", from_=0, to=100, number_of_steps=50)
#         self.slider.pack()
#
#         # Create a button to get the slider value
#         self.get_value_button = tk.Button(self, text="Get Slider Value", command=self.get_slider_value)
#         self.get_value_button.pack()
#
#     def get_slider_value(self):
#         # Get the current slider value and display it in a message box
#         value = self.slider.get()
#         tk.messagebox.showinfo("Slider Value", f"The current slider value is {value}.")
#
# root = tk.Tk()
# app = Application(master=root)
# app.mainloop()

import tkinter as tk
from tkinter import ttk

root = tk.Tk()

notebook = ttk.Notebook(root)
notebook.pack()

# # create the first tab
# frame1 = ttk.Frame(notebook)
# notebook.add(frame1, text='Tab 1')
#
# # create the second tab
# frame2 = ttk.Frame(notebook)
# notebook.add(frame2, text='Tab 2')
#
# # add a canvas to the second tab
# canvas = tk.Canvas(frame2, width=200, height=200)
# canvas.pack()
#
# # create a circle with center at (100, 100) and radius 50 pixels
# circle = canvas.create_oval(50, 50, 150, 150, fill='red')
#
# root.mainloop()

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
tim = np.linspace(0, 1, 100, endpoint=False)
y = signal.square(2 * np.pi * 1 * tim,duty = 0.8)


# frequency = 1 # Hz
# duration = 5 # seconds
# sampling_rate = 1000 # Hz
# t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
# square_wave = np.sign(np.sin(2 * np.pi * frequency * t))

# Plot the square wave
# plt.plot(t, square_wave)
# plt.xlabel('Time (s)')
# plt.ylabel('Amplitude')
# plt.title('Square Waveform')
# plt.show()
# for x in square_wave:
#     print(x)
